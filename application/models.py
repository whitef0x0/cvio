print("Starting to Load Models.py\n")

from index import db, bcrypt
import datetime

from sqlalchemy import event

def update_created_modified_on_create_listener(mapper, connection, target):
  """ Event listener that runs before a record is updated, and sets the create/modified field accordingly."""
  target.created = datetime.datetime.utcnow()
  target.modified = datetime.datetime.utcnow()

def update_modified_on_update_listener(mapper, connection, target):
  """ Event listener that runs before a record is updated, and sets the modified field accordingly."""
  # it's okay if this field doesn't exist - SQLAlchemy will silently ignore it.
  target.modified = datetime.datetime.utcnow()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    created = db.Column(db.Date)
    modified = db.Column(db.Date)
    documents = db.relationship("CoverLetter", back_populates="user")

    def __init__(self, email, password):
        self.email = email
        self.active = True
        self.password = User.hashed_password(password)
        self.created = datetime.datetime.now()

    @staticmethod
    def hashed_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    @staticmethod
    def get_user_with_email_and_password(email, password):
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None

class CoverLetter(db.Model):
    __tablename__ = 'coverletter'
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text(), unique=True)
    title = db.Column(db.String(255))
    created = db.Column(db.Date)
    modified = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="documents")

    def __init__(self, text, title=""):
        self.text = text
        self.title = title

    @staticmethod
    def get_coverletter_by_id(id):
        cv = CoverLetter.query.filter_by(id=id).first()
        if cv and len(cv.text) > 0:
            return cv
        else:
            return None

event.listen(User, 'after_insert', update_created_modified_on_create_listener)
event.listen(CoverLetter, 'after_insert', update_created_modified_on_create_listener)

event.listen(User, 'after_update', update_modified_on_update_listener)
event.listen(CoverLetter, 'after_update', update_modified_on_update_listener)

print("Loaded Models.py\n")

