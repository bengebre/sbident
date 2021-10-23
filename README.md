# sbident
A Python library for querying the [JPL Small Body Identification API](https://ssd-api.jpl.nasa.gov/doc/sb_ident.html)

## About
The Small Body Identification API returns known Solar System Objects within a field of view at a specified time and observer location.  SBIdent is a lightweight implementation of this API that returns results in an Astropy table.

## Installation
```console
pip install git+https://github.com/bengebre/sbident
```

## Usage
```python
from sbident import SBIdent
from astropy.time import Time
from astropy.coordinates import SkyCoord

mpc_obs = '567'                         #observer location (MPC observatory code)
time = Time.now()                       #observing time
center = SkyCoord(10, -20, unit="deg")  #observer field of view center

sbid = SBIdent(mpc_obs, time, center)   #query API 
sbid.table                              #returns table of SSOs requested
```
