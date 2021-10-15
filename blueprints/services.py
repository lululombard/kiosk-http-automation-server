from flask import jsonify
import dbus
import os
import logging
import flask
from flask import Blueprint, jsonify

services_blueprint = Blueprint("services", __name__)

allowed_services = os.getenv(
    "ALLOWED_KIOSK_SERVICES", "grafana-kiosk.service;vlc.service"
).split(";")

system_bus = dbus.SystemBus()
systemd1 = system_bus.get_object(
    "org.freedesktop.systemd1", "/org/freedesktop/systemd1"
)
systemd = dbus.Interface(systemd1, "org.freedesktop.systemd1.Manager")


@services_blueprint.route("/<string:service>/status", methods=["GET"])
def get_service_status(service: str) -> flask.Response:
    if service not in allowed_services:
        return jsonify(success=False, error="Service not allowed")
    try:
        for unit in systemd.ListUnits():
            if unit[0] == service:
                return jsonify(success=True, running=unit[3] == "active")

        return jsonify(success=True, running=False)
    except Exception as e:
        logging.error("Service failed to start: {}".format(str(e)))
        return jsonify(success=False, error=str(e))


@services_blueprint.route("/<string:service>/start", methods=["POST"])
def start_service(service: str) -> flask.Response:
    if service not in allowed_services:
        return jsonify(success=False, error="Service not allowed")
    try:
        systemd.StartUnit(service, "fail")
        return jsonify(success=True)
    except Exception as e:
        logging.error("Service failed to start: {}".format(str(e)))
        return jsonify(success=False, error=str(e))


@services_blueprint.route("/<string:service>/stop", methods=["POST"])
def stop_service(service: str) -> flask.Response:
    if service not in allowed_services:
        return jsonify(success=False, error="Service not allowed")
    try:
        systemd.StopUnit(service, "fail")
        return jsonify(success=True)
    except Exception as e:
        logging.error("Service failed to start: {}".format(str(e)))
        return jsonify(success=False, error=str(e))
