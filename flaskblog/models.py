from datetime import datetime
from flaskblog import db, LM, app
from flask_login import UserMixin
from itsdangerous import Serializer

@LM.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), nullable=False, unique=True)
    email=db.Column(db.String(100), nullable=False, unique=True)
    password= db.Column(db.String(60), nullable=False)
    img=db.Column(db.String(20), nullable=False, default='default.jpg')
    posts=db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expire_time=900):
        s=Serializer(app.config['SECRET_KEY'], expire_time)
        token= s.dumps({'user_id':self.id}).decode('utf-8')
        return token
    @staticmethod
    def verify_reset_token(token):
        s=Serializer(app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
            # extracts user_id component from user_data taken from s.loads(token) and assigns it to variable user_id
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}, {self.email}, {self.img}')"

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    Date_Posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content=db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post({self.title}, {self.Date_Posted})"