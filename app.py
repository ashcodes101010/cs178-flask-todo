# Built following the https://www.python-engineer.com/posts/flask-todo-app/
# tutorial 

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create Flask app
app = Flask(__name__)

# Configure DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define DB Model for Todo table
# Concept: model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# Home page displaying todo list
# Concept: routing
@app.route('/')
def home():
    # Concept: database
    todo_list = Todo.query.all()
    # Concept: template
    return render_template("base.html", todo_list=todo_list)

# Add todo to DB and rerender homepage
# Concept: routing
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

# Update todo in DB and rerender homepage
# Concept: routing
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

# Delete todo from DB and rerender homepage
# Concept: routing
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # Concept: database
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

# Create DB Todo table and run app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(debug=True) # Concept: debugger