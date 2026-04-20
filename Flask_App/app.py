from flask import Flask, request, jsonify
from datetime import datetime
import os
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection parameters
DB_HOST = os.environ.get('DB_HOST', 'project_mysql_container')
DB_PORT = int(os.environ.get('DB_PORT', 3306))
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'root')
DB_NAME = os.environ.get('DB_NAME', 'testdb')

def get_db_connection():
    """Create database connection"""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/health', methods=['GET'])
def health():
    """Health check - includes database connectivity"""
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"status": "unhealthy", "reason": "db_connection_failed"}), 503
        conn.close()
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503

@app.route('/api/data', methods=['POST'])
def receive_data():
    """Receive data and store in MySQL database"""
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data or 'value' not in data:
            return jsonify({"error": "user_id and value required"}), 400
        
        user_id = data['user_id']
        value = data['value']
        source = data.get('source', 'unknown')
        
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "database_connection_failed"}), 500
        
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO ingested_data (user_id, value, source) VALUES (%s, %s, %s)",
            (user_id, value, source)
        )
        cur.execute("UPDATE ingestion_metrics SET total_records = total_records + 1, last_ingestion = NOW()")
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "status": "received_and_stored",
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "value": value
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/metrics', methods=['GET'])
def metrics():
    """Return metrics about ingested data from database"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "database_connection_failed"}), 500
        
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT total_records, last_ingestion, updated_at FROM ingestion_metrics LIMIT 1")
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if result:
            return jsonify(result), 200
        else:
            return jsonify({"error": "no_metrics_found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)