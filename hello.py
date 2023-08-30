from flask import Flask, render_template

app = Flask(__name__, static_folder='static')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/grid")
def grid_page():
    return render_template('grid.html')
