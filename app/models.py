from datetime import datetime
from app import db  # Importing db from app/__init__.py

class User(db.Model):
    """User model for authentication and roles."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), default="user")  # "user" or "admin"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User {self.username}>'

    # Relationships
    files = db.relationship('File', back_populates='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)


class File(db.Model):
    """File model for tracking files and versions."""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(512), nullable=False)  # Path of the file
    size = db.Column(db.Integer, nullable=False)  # File size in bytes
    deleted_at = db.Column(db.DateTime)  # Timestamp when the file was deleted (if applicable)
    restored_at = db.Column(db.DateTime)  # Timestamp when the file was restored (if applicable)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Associated user
    user = db.relationship('User', back_populates='files')

    versions = db.relationship('FileVersion', backref='file', lazy=True)
    backups = db.relationship('FileBackup', backref='file', lazy=True)

    def __repr__(self):
        return f'<File {self.filename}>'


class FileVersion(db.Model):
    """File versioning model to track changes or multiple versions."""
    id = db.Column(db.Integer, primary_key=True)
    version_number = db.Column(db.Integer, nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    path = db.Column(db.String(512), nullable=False)  # Path to the versioned file

    def __repr__(self):
        return f'<FileVersion {self.version_number} of {self.file.filename}>'


class FileBackup(db.Model):
    """Model for tracking backups of files."""
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
    backup_path = db.Column(db.String(512), nullable=False)  # Path of the backup file
    backup_time = db.Column(db.DateTime, default=datetime.utcnow)  # Time when the backup was made

    def __repr__(self):
        return f'<FileBackup for {self.file.filename}>'


class Notification(db.Model):
    """Notification model to track alerts sent to users."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Notification for User {self.user_id}: {self.message}>'


class BackgroundJob(db.Model):
    """Model for background jobs such as scheduled notifications."""
    id = db.Column(db.Integer, primary_key=True)
    job_type = db.Column(db.String(100), nullable=False)  # E.g., 'restore', 'notify'
    status = db.Column(db.String(50), nullable=False, default="pending")  # 'pending', 'completed', 'failed'
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    result = db.Column(db.String(500))

    def __repr__(self):
        return f'<BackgroundJob {self.job_type} - Status: {self.status}>'
