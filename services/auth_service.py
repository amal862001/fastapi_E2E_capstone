from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.user import PlatformUser
from config import settings

# password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Password helpers 

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)   # checks if plain password matches the hashed password, returns True or False


# JWT helpers 

def create_access_token(user: PlatformUser) -> str:
    payload = {
        "sub"         : str(user.id),
        "agency_code" : user.agency_code,
        "role"        : user.role,
        "exp"         : datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        return None


# User helpers

def get_user_by_email(db: Session, email: str) -> PlatformUser:
    return db.query(PlatformUser).filter(PlatformUser.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> PlatformUser:
    return db.query(PlatformUser).filter(PlatformUser.id == user_id).first()


def create_user(db: Session, full_name: str, email: str, password: str, agency_code: str, role: str) -> PlatformUser:
    # check if email already exists
    existing = get_user_by_email(db, email)
    if existing:
        return None

    user = PlatformUser(
        full_name       = full_name,
        email           = email,
        hashed_password = hash_password(password),
        agency_code     = agency_code,
        role            = role
    )
    db.add(user)  
    db.commit() 
    db.refresh(user) # refresh the user instance to get the generated ID and other fields from the database
    return user


def authenticate_user(db: Session, email: str, password: str) -> PlatformUser:
    user = get_user_by_email(db, email) 
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user 