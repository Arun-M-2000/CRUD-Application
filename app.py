from flask import Flask, render_template, url_for, request, redirect ,flash
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


app.secret_key = "arunmsddhuhiuehikdnmszkhiuheifnkndiuhddfferrgtg"
# Home page
@app.route("/")
def home():
    con = mysql.connection.cursor()
    sql = "SELECT emp_id, name, salary FROM employees"
    con.execute(sql)
    result = con.fetchall()
    return render_template('home.html',data=result), 200

#Add Employeess
@app.route("/addemployee", methods=["POST", "GET"])
def addemployee():
    if request.method == "POST":
        con = mysql.connection.cursor()
        EMP_ID = request.form['id']
        NAME = request.form['name']
        SALARY = request.form['salary']
        con.execute("INSERT INTO employees (emp_id, name, salary) VALUES (%s, %s, %s)", (EMP_ID, NAME, SALARY))
        mysql.connection.commit()
        con.close()
        return redirect(url_for('home'))
    else:
        return render_template("addemployee.html")

#UPDTAE EMPLOYEES
@app.route("/update_emp",methods=["GET","POST"])
def update_emp():
    if request.method=="POST":
        EMP_ID = request.form.get('EMP_ID')
        NAME = request.form.get('name')
        SALARY = request.form.get('salary')
        con = mysql.connection.cursor()
        con.execute("UPDATE employees SET emp_id=%s, name=%s, salary=%s WHERE emp_id=%s", [EMP_ID, NAME, SALARY,EMP_ID])
        mysql.connection.commit()
        con.close()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
#Get Employees
@app.route("/get_emp/<string:id>",methods=["GET","POST"])
def get_emp(id):
    if request.method=="GET":
        con=mysql.connection.cursor()
        con.execute("SELECT * FROM employees WHERE emp_id = %s", (id,))
        result=con.fetchone()
        return render_template("update_emp.html",data=result)
    else:
        return redirect(url_for('home'))
#DELETE EMPLOYEES
@app.route("/delete_emp/<string:id>", methods=["GET","DELETE"])
def delete_emp(id):
    if request.args.get("_method") == "DELETE":
        con = mysql.connection.cursor()
        con.execute("DELETE FROM employees WHERE emp_id=%s", [id])
        mysql.connection.commit()
        con.close()
        flash("Employee deleted successfully")
        return redirect(url_for('home')), 302
    else:
        return redirect(url_for('home')), 302

if __name__ == '__main__':
    app.run(debug=True)

