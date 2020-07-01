from webshop.api import client

from flask import Flask


app = Flask(__name__)


def main():
    client.start_client()


if __name__ == "__main__":
    main()
#    app.run(debug=True)
