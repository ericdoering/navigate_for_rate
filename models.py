from cgi import MiniFieldStorage
import bcrypt
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    """Site user"""

    __tablename__ = "users"

    username = db.Column(db.String(20), nullable=False, unique=True, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.Text, nullable=False)
    company = db.Column(db.Text, nullable=False)
    state = db.Column(db.Text, nullable=False)

    routes = db.relationship("Route", backref="user", cascade="all, delete-orphan")

    @classmethod
    def register(cls, username, password, first_name, last_name, company, state):
        """Register a new user and encrypt their password"""

        hashed = bcrypt.generate_password_hash(password)
        hash_utf8 = hashed.decode("utf8")
        user = cls(
        username=username,
        password=hash_utf8,
        first_name=first_name,
        last_name=last_name,
        company=company,
        state=state
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate a user's credentials"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user

        else:
            return False


    @property 
    def full_name(self):
        "Full name of the user"

        return f"{self.first_name} {self.last_name}"


class Route(db.Model):
    """A driven route"""

    __tablename__ = "routes"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now().strftime("%c"))
    username = db.Column(db.String(20), db.ForeignKey("users.username"), nullable=False)
    start_point = db.Column(db.Text, nullable=False)
    end_point = db.Column(db.Text, nullable=False)
    mileage = db.Column(db.Float, nullable=False)
    travel_type = db.Column(db.String, nullable=False)
    map_url = db.Column(db.String, nullable=False)
    comments = db.Column(db.Text, nullable=True)

def connect_db(app):
    """Connecting the database to Flask App"""

    db.app = app
    db.init_app(app)