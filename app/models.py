import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin
from math import log


topics_table = db.Table('topics_table',
        db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
        db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'), primary_key=True))


class User(UserMixin, db.Model):
    """Model for the user table.
    
    Represents a user on the website.
    
    Parameters
    ----------
    id : int
        Unique id which is different for all users.
    username : str
        String for username which the user can pick and also change.
    email : str
        String that holds the user's email, for notifications.
    password_hash : str
        Contains the hashed password, for security purposes.
    posts : method
        Contains an sql query for all of the user's posts.
    
    Relationships
    -------------
    User-Post = One to many relationship
    User-Topic = Currently doesn't exist."""
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return self.username  

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    """Model for the posts table.
       
    Represents the posts made by a user on the website.
    
    Parameters
    ----------
    id : int
        Unique number that is different for all posts.
        
    text : str
        The main part of the post, so the text.
    timestamp: int
        The time at which the post was made.
    user_id : int
        The unique id of the user that originally made the post.
    title : str
        The title of the post.
    comments : method
        Sql query for all of the comments made in the post.

    score : int
        Upvotes - Downvotes of a post.
    upvotes : int
        The number of times a user has voted the post up.
    downvotes : int
        The number of times a user has voted the post down.
    importance : int
        The number of times a user has given a post importance.
    hotness : int
        Number which posts will be sorted by.

    age : int
        How old a post is, compared to the epoch time.
    topics : method
        Sql query which returns a list of all the topics a post has.

    created_on : int
       Same deal as the timestamp...

    Relationships
    --------------
    Posts-Topics = Many to Many
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(50))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    score = db.Column(db.Float)
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
    importance = db.Column(db.Integer)
    hotness = db.Column(db.Integer)

    age = db.Column(db.Integer)
    topics = db.relationship('Topic',
                    secondary=topics_table,
                    backref="posts")

    created_on = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return '<Post {}>'.format(self.text)

    def get_age(self):
        self.age = (self.timestamp - datetime.datetime(1970, 1, 1)).total_seconds()
        return self.age

    def get_score(self):
        self.score = self.upvotes - self.downvotes
        return self.score

    def get_hotness(self):
        self.get_age()
        self.hotness = db.engine.execute("UPDATE post SET hotness=(upvotes - downvotes) * age / importance")

    def set_hotness(self):
        self.hotness = self.get_hotness()
        db.session.commit()

    def upvote(self):
        self.upvotes = int(self.upvotes) + 1
        db.session.commit()

    def downvote(self):
        self.downvotes = int(self.downvote) + 1
        db.session.commit()

    def make_vote_int(self):
        if self.upvotes == None:
            self.upvotes = 1

        if self.downvotes == None:
            self.downvotes = 1

    def make_importance_int(self):
        if self.importance == None:
            self.importance = 1


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    username = db.Column(db.String(64))
    text = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Comment {}>'.format(self.text)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64), index=True, unique=True)
    # There should be a post_id, to reference all posts with this tag...

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

def find_users_post(user):
    posts = Post.query.all()
    user_posts = []
    for post in posts:
        if post.author.id == user.id:
            user_posts.append(post)

    return user_posts
