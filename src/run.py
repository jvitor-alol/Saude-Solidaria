#!/usr/bin/env python
import os

from app import create_app, create_db

config_name = os.getenv('FLASK_CONFIG', 'default')
app = create_app(config_name)
create_db(app)


if __name__ == '__main__':
    app.run()
