import random
from utils.secret import generate_secret_key


def welcome():
    welcome_messages = [
        "LGTM!",
        "This project will be the one to change the world.",
        "You are a great developer.",
        "Python is my love language.",
        "Don't forget to drink water.",
        "Remember your ambitions.",
        "Starting things is fun!",
    ]
    print(random.choice(welcome_messages))


def add_secret_key():
    "open .env, generate SECRET_KEY, write to .env, return secret"
    with open("./.env", "rw") as f:
        secret_key = generate_secret_key()
        # write
        dj_secret = f"DJANGO_SECRET_KEY={secret_key}"
        f.write(dj_secret)
    return secret_key


if __name__ == "__main__":
    sk = add_secret_key()
    print(sk)
