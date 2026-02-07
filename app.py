from flask import Flask, jsonify, request
import psycopg2
import psycopg2.extras
import os
import uuid
import qrcode

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)

@app.route("/qr/<patient_id>")
def get_patient(patient_id):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(
        "SELECT * FROM critical_info WHERE qr_id = %s",
        (patient_id,)
    )
    data = cursor.fetchone()
    cursor.close()

    if not data:
        return {"error": "No record found"}, 404

    return jsonify(data)

# 🔹 FUTURE-READY DATA INSERT API
@app.route("/patients", methods=["POST"])
def add_patient():
    data = request.json

    patient_id = str(uuid.uuid4())  # unique ID

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO critical_info (
            qr_id, name, blood_group, allergies,
            chronic_conditions, critical_medicines,
            emergency_contact, last_updated
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,NOW())
    """, (
        patient_id,
        data["name"],
        data["blood_group"],
        data["allergies"],
        data["chronic_conditions"],
        data["critical_medicines"],
        data["emergency_contact"]
    ))

    conn.commit()
    cursor.close()

    # QR generation
    qr_url = f"https://medical-qr-backend-1.onrender.com/qr/{patient_id}"
    img = qrcode.make(qr_url)
    img.save(f"{patient_id}.png")

    return {
        "message": "Patient added successfully",
        "patient_id": patient_id,
        "qr_url": qr_url
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
