from flask import Flask, jsonify, request, render_template
from games.hexapown import HexaPown

hp = HexaPown()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hexapown')
def hexapown():
    return render_template('hexapown.html')

