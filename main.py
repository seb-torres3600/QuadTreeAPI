import psycopg2

# Function to establish a connection to the PostgreSQL database
def connect_to_database():
    try:
        # Connect to your PostgreSQL database by providing the necessary information
        connection = psycopg2.connect(
            user="datauser",
            password="mypassword",
            host="localhost",
            port="5432",
            database="sampledatabase"
        )
        print("Connected to the database")
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)

# Function to read all items from a table
def read_items_from_table(connection, table_name):
    try:
        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Execute the SELECT query to fetch all items from the table
        cursor.execute(f"SELECT * FROM {table_name}")

        # Fetch all the rows
        rows = cursor.fetchall()

        # Print the rows
        for row in rows:
            print(row)

        # Close the cursor
        cursor.close()
    except (Exception, psycopg2.Error) as error:
        print("Error while reading data from PostgreSQL:", error)

# Example usage
if __name__ == "__main__":
    # Connect to the PostgreSQL database
    connection = connect_to_database()

    if connection:
        # Read all items from the "your_table_name" table
        read_items_from_table(connection, "data")

        # Close the connection when done
        connection.close()
        print("Connection closed")
