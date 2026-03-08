from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from services.auth_service import create_user, authenticate_user, create_access_token
from schemas.auth_schema import RegisterRequest, TokenResponse, UserResponse
from dependencies import get_current_user
from models.user import PlatformUser

router = APIRouter(prefix="/auth", tags=["Authentication"])


# Register 

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):

    user = create_user(
        db          = db,
        full_name   = request.full_name,
        email       = request.email,
        password    = request.password,
        agency_code = request.agency_code,
        role        = request.role
    )

    if user is None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail      = "Email already registered"
        )

    return user


# Login

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)

    if user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail      = "Invalid email or password"
        )

    token = create_access_token(user)
    return TokenResponse(access_token=token)


# Get current user

@router.get("/me", response_model=UserResponse)
def get_me(current_user: PlatformUser = Depends(get_current_user)):
    return current_user