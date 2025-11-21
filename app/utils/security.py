from passlib.context import CryptContext

# Configuration pour le hashing des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Vérifie si un mot de passe correspond au hash
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    # Hash le mot de passe
    return pwd_context.hash(password)