from . import app
import os
import json
from flask import jsonify, request, make_response

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

# Helper function to load data
def load_data():
    return data

@app.route("/health")
def health():
    return jsonify(status="OK"), 200

@app.route("/count")
def count():
    if data:
        return jsonify(length=len(data)), 200
    return jsonify(message="Internal server error"), 500

@app.route("/picture", methods=["GET"])
def get_pictures():
    return data

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return picture
    return {"message": "picture not found"}, 404

@app.route("/picture", methods=["POST"])
def create_picture():

    # get data from the json body
    picture_in = request.json
    print(picture_in)

    # if the id is already there, return 303 with the URL for the resource
    for picture in data:
        if picture_in["id"] == picture["id"]:
            return {
                "Message": f"picture with id {picture_in['id']} already present"
            }, 302

    data.append(picture_in)
    return picture_in, 201


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):

    # get data from the json body
    picture_in = request.json

    for index, picture in enumerate(data):
        if picture["id"] == id:
            data[index] = picture_in
            return picture, 201

    return {"message": "picture not found"}, 404

@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return "", 204
    
    return jsonify(message="Picture not found"), 404

