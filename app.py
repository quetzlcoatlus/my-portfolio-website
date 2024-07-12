from flask import Flask
from views import views
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# How every Flask app starts
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db = SQLAlchemy(app)


# db Model (required)
class Projects(db.Model):
    pass


app.register_blueprint(views, url_prefix="/")

if __name__ == '__main__':
    app.run(debug=True)
