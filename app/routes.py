from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from app import db
from app.models import FileBackup, User
from app.notifications import email_notifier, slack_notifier
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

main_blueprint = Blueprint('main', __name__)

# Home page: List backed-up files and show options to restore or download
@main_blueprint.route('/')
def index():
    files = FileBackup.query.all()  # Retrieve all file backups from the database
    return render_template('index.html', files=files)

# Page to restore deleted file
@main_blueprint.route('/restore/<int:file_id>', methods=['GET', 'POST'])
@login_required
def restore(file_id):
    file = FileBackup.query.get_or_404(file_id)

    if request.method == 'POST':
        try:
            # Example restore logic (implement your actual restore function)
            flash(f"Restoring {file.backup_path}...", 'success')

            # Send email notification
            email_notifier.send_email(
                subject="File Restoration Notification",
                recipient=current_user.email,  # Use the logged-in user's email
                message=f"The file {file.backup_path} has been restored."
            )

            # Send Slack notification
            slack_notifier.send_slack_notification(
                message=f"File {file.backup_path} has been restored successfully."
            )

            # Redirect back to the homepage after restoring
            return redirect(url_for('main.index'))

        except Exception as e:
            flash(f"Error restoring file: {e}", 'danger')
            return redirect(url_for('main.index'))

    return render_template('restore.html', file=file)

# Configuration page: Allow users to set folder or file paths for backup/restore
@main_blueprint.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    if request.method == 'POST':
        # Here, you'd process user inputs to configure file/folder paths
        # Example: saving paths to the config file or the database
        flash("Configuration updated successfully!", 'success')
        return redirect(url_for('main.config'))

    return render_template('config.html')

# User registration page
@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(password, method='sha256')

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email address already in use.", 'danger')
            return redirect(url_for('main.register'))

        # Create and add new user
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.", 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

# User login page
@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Login successful!", 'success')
            return redirect(url_for('main.index'))
        else:
            flash("Invalid email or password.", 'danger')
            return redirect(url_for('main.login'))

    return render_template('login.html')

# User logout route
@main_blueprint.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the current user
    flash("You have been logged out.", 'success')
    return redirect(url_for('main.index'))

# Page to download the file backup
@main_blueprint.route('/download/<int:file_id>')
@login_required
def download(file_id):
    file = FileBackup.query.get_or_404(file_id)

    # Logic to serve the file for download (for example, send it as a response)
    try:
        return send_file(file.backup_path, as_attachment=True, attachment_filename=file.file_name)
    except Exception as e:
        flash(f"Error occurred while downloading: {e}", 'danger')
        return redirect(url_for('main.index'))

# Page to handle any errors (e.g., 404)
@main_blueprint.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# Page for settings or configuration (for example, email and notification settings)
@main_blueprint.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Handle settings update, such as changing notification preferences or email settings
        flash("Settings updated successfully!", 'success')
        return redirect(url_for('main.settings'))

    return render_template('settings.html')

# Admin dashboard to view logs or perform other admin tasks
@main_blueprint.route('/admin')
@login_required
def admin():
    # Admin-only route (ensure only admin can access this)
    if current_user.role == 'admin':  # Check if the user has admin privileges
        return render_template('admin_dashboard.html')
    else:
        flash("You do not have permission to access this page.", 'danger')
        return redirect(url_for('main.index'))
