from flask import render_template, flash, redirect, url_for, request
from flask_login import logout_user, current_user, login_user, login_required
from werkzeug.urls import url_parse
from app.helpers import redirect_url
from app.models import User, Post, Comment, Topic,find_users_post
from app.forms import CommentForm, SubmitForm
from app import app, db


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = Post.query.order_by(Post.hotness.desc()).all()
    return render_template('index.html', title='Dopenet: You can do anything', posts=posts )

@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    form = SubmitForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, text=form.text.data, user_id=current_user.id, topics=[Topic(tag_name=form.topics.data)])
        post.upvotes = 1
        post.downvotes = 0
        post.importance = 1
        post.score = post.get_score()
        db.session.add(post)
        db.session.commit()
    
        flash('You have now made a post!')
        return redirect(url_for('index'))
    return render_template('submit.html', title='Submit', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = find_users_post(user)
    return render_template('user.html', user=user, posts=posts)

@app.route('/item/<post_id>', methods=['GET', 'POST'])
def item(post_id):

    post = Post.query.filter_by(id=post_id).first_or_404()

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.comment.data, post_id=post.id,
                user_id=current_user.id, username=current_user.username)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('item', post_id=post_id))

    comments = Comment.query.filter_by(post_id=post.id)
    user = post.author
    return render_template('item.html', user=user, post=post,
            comments=comments, form=form)


@app.route('/delete_comment/<post_id>/<comment_id>', methods=['POST'])
def delete_comment(post_id, comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment != None:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('item', post_id=post_id))


@app.route('/delete_post/<post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post != None:
        db.session.delete(post)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/vote/<post_id>', methods=['POST'])
def vote(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post != None:
        if post.upvotes == None:
            post.make_vote_int()

        
        if "upvote" in request.form:
            post.upvotes = post.upvotes + 1
            post.get_score()
            post.set_hotness()
            db.session.commit()
        if "downvote" in request.form:
            post.downvotes = post.downvotes + 1
            post.get_score()
            post.set_hotness()
            db.session.commit()

    return redirect(redirect_url()) # Look at snippet 62

@app.route('/give_importance/<post_id>', methods=['POST'])
def give_importance(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post != None:
        if post.importance == None:
            post.make_importance_int()
        post.importance = post.importance + 1
        post.set_hotness()
        db.session.commit()

    return redirect(redirect_url())


@app.route('/faq', methods=['GET'])
def faq():
    return render_template('faq.html')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/rules', methods=['GET'])
def rules():
    return render_template('rules.html')

