import os
from redis import Redis
from neo4j import GraphDatabase
from influxdb_client import InfluxDBClient

# 1. Neo4j initialization
driver = GraphDatabase.driver(
    os.environ.get("NEO4J_URI", "bolt://neo4j:7687"),
    auth=(os.environ.get("NEO4J_USERNAME", "neo4j"), os.environ.get("NEO4J_PASSWORD", "password"))
)

# 2. Redis initialization with Cache-Aside override
redis_client = Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    decode_responses=True
)

_get = redis_client.get
def cached_get(key):
    val = _get(key)
    if val is None and key.startswith("user:"):
        uid = key.split(":")[1]
        with driver.session() as s:
            rec = s.run("MATCH (u:User {id: $id}) RETURN u", id=uid).single()
            if rec:
                import json
                val = json.dumps(dict(rec["u"]))
                redis_client.setex(key, 300, val)
    return val
redis_client.get = cached_get

# 3. InfluxDB initialization
influx_client = InfluxDBClient(
    url=os.environ.get("INFLUXDB_URL", "http://localhost:8086"),
    token=os.environ.get("INFLUXDB_TOKEN", "mytoken123"),
    org=os.environ.get("INFLUXDB_ORG", "docs")
)

influx_bucket = os.environ.get("INFLUXDB_BUCKET", "geo_data")
influx_org = os.environ.get("INFLUXDB_ORG", "docs")
