import subprocess
import os
import logging
import flask
from flask import Blueprint, jsonify

display_blueprint = Blueprint("display", __name__)

linux_user = os.getenv("DISPLAY_KIOSK_USER", "ubuntu")
on_command = os.getenv("DISPLAY_KIOSK_ON_COMMAND", "DISPLAY=:0 xset dpms force on")
off_command = os.getenv(
    "DISPLAY_KIOSK_OFF_COMMAND", "DISPLAY=:0 xset dpms force suspend"
)
state_command = os.getenv("DISPLAY_KIOSK_STATE_COMMAND", "DISPLAY=:0 xset q 2")


def generate_bash_command(command: str) -> list:
    return ["bash", "-c", "sudo -u {} {}".format(linux_user, command)]


@display_blueprint.route("/status", methods=["GET"])
def get_state() -> flask.Response:
    try:
        result = subprocess.check_output(generate_bash_command(state_command))
        status = "Monitor is On" in result.decode("UTF-8")
        return jsonify(success=True, on=status)
    except Exception as e:
        logging.error("Display check failed: {}".format(str(e)))
        return jsonify(success=False, error=str(e))


@display_blueprint.route("/on", methods=["POST"])
def turn_on() -> flask.Response:
    try:
        subprocess.Popen(generate_bash_command(on_command))
        return jsonify(success=True)
    except Exception as e:
        logging.error("Display turn on failed: {}".format(str(e)))
        return jsonify(success=False, error=str(e))


@display_blueprint.route("/off", methods=["POST"])
def turn_off() -> flask.Response:
    try:
        subprocess.Popen(generate_bash_command(off_command))
        return jsonify(success=True)
    except Exception as e:
        logging.error("Display turn off failed: {}".format(str(e)))
        return jsonify(success=False, error=str(e))
