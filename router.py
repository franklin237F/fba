from fastapi import APIRouter,HTTPException, Header
from models import *
from tortoise.contrib.pydantic import pydantic_model_creator
from serialization import *
from utils import *



router = APIRouter()

#==================================CREATION DE COMPTE============================

@router.post("/create-account" , tags=['Creation de compte'])
async def createAccount(personne:PersonneModel):
    name = personne.firstname
    prenom = personne.lastname
    pays = personne.country
    ville = personne.town
    email = personne.email
    numero = personne.number
    type = personne.type
    motDePasse = personne.password1
    confirmMotPasse = personne.password2
    
    if await emailIsExist(email) == True:
        raise HTTPException(status_code= 406 , detail= 'Cette adresse email existe déjà')    
    else:
        if await checkEmail(email) == True:
            password = get_password_hash(motDePasse)
            numero = await generateCode()
            print(numero)
            if type == "Ambassadeur":
                personne = await Personne.create(name = name , prenom = prenom , pays = pays , ville = ville ,email = email , numero = numero , motPasse = password , type = "Ambassadeur")
                await Codes.create(user = personne , number = numero)
                return{
                    "status":201,
                    "infos":"Bienvenue "+name,
                    "code":numero
                    
                }
            elif type == "Mouvement":
                personne = await Personne.create(name = name , prenom = prenom , pays = pays , ville = ville ,email = email , numero = numero , motPasse = password , type = "Mouvement")
                await Codes.create(user = personne , number = numero)
                return{
                    "status":201,
                    "infos":"Bienvenue "+name,
                    "code":numero
                }
            elif type == "Partenaires":
                personne = await Personne.create(name = name , prenom = prenom , pays = pays , ville = ville ,email = email , numero = numero , motPasse = password , type = "Partenaire")
                await Codes.create(user = personne , number = numero)
                return{
                    "status":201,
                    "infos":"Bienvenue "+name,
                    "code":numero
                } 
            elif type == "Actionnaires":
                personne = await Personne.create(name = name , prenom = prenom , pays = pays , ville = ville ,email = email , numero = numero , motPasse = password , type = "Actionnaire")
                await Codes.create(user = personne , number = numero)
                return{
                    "status":201,
                    "infos":"Bienvenue "+name,
                    "code":numero
                }
            elif type =="MembrePleinDroit":
                personne = await Personne.create(name = name , prenom = prenom , pays = pays , ville = ville ,email = email , numero = numero , motPasse = password , type = "MembrePleinDroit")
                await Codes.create(user = personne , number = numero)
                return{
                    "status":201,
                    "infos":"Bienvenue "+name,
                    "code":numero
                }
            elif type == "Gerant":
                personne = await Personne.create(name = name , prenom = prenom , pays = pays , ville = ville ,email = email , numero = numero , motPasse = password , type = "MembrePleinDroit")
                await Codes.create(user = personne , number = numero)
                await Gerant.create(user = personne)
                return{
                    "status":201,
                    "infos":"Bienvenue "+name,
                    "code":numero
                }
        else:
            raise HTTPException(status_code=406 , detail='votre adresse email es incorrect')
  
  
#====================================VERIFIER LE CODE=============================      

@router.post('/verifycode' , tags=['Verify code'])
async def verifyCode(code : VerifyCode):
    email = code.email
    code = code.code
    if await checkEmail(email) == True:
        user = await Personne.get(email = email)
        codes = await Codes.get(user = user)
        numero = codes.number
        if numero == code:
            await Personne.filter(email = email).update(actif = True)
            # pensez a supprimer le code
            return {'status':f'Votre code es correct Bienvenue {email}'}
        else:
            return {'status':'Votre code es incorrect merci de verifier'}
    else:
        raise HTTPException(status_code= 406 , detail= "Cette adresse email n'existe pas déjà")    
        
    
#=================================LOGIN============================================

@router.post("/login" , tags=['Login'])
async def login(users:LoginModel):
    email = users.email
    password = users.password
    if await checkEmail(email) == False:
        raise HTTPException(status_code= 406 , detail= 'Cette adresse email est incorrect')    
    else:
        if await emailIsExist(email) == True:
            user = await Personne.get(email = email)
            actif = user.actif
            if actif == True:
                if verify_password(password , user.motPasse) == True:
                    token = await createToken(user.id)
                    return {'status':200 , 'token':token}
                else:
                    raise HTTPException(detail='mot de passe incorrect' , status_code=404)
            else:
                raise HTTPException(detail="Vote compte n'est pas activé" , status_code=404)
            
        else:
            raise HTTPException(status_code=404 , detail='Adresse email introuvable')
        

#==============================VERIFIER LE TOKEN===================

@router.post('/verify_token' , tags=['verify token'])    
async def verifyToken(token : str = Header()):
    decode = await decodeAndVerify(token)
    if decode:
        return {'status':200}
    else:
        raise HTTPException(detail='invalid token' , status_code=404)


#=================================CREATION DE COMPTE===================

@router.post('/add_account_ambassadeur' , tags=["Crediter un compte Ambassadeurs"])
async def saveAmbassadeur(modeles:AmbassadeursSchema , token: str = Header()):
    decode = await decodeAndVerify(token)
    print("decode = ",decode)
    
    if await isGerant(decode) == True:
        cotisation = modeles.cotisation
        email = modeles.email
        if await emailIsExist(email) == True:
            users = await Personne.get(email = email)
            print(users.type)
            if users == None:
                return {'responses':'user not exist'}
            else:
                if users.type == "Ambassadeur":
                    if cotisation < 1:
                        raise HTTPException(status_code=401 , detail="impossible d'effectuer cette operation")
                    else:
                        await Ambassadeurs.create(user = users , cotisation = cotisation)
                    return {"status":201}
                else:
                    raise HTTPException(status_code=401 , detail="utilisateur non conforme")
        else:
            raise HTTPException(status_code=404 , detail="Adresse email introuvable")
    

@router.post('/add_account_partenaire' , tags=["Crediter un compte partenaiire"])
async def savePartenaire(modeles:PartenairesSchema , token: str = Header()):
    decode = await decodeAndVerify(token)
    print("decode = ",decode)
    
    if await isGerant(decode) == True:
        cotisation = modeles.cotisation
        email = modeles.email
        type = modeles.type
        if await emailIsExist(email) == True:
            users = await Personne.get(email = email)
            print(users)
            if users == None:
                return {'responses':'user not exist'}
            else:
                if users.type == "Partenaire":
                    if cotisation < 1:
                        raise HTTPException(status_code=401 , detail="impossible d'effectuer cette operation")
                    else:
                        await Partenaires.create(user = users , cotisation = cotisation , type = type)
                    return {"status":201}
                else:
                    raise HTTPException(status_code=401 , detail="utilisateur non conforme")
        else:
            raise HTTPException(status_code=404 , detail="Adresse email introuvable")

             

@router.post('/add_member_Mouvement' , tags=["Crediter un compte du mouvement"])
async def saveMouvement(modeles:MouvementsSchema, token: str = Header()):
    decode = await decodeAndVerify(token)
    print("decode = ",decode)
    
    if await isGerant(decode) == True:
        cotisation = modeles.cotisation
        email = modeles.email
        nombre_action = modeles.nombre_action
        reste = modeles.reste
        if await emailIsExist(email) == True:
            users = await Personne.get(email = email)
            print(users)
            if users == None:
                return {'responses':'user not exist'}
            else:
                if users.type == "Mouvement":
                    if nombre_action < 1 and cotisation < 1:
                        raise HTTPException(status_code=401 , detail="impossible d'effectuer cette operation")
                    else:
                        if reste > 0:
                            await Mouvements.create(user = users , cotisation = cotisation , nombre_action = nombre_action , reste = reste)
                        else:
                            await Mouvements.create(user = users , cotisation = cotisation , nombre_action = nombre_action)
                    return {"status":201}
                else:
                    raise HTTPException(status_code=401 , detail="utilisateur non conforme")
                    
        else:
            raise HTTPException(status_code=404 , detail="Adresse email introuvable")       


@router.post('/add_Actionnaire' , tags=["Crediter un compte Actionnaire"])
async def saveActionnaire(modeles:ActionnairesSchema , token: str = Header()):
    decode = await decodeAndVerify(token)
    print("decode = ",decode)
    
    if await isGerant(decode) == True:
        nombre_action = modeles.nombre_action
        email = modeles.email
        benefices = modeles.benefice
        if await emailIsExist(email) == True:
            users = await Personne.get(email = email)
            print(users)
            if users == None:
                return {'responses':'user not exist'}
            else:
                if users.type == "Actionnaire":
                    if nombre_action < 1:
                        raise HTTPException(status_code=401 , detail="impossible d'effectuer cette operation")
                    else:
                        await Actionnaires.create(user = users , nombre_action = nombre_action , benefices = benefices)
                    return {"status":201}
                else:
                    raise HTTPException(status_code=401 , detail="utilisateur non conforme")

        else:
            raise HTTPException(status_code=404 , detail="Adresse email introuvable")
  
      
      

@router.post('/add_account_MembrePleinDroit' , tags=["Crediter un compte MembrePleinDroit"])
async def saveMembrePleinDroit(modeles:membrePleinDroitSchema , token: str = Header()):
    decode = await decodeAndVerify(token)
    print("decode = ",decode)
    
    if await isGerant(decode) == True:
        cotisation = modeles.cotisation
        email = modeles.email
        type = modeles.type
        if await emailIsExist(email) == True:
            users = await Personne.get(email = email)
            print(users)
            if users == None:
                return {'responses':'user not exist'}
            else:
                if users.type == "MembrePleinDroit":
                    if cotisation < 1:
                        raise HTTPException(status_code=401 , detail="impossible d'effectuer cette operation")
                    else:
                        await MembrePleinDroit.create(user = users , cotisation = cotisation , type = type)
                    return {"status":201}
                else:
                    raise HTTPException(status_code=401 , detail="utilisateur non conforme")
        else:
            raise HTTPException(status_code=404 , detail="Adresse email introuvable")


"""==========================RECUPERE AVEC PAR TYPE====================="""

@router.get('/take_all_user_by_type' , tags=["recupere les utilisateurs en fonction du type"])
async def get_user_by(type:str):
    user = await Personne.filter(type = type)
    data = []
    for i in user:
        data.append(
            {
                "name" : i.name,
                "email" : i.email,
                "pays" : i.pays,
                "ville" : i.ville,
                "type" : i.type
            }
        )
    return data

# =====================================RECUPERER LES UTILISATEURS===================

             
@router.get('/get_membre_plein_droit' , tags=["recuperer les membres plein droit"])
async def get_users(page:int, page_size:int):
    data = []
    users = await MembrePleinDroit.all().order_by("-date").limit(page_size).offset((page - 1) * page_size)
    print("users = ",users)
    
    for i in users:
        personne = await i.user.get()
        data.append(
            {
                "name" : personne.name,
                "email": personne.email,
                "pays" : personne.pays,
                "ville" : personne.ville,
                "numero" : personne.numero,
                "cotisation" : i.cotisation,
                "type" : i.type,
                "date" : i.date
            }
        )
    return data  
   


@router.get('/get_ambassadeur' , tags=["recuperer les Ambassadeurs"])
async def get_users(page:int, page_size:int):
    data = []
    users = await Ambassadeurs.all().order_by("-date").limit(page_size).offset((page - 1) * page_size)
    print("users = ",users)
    
    for i in users:
        personne = await i.user.get()
        data.append(
            {
                "name" : personne.name,
                "email": personne.email,
                "pays" : personne.pays,
                "ville" : personne.ville,
                "numero" : personne.numero,
                "cotisation" : i.cotisation,
                "date" : i.date
            }
        )
    return data   

   
   
@router.get('/get_partenaire' , tags=["recuperer les Partenaires"])
async def get_users(page:int, page_size:int):
    data = []
    users = await Partenaires.all().order_by("-date").limit(page_size).offset((page - 1) * page_size)
    print("users = ",users)
    
    for i in users:
        personne = await i.user.get()
        data.append(
            {
                "name" : personne.name,
                "email": personne.email,
                "pays" : personne.pays,
                "ville" : personne.ville,
                "numero" : personne.numero,
                "cotisation" : i.cotisation,
                "type": i.type,
                "date" : i.date
            }
        )
    return data   

   
   
@router.get('/get_actionnaire' , tags=["recuperer les Actionnaires"])
async def get_users(page:int, page_size:int):
    data = []
    users = await Actionnaires.all().order_by("-date").limit(page_size).offset((page - 1) * page_size)
    print("users = ",users)
    
    for i in users:
        personne = await i.user.get()
        data.append(
            {
                "name" : personne.name,
                "email": personne.email,
                "pays" : personne.pays,
                "ville" : personne.ville,
                "numero" : personne.numero,
                "cotisation" : i.cotisation,
                "nombre_action": i.nombre_action,
                "date" : i.date
            }
        )
    return data      


   
   
@router.get('/get_partenaire' , tags=["recuperer les membres du mouvement"])
async def get_users(page:int, page_size:int):
    data = []
    users = await Mouvements.all().order_by("-date").limit(page_size).offset((page - 1) * page_size)
    print("users = ",users)
    
    for i in users:
        personne = await i.user.get()
        data.append(
            {
                "name" : personne.name,
                "email": personne.email,
                "pays" : personne.pays,
                "ville" : personne.ville,
                "numero" : personne.numero,
                "cotisation" : i.cotisation,
                "nombre_action": i.nombre_action,
                "reste": i.reste,
                "date" : i.date
            }
        )
    return data    


#=============================UPdate password=========

@router.post('/update-password' , tags=["Modifier le mot de passe"])
async def updatePassword_users(updatePassword:UpdatePasswordSchema):
    email = updatePassword.email
    old = updatePassword.old
    password = updatePassword.password1
    
    if await checkEmail(email) == False:
        raise HTTPException(status_code= 406 , detail= 'Cette adresse email est incorrect')    
    else:
        if await emailIsExist(email) == True:
            user = await Personne.get(email = email)
            actif = user.actif
            if actif == True:
                if verify_password(old , user.motPasse) == True:
                    password = get_password_hash(password)
                    user.motPasse = password
                    user.save()
                    return {'status':200 }
                else:
                    raise HTTPException(detail='Ancien mot de passe incorrect' , status_code=404)
            else:
                raise HTTPException(detail="Vote compte n'est pas activé" , status_code=404)
            
        else:
            raise HTTPException(status_code=404 , detail='Adresse email introuvable')
        
