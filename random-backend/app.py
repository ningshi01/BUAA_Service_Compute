from flask import Flask, jsonify
from flask_cors import CORS
import random
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    logger.info("Health check requested")
    return jsonify({"status": "healthy", "service": "random-backend"}), 200

@app.route('/random', methods=['GET'])
def generate_random():
    """生成1到100之间的随机整数"""
    random_number = random.randint(1, 100)
    logger.info(f"Generated random number: {random_number}")
    return jsonify({
        "random_number": random_number,
        "min": 1,
        "max": 100
    }), 200

@app.route('/random/float', methods=['GET'])
def generate_random_float():
    """生成0到1之间的随机浮点数"""
    random_float = random.random()
    logger.info(f"Generated random float: {random_float}")
    return jsonify({
        "random_float": random_float,
        "min": 0.0,
        "max": 1.0
    }), 200

@app.route('/random/range/<int:min_val>/<int:max_val>', methods=['GET'])
def generate_random_range(min_val, max_val):
    """生成指定范围内的随机整数"""
    if min_val >= max_val:
        logger.warning(f"Invalid range: min={min_val}, max={max_val}")
        return jsonify({"error": "最小值必须小于最大值"}), 400
    
    random_number = random.randint(min_val, max_val)
    logger.info(f"Generated random number in range [{min_val}, {max_val}]: {random_number}")
    return jsonify({
        "random_number": random_number,
        "min": min_val,
        "max": max_val
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
