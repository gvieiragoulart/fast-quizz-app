from sqlalchemy.orm import Session
from src.infrastructure.database.models import UserModel
from src.infrastructure.database.connection import SessionLocal
from passlib.context import CryptContext

def seed_user():
    """Seed a default user into the database."""
    db: Session = SessionLocal()
    try:
        # Check if the user already exists
        existing_user = db.query(UserModel).filter(UserModel.email == "admin@example.com").first()
        if not existing_user:
            # Hash the password
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            hashed_password = pwd_context.hash("admin123")

            # Create the user
            user = UserModel(
                username="Admin User",
                email="admin@example.com",
                hashed_password=hashed_password,
                type="admin",
                is_active=True,
            )
            db.add(user)
            db.commit()
            print("Default admin user created.")
        else:
            print("Default admin user already exists.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_user()