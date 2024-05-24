from flask import Flask, jsonify
from connection import connect_to_database, read_items_from_table
from waitress import serve
import os
import logging


app = Flask(__name__)

@app.route('/status')
def get_status():
    try:
        return jsonify({'status': 'OK'}), 200
    except Exception as e:
        logging.error(f'Failed to get status: {e}')
        # If an error occurs, return a 500 Internal Server Error response
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get_zones/<table>/<coordinates>')
def get_zones(coordinates, table):
    try: 
        # Decode the coordinates string into a list
        coordinates_list = coordinates.split(',')

        # Connect to the database
        connection = connect_to_database()

        # Read items from the database based on the provided coordinates
        result = read_items_from_table(connection, table, coordinates_list)
        # Close connection after reading from table
        connection.close()
        return result
    except Exception as e:
        logging.error(f"Failed to read items from database: {e}")

if __name__ == '__main__':
    api_port = os.getenv("API_PORT", 8080)
    api_host = os.getenv("API_HOST", "localhost")
    serve(app, host=api_host, port=api_port)