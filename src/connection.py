import psycopg2
import os
import logging

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
        logging.error("Error while connecting to PostgreSQL:", error)

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
        logging.error("Error while reading data from PostgreSQL:", error)

# Function to read all items from a table
def read_items_from_table(connection, table_name, constraints):
    try:
        rectangle_rows = get_rectangle_zones(connection, table_name, constraints)
        circle_rows = get_circle_zones(connection, table_name, constraints)
        triangle_rows = get_triangle_zones(connection, table_name, constraints)

        return rectangle_rows + circle_rows + triangle_rows
    except (Exception, psycopg2.Error) as error:
        logging.error("Error while reading data from PostgreSQL:", error)


def get_rectangle_zones(connection, table_name, constraints):
    try:
        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        rectangle_query = f"SELECT json_agg(data_row) AS data_json FROM \
                            (SELECT id, shape, coordinates FROM {table_name} \
                            WHERE shape='rectangle' \
                            AND box(point({constraints[0]},{constraints[1]}), point({constraints[2]},{constraints[3]})) @> \
                            box(point(coordinates[1], coordinates[2]), \
                            point(coordinates[3], coordinates[4]))) AS data_row;"

        # Execute the SELECT query to fetch rectangle zones from the table and aggregate as JSON
        cursor.execute(rectangle_query)

        # Fetch the JSON result
        json_result = cursor.fetchone()[0]
         # Close the cursor
        cursor.close()

        if json_result == None:
            return []
        # Return the JSON result
        return json_result
    except (Exception, psycopg2.Error) as error:
        logging.error("Error while reading rectangle data from PostgreSQL:", error)
        return []


def get_circle_zones(connection, table_name, constraints):
    try:
        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        circle_query = f"SELECT json_agg(data_row) AS data_json FROM \
                        (SELECT id, shape, coordinates FROM {table_name} \
                        WHERE shape='circle' \
                        AND box(point({constraints[0]},{constraints[1]}), point({constraints[2]},{constraints[3]})) @> \
                        box(circle(point(coordinates[1], coordinates[2]), coordinates[3]))) AS data_row;"

        # Execute the SELECT query to fetch circle zones from the table and aggregate as JSON
        cursor.execute(circle_query)
        # Fetch the JSON result
        json_result = cursor.fetchone()[0]
        # Close the cursor
        cursor.close()

        if json_result == None:
            return []
        # Return the JSON result
        return json_result
    except (Exception, psycopg2.Error) as error:
        logging.error("Error while reading circle data from PostgreSQL:", error)
        return []

def get_triangle_zones(connection, table_name, constraints):
    try:
        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        triangle_query = f"SELECT json_agg(data_row) AS data_json FROM \
                            (SELECT id, shape, coordinates FROM {table_name} \
                            WHERE shape='triangle') AS data_row;"

        # Execute the SELECT query to fetch triangle zones from the table and aggregate as JSON
        cursor.execute(triangle_query)
        # Fetch the JSON result
        all_results = cursor.fetchone()[0]
        # Close the cursor
        cursor.close()
        json_result = []
        for result in all_results:
            if triangle_fits(result, constraints):
                json_result.append(result)
        # Return the JSON result
        return json_result
    except (Exception, psycopg2.Error) as error:
        logging.error("Error while reading triangle data from PostgreSQL:", error)
        return []



def triangle_fits(data, constraints):
    '''
    See if the triangle in the database fits in the constraints
    '''
    points = data["coordinates"]
    x_const_low = float(constraints[0])
    y_const_low = float(constraints[1])
    x_const_high = float(constraints[2])
    y_const_high = float(constraints[3])
    for p in range(0, len(points), 2):
        x_coord = float(points[p])
        y_coord = float(points[p+1])
        if x_coord < x_const_low or x_coord > x_const_high:
            return False
        if y_coord < y_const_low or y_coord > y_const_high:
            return False
    return True
