import os
from generator.util import convert_camel_case_to_underline
def get_geo_template(file_name, class_name):
    return '''<!DOCTYPE html>
<html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>Vector Layer</title>
      <!-- Pointer events polyfill for old browsers, see https://caniuse.com/#feat=pointer -->
      <!-- <script src="https://unpkg.com/elm-pep"></script>     -->
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/openlayers/openlayers.github.io@master/en/v6.5.0/css/ol.css" type="text/css">
      <style> #map { width: 100%; height:400px; } </style>
      <script type="application/ld+json">
      {
          "@context": {
              "geojson": "https://purl.org/geojson/vocab#",
              "Feature": "geojson:Feature",
              "FeatureCollection": "geojson:FeatureCollection",
              "MultiPolygon": "geojson:MultiPolygon",
              "type": "@type",
              "coordinates": {
                  "@container": "@list",
                  "@id": "geojson:coordinates"
              },
              "features": {
                  "@container": "@set",
                  "@id": "geojson:features"
              },
              "geometry": "geojson:geometry",
              "properties": "geojson:properties",
              "type": "@type"
          }
      }
      </script>
  </head>
  <body>
      <div id="map" class="map"></div>
      <div id="info">&nbsp;</div>
      <script src="https://cdn.jsdelivr.net/gh/openlayers/openlayers.github.io@master/en/v6.5.0/build/ol.js"></script>

      <script type="module">
        var style = new ol.style.Style({
            fill: new ol.style.Fill({
                color: "rgba(255, 255, 255, 0.6)",
            }),
            stroke: new ol.style.Stroke({
                color: "#319FD3",
                width: 1,
            }),
            text: new ol.style.Text({
                font: "12px Calibri,sans-serif",
                fill: new ol.style.Fill({
                    color: "#000",
                }),
                stroke: new ol.style.Stroke({
                    color: "#fff",
                    width: 3,
                }),
            }),
        });

        var vectorLayer = new ol.layer.Vector({
            source: new ol.source.Vector({
                url: window.location.href,
                format: new ol.format.GeoJSON(),
            })
        });

        var map = new ol.Map({
            layers: [
                new ol.layer.Tile({source: new ol.source.OSM()}),
                vectorLayer
            ],
            target: "map",
            view: new ol.View({
                center: [-6031024.58685793, -1976355.8033415168],
                zoom:5,
                zoomFactor:1.5,
                minZoom:2
            }),
        });
      </script>
    </body>
</html>'''
def get_template(file_name, class_name):
    return ''''''
def generate_static_file(path, file_name, class_name, is_geo: bool = False):
    file_with_path = os.path.join(path, f'{file_name}.html')
    with open(file_with_path, 'w') as file:
        if is_geo:
            file.write(get_geo_template(file_name, class_name))
        else:
            file.write(get_template(file_name, class_name))

def generate_all_static_files(clsmembers, is_geo: bool = False):
    path = os.path.join(os.getcwd(), 'src', 'static')
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

    for class_name_class in clsmembers:
        class_name = class_name_class[0]
        file_name = convert_camel_case_to_underline(class_name)
        generate_static_file(path, file_name, class_name, is_geo)