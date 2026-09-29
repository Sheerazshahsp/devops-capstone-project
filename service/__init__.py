"""
Package initializer for Accounts service
"""
import sys
from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman
from service import config
from service.common import log_handlers

# Create the Flask app
app = Flask(__name__)
app.config.from_object(config)

# Initialize CORS
CORS(app)

# Initialize Talisman with security headers configuration
talisman = Talisman(
    app,
    content_security_policy={
        'default-src': '\'self\'',
        'object-src': '\'none\''
    },
    force_https=False
)

# Dependencies that require the app context
from service import routes, models  # noqa: F401, E402
from service.common import error_handlers  # noqa: F401, E402

# Set up logging for production
log_handlers.init_app(app)

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T S   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    models.init_db(app)  # make sure database is initialized
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    # gunicorn needs exit code 4 to stop spawning workers when DB is down
    sys.exit(4)

app.logger.info("Service initialized!")
