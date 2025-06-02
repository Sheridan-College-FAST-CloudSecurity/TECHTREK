from flask import Blueprint, jsonify, request

billing_bp = Blueprint('billing_bp', __name__)

billing_records = []

@billing_bp.route('/billing', methods=['POST'])
def add_billing_record():
    data = request.json
    billing_id = len(billing_records) + 1
    record = {
        "id": billing_id,
        "patient_id": data.get("patient_id"),
        "amount": data.get("amount"),
        "billing_date": data.get("billing_date"),
        "details": data.get("details"),
        "paid": data.get("paid", False)
    }
    billing_records.append(record)
    return jsonify({"message": "Billing record added", "record": record}), 201

@billing_bp.route('/billing', methods=['GET'])
def get_billing_records():
    return jsonify(billing_records)

@billing_bp.route('/billing/<int:billing_id>', methods=['GET'])
def get_billing_record(billing_id):
    for record in billing_records:
        if record["id"] == billing_id:
            return jsonify(record)
    return jsonify({"message": "Billing record not found"}), 404
