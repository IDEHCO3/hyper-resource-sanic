
Project to build APIs of 3rd level
Steps to run this project:
## Installation

1. install poetry: pip install poetry
2. git clone https://github.com/IDEHCO3/hyper-resource-sanic
3. Inside hyper-resource-sanic folder, via cmd/shell, execute: poetry install
4. In hyper-resource-sanic folder, via cmd/shell, using reverse engineerings in database such as postgres, execute: python hrcodegen.py --schema a_schema postgresql://an_user_name:a_password@a_host:a_port/a_database --outfile ./generator/all_models.py <br>
   4.1 Example: python hrcodegen.py --schema public postgresql://postgres:12345@127.0.0.1:5432/postgres --outfile ./generator/all_models.py
5. Inspect and if necessary adjust, the file all_models.py that was generated in folder generator. For example, rename classes or attributes or remove.
6. Still in hyper-resource-sanic folder, execute:
   python -m generator.generate_all_files <br>
   6.1 By default get, head and options is generated. To generating patch/put, post and delete execute: python -m generator.generate_all_files  True True True
7. In hyper-resource-sanic folder modify the file .env and configure to your database (if necessary). See the environment variable URLDB.
8. In hyper-resource-sanic folder execute: python -m src.index
   See in http://127.0.0.1:8000/

## Troubleshooting

### GDAL
If you don't have GDAL lib or python GDAL bindings installed in your environment probrably will face similar probrems like the following
#### Unable to install GDAL python bindings
![Unable to install GDAL python bindings](python-gdal-intallation-failed-sliced.png)
#### GDAL lib not find
![GDAL lib not find](gdal-config-not-find.png)
#### GNU GCC lib not find
![GNU GCC lib not find](gnu-gcc-not-find.png)

Try to solve this executing the following commands:
### `sudo apt-get install libpq5=12.9-0ubuntu0.20.04.1 # change versions to match your ubuntu installation` 
### `sudo apt-get install libpq-dev`
### `sudo apt-get install libgdal-dev`