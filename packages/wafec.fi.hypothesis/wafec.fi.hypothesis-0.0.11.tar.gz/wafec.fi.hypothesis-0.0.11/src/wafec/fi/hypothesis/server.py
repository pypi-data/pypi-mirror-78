from wafec.fi.hypothesis.controllers import app

import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--host', type=str, default='localhost')
    parser.add_argument('-p', '--port', type=int, default=8080)
    args = parser.parse_args()
    app.run(port=args.port, host=args.host)
