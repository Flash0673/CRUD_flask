from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'no one should know this'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_crud'

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

@app.route('/')
def Index():

    students = db.session.execute(db.select(Student).order_by(Student.name)).scalars()

    return render_template('index.html', students=students )



@app.post('/insert')
def insert():

    flash("Data Inserted Successfully")
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    new_student = Student(name, email, phone)
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('Index'))




@app.route('/delete/<string:id>', methods = ['GET'])
def delete(id):
    student = db.get_or_404(Student, id)
    db.session.delete(student)
    db.session.commit()
    flash("Record Has Been Deleted Successfully")
    return redirect(url_for('Index'))





@app.route('/update<string:id>',methods=['POST','GET'])
def update(id):

    if request.method == 'POST':
        id = int(id)
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        student = db.get_or_404(Student, id)
        student.name = name
        student.email = email
        student.phone = phone
        db.session.commit()  
        flash("Data Updated Successfully")
        return redirect(url_for('Index'))









if __name__ == "__main__":
    app.run(debug=True)