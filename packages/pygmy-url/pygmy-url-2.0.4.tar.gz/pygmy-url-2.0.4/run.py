#!/usr/bin/env python
from flask import Flask

from shorty.shorty import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
