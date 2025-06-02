from flask import Blueprint, jsonify, request

departments_bp = Blueprint('departments_bp', __name__)

departments = []

@departments_bp.route('/departments', methods=['POST'])
def add_department():
    data = request.json
    department_id = len(departments) + 1
    department = {
        "id": department_id,
        "name": data.get("name"),
        "head": data.get("head"),  # name of department head
        "contact": data.get("contact"),
        "floor": data.get("floor")
    }
    departments.append(department)
    return jsonify({"message": "Department added", "department": department}), 201

@departments_bp.route('/departments', methods=['GET'])
def get_departments():
    return jsonify(departments)

@departments_bp.route('/departments/<int:department_id>', methods=['GET'])
def get_department(department_id):
    for dept in departments:
        if dept["id"] == department_id:
            return jsonify(dept)
    return jsonify({"message": "Department not found"}), 404
