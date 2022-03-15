#https://github.com/SereneWizard/shapefile-to-postgis/blob/master/Shapefile_to_postgis.ipynb
# Import necessary libraries
import os
import glob
import psycopg2
import fiona
from shapely.geometry import Polygon

infname = glob.glob('vector/*.shp')[0]
with fiona.drivers():
    with fiona.open(infname) as src:
        geom = src.crs
        feat = src.next()
        attributes = feat['properties'].keys()
        gemtype = feat['geometry']['type']

connection = psycopg2.connect(database="mydatabase",
                              user="myusername",
                              password="mypassword",
                              host="localhost")
cursor = connection.cursor()
tablename = "Mclean_Dupage"
cursor.execute("DROP TABLE IF EXISTS {}".format(tablename))
cursor.execute("""
               CREATE TABLE {}
               (id SERIAL PRIMARY KEY,
               COUNTY_NAM VARCHAR NOT NULL,
               CO_FIPS BIGINT NOT NULL,
               geom GEOMETRY)""".format(tablename))
connection.commit()

with fiona.drivers():
    with fiona.open(infname) as src:
        for i in src:
            record = list(i['properties'].values())
            print ("{} county has {} fips".format(*record))
            geometry = Polygon(i['geometry']['coordinates'][0])
            wktgeometry = geometry.wkt
            cursor.execute("""
                   INSERT INTO {} (COUNTY_NAM, CO_FIPS, geom)
                   VALUES ('{}', {}, ST_GeomFromText('{}'))
                   """.format(tablename, *record, wktgeometry))
            connection.commit()