#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)


def main():
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='127.0.0.1', port=8000)


if __name__ == '__main__':
    main()
