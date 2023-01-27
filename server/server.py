import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/html', '.html')


from flask import Flask, render_template
from flask_cors import CORS
from flask import jsonify
from flask import render_template




app = Flask(__name__,
            static_folder = "../client/dist",
            template_folder = "../client/dist")
CORS(app)

@app.route("/")
def index():
 return render_template('index.html')
