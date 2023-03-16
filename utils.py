
import re
from datetime import datetime, timedelta, timezone
import time
import jwt
from models import *
from passlib.context import CryptContext
import random
from fastapi import HTTPException


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET = 'token'
ALGORITHME = 'HS256'

async def checkEmail(email):

	if(re.fullmatch(regex, email)):
		return True

	else:
		return False

async def emailIsExist(email):
    user = await Personne.filter(email = email)
    print(user)
    if user == []:
        return False
    else:
        return True    
    
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

async def generateCode():
    liste = []
    for i in range(3):
        r = random.randint(0 , 9)
        liste.append(str(r))
    
    for i in range(3):
        r2 = random.randint(0 , 9)
        liste.append(str(r2))
    code = ''
    for i in range(len(liste)):
        code = code+liste[i] 
    return code
    
    
async def createToken(user):
    payload = {
    "sub": user,
    "iat": datetime.utcnow(),
    "exp": datetime.utcnow() + timedelta(minutes=30)
    }

    token = jwt.encode(payload , SECRET , algorithm = ALGORITHME )
    return token

async def decodeAndVerify(encoded):
    try:
        decoded_jwt = jwt.decode(encoded, SECRET, algorithms=ALGORITHME,verify_expiration=True)
        return decoded_jwt['sub']
    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(detail="JWT signature is invalid." , status_code=401)
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(detail="JWT has expired.",status_code=401)


async def isGerant(gerant):
    print('gerant = ',type(str(gerant)))
    user = await Personne.filter(id = gerant)
    print("user = ",user)
    if user == []:
        raise HTTPException(status_code=404 , detail="utilisateur non trouvez")
        
    else:
        user = await Personne.get(id = gerant) 
        g = await Gerant.get(user = user)
        if g:
            return True
        else:
            raise HTTPException(status_code=401 , detail="vous n'etez pas autoriser à faire cette action")