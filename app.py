#!/usr/bin/env python
from src import create_app, create_db


def main() -> None:
    app = create_app()
    create_db(app)
    app.run(debug=True)


if __name__ == '__main__':
    main()
#qualquer coisa