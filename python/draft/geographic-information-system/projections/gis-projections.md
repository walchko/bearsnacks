---
title: GIS Projections
date: 4 Apr 2020
author: Kevin J. Walchko, Phd
image: "https://i.pinimg.com/564x/46/cc/5b/46cc5be351b6b6474deedb8eac88907d.jpg"
image-height: "400px"
---

Common coordinate reference systems (CRS) used are:

- **proj or proj.4:** compact string way of representing a CRS, but most tools are moving away from this format
    - Maryland (NAD83): `+proj=lcc +lat_1=39.45 +lat_2=38.3 +lat_0=37.66666666666666 +lon_0=-77 +x_0=400000 +y_0=0 +ellps=GRS80 +units=m +no_defs `
- **EPSG:** 4 to 5 digit numbers representing CRS. EPSG stands for European Petroleum Survey Group.
- **WKT:** compact machine/human readable format for CRS. WKT stands for Well-known Text.
    ```
    PROJCS["NAD83(HARN) / Maryland",
        GEOGCS["NAD83(HARN)",
            DATUM["NAD83_High_Accuracy_Regional_Network",
                SPHEROID["GRS 1980",6378137,298.257222101,
                    AUTHORITY["EPSG","7019"]],
                AUTHORITY["EPSG","6152"]],
            PRIMEM["Greenwich",0,
                AUTHORITY["EPSG","8901"]],
            UNIT["degree",0.01745329251994328,
                AUTHORITY["EPSG","9122"]],
            AUTHORITY["EPSG","4152"]],
        UNIT["metre",1,
            AUTHORITY["EPSG","9001"]],
        PROJECTION["Lambert_Conformal_Conic_2SP"],
        PARAMETER["standard_parallel_1",39.45],
        PARAMETER["standard_parallel_2",38.3],
        PARAMETER["latitude_of_origin",37.66666666666666],
        PARAMETER["central_meridian",-77],
        PARAMETER["false_easting",400000],
        PARAMETER["false_northing",0],
        AUTHORITY["EPSG","2804"],
        AXIS["X",EAST],
        AXIS["Y",NORTH]]
    ```

# WGS-84 (EPSG:4326)

### References

- wikipeidia: [World Geodetic System](https://en.wikipedia.org/wiki/World_Geodetic_System)
- spatialreference.org: [EPSG:4326](https://spatialreference.org/ref/epsg/4326/)
- epsg.io: [EPSG:4326](https://epsg.io/4326)

### Details

- WGS84 Bounds: -180.0000, -90.0000, 180.0000, 90.0000
- Projected Bounds: -180.0000, -90.0000, 180.0000, 90.0000
- Scope: Horizontal component of 3D system. Used by the GPS satellite navigation system and for NATO military geodetic surveying.
- Last Revised: Aug. 27, 2007
- Area: World

```wkt
GEOGCS["WGS 84",
    DATUM["WGS_1984",
        SPHEROID["WGS 84",6378137,298.257223563,
            AUTHORITY["EPSG","7030"]],
        AUTHORITY["EPSG","6326"]],
    PRIMEM["Greenwich",0,
        AUTHORITY["EPSG","8901"]],
    UNIT["degree",0.01745329251994328,
        AUTHORITY["EPSG","9122"]],
    AUTHORITY["EPSG","4326"]]
```
`Proj4js.defs["EPSG:4326"] = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs";`
