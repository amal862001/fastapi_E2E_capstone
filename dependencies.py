from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from services.auth_service import decode_access_token, get_user_by_id
from models.user import PlatformUser

# bearer token extractor
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> PlatformUser:

    # extract token from Authorization header
    token = credentials.credentials

    # decode the token
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail      = "Invalid or expired token"
        )

    # get user from database
    user_id = int(payload.get("sub"))
    user    = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail      = "User not found"
        )

    return user