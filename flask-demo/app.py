from flask import Flask, redirect, url_for, abort, render_template, request, flash, send_from_directory
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from cedarpy import is_authorized, AuthzResult, Decision
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

# This class sets up watchdog on the policy file. 

class FileChangeHandler(FileSystemEventHandler):
    global file_content

    def on_modified(self, event):
        if event.src_path == 'flask.cedar.policy':  # Modify path if needed
            file_content = read_file_to_string(event.src_path)

def read_file_to_string(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

# Load up Demo App Entities and Schema from file

cedar_app_entities = read_file_to_string('entities.json')
cedar_app_schema = read_file_to_string('schema.json')

currentdir = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__,instance_path=currentdir)
print(app.instance_path)
app.secret_key = '1234'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load sample users to login from users.dat

def load_users_from_file(file_path):
    users = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 3:
                username, password, role = parts
                users[username] = {'password': password, 'role': role}
    return users

users = load_users_from_file('users.dat')

class User(UserMixin):
    def __init__(self, username, role):
        self.id = username
        self.role = role

@login_manager.user_loader
def load_user(username):
    if username not in users:
        return None
    user_data = users[username]
    return User(username, user_data['role'])

# This ensures you cannot bypass security for accessing images

@app.route('/protected/<path:filename>')
@login_required
def protected(filename):
    return send_from_directory(
        os.path.join(app.instance_path, 'protected'),
        filename
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username]['password'] == password:
            user = User(username, users[username]['role'])
            login_user(user)
            # Don't do this in real life - this is just for demo purposes to make it easier to follow along
            global request_adm
            global request_photo
            global request_manage
            global public_photos
            request_adm = {"principal": f"PhotoApp::User::\"{current_user.id}\"","action": "PhotoApp::Action::\"siteAdmin\"","resource": "PhotoApp::Photo::\"\"","context": { }}
            request_photo = {"principal": f"PhotoApp::User::\"{current_user.id}\"","action": "PhotoApp::Action::\"viewPhoto\"","resource": "PhotoApp::Album::\"DoePhotos\"","context": { }}
            public_photos = {"principal": f"PhotoApp::User::\"{current_user.id}\"","action": "PhotoApp::Action::\"viewPhoto\"","resource": "PhotoApp::Album::\"DoePublicPhotos\"","context": { }}
            request_manage = {"principal": f"PhotoApp::User::\"{current_user.id}\"","action": "PhotoApp::Action::\"managePhoto\"","resource": "PhotoApp::Album::\"DoePhotos\"","context": { }}
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
#@login_required
def index():
    return render_template('index.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    policy = read_file_to_string('flask.cedar.policy')
    authz_result: AuthzResult = is_authorized(request_adm, policy, cedar_app_entities, cedar_app_schema, False)
    if Decision.Deny == authz_result.decision:
        return render_template('denied.html')
        abort(403)  # Forbidden
    return render_template('admin.html')

@app.route('/photos')
@login_required
def photo_page():
    policy = read_file_to_string('flask.cedar.policy')
    authz_result: AuthzResult = is_authorized(request_photo, policy, cedar_app_entities, cedar_app_schema, False)
    if Decision.Deny == authz_result.decision:
        return render_template('denied.html')
        abort(403)  # Forbidden
    return render_template('photos.html')

@app.route('/public-photos')
@login_required
def public_page():
    policy = read_file_to_string('flask.cedar.policy')
    authz_result: AuthzResult = is_authorized(public_photos, policy, cedar_app_entities, cedar_app_schema, False)
    if Decision.Deny == authz_result.decision:
        return render_template('denied.html')
        abort(403)  # Forbidden
    return render_template('public-photos.html')

@app.route('/manage')
@login_required
def photo_manage():
    policy = read_file_to_string('flask.cedar.policy')
    authz_result: AuthzResult = is_authorized(request_manage, policy, cedar_app_entities, cedar_app_schema, False)
    if Decision.Deny == authz_result.decision:
        return render_template('denied.html')
        abort(403)  # Forbidden
    return render_template('photos-manage.html')

if __name__ == '__main__':
    policy = read_file_to_string('flask.cedar.policy')
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path='flask.cedar.policy', recursive=False)
    observer.start()
    try:
        app.run(port=8080,debug=True)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
