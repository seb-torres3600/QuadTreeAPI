from flask import Flask, jsonify
from connection import connect_to_database, read_items_from_table
from waitress import serve

app = Flask(__name__)

@app.route('/get_zones/<coordinates>')
def get_zones(coordinates):
    # Decode the coordinates string into a list
    coordinates_list = coordinates.split(',')

    # Connect to the database
    tmp_connection = connect_to_database()

    # Read items from the database based on the provided coordinates
    result = read_items_from_table(tmp_connection, "data", coordinates_list)

    # Return the result as JSON
    return jsonify({"result": result})

if __name__ == '__main__':
    serve(app, host='localhost', port=8080)
