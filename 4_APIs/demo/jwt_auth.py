#Load env file
from dotenv import load_dotenv
load_dotenv()
import os

from pydantic import BaseModel
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    email: str = None
    hashed_password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type:str

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)

# Creating and Signing JWT Tokens
from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt


SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 5

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Login Endpoint
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Dummy user for demo
dummy_users_db = {
    "Suganth": {
        "username": "Suganth",
        "hashed_password": get_password_hash(os.environ.get('DUMMY_PWD')),
    }
}

@app.get("/")
async def index():
    return {"message": "Hello, Learn JWT"}

@app.post("/token", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    user_dict = dummy_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400, 
            detail="Incorrect User")
    user = User(**user_dict)
    if not verify_password(plain_password=form_data.password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub":user.username},
        expires_delta=access_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )
    #return {"access_token":access_token, "token_type":"bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentilals_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentilals_exception
    except JWTError:
        raise credentilals_exception
    
    user = dummy_users_db.get(username)
    if user is None:
        raise credentilals_exceptio
    return user

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user