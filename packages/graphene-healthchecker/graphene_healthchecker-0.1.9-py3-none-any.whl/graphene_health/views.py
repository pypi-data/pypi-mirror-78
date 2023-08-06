from . import app, health, envdump
from flask import jsonify, request
from datetime import datetime, timedelta

from prometheus_client import Gauge
from prometheus_client import make_wsgi_app
from werkzeug.wsgi import DispatcherMiddleware

from .utils import query, parse_time, format_time

object_210 = dict()


def check_blockchain_alive():
    global object_210
    object_210 = query(
        app.config["witness_url"], ["database", "get_objects", [["2.1.0"]]]
    )
    return True, object_210


def check_network_node_plugin():
    return True, query(app.config["witness_url"], ["network_node", "get_info", []])


def check_headblock_timestamp():
    head_time = parse_time(object_210.get("time"))
    try:
        if not head_time:
            return False, "No 2.1.0 object available yet"
        if head_time < datetime.utcnow() + timedelta(
            seconds=30
        ) and head_time > datetime.utcnow() - timedelta(seconds=30):
            return True, "head_block_time ok"
    except Exception:
        pass
    return False, f"head_block_time not ok: {head_time}"


def check_maintenance_block_in_future():
    try:
        maint_time = parse_time(object_210.get("next_maintenance_time"))
        if not maint_time:
            return False, "No 2.1.0 object available yet"
        if maint_time > datetime.utcnow() - timedelta(seconds=60):
            return True, "maintenance_block_time ok"
    except Exception:
        pass
    return False, f"maintenance_block_time not ok: {maint_time}"


def additional_data():
    return dict()


def get_headblock():
    data = dict()
    try:
        data = query(
            app.config["witness_url"], ["database", "get_objects", [["2.1.0"]]]
        )
    except Exception:
        pass
    return data.get("head_block_number") or 0


def get_connected_count():
    try:
        network_info = query(
            app.config["witness_url"], ["network_node", "get_info", []]
        )
        return network_info.get("connection_count") or 0
    except Exception:
        return 0


# Healthchecker
health.add_check(check_blockchain_alive)
# health.add_check(check_network_node_plugin)
health.add_check(check_headblock_timestamp)
health.add_check(check_maintenance_block_in_future)
envdump.add_section("additional_data", additional_data)

app.add_url_rule("/-/health", "healthcheck", view_func=lambda: health.run())
app.add_url_rule("/", "healthcheckroot", view_func=lambda: health.run())
app.add_url_rule("/-/env", "environment", view_func=lambda: envdump.run())


# Prometheus exporeter
clean_endpoint = app.config["witness_url"].split("@")[-1]
BACKEND_HEADBLOCK_NUM = Gauge(
    "backend_headblock_number", "Backend Head Block Number", ["endpoint"]
)
BACKEND_CONNECTIONS_NUM = Gauge(
    "backend_num_connections", "Backend Connections in P2P network", ["endpoint"]
)
BACKEND_HEADBLOCK_NUM.labels(clean_endpoint).set_function(get_headblock)
# BACKEND_CONNECTIONS_NUM.labels(clean_endpoint).set_function(get_connected_count)
# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})
