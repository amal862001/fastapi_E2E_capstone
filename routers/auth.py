from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from services.auth_service import create_user, authenticate_user, create_access_token
from schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from dependencies import get_current_user
from models.user import PlatformUser


router = APIRouter(prefix="/auth", tags=["Authentication"])

@