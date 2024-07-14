#!/usr/bin/env python
import os

from src import create_app, create_db

config_name = os.getenv('FLASK_CONFIG', 'default')
app = create_app(config_name)


if __name__ == '__main__':
    if config_name == 'development':
        create_db(app)
    app.run()
