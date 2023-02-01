from flask import Flask
from flask_cors import CORS
from flask import jsonify, request
from name_generator import NameGenerator

app = Flask(__name__)
ng = NameGenerator()
CORS(app)

@app.route("/")
def index():
   return jsonify("miau")

@app.route("/create_generator", methods = ['POST'])
def create_generator():

    return jsonify(ng.create_generator(request.json['name'], request.json['depth'],request.json['filenames'],request.json['optional_values'], request.json['lmin'], request.json['lmax']))

@app.route("/get_generators")
def get_generators():
    print("gens: " + str(ng.get_generators()))
    return jsonify(ng.get_generators())


@app.route("/get_inputfiles")
def get_input_files():
    return jsonify(ng.get_input_files())

@app.route("/generate_names", methods = ['POST'])
def generate_names():
    return jsonify(ng.generate_names(
        request.json['generator_name'],
        request.json['amount'],
        request.json['depth'],
        request.json['lmin'],
        request.json['lmax']))
