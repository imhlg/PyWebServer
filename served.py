import os

from flask import Flask, render_template, url_for, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

JD_FOLDER = os.path.join(os.path.dirname(__file__), 'JDs')
os.makedirs(JD_FOLDER, exist_ok=True)


@app.route('/world')
def hello_world():
    print('hello world')
    return 'Hello World! from Pycharm on browser and editing more, vene now'


@app.route('/')
def home():
    print(url_for('static', filename='iconlight.ico'))
    return render_template('index.html')


@app.route('/robots.txt')
def robots():
    return send_from_directory('.', 'robots.txt', mimetype='text/plain')


@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml', mimetype='application/xml')


@app.route('/upload_jd', methods=['POST'])
def upload_jd():
    file = request.files.get('jd_file')
    message = 'Please choose a JD file to upload.'

    if file and file.filename:
        filename = secure_filename(file.filename)
        save_path = os.path.join(JD_FOLDER, filename)
        file.save(save_path)
        message = f'JD uploaded successfully to JDs/{filename}.'

    return render_template('cv.html', jd_message=message)


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
    return render_template('/world.html')


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
