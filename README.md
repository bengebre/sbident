# sbident
A Python module for querying the [JPL Small Body Identification API](https://ssd-api.jpl.nasa.gov/doc/sb_ident.html)

## About
The Small Body Identification API returns known Solar System Objects within a field of view at a specified time and observer location.  The sbident module is a lightweight implementation of this API that returns the results as an Astropy table.

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
print(sbid.table)                       #table of SSOs requested
```
```
    Object name      Astrometric RA (hh:mm:ss) ... Est. error Dec (")
-------------------- ------------------------- ... ------------------
  20701 (1999 VL179)                  00:39:52 ...              27.68
   89382 (2001 VS97)                  00:38:40 ...              34.67
   95046 (2002 AY36)                  00:39:09 ...              31.66
   128028 (2003 KM5)                  00:37:50 ...              37.36
 356741 (2011 UZ204)                  00:38:24 ...              30.15
  359131 (2009 BL77)                  00:40:03 ...              33.01
  386490 (2009 AZ47)                  00:40:55 ...              28.69
  475798 (2006 XH54)                  00:37:55 ...              36.91
 501925 (2014 WP487)                  00:40:06 ...              33.36
           (1927 LA)                  23:42:18 ...              5.5E6
                 ...                       ... ...                ...
   C/2017 M5 (TOTAS)                  01:43:29 ...              1.7E5
  C/2017 S7 (Lemmon)                  02:14:01 ...              2.1E5
 P/2017 Y3 (Leonard)                  00:58:30 ...              2.2E5
   C/2018 A3 (ATLAS)                  00:21:01 ...              1.1E5
  C/2018 C2 (Lemmon)                  00:32:45 ...              1.6E5
 C/2018 DO4 (Lemmon)                  21:21:08 ...              1.8E5
 C/2018 EF9 (Lemmon)                  00:26:28 ...              1.7E5
 C/2018 K1 (Weiland)                  11:22:26 ...              8.0E5
C/2018 M1 (Catalina)                  10:14:28 ...              7.4E5
   C/2018 O1 (ATLAS)                  09:37:26 ...              9.2E5
C/2018 W1 (Catalina)                  15:52:01 ...              5.3E5
Length = 1530 rows
```
