from flask import Blueprint, jsonify, request

doctors_bp = Blueprint('doctors_bp', __name__)

doctors = []

@doctors_bp.route('/doctors', methods=['POST'])
def add_doctor():
    data = request.json
    doctor_id = len(doctors) + 1
    doctor = {
        "id": doctor_id,
        "name": data.get("name"),
        "specialization": data.get("specialization"),
        "contact": data.get("contact"),
        "availability": data.get("availability")  # e.g. ["Mon 9-5", "Wed 9-1"]
    }
    doctors.append(doctor)
    return jsonify({"message": "Doctor added", "doctor": doctor}), 201

@doctors_bp.route('/doctors', methods=['GET'])
def get_doctors():
    return jsonify(doctors)

@doctors_bp.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    for doctor in doctors:
        if doctor["id"] == doctor_id:
            return jsonify(doctor)
    return jsonify({"message": "Doctor not found"}), 404
