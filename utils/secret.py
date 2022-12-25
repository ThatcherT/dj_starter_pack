import secrets


def generate_secret_key():
    return secrets.token_urlsafe()
