
Project to build APIs of 3rd level
Steps to run this project:

1. install poetry: pip install poetry
2. git clone https://github.com/IDEHCO3/hyper-resource-sanic
3. Inside hyper-resource-sanic folder, via cmd/shell, execute: poetry install
4. In hyper-resource-sanic folder, via cmd/shell, using reverse engineerings in database such as postgres, execute: sqlacodegen --schema a_schema postgresql://an_user_name:a_password@a_host:a_port/a_database --outfile ./generator/all_models.py <br>
   4.1 Example: sqlacodegen --schema public postgresql://postgres:12345@127.0.0.1:5432/postgres --outfile ./generator/all_models.py
5. Inspect and if necessary adjust, the file all_models.py that wa generated in folder generator. For example, rename classes or attributes or remove.
6. Still in hyper-resource-sanic folder, execute:
   python -m generator.generate_all_files <br>
   6.1 By default get, head and options is generated. To generating patch/put, post and delete execute: python -m generator.generate_all_files  True True True
7. In hyper-resource-sanic folder rename the file .env_template to .env and configure to your database. See the environment variable URLDB.
8. In hyper-resource-sanic folder execute: python -m src.index
   See in http://127.0.0.1:8002/
