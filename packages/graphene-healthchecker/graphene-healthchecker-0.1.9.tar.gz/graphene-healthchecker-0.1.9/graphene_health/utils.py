import re
import requests
import datetime
from flask import jsonify


timeFormat = "%Y-%m-%dT%H:%M:%S"


def parse_time(block_time):
    # convert backend time into timestamp
    if "." in block_time:
        # remove deci seconds
        block_time = re.sub(r"\.\d", "", block_time)
    return datetime.datetime.strptime(block_time, timeFormat)


def format_time(datim):
    return datim.strftime(timeFormat)


def query(url, data):
    try:
        req = requests.post(
            url,
            json={"method": "call", "params": data, "jsonrpc": "2.0", "id": 1},
            timeout=2,
        )
    except Exception as e:
        raise Exception("Node timed out: {}".format(str(e)))

    if req.status_code != 200:
        raise Exception("Node returns an error core {}".format(req.status_code))

    try:
        data = req.json()
    except Exception as e:
        raise ValueError(e)

    if "result" not in data:
        raise ValueError(data)

    result = data.get("result")
    if isinstance(result, (list, set)):
        return result[0]
    else:
        return result
