from flask import Flask
from views import views
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


app.register_blueprint(views, url_prefix="/")

if __name__ == '__main__':
    app.run(debug=True)
