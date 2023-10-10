# student_routes.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from App.controllers import StudentController

from.index import index_views

student_bp = Blueprint("student", __name__, 
template_folder='../templates')

# Create an instance of the StudentController
student_controller = StudentController()

# # Define the route for adding a student
# @student_bp.route("/api/students", methods=["POST"])
# @jwt_required  # You can apply authentication as needed
# def add_student():
#     try:
#         # Parse the JSON request data
#         data = request.get_json()

#         # Check if the required fields are present in the request
#         if "firstName" not in data or "lastName" not in data or "email" not in data or "phoneNumber" not in data:
#             return jsonify({"error": "Invalid request payload"}), 400

#         # Extract student data from the request
#         first_name = data["firstName"]
#         last_name = data["lastName"]
#         email = data["email"]
#         phone_number = data["phoneNumber"]

#         # Call the create_student method from the StudentController
#         result = student_controller.create_student(first_name, last_name, email, phone_number)

#         if result:
#             return jsonify({"message": "Student added successfully", "studentID": result.id}), 201
#         else:
#             return jsonify({"error": "Student creation failed"}), 500  # You can choose an appropriate status code

#     except Exception as e:
#         # Handle any exceptions (e.g., database errors) here
#         print(str(e))
#         return jsonify({"error": "Internal Server Error"}), 500

# # Add more student-related routes as needed
# @student_bp.route('/api/search', methods=['GET'])
# #@jwt_required
# def search_student():
#     try:
#         # Get the student ID from the request JSON data
#         data = request.get_json()
#         student_id = data.get("studentID")

#         if student_id is None:
#             return jsonify({"error": "Invalid request payload"}), 400

#         # Call the search_student method from the StudentController
#         student_info = student_controller.search_student(student_id)

#         if student_info:
#             # If the student is found, return the student information
#             return jsonify([{
#                 "studentID": student_info["student_id"],
#                 "firstName": student_info["first_name"],
#                 "lastName": student_info["last_name"],
#                 "email": student_info["email"],
#                 "phoneNumber": student_info["phone_number"]
#             }]), 200
#         else:
#             # If the student is not found, return a 404 error
#             return jsonify({"error": "Student not found"}), 404

#     except Exception as e:
#         # Handle any exceptions (e.g., database errors) here
#         print(str(e))
#         return jsonify({"error": "Internal Server Error"}), 500
