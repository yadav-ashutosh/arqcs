import sqlite3

def print_all_data():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("arqdb.db")
        cursor = conn.cursor()

        # Fetch all data from the "users" table
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        # Print the column headers
        column_names = [description[0] for description in cursor.description]
        print("\t".join(column_names))

        # Print the data rows
        for row in rows:
            print("\t".join(map(str, row)))

    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        # Close the database connection
        if conn:
            conn.close()

if __name__ == "__main__":
    print_all_data()
