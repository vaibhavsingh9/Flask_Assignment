from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        student_id = userDetails['student_id']
        student_fname = userDetails['student_fname']
        student_lname = userDetails['student_lname']
        gender	= userDetails['gender']
        Class = userDetails['Class']
        dob = userDetails['dob']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students(student_id, student_fname, student_lname, gender, Class, dob) VALUES(%s, %s, %s, %s, %s, %s)",(int(student_id), student_fname, student_lname, gender, Class, dob))
        mysql.connection.commit()
        cur.close()
        return redirect('/students')
    return render_template('index.html')

@app.route('/students')
def students():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM students")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('students.html',userDetails=userDetails)

if __name__ == '__main__':
    app.run(debug=True)