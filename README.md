# sbident
A Python package for querying the [JPL Small Body Identification API](https://ssd-api.jpl.nasa.gov/doc/sb_ident.html)

## About
The Small Body Identification API returns known Solar System Objects within a field of view at a specified time for an observer location.  The sbident package is a lightweight implementation of this API that returns results in an Astropy table.

## Installation
```console
pip install git+https://github.com/bengebre/sbident
```

## Basic usage
```python
from sbident import SBIdent
from astropy.time import Time
from astropy.coordinates import SkyCoord

mpc_obs = '567'                         #observer location (MPC observatory code)
time = Time('2021-10-01 00:00:00')      #observing time
center = SkyCoord(10, -20, unit="deg")  #observing field of view center

#call API with above parameters and (optional) magnitude limit, 
#field of view half width (deg) and precision filters
sbid = SBIdent(mpc_obs, time, center, maglim=19, hwidth=1, precision='high')

print(sbid.results)                     #table of SSOs returned
```
```
    Object name     Astrometric RA (hh:mm:ss) Astrometric Dec (dd mm'ss") Dist. from center RA (") Dist. from center Dec (") Dist. from center Norm (") Visual magnitude (V) RA rate ("/h) Dec rate ("/h)
------------------- ------------------------- --------------------------- ------------------------ ------------------------- -------------------------- -------------------- ------------- --------------
  35889 (1999 JA81)               00:41:42.21                -19 04'47.8"                     1.E3                      3.E3                      3614.                 18.6    -3.174E+01     -1.306E+01
 57855 (2001 XT144)               00:40:35.35                -20 39'18.8"                     498.                     -2.E3                      2411.                 18.8    -3.346E+01     -9.137E+00
  91101 (1998 HK15)               00:37:26.23                -20 33'44.7"                    -2.E3                     -2.E3                      2963.                 17.7    -3.600E+01     -6.281E-01
 93867 (2000 WQ115)               00:41:43.02                -19 05'14.9"                     1.E3                      3.E3                      3593.                 17.8    -3.701E+01     -8.077E-01
  120306 (2004 KE6)               00:36:31.25                -20 30'11.0"                    -3.E3                     -2.E3                      3451.                 19.0    -3.658E+01     -2.018E+00
 172806 (2004 GT10)               00:40:33.40                -19 43'58.6"                     471.                      961.                      1071.                 18.7    -2.659E+01     -1.926E+01
255370 (2005 WS111)               00:41:44.59                -20 05'42.9"                     1.E3                     -343.                      1512.                 18.8    -3.015E+01     -5.458E+00
```

## More examples
More examples are available in this [rendered notebook](https://github.com/bengebre/sbident/blob/main/examples/sbident-examples.ipynb) in the [examples](https://github.com/bengebre/sbident/blob/main/examples/) directory.
