# import the flask web framework
import json
import redis
from flask import Flask, request
from loguru import logger
from statistics import mean

HISTORY_LENGTH = 10
DATA_KEY = "engine_temperature"
# create a Flask server, and allow us to interact with it using the app variable
app = Flask(__name__)


# defines an endpoint which accepts POST requests, and is reachable from the /record endpoint
@app.route('/record', methods=['POST'])
def record_engine_temperature():
    payload = request.get_json(force=True)
    logger.info(f"(*) record request --- {json.dumps(payload)} (*)")

    engine_temperature = payload.get("engine_temperature")
    logger.info(f"engine temperature to record is: {engine_temperature}")

    database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    database.lpush(DATA_KEY, engine_temperature)
    logger.info(f"stashed engine temperature in redis: {engine_temperature}")

    while database.llen(DATA_KEY) > HISTORY_LENGTH:
        database.rpop(DATA_KEY)
    engine_temperature_values = database.lrange(DATA_KEY, 0, -1)
    logger.info(f"engine temperature list now contains these values: {engine_temperature_values}")

    logger.info(f"record request successful")
    return {"success": True}, 200

# defines an endpoint which accepts POST requests, and is reachable from the /collect endpoint
@app.route('/collect', methods=['POST'])
def collect_engine_temperature():
    
    payload = request.get_json(force=True)
    engine_temperature = payload.get("engine_temperature")
    database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    database.lpush(DATA_KEY, engine_temperature)
    engine_temperature_values = database.lrange(DATA_KEY, 0, -1)

# convert temperatures to floats for mean calculation
    engine_temperature_values = [float(temperature) for temperature in engine_temperature_values]

# finds most recent engine temperature reading in database
    current_engine_temperature = float(database.lindex(DATA_KEY, 0))
    logger.info(f"current engine temperature is: {current_engine_temperature}")

# finds the average of the 10 latest engine temperatures
    average_engine_temperature = mean(engine_temperature_values)
    logger.info(f"average engine temperature is: {average_engine_temperature}")

    records = {
        "current engine temperature" : current_engine_temperature,
        "average engine temperature": average_engine_temperature,
    }

    logger.info(f"record request successful")
    return records, 200
    