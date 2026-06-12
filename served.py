from flask import Flask,render_template

app = Flask(__name__)
@app.route('/world')
def hello_world():
    print('hello world')
    return 'Hello World! from Pycharm on browser and editing more, vene now'

@app.route('/')
def home():
    return render_template('index.html')
