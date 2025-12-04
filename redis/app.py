from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 配置 Redis 连接
# 假设 Redis 服务名为 'redis-service'，端口为 6379
redis_host = os.environ.get('REDIS_HOST', 'redis-service')
redis_port = os.environ.get('REDIS_PORT', 6379)
redis_password = os.environ.get('REDIS_PASSWORD', None)

try:
    r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    r.ping()
    logger.info(f"Connected to Redis at {redis_host}:{redis_port}")
    print(f"Connected to Redis at {redis_host}:{redis_port}")
except redis.ConnectionError:
    logger.error(f"Failed to connect to Redis at {redis_host}:{redis_port}")
    print(f"Failed to connect to Redis at {redis_host}:{redis_port}")

@app.route('/health', methods=['GET'])
def health():
    try:
        if r.ping():
            logger.info("Health check passed")
            return jsonify({"status": "healthy", "redis": "connected"}), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "unhealthy", "redis": str(e)}), 500

@app.route('/cache/<key>', methods=['GET'])
def get_cache(key):
    try:
        val = r.get(key)
        if val:
            logger.info(f"Cache hit for key: {key}")
            return jsonify({"key": key, "value": val}), 200
        else:
            logger.info(f"Cache miss for key: {key}")
            return jsonify({"key": key, "value": None, "message": "Not found"}), 404
    except Exception as e:
        logger.error(f"Error getting cache for key {key}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/cache', methods=['POST'])
def set_cache():
    data = request.get_json()
    if not data or 'key' not in data or 'value' not in data:
        logger.warning("Invalid cache set request: missing key or value")
        return jsonify({"error": "Invalid request. 'key' and 'value' are required."}), 400
    
    key = data['key']
    value = data['value']
    # 默认过期时间 3600 秒
    ttl = data.get('ttl', 3600)

    try:
        r.setex(key, ttl, value)
        logger.info(f"Cache set for key: {key}, ttl: {ttl}")
        return jsonify({"message": "Cached successfully", "key": key}), 201
    except Exception as e:
        logger.error(f"Error setting cache for key {key}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/cache/<key>', methods=['DELETE'])
def delete_cache(key):
    try:
        r.delete(key)
        logger.info(f"Cache deleted for key: {key}")
        return jsonify({"message": "Deleted successfully", "key": key}), 200
    except Exception as e:
        logger.error(f"Error deleting cache for key {key}: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
