from api import app
import os

if __name__ == '__main__': # Get the environment (development or production)
    environment = os.getenv('FLASK_ENV', 'development')
    if environment == 'development': # Development settings
        app.run(debug=True, host='0.0.0.0', port=5000)
    else: # Production settings (ensure to run behind a production server, like Gunicorn or uWSGI)
        app.run(debug=False, host='0.0.0.0', port=5000)