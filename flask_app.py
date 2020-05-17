# convert this into an API that takes a bunch of loans and returns enhanced loans
from flask import Flask, request, jsonify
from generate_graphs import generate_random_graph_data, generate_graph_combinations
import pandas as pd
import numpy as np
import json

app = Flask(__name__)


@app.route("/getjourneydata", methods=["POST"])
def generate_journey_data():
    # Get the graph type
    # Provide a starting value for generating graphs
    # call the function and return the value to the user
    req_data = request.get_json()
    journey_parameters = {
        "journey_type": req_data["journey_type"],
        "init_value": req_data["init_value"] if req_data["init_value"] is not None else 25000,
    }
    print(journey_parameters)
    journey_details = generate_random_graph_data(**journey_parameters)
    return jsonify(journey_details)


@app.route("/generatealldata", methods=["POST"])
def generate_all_journey_data():
    # construct the loan input DF and also load the rates df
    req_data = request.get_json()
    journey_parameters = {"journey_types": req_data["journey_types"]}
    print(journey_parameters)

    journey_df = generate_graph_combinations(**journey_parameters)
    return_json = journey_df.to_json(orient="records")
    return return_json


if __name__ == "__main__":
    app.run(debug=True, port=5000)
