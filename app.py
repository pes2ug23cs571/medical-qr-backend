import os
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Connect using Render PostgreSQL URL
DATABASE_URL = os.environ.get("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)

@app.route("/qr/<qr_id>")
def get_critical_info(qr_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT name, blood_group, allergies,
               chronic_conditions, critical_medicines,
               emergency_contact, last_updated
        FROM critical_info
        WHERE qr_id = %s
    """, (qr_id,))

    row = cur.fetchone()
    cur.close()

    if not row:
        return {"error": "No record found"}, 404

    return jsonify({
        "name": row[0],
        "blood_group": row[1],
        "allergies": row[2],
        "chronic_conditions": row[3],
        "critical_medicines": row[4],
        "emergency_contact": row[5],
        "last_updated": row[6]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
