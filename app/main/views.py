from . import main
import flask
from flask_login import login_required,current_user
from flask import render_template,abort,redirect,url_for,request
from ..models import Role,User
from .forms import UpdateProfile,BlogForm,CommentForm
from .. import db,photos
from app.models import User,blog,Comment
from ..forms import UpdateProfile

#main route
@main.route("/")
def index():
    """
    view root page that returns the index page and its data
    """
    return render_template("index.html")

#profile
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


#photos logic
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update_profile.html',form =form)


@main.route('/blog/new', methods = ['GET','POST'])
@login_required
def new_blog():
    blog_form = BlogForm()
    if blog_form.validate_on_submit():
        title = blog_form.title.data
        blog = blog_form.text.data
        category = blog_form.category.data
        # Updated blog instance
        new_blog = blog(blog_title=title,blog_content=blog,category=category, user=current_user,likes=0,dislikes=0)

        # Save blog method
        new_blog.save_blog()
        return redirect(url_for('.index'))

    title = 'New blog'
    return render_template('new_blog.html',title = title,blog_form=blog_form )




@main.route('/blogs/science_blogs')
def science_blogs():

    blogs = blog.get_blogs('science')

    return render_template("science_blogs.html", blogs = blogs)


@main.route('/blogs/anaconda_blogs')
def anaconda_blogs():

    blogs = blog.get_blogs('anaconda')

    return render_template("anaconda_blogs.html", blogs = blogs)


@main.route('/blogs/alien_blogs')
def alien_blogs():

    blogs = blog.get_blogs('alien')

    return render_template("alien_blogs.html", blogs = blogs)



@main.route('/blogs/birds_blogs')
def birds_blogs():

    blogs = blog.get_blogs('birds')

    return render_template("birds_blogs.html", blogs = blogs)


@main.route('/blogs/culture_blogs')
def culture_blogs():

    blogs = blog.get_blogs('culture')

    return render_template("culture_blogs.html", blogs = blogs)


@main.route('/blogs/poetry_blogs')
def poetry_blogs():

    blogs = blog.get_blogs('poetry')

    return render_template("poetry_blogs.html", blogs = blogs)


@main.route('/blog/<int:id>', methods = ['GET','POST'])
def blog(id):
    blog = blog.get_blog(id)
    posted_date = blog.posted.strftime('%b %d, %Y')

    if request.args.get("like"):
        blog.likes = blog.likes + 1

        db.session.add(blog)
        db.session.commit()

        return redirect("/blog/{blog_id}".format(blog_id=blog.id))
                                

    elif request.args.get("dislike"):
        blog.dislikes = blog.dislikes + 1

        db.session.add(blog)
        db.session.commit()

        return redirect("/blog/{blog_id}".format(blog_id=blog.id))

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.text.data

        new_comment = Comment(comment = comment,user = current_user,blog_id = blog)

        new_comment.save_comment()


    comments = Comment.get_comments(blog)

    return render_template("blog.html", blog = blog, comment_form = comment_form, comments = comments, date = posted_date)

@main.route('/user/<uname>/blogs')
def user_blogs(uname):
    user = User.query.filter_by(username=uname).first()
    blogs = blog.query.filter_by(user_id = user.id).all()
    blogs_count = blog.count_blogs(uname)
    

    return render_template("profile/user_blogs.html", user=user,blogs=blogs,blogs_count=blogs_count)
