from app.extensions import db, bcrypt

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=True)
    dob = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(500), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True, default="avatar.jpg")
    role = db.Column(db.String(20), nullable=False, default="user")
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Hash password before storing
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Check hashed password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    def __repr__(self):
        return f"<User {self.email} - {self.role}>"
