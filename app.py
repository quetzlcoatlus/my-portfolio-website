from flask import Flask, Blueprint, render_template, request, redirect
from werkzeug.utils import secure_filename

from flask_sqlalchemy import SQLAlchemy  # converts python into SQL
from datetime import datetime


# How every Flask app starts
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db = SQLAlchemy(app)


# db Model (required)
class Projects(db.Model):
    # data base columns
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


@app.route("/projects", methods=["POST", "GET"])
def projects():
    if request.method == "POST":
        project_name = request.form["project-name"]
        project_thumbnail = request.files["project-thumbnail"].read()

        # thumbnail = Img(img=project_thumbnail.read(), mimetype=project_thumbnail.mimetype, name=secure_filename(project_thumbnail.filename))

        project_description = request.form["project-description"]
        date_string = request.form["project-date"]
        project_date = datetime.strptime(date_string, "%Y-%m-%d")

        new_project = Projects(name=project_name, thumbnail=project_thumbnail, description=project_description, date=project_date)

        # Push to database
        # try:
        db.session.add(new_project)
        db.session.commit()
        return redirect("/projects")
        # except:
        #     return "error occurred"

    else:
        projects_list = Projects.query.order_by(Projects.date)
        return render_template("projects.html", projects=projects_list)


@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


if __name__ == '__main__':
    app.run(debug=True)
