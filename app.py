from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection

db = mysql.connector.connect(
    host="mysql.railway.internal",
    user="root",
    password="IbYnOfdheNcHeXECWJbejuPYoDeyqNkP",
    database="railway",
    port=int("3306")
)


@app.route("/qr/<qr_id>")
def get_critical_info(qr_id):
    cursor = db.cursor(dictionary=True)
    query = "SELECT name, blood_group, allergies, chronic_conditions, critical_medicines, emergency_contact, last_updated FROM critical_info WHERE qr_id = %s"
    cursor.execute(query, (qr_id,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return {"error": "No record found"}, 404

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)