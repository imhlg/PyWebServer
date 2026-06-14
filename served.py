import os

from flask import Flask, abort, jsonify, redirect, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

JD_FOLDER = os.path.join(os.path.dirname(__file__), 'JDs')
FORUM_FILE = os.path.join(os.path.dirname(__file__), 'forum-responses.txt')
os.makedirs(JD_FOLDER, exist_ok=True)


def list_jd_files():
    if not os.path.isdir(JD_FOLDER):
        return []

    files = []
    for entry in os.listdir(JD_FOLDER):
        full_path = os.path.join(JD_FOLDER, entry)
        if os.path.isfile(full_path):
            files.append({
                'name': entry,
                'size': os.path.getsize(full_path),
                'updated_at': os.path.getmtime(full_path),
            })

    files.sort(key=lambda item: item['updated_at'], reverse=True)
    return files


@app.route('/achalgarg')
def hello_world():
    print('hello world')
    return 'Hello World! Custom built website via copilot, but functionality hand made by HL'


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

    return render_template('cv.html', jd_message=message, jd_files=list_jd_files())


@app.route('/api/jd-files')
def api_jd_files():
    return jsonify({'files': [item['name'] for item in list_jd_files()]})


@app.route('/download_jd/<path:filename>')
def download_jd(filename):
    safe_name = secure_filename(filename)
    if not safe_name or not os.path.isfile(os.path.join(JD_FOLDER, safe_name)):
        abort(404)
    return send_from_directory(JD_FOLDER, safe_name, as_attachment=True)


@app.route('/<string:page_name>')
def dynamicgenpages(page_name):
    template_context = {}
    if page_name == 'cv.html':
        template_context['jd_files'] = list_jd_files()
    return render_template(page_name, **template_context)


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
        fwriter(fdata)
        return redirect(url_for('dynamicgenpages', page_name='forum.html'))
    return render_template('forum.html', posts=read_forum_posts())


@app.route('/api/forum-posts')
def api_forum_posts():
    return jsonify({'posts': read_forum_posts()})


def read_forum_posts():
    if not os.path.exists(FORUM_FILE):
        return []

    posts = []
    with open(FORUM_FILE, 'r', encoding='utf-8') as database:
        for raw_line in database:
            line = raw_line.strip()
            if not line or ',' not in line:
                continue
            author, message = line.split(',', 1)
            author = author.strip()
            message = message.replace('\t', ' ').strip()
            if author and message:
                posts.append({'author': author, 'message': message})

    return posts


def fwriter(data):
    author = (data.get('author') or '').strip()
    message = (data.get('message') or '').strip()
    if not author or not message:
        return

    with open(FORUM_FILE, mode='a', encoding='utf-8') as database:
        database.write(f'\n{author},\t{message}\n')


def writefile(ndata):
    with open('contact-form-responses.txt', mode='a') as database:
        mail = ndata['email']
        subj = ndata['subject']
        body = ndata['message']
        file = database.write(f'\n{mail},\t{subj},\t{body}\n')
