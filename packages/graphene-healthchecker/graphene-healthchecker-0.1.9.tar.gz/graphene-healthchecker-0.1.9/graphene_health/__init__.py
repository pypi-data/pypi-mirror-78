from flask import Flask
from healthcheck import HealthCheck, EnvironmentDump
from .config import config


app = Flask(__name__)
health = HealthCheck()
envdump = EnvironmentDump()

app.config.update(dict(config))


print("Configured to monitor:      {}".format(app.config.get("witness_url")))
print("Configured to list on port: {}".format(app.config.get("port")))
