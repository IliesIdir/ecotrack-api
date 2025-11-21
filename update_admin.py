from app.database import SessionLocal
from app.models.user import User

# Créer une session
db = SessionLocal()

# Trouver l'utilisateur admin
admin_user = db.query(User).filter(User.email == "admin@ecotrack.com").first()

if admin_user:
    admin_user.role = "admin"
    db.commit()
    print(f"User {admin_user.username} is now an admin!")
else:
    print("User not found")

db.close()