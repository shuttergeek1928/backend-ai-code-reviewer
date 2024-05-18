
from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
import uuid
import  datetime
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Password123'
app.config['MYSQL_DATABASE_DB'] = 'codereview'

mysql = MySQL(app)

class CRUD:
    def __init__(self):
        pass

# Routes for CRUD operations on 'emp' table
@app.route('/emp', methods=['POST'])
def create_emp():
    data = request.get_json()
    conn = mysql.get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO emp (emp_id, first_name, last_name, email, phone, password) VALUES (%s, %s, %s, %s, %s, %s)",
                   (data['emp_id'], data['first_name'], data['last_name'], data['email'], data['phone'], data['password']))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Employee created successfully'}), 201

@app.route('/emp/<string:emp_id>', methods=['GET'])
def get_emp(emp_id):
    conn = mysql.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emp WHERE emp_id = %s", (emp_id,))
    emp = cursor.fetchone()
    cursor.close()
    return jsonify(emp)

@app.route('/emp/<string:emp_id>', methods=['PUT'])
def update_emp(emp_id):
    data = request.get_json()
    conn = mysql.get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE emp SET first_name = %s, last_name = %s, email = %s, phone = %s, password = %s WHERE emp_id = %s",
                   (data['first_name'], data['last_name'], data['email'], data['phone'], data['password'], emp_id))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Employee updated successfully'})

@app.route('/emp/<string:emp_id>', methods=['DELETE'])
def delete_emp(emp_id):
    conn = mysql.get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM emp WHERE emp_id = %s", (emp_id,))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Employee deleted successfully'})

# Routes for CRUD operations on 'review' table
@app.route('/review', methods=['POST'])
def create_review():
    data = request.get_json()
    review_id = str(uuid.uuid4())
    conn = mysql.get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO review (review_id, emp_id, language, input, output, time_and_date, explanation, accuracy, raw_response) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (review_id, data['emp_id'], data['language'], data['input'], data['output'], data['time_and_date'], data['explanation'], data['accuracy'], data['raw_response']))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Review created successfully'}), 201

@app.route('/review/<string:review_id>', methods=['GET'])
def get_review(review_id):
    conn = mysql.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM review WHERE review_id = %s", (review_id,))
    review = cursor.fetchone()
    cursor.close()
    return jsonify(review)

@app.route('/review/<string:review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.get_json()
    conn = mysql.get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE review SET emp_id = %s, language = %s, input = %s, output = %s, time_and_date = %s, explanation = %s, accuracy = %s, raw_response = %s WHERE review_id = %s",
                   (data['emp_id'], data['language'], data['input'], data['output'], data['time_and_date'], data['explanation'], data['accuracy'], data['raw_response'], review_id))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Review updated successfully'})

@app.route('/review/<string:review_id>', methods=['DELETE'])
def delete_review(review_id):
    conn = mysql.get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM review WHERE review_id = %s", (review_id,))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Review deleted successfully'})




if __name__ == '__main__':
    app.run(debug=False)
