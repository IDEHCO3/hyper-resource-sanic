Project to build APIs of 3rd level
Steps to run this project: 

1. install poetry: pip install poetry

2. git clone https://github.com/IDEHCO3/hyper-resource-sanic
3. Inside hyper-resource-sanic folder, via cmd/shell, execute: poetry install
4. In hyper-resource-sanic folder, via cmd/shell, using reverse engineerings in database such as postgres, execute: sqlacodegen --schema aschema postgresql://an_user_name:a_password@host:port/a_database --outfile ./generator/all_models.py
5. Inspect and if necessary adjust, the file all_models.py that wa generated in folder generator. For example, rename classes or attributes or remove.
6. Still in hyper-resource-sanic folder, execute:
   python generator/generate_all_files.py
6.1. If doesn't work, cd into generator folder and execute python generate_all_files.py
7. In hyper-resource-sanic folder rename the file .env_template to .env and configure to your database. See the environment variable URLDB.
8. In hyper-resource-sanic folder execute: python src/index.py
   See in http://127.0.0.1:8002/
