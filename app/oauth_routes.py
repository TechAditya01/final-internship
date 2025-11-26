from flask import Blueprint, redirect, url_for, session
from requests_oauthlib import OAuth2Session

oauth_bp = Blueprint("oauth", __name__)

@oauth_bp.route("/auth/google")
def google_login():
    # Example minimal OAuth setup
    client_id = "YOUR_CLIENT_ID"
    redirect_uri = url_for("oauth.google_callback", _external=True)
    scope = ["https://www.googleapis.com/auth/userinfo.email"]
    google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = google.authorization_url(
        "https://accounts.google.com/o/oauth2/auth",
        access_type="offline",
        prompt="select_account"
    )
    session["oauth_state"] = state
    return redirect(authorization_url)

@oauth_bp.route("/auth/google/callback")
def google_callback():
    return "Google OAuth callback reached"
