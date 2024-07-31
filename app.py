from flask import Flask, Blueprint, render_template, request, redirect

from flask_sqlalchemy import SQLAlchemy  # converts python into SQL
from datetime import datetime

# How every Flask app starts
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db = SQLAlchemy(app)


# db Model (required)
class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    thumbnail = db.Column(db.BLOB)
    description = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


views = Blueprint(__name__, "views")
app.register_blueprint(views, url_prefix="/")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/projects")
def projects():
    if request.method == "POST":
        project_name = request.form["project-name"]
        new_project = Projects(name=project_name)

        # Push to database
        try:
            db.session.add(new_project)
            db.session.commit()
            return redirect("/projects")
        except:
            return "error occurred"

    else:
        projects_list = Projects.query.order_by(Projects.date)
        return render_template("projects.html", projects=projects_list)


@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


if __name__ == '__main__':
    app.run(debug=True)
