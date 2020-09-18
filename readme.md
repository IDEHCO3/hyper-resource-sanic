Project to build APIs of 3rd level
Steps to run this project:
0. install poetry: pip install poetry
1. git clone https://github.com/IDEHCO3/hyper-resource-sanic
2. Inside hyper-resource-sanic folder, via cmd/shell, execute: poetry install
3. In hyper-resource-sanic folder, via cmd/shell, using reverse engineerings in database such as postgres, execute: sqlacodegen --schema aschema postgresql://an_user_name:a_password@host:port/a_database --outfile ./generator/all_models.py
4. Inspect and if necessary adjust, the file all_models.py that wa generated in folder generator. For example, rename classes or attributes or remove.
5. Still in hyper-resource-sanic folder, execute:
   python -m generator.generate_all_files.py
6. In hyper-resource-sanic folder rename the file .env_template to .env and configure to your database. See the environment variable URLDB.
7. In hyper-resource-sanic folder execute: python -m src.index
   See in http://127.0.0.1:8002/
