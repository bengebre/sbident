import requests
import warnings
from pandas import DataFrame
from astropy.time import Time
from astropy.table import Table
from astropy.coordinates import SkyCoord
from urllib.parse import urlencode

class SBIdent:
	"""
	A library for querying the JPL Small Body Identification API.
	https://ssd-api.jpl.nasa.gov/doc/sb_ident.html
	"""

	API_VERSION = '1.0' # expected API version

	def __init__(self, location=None, obstime=None, fov=None, precision='low', hwidth=None, elem=False, maglim=None, 
							magreq=True, filters=None, request=True):

		# initializing some attributes
		self.json = None
		self.summary = None
		self.data_field = None
		self.table = None
		self.num_results = 0

		# minimal warning format
		warnings.formatwarning = lambda msg, *args, **kwargs: f'{msg}\n'

		# args: elem, magreq, request
		# test boolean arguments are boolean and set
		for a in ['elem', 'magreq', 'request']:
			if not isinstance(eval(a), bool):
				raise TypeError("{} must be either True or False".format(a))

		self.elem = elem
		self.req_elem = {'req-elem': str(elem).lower()}

		self.magreq = magreq
		self.mag_required = {'mag-required': str(magreq).lower()}

		self.request = request

		# test maglim is numeric or None
		if isinstance(maglim, (int,float)): 
			self.maglim = float(maglim)
			self.vmag_lim = {'vmag-lim': self.maglim}
		elif maglim==None:
			self.maglim = maglim
			self.vmag_lim = None
		else:
			raise TypeError("maglim must be either numeric or None")

		# test precision is either 'high' or 'low'
		if precision not in ['high', 'low']:
			raise TypeError("precision values must be either 'high' or 'low'")

		self.precision = precision
		self.two_pass = {'two-pass': str(self.precision=='high').lower()}
		self.suppress_first_pass = {'suppress-first-pass': str(self.precision=='high').lower()}

		# test filters is dict
		if isinstance(filters, dict) or filters==None:
			self.filters = filters
		else:
			raise TypeError("filters must be either a dictionary or None")

		# parse location
		if isinstance(location, str):
			# using observatory mpc-code location
			self.location = {'mpc-code': location}
		elif isinstance(location, dict):
			if ('mpc-code' in location):
				# using observatory mpc-code location
				self.location = {'mpc-code': location['mpc-code']}
			elif ('lat' in location and 'lon' in location and 'alt' in location):
				# using geodetic location 
				self.location = {k:location[k] for k in ['lat', 'lon', 'alt']}
			elif ('lon' in location and 'dxy' in location and 'dz' in location):
				# using parallax location 
				self.location = {k:location[k] for k in ['lon', 'dxy', 'dz']}
			elif ('xobs' in location):
				# using geocentric location 
				self.location = {'xobs': location['xobs']}
			elif ('xobs-hel' in location):
				# using heliocentric location 
				self.location = {'xobs-hel': location['xobs-hel']}
			else:
				# location missing some required fields
				raise ValueError('location input missing some required fields')
		else:
				# location type unexpected
				raise TypeError('Unexpected argument type for location. Must be string or dictionary.')

		# parse obstime; handle string, float (jdate), Time or dict
		if isinstance(obstime, str):
			# passing UTC string
			self.obstime = {'obs-time': obstime}
		elif isinstance(obstime, float):
			# assumes float is jdate
			self.obstime = {'obs-time': Time(obstime, format='jd', precision=0).utc.iso}
		elif isinstance(obstime, Time):
			# passing Time object
			obstime.precision = 0
			self.obstime = {'obs-time': obstime.utc.iso}
		elif isinstance(obstime, dict) and 'obs-time' in obstime:
			self.obstime = obstime
		else:
			# obstime type unexpected
			raise TypeError('Unexpected argument type for obstime. Must be string, float (jdate) or Time.')

		# parse and rewrite fov when a SkyCoord center
		if isinstance(fov, SkyCoord):
			# if fov is of type SkyCoord get a center relative fov 
			radec_jpl = self.skycoord_to_jplstr(fov)
			fov = {'fov-ra-center': radec_jpl[0], 'fov-dec-center': radec_jpl[1]}
			
		# handle hwidth - this has precedence if it's defined
		if hwidth is not None:
			if isinstance(hwidth, (tuple, list)) and len(hwidth)==2:
				fov['fov-ra-hwidth'] = str(hwidth[0])
				fov['fov-dec-hwidth'] = str(hwidth[1])
			elif isinstance(hwidth, (int, float)):
				fov['fov-ra-hwidth'] = str(hwidth)
				fov['fov-dec-hwidth'] = str(hwidth)
			
		# continued fov parsing
		if isinstance(fov, dict):
			if ('fov-ra-center' in fov and 'fov-dec-center' in fov):
				# center fov method
				self.fov = {k:fov[k] for k in ['fov-ra-center', 'fov-dec-center']}

				if 'fov-ra-hwidth' in fov:
					self.fov['fov-ra-hwidth'] = fov['fov-ra-hwidth']
				#else:
					#self.fov['fov-ra-hwidth'] = '0.5'

				if 'fov-dec-hwidth' in fov:
					self.fov['fov-dec-hwidth'] = fov['fov-dec-hwidth']
				#else:
				#	self.fov['fov-dec-hwidth'] = '0.5'
			elif ('fov-ra-lim' in fov and 'fov-dec-lim' in fov):
				# edge fov method
				self.fov = {k:fov[k] for k in ['fov-ra-lim', 'fov-dec-lim']}
			else:
				# fov missing some required fields
				raise ValueError('fov input must include ...')
		else:
			# fov type unexpected
			raise TypeError('Unexpected argument type for fov ...')

		self.form_uri()

		if request:
			self.make_request()
		else:
			self.request = False

	def __repr__(self):
		# show representation of object in terms that are instantiate-able
		repr = "<SBIdent(location={l}, obstime={t}, fov={fov}, filters={op}, precision='{p}', maglim={ml}, magreq={mr}, request={req})>"
		return repr.format(l=self.location, t=self.obstime, fov=self.fov, op=self.filters, p=self.precision, ml=self.maglim,
											mr=self.magreq, req=self.request)

	def form_uri(self):
		# forms uri from parameters specified in init

		base_uri = "https://ssd-api.jpl.nasa.gov/sb_ident.api?"

		params = {}
		build = [self.location, self.obstime, self.fov, self.two_pass, self.suppress_first_pass, self.vmag_lim, 
						self.mag_required, self.req_elem]

		for b in build:
			if b is not None:
				params.update(b)

		self.uri = base_uri + urlencode(params)

		if self.filters is not None:
			self.uri = self.uri + "&" + urlencode(self.filters)

		return self.uri

	def read_uri(self):
		# read & set json
		response = requests.get(self.uri)
		json = response.json()
		self.json = json

		# report API error if one exists
		if 'code' in self.json:
			raise SystemError("API error: {}".format(self.json['message']))

		# warn if API version is unexpected
		ver = self.json['signature']['version']
		if ver != self.API_VERSION:
			version_warning = "Expected API version '{ev}' but response indicated version '{v}'. Unexpected behavior possible."
			warnings.warn(version_warning.format(API_VERSION,ver))

	def parse_json(self):
		# make sure json exists
		if self.json is None:
			raise UnboundLocalError("No json to parse in API response")

		# report API warning if one exists
		if 'warning' in self.json:
			warnings.warn("API warning: {}".format(self.json['warning']))

		# set summary
		self.summary = self.json['summary']

		# set table to the most precise table present
		data_fields = ['data_second_pass', 'data_first_pass', 'elem_first_pass', 'elem_second_pass']
		for d in data_fields:
			if d in self.json:
				self.data_field = d
				continue

		# no data returned
		if self.data_field is None:
			return

		# column fields depend on first or second pass selection
		if 'first' in self.data_field:
			col_field = 'fields_first'
			count_field = 'n_first_pass'
		else:
			col_field = 'fields_second'
			count_field = 'n_second_pass'

		# rows in table
		self.num_results = self.json[count_field]

		# the actual json parse
		rows = self.json[self.data_field]
		columns = self.json[col_field]
		df = DataFrame(rows, columns=columns)
		table = Table.from_pandas(df)
		self.table = table

	def make_request(self):
		# make the API call and parse return

		self.read_uri()
		self.parse_json()

	@classmethod
	def skycoord_to_jplstr(cls,c):
		cstr = c.icrs.to_string('hmsdms', sep=":", precision=2)
		radec_jpl = cstr.replace('-','M').replace(':','-').split(' ')

		return radec_jpl
