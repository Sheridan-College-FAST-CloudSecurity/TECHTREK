from flask import Blueprint, jsonify, request

medicines_bp = Blueprint('medicines_bp', __name__)

medicines = []

@medicines_bp.route('/medicines', methods=['POST'])
def add_medicine():
    data = request.json
    medicine_id = len(medicines) + 1
    medicine = {
        "id": medicine_id,
        "name": data.get("name"),
        "manufacturer": data.get("manufacturer"),
        "price": data.get("price"),
        "quantity_available": data.get("quantity_available"),
        "expiry_date": data.get("expiry_date"),
        "dosage": data.get("dosage")
    }
    medicines.append(medicine)
    return jsonify({"message": "Medicine added", "medicine": medicine}), 201

@medicines_bp.route('/medicines', methods=['GET'])
def get_medicines():
    return jsonify(medicines)

@medicines_bp.route('/medicines/<int:medicine_id>', methods=['GET'])
def get_medicine(medicine_id):
    for med in medicines:
        if med["id"] == medicine_id:
            return jsonify(med)
    return jsonify({"message": "Medicine not found"}), 404
