from flask import Flask, render_template, url_for, request, redirect
from flask_mysqldb import MySQL
from flask import jsonify
import MySQLdb
from MySQLdb import IntegrityError

app = Flask(__name__)

# MySQL connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Arun@2000"
app.config["MYSQL_DB"] = "tata"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

# Home page
@app.route("/")
def home():
    print("homeemployee")
    con = mysql.connection.cursor()
    sql = "SELECT emp_id, name, salary FROM employees"
    con.execute(sql)
    result = con.fetchall()
    #return render_template('home.html', data=result)
    return jsonify(result), 200

#Add employees
@app.route("/addemployee", methods=["GET","POST","DELETE","PUT","PATCH"])
def addemployee():
    print("addemployee")
    if request.method == "POST":
            EMP_ID = request.form['id']
            NAME = request.form['name']
            SALARY = request.form['salary']
            print("SALARY",SALARY)
            print("EMP",NAME,EMP_ID)
            con = mysql.connection.cursor()
            sql = "INSERT INTO employees (emp_id, name, salary) VALUES (%s, %s, %s)"
            try:
                con.execute(sql, [EMP_ID, NAME, SALARY])
                print("sql",sql)
                mysql.connection.commit()
                con.close()
                print("employee added")
                return jsonify(response={
                "Error_message":"",
                "Status":"Success",
                "Text":"Employee added successfully"
        }),200
            except MySQLdb.IntegrityError as IntEr:
                    print("Error:", str(IntEr))
                    return jsonify(response={
                    "Error_message":"Duplicate entry for 'emp_id'",
                    "Status":"Fail",
                    "Text":"employee not added successfully"
                     }),404
    else:
        return jsonify(response={
             "Error_message":"method is not POST",
             "Status":"Fail",
             "Text":"Give the HTTP method as POST"
        }),404
            
#UPDTAE EMPLOYEES
@app.route("/update_emp",methods=["GET","POST","DELETE","PUT","PATCH"])
def update_emp():
    print("updateemployee1")
    con=mysql.connection.cursor()
    print("updateemployee2")
    EMP_ID = request.form.get('EMP_ID')
    print("updateemployee3")
    con.execute("SELECT emp_id FROM employees WHERE emp_id=%s",(EMP_ID,))
    success=con.fetchone()
    print("updateemployee4")
    if success is not None:
        print("updateemployee5")
        if request.method=="POST":
            EMP_ID = request.form.get('EMP_ID')
            NAME = request.form.get('name')
            SALARY = request.form.get('salary')
            con = mysql.connection.cursor()
            con.execute("UPDATE employees SET emp_id=%s, name=%s, salary=%s WHERE emp_id=%s", (EMP_ID, NAME, SALARY,EMP_ID))
            mysql.connection.commit()
            con.close()
            return jsonify(response={
             "Error_message":"",
             "Status":"Success",
             "Text":"update employee successfully"
        }),200
        else:
             return jsonify(response={
             "Error_message":"YOUR METHOD IS NOT POST",
             "Status":"FAIL",
             "Text":"CHANGE YOUR HTTP REQUEST AS POST"
        }),404

    else:
        return jsonify(response={
             "Error_message":"There is no employee in provided emp_id",
             "Status":"Fail",
             "Text":"Employee NOT FOUND"
        }),404
#Get Employees
@app.route("/get_emp/<string:id>",methods=["GET","POST","PUT","DELETE","PATCH"])
def get_emp(id):
    con = mysql.connection.cursor()
    con.execute("SELECT emp_id FROM employees WHERE emp_id=%s",(id,))
    success=con.fetchone()
    if success is not None:
        if request.method=="GET":
            con=mysql.connection.cursor()
            con.execute("SELECT * FROM employees WHERE emp_id = %s", (id,))
            result=con.fetchone()
            print("goupdate=",result)
            return jsonify(response={
                "Error_message":"",
                "Status":"Success",
                "Text":"get employee successfully."
            }),200
        else:
            return jsonify (response={
                "Error_message":"YOUR HTTP REQUEST IS NOT GET",
                "Status":"Fail",
                "Text":"Use HTTP Request as GET"
            }),404
    else:
        return jsonify(response={
             "Error_message":"There is no employee in given emp_id",
             "Status":"Fail",
             "Text":"Employee not get"
        }),404

#DELETE EMPLOYEES
@app.route("/delete_emp/<string:id>", methods=["GET","POST","DELETE","PUT","PATCH"])
def delete_emp(id):
    print("deleteemployee")
    con=mysql.connection.cursor()
    con.execute("SELECT emp_id FROM employees WHERE emp_id=%s",[id])
    success=con.fetchone()
    if success is not None:
        if request.method=="DELETE":
            con=mysql.connection.cursor()
            con.execute("DELETE FROM employees WHERE emp_id=%s",[id])
            mysql.connection.commit()
            con.close()
            return jsonify (response={    
            "error_message":"",
            "status":"success",
            "text":"emoloyee deleted",
             }),200
        else:
            return jsonify (response={
                "Error_message":"YOUR HTTP REQUEST IS NOT DELETE",
                "Status":"Fail",
                "Text":"Use HTTP Request as DELETE"
            }),404
    else:
        return jsonify (response={    
        "error_message":"Employee id is not available ",
        "status":"fail",
        "text":"emoloyee not deleted",
            }),404

if __name__ == '__main__':
    app.run(debug=True)
