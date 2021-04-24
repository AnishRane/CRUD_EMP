from flask import Flask,redirect,render_template,request,redirect,url_for,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.secret_key = "98hi54"

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db = SQLAlchemy(app) 
ma = Marshmallow(app)


class Employees(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(100))
	email=db.Column(db.String(100))
	phone=db.Column(db.String(100))

	def __init__(self,name,email,phone):
		self.name= name
		self.email=email
		self.phone=phone


class EmployeeSchema(ma.Schema):
	class Meta:
		fields=('id','name','email','phone')


employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)




#front-end
@app.route('/')
def Index():
	all_data = Employees.query.all()

	return render_template("index.html",employees=all_data)

#getEmployees API_InterFace
@app.route('/getEmployees',methods=['GET'])
def get_employees():
	employees = Employees.query.all()
	result = employees_schema.dump(employees)
	return jsonify(result)

#getEmployee API_InterFace
@app.route('/getEmployee/<id>',methods=['GET'])
def get_employee(id):
	employee = Employees.query.get(id)
	result = employee_schema.dump(employee)
	return jsonify(result)




@app.route('/insert',methods=['POST'])
def insert():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		phone = request.form['phone']

		emp_data = Employees(name,email,phone)
		db.session.add(emp_data)
		db.session.commit()
		flash("Employee Added Sucessfully")

		return redirect(url_for('Index'))

#insert API_INTERFACE
@app.route('/insertEmployee',methods=['POST'])
def insertEmployee():
	name = request.json['name']
	email = request.json['email']
	phone = request.json['phone']

	newEmployee = Employees(name,email,phone)
	db.session.add(newEmployee)
	db.session.commit()

	return employee_schema.jsonify(newEmployee)





@app.route('/update',methods=['GET','POST'])
def update():
	if request.method == "POST":
		emp_data = Employees.query.get(request.form.get('id'))
		emp_data.name=request.form['name']
		emp_data.email=request.form['email']
		emp_data.phone = request.form['phone']

		db.session.commit()
		flash("Employee Updated Sucessfully")

		return redirect(url_for("Index"))


#UPDATE EMPLOYEE API_INTERFACE
@app.route('/updateEmployee/<id>',methods=['PUT'])
def updateEmployee(id):
	employee = Employees.query.get(id)
	name = request.json['name']
	email = request.json['email']
	phone = request.json['phone']

	employee.name = name
	employee.email = email
	employee.phone = phone

	db.session.commit()

	result = employee_schema.dump(employee)
	return jsonify(result)










@app.route('/delete/<id>/',methods=['GET','POST'])
def delete(id):
	emp_data=Employees.query.get(id)
	db.session.delete(emp_data)
	db.session.commit()
	flash("Employee Deleted Sucessfully")
	return redirect(url_for('Index'))

#deleteUser 
@app.route('/delete/<id>',methods=['DELETE'])
def deleteEmployee(id):
	employee = Employees.query.get(id)
	db.session.delete(employee)
	db.session.commit()

	return jsonify({"msg":"Employee Deleted Sucessfully"})


if __name__ == "__main__":
	app.run(host='0.0.0.0')
