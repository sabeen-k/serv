"""
WSGI entry point for the Flask application.

This file serves as the WSGI entry point for production deployment,
allowing the application to be served by WSGI-compliant servers
like Gunicorn, uWSGI, or Apache with mod_wsgi.
"""

from app import app

if __name__ == "__main__":
    # When run directly, start the Flask development server
    app.run()
else:
    # When imported by a WSGI server, provide the application
    application = app