import psycopg2
import os

# Function to establish a connection to the PostgreSQL database
def connect_to_database():
    try:
        # Connect to your PostgreSQL database by providing the necessary information
        connection = psycopg2.connect(
            user=os.getenv("DATABASE_USER", "datauser"),
            password=os.getenv("DATABASE_PASSWORD", "mypassword"),
            host=os.getenv("DATABASE_HOST", "localhost"),
            port=os.getenv("DATABASE_PORT", 5432),
            database=os.getenv("DATABASE_NAME", "quadtreedatabase")
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)

# Function to read all items from a table
def read_all_items_from_table(connection, table_name):
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

# Function to read all items from a table
def read_items_from_table(connection, table_name, constraints):
    try:
        rectangle_rows = get_rectangle_zones(connection, table_name, constraints)
        circle_rows = get_circle_zones(connection, table_name, constraints)
        triangle_rows = get_triangle_zones(connection, table_name, constraints)

        return rectangle_rows + circle_rows + triangle_rows
    except (Exception, psycopg2.Error) as error:
        print("Error while reading data from PostgreSQL:", error)


def get_rectangle_zones(connection, table_name, constraints):
    try:
        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        rectangle_query = f"SELECT * FROM {table_name} \
                WHERE shape='rectangle' \
                AND box(point({constraints[0]},{constraints[1]}), point({constraints[2]},{constraints[3]})) @> \
                box(point(coordinates[1], coordinates[2]), \
                point(coordinates[3], coordinates[4]));" 

        # Execute the SELECT query to fetch all items from the table
        cursor.execute(rectangle_query)
        # Fetch all the rows
        rows = cursor.fetchall()
        # Close the cursor
        cursor.close()
        
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error while reading data from PostgreSQL:", error)


def get_circle_zones(connection, table_name, constraints):
    try:
        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        circle_query = f"SELECT * FROM {table_name} \
                WHERE shape='circle' \
                AND box(point({constraints[0]},{constraints[1]}), point({constraints[2]},{constraints[3]})) @> \
                box(circle(point(coordinates[1], coordinates[2]), coordinates[3]));"

        # Execute the SELECT query to fetch all items from the table
        cursor.execute(circle_query)

        # Fetch all the rows
        rows = cursor.fetchall()
        # Close the cursor
        cursor.close()
        
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error while reading data from PostgreSQL:", error)


def get_triangle_zones(connection, table_name, constraints):
    try:
        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        circle_query = f"SELECT * FROM {table_name} \
                WHERE shape='triangle' \
                AND box(point({constraints[0]},{constraints[1]}), point({constraints[2]},{constraints[3]})) @> \
                box(polygon(point(coordinates[1], coordinates[2]), point(coordinates[3], coordinates[4]), \
                point(coordinates[5], coordinates[6])));"

        # Execute the SELECT query to fetch all items from the table
        cursor.execute(circle_query)

        # Fetch all the rows
        rows = cursor.fetchall()
        # Close the cursor
        cursor.close()
        
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error while reading data from PostgreSQL:", error)