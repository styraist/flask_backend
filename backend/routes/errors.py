import traceback

from flask import Blueprint, jsonify
from werkzeug.exceptions import NotFound
from marshmallow import ValidationError

error_bp = Blueprint('errors', __name__)


@error_bp.app_errorhandler(ValidationError)
def handle_invalid_data(error):
    print(traceback.format_exc())
    return jsonify({"message": "Incorrect format data"}), 400

@error_bp.app_errorhandler(NotFound)
def handle_not_found(error):
    print(traceback.format_exc())
    return jsonify({"message": "This resource isn't available"}), 404

@error_bp.app_errorhandler(Exception)
def handle_generic_exception(error):
    print(traceback.format_exc())
    return jsonify({"message": "Unknown error occured. Please check the logs for more details"}), 500