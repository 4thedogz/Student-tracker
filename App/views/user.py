from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate, 
    get_all_users,
    get_all_users_json,
    jwt_required
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    create_user(data['id'], data['username'], data['password'])
    return jsonify({'message': f"user {data['username']} created"})

# @user_views.route('/users', methods=['POST'])
# def create_user_action():
#     data = request.form
#     flash(f"User {data['username']} created!")
#     create_user(data['username'], data['password'])
#     return redirect(url_for('user_views.get_user_page'))

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')

#--------------Student testing---------------------------------------------
from App.controllers import ReviewController
from App.controllers import StudentController

student_controller = StudentController()
review_controller = ReviewController()

#karma
from App.models.review import Reviews
from App.controllers import create_karma_vote

@user_views.route('/api/search', methods=['GET'])
#@jwt_required()
#@login_required
def search_student():
    try:
        # Get the student ID from the request JSON data
        data = request.get_json()
        student_id = data.get("studentID")

        if student_id is None:
            return jsonify({"error": "Invalid request payload"}), 400

        # Call the search_student method from the StudentController
        student_info = student_controller.search_student(student_id)

        if student_info:
            # If the student is found, return the student information
            return jsonify([{
                "studentID": student_info["student_id"],
                "firstName": student_info["first_name"],
                "lastName": student_info["last_name"],
                "email": student_info["email"],
                "phoneNumber": student_info["phone_number"]
            }]), 200
        else:
            # If the student is not found, return a 404 error
            return jsonify({"error": "Student not found"}), 404

    except Exception as e:
        # Handle any exceptions (e.g., database errors) here
        print(str(e))
        return jsonify({"error": "Internal Server Error"}), 500


@user_views.route("/api/students", methods=["POST"])
#@jwt_required  # You can apply authentication as needed
def add_student():
    try:
        # Parse the JSON request data
        data = request.get_json()

        # Check if the required fields are present in the request
        if "firstName" not in data or "lastName" not in data or "email" not in data or "phoneNumber" not in data:
            return jsonify({"error": "Invalid request payload"}), 400

        # Extract student data from the request
        first_name = data["firstName"]
        last_name = data["lastName"]
        email = data["email"]
        phone_number = data["phoneNumber"]

        # Call the create_student method from the StudentController
        result = student_controller.create_student(first_name, last_name, email, phone_number)

        if result:
            return jsonify({"message": "Student added successfully", "studentID": result}), 201
        else:
            return jsonify({"error": "Student creation failed"}), 500  # You can choose an appropriate status code

    except Exception as e:
        # Handle any exceptions (e.g., database errors) here
        print(str(e))
        return jsonify({"error": "Internal Server Error"}), 500

@user_views.route("/api/update/<int:student_id>", methods=["POST"])
#@jwt_required
def update_student(student_id):
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Call the update_student method from the StudentController
        result = student_controller.update_student(student_id, data)

        if result:
            # If the student is updated successfully, return a success response
            return jsonify({"message": "Student updated successfully"}), 200
        else:
            # If the student is not found or update fails, return an appropriate error response
            return jsonify({"error": "Student not found or update failed"}), 400  # You can choose an appropriate status code

    except Exception as e:
        # Handle any exceptions (e.g., database errors) here
        print(str(e))
        return jsonify({"error": "Internal Server Error"}), 500  


@user_views.route("/api/reviews/<int:student_id>", methods=["POST"])
#@jwt_required
def log_review(student_id):
    try:
        # Get the logged-in student's ID from the JWT token
        #student_id = get_jwt_identity()

        # Get the JSON data from the request
        data = request.get_json()

        # Check if the required fields are present in the request
        if "message" not in data:
            return jsonify({"error": "Invalid request payload"}), 400

        # Extract review data from the request
        message = data["message"]
        #staff_id = data["staff_id"]
        staff_id = 1 #todo: change this to use jwt identify 
      
        # Call the create_log_review method from the ReviewController
        new_review = review_controller.create_log_review(student_id, message, staff_id)

        if new_review:
            # If the review is created successfully, return a success response
            return jsonify({"message": "Review logged successfully", "review_id": new_review.id}), 201
        else:
            # If the review creation fails, return an appropriate error response
            return jsonify({"error": "Review creation failed"}), 500  # You can choose an appropriate status code

    except Exception as e:
        # Handle any exceptions (e.g., database errors) here
        print(str(e))
        return jsonify({"error": "Internal Server Error"}), 500

# ... (other routes)


@user_views.route('/api/reviews/<int:review_id>/karma', methods=['POST'])
#@jwt_required
def karma_ranking(review_id):
    try:
        # Get the logged-in staff member's ID from the JWT token
        #staff_id = get_jwt_identity()
      
        staff_id = 2 #todo change this to jwt identify
      
        # Get the JSON data from the request
        data = request.get_json()

        # Check if the required field 'value' is present in the request JSON
        if 'value' not in data:
            return jsonify({"error": "Invalid request payload"}), 400

        # Extract the 'value' field from the request JSON
        value = data['value']

        # Ensure 'value' is either 1 (upvote) or -1 (downvote)
        if value not in [1, -1]:
            return jsonify({"error": "Invalid 'value' field"}), 400

        # Call the create_karma_vote function to create or update a karma vote
        new_vote = create_karma_vote(staff_id, review_id, value)

        if new_vote:
            return jsonify({"message": "Karma vote recorded successfully"}), 201
        else:
            return jsonify({"error": "Failed to record karma vote"}), 500  # You can choose an appropriate status code
    except Exception as e:
        # Handle any exceptions (e.g., database errors) here
        print(str(e))
        return jsonify({"error": "Internal Server Error"}), 500