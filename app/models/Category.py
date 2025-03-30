from app.extensions import db

class Category(db.Model):
    __tablename__ = "category"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    def __repr__(self):
        return f"<Category {self.name}>"
