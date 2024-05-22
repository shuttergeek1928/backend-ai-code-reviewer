from flask import Flask, request, g
from flaskext.mysql import MySQL
import json
import streamlit as st
from openai import AzureOpenAI
import datetime
import dataconnect as dconnect
# Create Flask app
app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Password1!'
app.config['MYSQL_DATABASE_DB'] = 'mydatabase'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'  # Change this if your MySQL server is hosted elsewhere
mysql = MySQL(app)


def get_db():
    """
    Get a database connection. This function is called internally by Flask.
    """
    if 'db' not in g:
        g.db = mysql.connect()
    return g.db


def close_db(e=None):
    """
    Close the database connection at the end of the request.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def store_code_review(dblang, code_input,dbcode, dbexplain, dbaccuracy,json_op):
    """
    Store code review data in the database.
    """
    with app.app_context():
        db = get_db()
        cur = db.cursor()

        review_id = "hhhh"
        emp_id = 100

        time_and_date=datetime.datetime.now()
        sql_query = "INSERT INTO review (emp_id,language,input,output,time_and_date, explanation, accuracy,raw_response) VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)"
        cur.execute(sql_query, (emp_id,dblang, code_input,dbcode,time_and_date, dbexplain, dbaccuracy,raw_response))
        db.commit()
        cur.close()


def run_code_review(code):
    """
    Run code review using Azure OpenAI API.
    """
    example_json = {
        "detected_language": "c++",
        "corrected_code": "#include <iostream> \n using namespace std \n int main()\n{\n \n} ",
        "explanation": "The corrected code includes the correct header file for input/output stream, which is <iostream> in C++. The incorrect use of \'iostream.h\' has been replaced with the correct header file.\n",
        "code_accuracy": '100%'
    }
    client = AzureOpenAI(
        azure_endpoint="https://1000071505.openai.azure.com/",
        api_key="f9199526d750434cb2a399963287c38a",
        api_version="2024-02-15-preview"
    )
    message_text = [
        {"role": "system",
         "content": 'Please review the following code and send me corrected code in the json format with four main keys "corrected code" having actual corrected code and "explantion" having code correction explaination , detected languge is having language name of provided code and code accuracy percentage is having code accuracy percentage.The data scheme should be like this ' + json.dumps(
             example_json)},
        {"role": "user",
         "content": code}, ]

    completion = client.chat.completions.create(
        model="CodeReview",  # model = "deployment_name"
        messages=message_text,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        response_format={"type": "json_object"}

    )

    return completion


def main():
    st.title("Code Review Application")

    code_input = st.text_area("Paste your code here:")
    if st.button("Review"):
        messages = run_code_review(code_input)
        if messages:
            st.write("Code Review Result:")
            json_op = json.loads(messages.choices[0].message.content)
            new_lang = json_op['detected_language'].lower()

            if new_lang == 'c++':
                new_lang = 'cpp'


            st.code(json_op['corrected_code'], language=new_lang)
            st.markdown(json_op['explanation'])
            st.markdown("The Code Accuracy is: " + json_op['code_accuracy'])

            corrected_code=json_op['corrected_code']
            explanation=json_op['explanation']
            code_accuracy=json_op['code_accuracy']
            print(new_lang)
            print(corrected_code)
            print(explanation)
            print(code_accuracy)
            print(type(new_lang))
            print(type(explanation))
            print(type(code_accuracy))
            print(type(corrected_code))
            print(type(code_input))
            stroutput= json.dumps(json_op)
            print(stroutput)
            print(type(stroutput))
            print(type(json_op))

            # Store data in MySQL Workbench table
            store_code_review(new_lang,code_input,corrected_code,explanation,code_accuracy)

            # Print the stored data for debugging


if __name__ == '__main__':
    app.teardown_appcontext(close_db)  # Register function to close database connection at the end of the request
    main()
