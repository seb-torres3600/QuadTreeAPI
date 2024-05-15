from flask import Flask
from connection import connect_to_database, read_items_from_table
from waitress import serve
import os

app = Flask(__name__)

@app.route('/get_zones/<table>/<coordinates>')
def get_zones(coordinates, table):
    # Decode the coordinates string into a list
    coordinates_list = coordinates.split(',')

    # Connect to the database
    tmp_connection = connect_to_database()

    # Read items from the database based on the provided coordinates
    result = read_items_from_table(tmp_connection, table, coordinates_list)
    return result

if __name__ == '__main__':
    api_port = os.getenv("API_PORT", 8080)
    api_host = os.getenv("API_HOST", "0.0.0.0")
    serve(app, host=api_host, port=api_port)