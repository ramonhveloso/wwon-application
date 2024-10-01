import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# Pega a chave secreta da variável de ambiente
SECRET_KEY = os.getenv("SECRET_KEY")

if SECRET_KEY is None:
    raise ValueError("A variável de ambiente SECRET_KEY não está definida.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração do OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# Função para verificar se a senha em texto puro é equivalente à senha hash armazenada
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Função para gerar um hash da senha
def get_password_hash(password):
    return pwd_context.hash(password)


# Função para criar um token de acesso JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})

    # Gera o token JWT utilizando a SECRET_KEY
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt


# Função para decodificar e validar um token JWT
def decode_access_token(token: str):
    try:
        # Decodifica o token e valida o algoritmo utilizado
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # Se houver um erro na decodificação, lança uma exceção de autenticação inválida
        raise HTTPException(status_code=401, detail="Invalid token or expired token")


# Função para obter o usuário atual a partir do token
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    username = payload.get("sub")  # 'sub' é o campo padrão que contém o nome de usuário
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username
