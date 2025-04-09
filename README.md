# Ghostguard
GhostGuard: A Smart File Deletion Interception and Backup System
GhostGuard is a cybersecurity tool designed to protect against accidental file deletions and insider threats. It monitors your system for file deletion events and automatically intercepts them, archiving the files to a secure backup location. This ensures that no important files are lost and provides an extra layer of data protection.

Key Features:
File Deletion Monitoring: Continuously monitors specified directories or the entire system for any file deletion actions.

Smart Archiving: Intercepts deleted files and archives them to a backup directory with a timestamp for easy retrieval.

Backup Management: Automatically organizes and stores backups to prevent data loss from accidental or malicious deletions.

Future Integrations: Plans to integrate with a web dashboard, email alerts, and other notification systems like Slack and WhatsApp for proactive data recovery.

Technologies Used:
Python: The core language used for building the application.

Watchdog: For monitoring filesystem changes and detecting file deletions.

Flask (Phase 2): For building a web dashboard to manage logs and restore deleted files.

SMTP / Slack / WhatsApp API: For sending notifications on file deletions.

Installation:
Clone the repository.

Create a virtual environment: python -m venv venv

Install dependencies: pip install -r requirements.txt

Configure .env file for email, Slack, and WhatsApp notifications.

Future Enhancements:
Web dashboard to view logs and restore deleted files.

Configurable file/folder protection settings.

Background service for continuous file monitoring.
