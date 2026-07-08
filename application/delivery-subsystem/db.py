import os
from redis import Redis
from neo4j import GraphDatabase
from influxdb_client import InfluxDBClient

driver = GraphDatabase.driver(
    os.environ.get("NEO4J_URI", "bolt://neo4j:7687"),
    auth=(os.environ.get("NEO4J_USERNAME", "neo4j"), os.environ.get("NEO4J_PASSWORD", "password"))
)

redis_client = Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    decode_responses=True
)

import json
from functools import wraps
from flask import request, jsonify, Response

def redis_cache(key_prefix, ttl=300):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            entity_id = kwargs.get("user_id") or kwargs.get("courier_id") or kwargs.get("delivery_id") or request.args.get("user_id") or (args[0] if args else None)
            key = f"{key_prefix}:{entity_id}" if entity_id else key_prefix
            
            try:
                cached_val = redis_client.get(key)
                if cached_val:
                    return Response(cached_val, mimetype="application/json")
            except Exception as e:
                print(f"Cache read error: {e}")
                
            response = func(*args, **kwargs)
            
            status_code = 200
            data_to_cache = None
            
            if isinstance(response, tuple):
                resp_data, status_code = response
                if isinstance(resp_data, Response):
                    data_to_cache = resp_data.get_data(as_text=True)
                else:
                    data_to_cache = json.dumps(resp_data)
            elif isinstance(response, Response):
                status_code = response.status_code
                data_to_cache = response.get_data(as_text=True)
            else:
                data_to_cache = json.dumps(response)
                
            if status_code == 200 and data_to_cache is not None:
                try:
                    redis_client.setex(key, ttl, data_to_cache)
                except Exception as e:
                    print(f"Cache write error: {e}")
                    
            return response
        return wrapper
    return decorator

def invalidate_cache(key_prefix):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            entity_id = kwargs.get("user_id") or kwargs.get("courier_id") or kwargs.get("delivery_id") or request.args.get("user_id") or (args[0] if args else None)
            key = f"{key_prefix}:{entity_id}" if entity_id else key_prefix
            
            response = func(*args, **kwargs)
            
            status_code = 200
            if isinstance(response, tuple):
                _, status_code = response
            elif isinstance(response, Response):
                status_code = response.status_code
                
            if 200 <= status_code < 300:
                try:
                    redis_client.delete(key)
                except Exception as e:
                    print(f"Cache delete error: {e}")
                    
            return response
        return wrapper
    return decorator

influx_client = InfluxDBClient(
    url=os.environ.get("INFLUXDB_URL", "http://localhost:8086"),
    token=os.environ.get("INFLUXDB_TOKEN", "mytoken123"),
    org=os.environ.get("INFLUXDB_ORG", "docs")
)

influx_bucket = os.environ.get("INFLUXDB_BUCKET", "geo_data")
influx_org = os.environ.get("INFLUXDB_ORG", "docs")
