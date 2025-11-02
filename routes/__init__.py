from flask import Blueprint

# Create blueprint instances
auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__)
clerk_bp = Blueprint('clerk', __name__)
resident_bp = Blueprint('resident', __name__)
public_bp = Blueprint('public', __name__)

# Import route handlers
from . import auth, admin, clerk, resident, public