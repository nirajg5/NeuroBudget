from sqlalchemy import inspect

from database.db import engine


inspector = inspect(engine)

tables = inspector.get_table_names()

print()

print("Tables in Database:")

for table in tables:

    print("-", table)