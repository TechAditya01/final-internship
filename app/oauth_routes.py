import os
from flask import Blueprint, redirect, url_for, session, request, jsonify
from requests_oauthlib import OAuth2Session

oauth_bp = Blueprint("oauth", __name__)

# --- Load from environment variables ---
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# --- Google endpoints ---
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

# Required scopes
SCOPE = ["https://www.googleapis.com/auth/userinfo.email", "openid", "profile"]

@oauth_bp.route("/auth/google")
def google_login():
    if not CLIENT_ID or not CLIENT_SECRET:
        return "❌ Google OAuth not configured. Missing GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET.", 500

    google = OAuth2Session(
        CLIENT_ID,
        scope=SCOPE,
        redirect_uri=url_for("oauth.google_callback", _external=True)
    )

    auth_url, state = google.authorization_url(
        AUTHORIZATION_BASE_URL,
        access_type="offline",
        prompt="select_account"
    )

    session["oauth_state"] = state
    return redirect(auth_url)


@oauth_bp.route("/auth/google/callback")
def google_callback():
    google = OAuth2Session(
        CLIENT_ID,
        state=session.get("oauth_state"),
        redirect_uri=url_for("oauth.google_callback", _external=True)
    )

    token = google.fetch_token(
        TOKEN_URL,
        client_secret=CLIENT_SECRET,
        authorization_response=request.url
    )

    # Fetch user info
    resp = google.get(USER_INFO_URL)
    user_info = resp.json()

    # Store in session
    session["user"] = user_info

    return jsonify({
        "message": "Login Successful",
        "user": user_info
    })
