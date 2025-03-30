from app.extensions import db
from datetime import datetime
import json

class Blog(db.Model):
    __tablename__ = "blog"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    description_text = db.Column(db.Text, nullable=False)
    description_content = db.Column(db.Text, nullable=True, default='')
    
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    
    images_list = db.Column(db.Text, nullable=True, default='[]')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    author = db.relationship('Users', backref=db.backref('blogs', lazy=True))
    category = db.relationship('Category', backref=db.backref('blogs', lazy=True))

    def __repr__(self):
        return f"<Blog {self.title} by User {self.author_id}>"

    def get_images(self):
        """Convert stored JSON string to a Python list."""
        return json.loads(self.images_list) if self.images_list else []
    
    def add_image(self, image_filename):
        """Add a new image to the images list and update the database."""
        images = self.get_images()
        images.append(image_filename)
        self.images_list = json.dumps(images)
        db.session.commit()
