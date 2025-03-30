from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os, json
from datetime import datetime

from app.utils import login_required
from app.models import Blog, Users
from app.extensions import db

blog = Blueprint("blog", __name__)

# Path to store uploaded images
UPLOAD_FOLDER = "app/static/images/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@blog.route("/add_blog", methods=["GET", "POST"])
@login_required
def add_blog():
    user_session_data = session.get("login_user")
    if not user_session_data:
        flash("You need to log in to create a blog.", "warning")
        return redirect(url_for("auth.login_user"))

    current_user = Users.query.get(user_session_data["user_id"])
    if not current_user:
        flash("User not found. Please log in again.", "danger")
        return redirect(url_for("auth.logout"))

    if request.method == "POST":
        title = request.form.get("title").strip()  # Remove extra spaces
        description_text = request.form.get("description_text")
        description_content = request.form.get("description_content")
        images_list = []

        # Ensure the title is unique
        existing_blog = Blog.query.filter_by(title=title).first()
        if existing_blog:
            flash("A blog with this title already exists. Please choose a different title.", "danger")
            return redirect(url_for("blog.add_blog"))

        # Handle file uploads
        if "images" in request.files:
            files = request.files.getlist("images")
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"{current_user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(file_path)
                    images_list.append(filename)
                elif file.filename:
                    flash("Invalid file format. Please upload PNG, JPG, JPEG, or GIF.", "danger")

        # Create and save the blog post
        new_blog = Blog(
            title=title,
            description_text=description_text,
            description_content=description_content,
            images_list=json.dumps(images_list),
            author_id=current_user.id,
            created_at=datetime.utcnow()
        )
        db.session.add(new_blog)
        db.session.commit()

        flash("Blog post created successfully!", "success")
        return redirect(url_for("blog.view_blog", blog_id=new_blog.id))

    return render_template("add_blog.html")

@blog.route("/view_blog/<int:blog_id>", methods=["GET"])
def view_blog(blog_id):
    blog_post = Blog.query.get_or_404(blog_id)

    # Convert stored JSON images list to Python list before passing to the template
    images_list = json.loads(blog_post.images_list) if blog_post.images_list else []

    return render_template("view_blog.html", blog=blog_post, images=images_list)


@blog.route("/edit_blog/<int:blog_id>", methods=["GET", "POST"])
@login_required
def edit_blog(blog_id):
    blog_post = Blog.query.get_or_404(blog_id)

    # Ensure only the author can edit
    if session.get("login_user")["user_id"] != blog_post.author_id:
        flash("You are not authorized to edit this blog.", "danger")
        return redirect(url_for("blog.view_blog", blog_id=blog_id))

    if request.method == "POST":
        blog_post.title = request.form.get("title")
        blog_post.description_text = request.form.get("description_text")
        blog_post.description_content = request.form.get("description_content")
        db.session.commit()
        flash("Blog post updated successfully!", "success")
        return redirect(url_for("blog.view_blog", blog_id=blog_id))

    return render_template("edit_blog.html", blog=blog_post)


@blog.route("/delete_blog/<int:blog_id>", methods=["POST"])
@login_required
def delete_blog(blog_id):
    blog_post = Blog.query.get_or_404(blog_id)

    # Ensure only the author can delete
    if session.get("login_user")["user_id"] != blog_post.author_id:
        flash("You are not authorized to delete this blog.", "danger")
        return redirect(url_for("blog.view_blog", blog_id=blog_id))

    db.session.delete(blog_post)
    db.session.commit()
    flash("Blog post deleted successfully!", "success")
    return redirect(url_for("main.dashboard"))
