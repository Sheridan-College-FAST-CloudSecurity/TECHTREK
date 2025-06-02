from flask import Blueprint, jsonify, request

patients_bp = Blueprint('patients_bp', __name__)

# In-memory patients list
patients = []

@patients_bp.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    patient_id = len(patients) + 1
    patient = {
        "id": patient_id,
        "name": data.get("name"),
        "age": data.get("age"),
        "gender": data.get("gender"),
        "contact": data.get("contact"),
        "address": data.get("address"),
        "blood_group": data.get("blood_group"),
        "medical_history": data.get("medical_history", []),
        "allergies": data.get("allergies", [])
    }
    patients.append(patient)
    return jsonify({"message": "Patient added", "patient": patient}), 201

@patients_bp.route('/patients', methods=['GET'])
def get_patients():
    return jsonify(patients)

@patients_bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    for patient in patients:
        if patient["id"] == patient_id:
            return jsonify(patient)
    return jsonify({"message": "Patient not found"}), 404
