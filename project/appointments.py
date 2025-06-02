from flask import Blueprint, jsonify, request

appointments_bp = Blueprint('appointments_bp', __name__)

appointments = []

@appointments_bp.route('/appointments', methods=['POST'])
def add_appointment():
    data = request.json
    appointment_id = len(appointments) + 1
    appointment = {
        "id": appointment_id,
        "patient_id": data.get("patient_id"),
        "doctor_id": data.get("doctor_id"),
        "date": data.get("date"),
        "time": data.get("time"),
        "reason": data.get("reason"),
        "status": data.get("status", "scheduled")  # default to scheduled
    }
    appointments.append(appointment)
    return jsonify({"message": "Appointment added", "appointment": appointment}), 201

@appointments_bp.route('/appointments', methods=['GET'])
def get_appointments():
    return jsonify(appointments)

@appointments_bp.route('/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    for appt in appointments:
        if appt["id"] == appointment_id:
            return jsonify(appt)
    return jsonify({"message": "Appointment not found"}), 404
