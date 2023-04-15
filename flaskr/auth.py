from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity

from models.member import Member
from services.database import db_session
from services.utilities import Utilities, admin_required, user_required, config

from bcrypt import checkpw

# Configure blueprint
auth = Blueprint('auth', __name__, url_prefix=f'{config.server.version}/auth')


@auth.route("/login", methods=['POST'])
def post_auth_login():
    """
    Logs a user in.\n
    Returns a ``JWT`` token for authentication.

    :return: JSON detailed status response with (login) data.
    """
    try:
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not isinstance(email, str):
            raise ValueError(f"Expected str, instead got {type(email)} for field <email>")
        if not isinstance(password, str):
            raise ValueError(f"Expected str, instead got {type(password)} for field <password>")

    except (AttributeError, ValueError) as e:
        return Utilities.detailed_response(400, "Bad request, see details.", {"error": e.__str__()})

    member = Member.query.filter_by(email=email).first()

    if member is None or checkpw(password.encode("UTF-8"), member.password.encode("UTF-8")) is False:
        return Utilities.response(401, "Unauthorized, wrong username/password")

    lifetime = Utilities.generate_token_timedelta()
    member.token = create_access_token(identity=member.uuid, fresh=False, expires_delta=lifetime,
                                     additional_claims={"email": member.email, "admin": member.admin})
    db_session.commit()

    member.perform_tracking(address=request.remote_addr, login=True)

    return Utilities.custom_response(200, f"Successfully logged in as {member.get_fullname()}",
                                     {"login": {"uuid": member.uuid, "token": member.token,
                                                "lifetime": lifetime.total_seconds()}})


@auth.route("/test", methods=['GET'])
@user_required()
def get_auth_test():
    """
    Simply checks if you're properly logged in.

    :return: JSON status response.
    """
    current_member = Member.query.filter_by(uuid=get_jwt_identity()).first()

    if current_member is None:
        return Utilities.response(401, "Unauthorized")

    return Utilities.custom_response(200, f"Logged in as {current_member.get_fullname()}",
                                     {"login": {"uuid": current_member.uuid, "admin": current_member.admin}})


@auth.route("/admin/test", methods=['GET'])
@admin_required()
def get_auth_admin_test():
    """
    Simply checks if you're properly logged in as an administrator.

    :return: JSON status response.
    """
    current_member = Member.query.filter_by(uuid=get_jwt_identity()).first()

    if current_member is None:
        return Utilities.response(401, "Unauthorized")

    return Utilities.custom_response(200, f"Logged in as {current_member.get_fullname()}",
                                     {"login": {"uuid": current_member.uuid, "admin": current_member.admin}})
