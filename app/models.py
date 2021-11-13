from . import db
from werkzeug.security import check_password_hash, generate_password_hash
from . import login_manager
from flask_login import UserMixin
from datetime import datetime
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    blogs = db.relationship('blog',backref = 'user',lazy = "dynamic")
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    pass_secure  = db.Column(db.String(255))
    #date_joined = db.Column(db.DateTime,default=datetime.utcnow)
    comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")
    def __repr__(self):
        return f'User {self.username}'
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'

class blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer,primary_key = True)
    blog_title = db.Column(db.String)
    blog_content = db.Column(db.String(1000))
    category = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    comments = db.relationship('Comment',backref =  'blog_id',lazy = "dynamic")

    def __repr__(self):
        return f'User {self.blog_title}'

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blogs(cls,category):
        blogs = blog.query.filter_by(category=category).all()
        return blogs

    @classmethod
    def get_blog(cls,id):
        blog = blog.query.filter_by(id=id).first()

        return blog

    @classmethod
    def count_blogs(cls,uname):
        user = User.query.filter_by(username=uname).first()
        blogs = blog.query.filter_by(user_id=user.id).all()

        blogs_count = 0
        for blog in blogs:
            blogs_count += 1

        return blogs_count

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(1000))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    blog = db.Column(db.Integer,db.ForeignKey("blogs.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,blog):
        comments = Comment.query.filter_by(blog_id=blog).all()
        return comments