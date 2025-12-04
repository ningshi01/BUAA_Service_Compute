from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    logger.info("Health check requested")
    return jsonify({"status": "healthy", "service": "compute-backend"}), 200

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        logger.info(f"Received calculation request: {data}")
        
        if not data:
            logger.warning("Request data is empty")
            return jsonify({"error": "请求数据为空"}), 400
        
        num1 = data.get('num1')
        num2 = data.get('num2')
        operation = data.get('operation')
        
        if num1 is None or num2 is None or operation is None:
            logger.warning("Missing required parameters")
            return jsonify({"error": "缺少必要参数"}), 400
        
        num1 = float(num1)
        num2 = float(num2)
        
        result = None
        
        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 == 0:
                logger.warning("Division by zero attempt")
                return jsonify({"error": "除数不能为0"}), 400
            result = num1 / num2
        else:
            logger.warning(f"Unsupported operation: {operation}")
            return jsonify({"error": f"不支持的操作: {operation}"}), 400
        
        logger.info(f"Calculation result: {result}")
        return jsonify({
            "num1": num1,
            "num2": num2,
            "operation": operation,
            "result": result
        }), 200
        
    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        return jsonify({"error": f"数值转换错误: {str(e)}"}), 400
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
