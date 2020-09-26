import os

from flask import Flask
from flask import render_template, redirect
from flask import request
from flask_sqlalchemy import SQLAlchemy


SQLALCHEMY_DATABASE_URI = 'postgres://saif:brick@localhost/todo_db'



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)



#models
class Todos(db.Model):
	_tablename = "todos"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)
	Duration = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return "<Title: {}>".format(self.title)

#routes
@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        todo = Todos(
        			title=request.form.get("title"),
        			description= request.form.get("description"),
        			Duration = request.form.get("duration")
        				)
        db.session.add(todo)
        db.session.commit()
    todos = Todos.query.all()
    return render_template("index.html", todos=todos)

@app.route("/<int:page_id>/update", methods=["GET", "POST"])
def update(page_id):
    todo = Todos.query.filter_by(id=page_id).first()
    print(todo)

    if request.form:
	    newtitle = request.form.get("newtitle")
	    newdescription = request.form.get("newdescription")
	    newduration = request.form.get("newduration")
	    todo.title = newtitle
	    todo.description = newdescription
	    todo.Duration = newduration
	    db.session.commit()
	    return redirect("/")
	    
    return render_template("update.html", todo=todo)


@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    todo = Todos.query.filter_by(title=title).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)