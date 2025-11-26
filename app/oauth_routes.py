import os
from flask import Blueprint, redirect, url_for, session, request, flash
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from app.models import Student, Admin, db

oauth_bp = Blueprint("oauth", __name__)

# --- OAuth Home Test ---
@oauth_bp.route("/oauth")
def oauth_home():
    return "OAuth blueprint is working!"

# --- Google OAuth login ---
@oauth_bp.route("/auth/google")
def google_login():
    user_type = request.args.get("type")  # student or admin
    if user_type not in ["student", "admin"]:
        return "Invalid type parameter", 400

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [os.environ.get("GOOGLE_REDIRECT_URI")],
            }
        },
        scopes=["openid", "email", "profile"]
    )
    flow.redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI")

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )
    session["state"] = state
    session["user_type"] = user_type
    return redirect(authorization_url)

# --- OAuth Callback ---
@oauth_bp.route("/auth/callback")
def google_callback():
    state = session.get("state")
    user_type = session.get("user_type")
    if not state or not user_type:
        return "Session expired or invalid.", 400

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [os.environ.get("GOOGLE_REDIRECT_URI")],
            }
        },
        scopes=["openid", "email", "profile"],
        state=state
    )
    flow.redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI")

    # Get authorization response URL
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Get user info
    credentials = flow.credentials
    request_session = google_requests.Request()
    id_info = id_token.verify_oauth2_token(
        credentials.id_token, request_session, os.environ.get("GOOGLE_CLIENT_ID")
    )

    email = id_info.get("email")
    name = id_info.get("name")

    # --- Check / Create user in DB ---
    if user_type == "student":
        user = Student.query.filter_by(email=email).first()
        if not user:
            user = Student(name=name, email=email)
            db.session.add(user)
            db.session.commit()
    else:
        user = Admin.query.filter_by(email=email).first()
        if not user:
            user = Admin(name=name, email=email)
            db.session.add(user)
            db.session.commit()

    session["user_id"] = user.id
    session["user_type"] = user_type

    flash(f"Logged in successfully as {name} ({user_type})", "success")
    return redirect(url_for("main.index"))
