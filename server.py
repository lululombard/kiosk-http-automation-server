import os
import argparse
import sys
import flask
from flask import (
    Flask,
    jsonify,
)
from blueprints.display import display_blueprint
from blueprints.services import services_blueprint

if not os.geteuid() == 0 and not os.environ.get("IGNORE_KIOSK_ROOT"):
    messages = [
        "This service requires root access in order to use certain ports, summon systemd services, and run apps as other users",
        "Please try again with sudo to fix this issue",
        "You can also set the environment variable IGNORE_KIOSK_ROOT to 1 but expect things to break",
    ]
    print("\n".join(messages))
    sys.exit(1)

app = Flask(__name__)

app.register_blueprint(display_blueprint, url_prefix="/display")
app.register_blueprint(services_blueprint, url_prefix="/services")


@app.route("/healthcheck", methods=["GET"])
def healthcheck() -> flask.Response:
    return jsonify(success=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dev machine service")

    parser.add_argument(
        "--host",
        type=str,
        help="Bind host address for the web server",
        default="0.0.0.0",
    )
    parser.add_argument(
        "--port", type=int, help="Bind port for the web server", default=5000
    )

    args = parser.parse_args()

    app.run(host=args.host, port=args.port)
