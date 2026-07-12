from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from App.auth.dependencies import get_current_user
from App.auth.hashing import hash_password, verify_password
from App.auth.jwt_handler import create_access_token
from App.database.database import get_db
from App.models.user import User
from App.schemas.user import (
    UserRegister,
    UserLogin,
    UserResponse,
    Token,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ----------------------------------------------------
# Register
# ----------------------------------------------------
@router.post("/register", response_model=UserResponse)
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ----------------------------------------------------
# Login (JSON) - Used by Frontend
# ----------------------------------------------------
@router.post("/login", response_model=Token)
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    print("\n========== LOGIN START ==========")
    print("STEP 1 : Login request received")

    db_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    print("STEP 2 : User fetched ->", db_user)

    if not db_user:
        print("User not found")
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    print("STEP 3 : Verifying password")

    if not verify_password(
        user.password,
        db_user.hashed_password,
    ):
        print("Password incorrect")
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    print("STEP 4 : Creating JWT Token")

    access_token = create_access_token(
        {
            "sub": db_user.email,
            "role": db_user.role,
        }
    )

    print("STEP 5 : Login Successful")
    print("========== LOGIN END ==========\n")

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# ----------------------------------------------------
# OAuth2 Login - Used by Swagger
# ----------------------------------------------------
@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    print("\n========== SWAGGER LOGIN START ==========")
    print("STEP 1 : Swagger login request")

    db_user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )

    print("STEP 2 : User fetched ->", db_user)

    if not db_user:
        print("User not found")
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )

    print("STEP 3 : Verifying password")

    if not verify_password(
        form_data.password,
        db_user.hashed_password,
    ):
        print("Password incorrect")
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )

    print("STEP 4 : Creating JWT Token")

    access_token = create_access_token(
        {
            "sub": db_user.email,
            "role": db_user.role,
        }
    )

    print("STEP 5 : Login Successful")
    print("========== SWAGGER LOGIN END ==========\n")

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# ----------------------------------------------------
# Current Logged-in User
# ----------------------------------------------------
@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user