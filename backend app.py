from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="employee_db"
    )


# ==========================================
# TEST API
# ==========================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Employee Management System Backend is Running"
    })


# ==========================================
# CREATE - ADD EMPLOYEE
# ==========================================

@app.route("/api/employees", methods=["POST"])
def add_employee():

    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        department = data.get("department")
        designation = data.get("designation")

        # Validation
        if not all([
            name,
            email,
            phone,
            department,
            designation
        ]):
            return jsonify({
                "error": "All fields are required"
            }), 400

        db = get_db()
        cursor = db.cursor()

        query = """
            INSERT INTO employees
            (name, email, phone, department, designation)
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            name,
            email,
            phone,
            department,
            designation
        )

        cursor.execute(query, values)

        db.commit()

        cursor.close()
        db.close()

        return jsonify({
            "message": "Employee added successfully"
        }), 201

    except Error as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# READ - GET ALL EMPLOYEES
# ==========================================

@app.route("/api/employees", methods=["GET"])
def get_employees():

    try:

        db = get_db()

        cursor = db.cursor(
            dictionary=True
        )

        query = """
            SELECT *
            FROM employees
            ORDER BY id DESC
        """

        cursor.execute(query)

        employees = cursor.fetchall()

        cursor.close()
        db.close()

        return jsonify(employees)

    except Error as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# READ - GET SINGLE EMPLOYEE
# ==========================================

@app.route("/api/employees/<int:id>", methods=["GET"])
def get_employee(id):

    try:

        db = get_db()

        cursor = db.cursor(
            dictionary=True
        )

        query = """
            SELECT *
            FROM employees
            WHERE id = %s
        """

        cursor.execute(
            query,
            (id,)
        )

        employee = cursor.fetchone()

        cursor.close()
        db.close()

        if employee is None:

            return jsonify({
                "error": "Employee not found"
            }), 404

        return jsonify(employee)

    except Error as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# UPDATE - UPDATE EMPLOYEE
# ==========================================

@app.route("/api/employees/<int:id>", methods=["PUT"])
def update_employee(id):

    try:

        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        department = data.get("department")
        designation = data.get("designation")

        # Validation
        if not all([
            name,
            email,
            phone,
            department,
            designation
        ]):

            return jsonify({
                "error": "All fields are required"
            }), 400

        db = get_db()

        cursor = db.cursor()

        query = """
            UPDATE employees
            SET
                name = %s,
                email = %s,
                phone = %s,
                department = %s,
                designation = %s
            WHERE id = %s
        """

        values = (
            name,
            email,
            phone,
            department,
            designation,
            id
        )

        cursor.execute(
            query,
            values
        )

        db.commit()

        if cursor.rowcount == 0:

            cursor.close()
            db.close()

            return jsonify({
                "error": "Employee not found"
            }), 404

        cursor.close()
        db.close()

        return jsonify({
            "message":
                "Employee updated successfully"
        })

    except Error as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# DELETE - DELETE EMPLOYEE
# ==========================================

@app.route("/api/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):

    try:

        db = get_db()

        cursor = db.cursor()

        query = """
            DELETE FROM employees
            WHERE id = %s
        """

        cursor.execute(
            query,
            (id,)
        )

        db.commit()

        if cursor.rowcount == 0:

            cursor.close()
            db.close()

            return jsonify({
                "error": "Employee not found"
            }), 404

        cursor.close()
        db.close()

        return jsonify({
            "message":
                "Employee deleted successfully"
        })

    except Error as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
