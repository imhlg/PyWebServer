from flask import Flask, render_template, url_for, request

app = Flask(__name__)


@app.route('/world')
def hello_world():
    print('hello world')
    return 'Hello World! from Pycharm on browser and editing more, vene now'


@app.route('/')
def home():
    print(url_for('static', filename='iconlight.ico'))
    return render_template('forum.html')


@app.route('/<string:page_name>')
def dynamicgenpages(page_name):
    return render_template(page_name)


@app.route('/submit_form', methods=['POST', 'GET'])
def submitt():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        writefile(data)
    return render_template('/world.html')


@app.route('/forum_details', methods=['POST', 'GET'])
def fsubmitt():
    if request.method == 'POST':
        fdata = request.form.to_dict()
        print(fdata)
        fwriter(fdata)
    return render_template('/index.html')


def fwriter(data):
    with open('forum-responses.txt', mode='a') as database:
        auth = data['author']
        messg = data['message']
        file = database.write(f'\n{auth},\t{messg}\n')


def writefile(ndata):
    with open('contact-form-responses.txt', mode='a') as database:
        mail = ndata['email']
        subj = ndata['subject']
        body = ndata['message']
        file = database.write(f'\n{mail},\t{subj},\t{body}\n')
