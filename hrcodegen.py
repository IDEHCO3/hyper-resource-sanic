import argparse
import sys
import os
from typing import List

def env_template(urldb:str):
    return f"""DEBUG=True
ACESS_LOG=True
HOST=127.0.0.1
PORT=8000
URLDB={urldb}
PROTOCOL=http:
ECHO=debug"""

def generate_env_file(urldb:str):
    with open(".env", "w") as env:
        env.write(env_template(urldb))

def main():
    ### sqlacodegen 2.3.0 code
    parser = argparse.ArgumentParser(description='Generates SQLAlchemy model code from an existing database.')
    parser.add_argument('url', nargs='?', help='SQLAlchemy url to the database')
    parser.add_argument('--version', action='store_true', help="print the version number and exit")
    parser.add_argument('--schema', help='load tables from an alternate schema')
    parser.add_argument('--tables', help='tables to process (comma-separated, default: all)')
    parser.add_argument('--noviews', action='store_true', help="ignore views")
    parser.add_argument('--noindexes', action='store_true', help='ignore indexes')
    parser.add_argument('--noconstraints', action='store_true', help='ignore constraints')
    parser.add_argument('--nojoined', action='store_true', help="don't autodetect joined table inheritance")
    parser.add_argument('--noinflect', action='store_true', help="don't try to convert tables names to singular form")
    parser.add_argument('--noclasses', action='store_true', help="don't generate classes, only tables")
    parser.add_argument('--nocomments', action='store_true', help="don't render column comments")
    parser.add_argument('--outfile', help='file to write output to (default: stdout)')
    args = parser.parse_args()
    ### sqlacodegen 2.3.0 code

    if args.url is not None:
        generate_env_file(args.url)

    hrcodegen_comm = sys.argv
    sqlacodegen_comm = corvert_to_sqlacodegen_command(hrcodegen_comm)
    os.system(sqlacodegen_comm)

def corvert_to_sqlacodegen_command(hrcodegen_comm: List[str]) -> str:
    hrcodegen_comm[0] = "sqlacodegen"
    sqlacodegen_comm = " ".join(hrcodegen_comm)
    return sqlacodegen_comm

if __name__ == "__main__":
   main()