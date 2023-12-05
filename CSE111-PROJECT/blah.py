import sqlite3

def get_all_tables(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Retrieve all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Extract table names from tuples
    table_names = [table[0] for table in tables]

    return table_names

def get_table_schema(db_path, table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Retrieve schema of the table
    cursor.execute(f"PRAGMA table_info({table_name});")
    schema = cursor.fetchall()

    # Close the database connection
    conn.close()

    return schema

def print_table_schema(table_name, schema):
    print(f"\nSchema for {table_name}:")
    print(f"Column Name{' ' * 4}Type")
    print("-" * 30)
    for column in schema:
        print(f"{column[1]}{' ' * (12-len(column[1]))}{column[2]}")

if __name__ == "__main__":
    db_path = 'your_db.sqlite3'  # Your SQLite database path
    
    # Retrieve all table names
    all_tables = get_all_tables(db_path)
    
    # Fetch and print schema for each table
    for table in all_tables:
        schema = get_table_schema(db_path, table)
        print_table_schema(table, schema)
