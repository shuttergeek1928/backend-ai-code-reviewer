import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
from dataconnect import run_code_review
import datetime as dt
import json
from flask import Flask
from flask_cors import CORS, cross_origin

def store_code_review(empId,inputCode,language,correctedCode,explain,accuracy,raw_res):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        currdate=dt.datetime.now()
        #raw_res="testing"
        strId=empId
        print(type(currdate))
        print(type(strId))
        print(type(inputCode))
        print(type(language))
        print(type(correctedCode))
        print(type(explain))
        print(type(accuracy))
        sql_query = "INSERT INTO review (emp_id,language,input,output,time_and_date, explanation, accuracy,raw_response) VALUES(%s, %s, %s, %s,%s, %s, %s, %s)"
        cursor.execute(sql_query, (strId,language, inputCode,correctedCode,currdate, explain, accuracy, raw_res))
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
    _id = __json['id']
    code=__json['code_input']
    response=run_code_review(code)
    res=response.choices[0].message.content
    print(type(res))
    json_op= json.loads(res)
    print(json_op)

    try:
        print("testing")
        _id=int(_id)
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
        _id=__json['emp_id']
        cursor.execute("SELECT * FROM REVIEW WHERE EMP_ID=%s",__id)
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

@app.route('/login',methods=['GET'])
def user_auth():
    __json=request.json
    _id=_json['emp_id']
    _password=_json['password']
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT PASSWORD FROM EMP WHERE EMP_ID=%s",__id)
        emp_res=cursor.fetchOne()

        emp_res_op=jsonify(emp_res)
        print(emp_res_op["PASSWORD"])
        return emp_res
        #print(res_emp)
        # if(emp_res):
        #     if emp_res["PASSWORD"]==__password:
        #         response = jsonify({"user_auth":"1"})
        #         response.status_code=200
        #         return response
        # else:
        #     response=jsonify({"user_auth":"0"})
        #     response.status_code=200
        #     return response
           # return ("User not Found"){
    except Exception as e:
        print(e)
    finally:
        print("review  executed")










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