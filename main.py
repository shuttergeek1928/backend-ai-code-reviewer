import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request,session
from dataconnect import run_code_review
import datetime as dt
import json
import re, hashlib
from flask_cors import CORS, cross_origin

def store_code_review(email,inputCode,language,correctedCode,explain,accuracy,raw_res):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        currdate=dt.datetime.now()
        #raw_res="testing"
        print(type(currdate))
        #print(type(strId))
        print(type(inputCode))
        print(type(language))
        print(type(correctedCode))
        print(type(explain))
        print(type(accuracy))
        sql_query = "INSERT INTO review (email,language,input,output,time_and_date, explanation, accuracy,raw_response) VALUES(%s, %s, %s, %s,%s, %s, %s, %s)"
        cursor.execute(sql_query, (email,language, inputCode,correctedCode,currdate, explain, accuracy, raw_res))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        print("coooodee")


@app.route('/create', methods=['POST'])
def create_emp():
    try:
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _phone = _json['phone']
        _address = _json['address']
        if _name and _email and _phone and _address and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO emp(name, email, phone, address) VALUES(%s, %s, %s, %s)"
            bindData = (_name, _email, _phone, _address)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            cursor.close()
            conn.close()
            respone = jsonify('Employee added successfully!')
            respone.status_code = 200

            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        print("dsdfsdf")
        


@app.route('/emp')
def emp():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT emp_id FROM emp")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        cursor.close()
        conn.close()
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        print("sdada")
       


@app.route('/emp/')
def emp_details(emp_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, email, phone, address FROM emp WHERE id =%s", emp_id)
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update', methods=['PUT'])
def update_emp():
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _email = _json['email']
        _phone = _json['phone']
        _address = _json['address']
        if _name and _email and _phone and _address and _id and request.method == 'PUT':
            sqlQuery = "UPDATE emp SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s"
            bindData = (_name, _email, _phone, _address, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Employee updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete/', methods=['DELETE'])
def delete_emp(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM emp WHERE id =%s", (id,))
        conn.commit()
        respone = jsonify('Employee deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/gpt', methods=['POST'])
def gpt():
    __json = request.json
    print(request)
    _id = __json['email']
    code=__json['code_input']
    response=run_code_review(code)
    res=response.choices[0].message.content
    print(type(res))
    json_op= json.loads(res)
    print(json_op)

    try:
        print("testing")
        store_code_review(_id,code,json_op['detected_language'],json_op['corrected_code'],json_op['explanation'],json_op['code_accuracy'],res)

    except Exception as e:
        print(e)
    print(res)
    #res.headers.add("Access-Control-Allow-Origin", "*")
    return res

@app.route('/getreview',methods=['GET'])
def get_review():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        __json=request.json
        __id=__json['email']
        cursor.execute("SELECT * FROM REVIEW WHERE EMAIL=%s",__id)
        reviewrows = cursor.fetchall()
        response = jsonify(reviewrows)
        cursor.close()
        conn.close()
        response.status_code = 200
        return response

    except Exception as e:
        print(e)
    finally:
        print("review  executed")

@app.route('/login',methods=['POST'])
def user_auth():
    if request.method == 'POST' :
    # and 'email' in request.form and 'password' in request.form:
        res={}
        username = request.json['email']
        password = request.json['password']
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery="SELECT *FROM USERS WHERE EMAIL=%s AND PASSWORD=%s"
        cursor.execute(sqlQuery,(username,password))
        account=cursor.fetchone()
        cursor.close()
        conn.close()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['email']
            session['username'] = account['password']
            return {"IsAuthenticated":"true"}
        else: 
            return   {"IsAuthneticated":"false","ErrorMessage":"Invalid Username/Password"}

@app.route('/register',methods=['POST'])
def register():

    try:
        if request.method == 'POST': 
        # and 'email' in request.form and 'password' in request.form and "firstname" in request.form and "lastname" in request.form:
            __email=request.json['email']
            __password=request.json['password']
            __firstname=request.json['firstname']
            __lastname=request.json['lastname']
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE email = %s', (__email,))
            account = cursor.fetchone()
            if account:
                return {"Response":"Account is Already exists!"}
               
            else:
                hash = __password + app.secret_key
                hash = hashlib.sha1(hash.encode())
                password = hash.hexdigest()
                sqlQuery="INSERT INTO users (firstname, lastname, email,password) values(%s,%s,%s,%s)"
                __bindData=(__firstname, __lastname,__email,password)
                cursor.execute(sqlQuery,__bindData)
                conn.commit()
                cursor.close()
                conn.close()
                return {"Response":"Successfully Registered!!"}
        elif request.method == 'POSTX':
                return {"Response":"Please Fill out the form!!"}
    except Exception as e:
        print(e)
    finally:
        print("executing Finally")    






@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


if __name__== "__main__":
    app.run()