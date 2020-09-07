Project to build APIs of 3rd level
Steps to run this project: 

1. install poetry: pip install poetry

2. git clone --brach linux-compatible https://github.com/IDEHCO3/hyper-resource-sanic
3. Inside hyper-resource-sanic folder, via cmd/shell, execute: poetry install
4. In hyper-resource-sanic folder, via cmd/shell, using reverse engineerings in database such as postgres, execute: sqlacodegen --schema aschema postgresql://an_user_name:a_password@host:port/a_database --outfile ./generator/all_models.py
5. Inspect and if necessary adjust, the file all_models.py that wa generated in folder generator. For example, rename classes or attributes or remove.
6. cd into generator folder, execute:
   python generate_all_files.py
7. In hyper-resource-sanic folder rename the file .env_template to .env and configure to your database. See the environment variable URLDB.
8. Move to src folder using cd ../src command and execute: python index.py
   See in http://127.0.0.1:8002/
