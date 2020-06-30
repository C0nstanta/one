from webshop.api import client

from flask import Flask


app = Flask(__name__)


if __name__ == "__main__":
    client.start_client()
    app.run(debug=True)
