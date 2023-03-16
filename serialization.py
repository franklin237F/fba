from pydantic import BaseModel, validator
from enum import Enum
from fastapi import HTTPException


class MyEnum(Enum):
    Ambassadeur = "Ambassadeur"
    Mouvement = "Mouvement"
    Partenaire = "Partenaire"
    Actionnaire = "Actionnaire"
    MembrePleinDroit = "MembrePleinDroit"
    Gerant = "Gerant"
    
    
class PartEnum(Enum):
    Epargne = "Epargne"
    Investissement = "Investissement"
    Retrait = "Retrait"


class MembrePleinDroitEnum(Enum):
    Pret = "Pret"
    Epargne = "Epargne"
    Assurance = "Assurance"



class PersonneModel(BaseModel):
    firstname:str
    lastname:str
    country:str
    town:str
    email:str
    type:str
    number :str
    password1: str
    password2: str
    
    @validator("type")
    def check_type(cls, value):
        if value not in MyEnum.__members__:
            raise HTTPException(status_code=406, detail = f"ce poste (type) n'existe pas au sein de la FBA EMPIRE veillez choissir un poste qui existe: {', '.join(MyEnum.__members__)}")
        return value
    
    
    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise HTTPException(status_code=406 , detail='Les mots de passe ne sont pas identique')
            
        return v
    
    
class LoginModel(BaseModel):
    email : str
    password : str
    
    
class VerifyCode(BaseModel):
    email:str
    code : int
    
    
class AmbassadeursSchema(BaseModel):
    email:str
    cotisation:int
    
    
    
class PartenairesSchema(BaseModel):
    email:str
    type:str
    cotisation:int
    
    @validator("type")
    def check_type(cls, value):
        if value not in PartEnum.__members__:
            raise HTTPException(status_code=406, detail = f"ce type n'existe veillez choissir un type qui existe: {', '.join(PartEnum.__members__)}")
        return value
        
    
class TokenSchema(BaseModel):
    token : str
    
    
class MouvementsSchema(BaseModel):
    email:str
    nombre_action:int
    cotisation:int
    reste:int
    
    
class ActionnairesSchema(BaseModel):
    email:str
    nombre_action:int
    benefice:int
    
    
class membrePleinDroitSchema(BaseModel):
    email:str
    type:str
    cotisation:int
    
    
    @validator("type")
    def check_type(cls, value):
        if value not in MembrePleinDroitEnum.__members__:
            raise HTTPException(status_code=406, detail = f"ce type n'existe pas veillez choissir un type qui existe: {', '.join(MembrePleinDroitEnum.__members__)}")
        return value
    
class UpdatePasswordSchema(BaseModel):
    email:str
    old:str
    password1:str
    password2:str
    
    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise HTTPException(status_code=406 , detail='Les mots de passe ne sont pas identique')
            
        return v
    