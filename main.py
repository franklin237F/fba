from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import router as rout
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

description = """
FBA EMPIRE API 🚀

## Routes Lists

### /create-account

Pour la creation de compte **Mouvement , Partenaire , Actionnaire , Membre plein droit**.

### /verifycode

Pour verifier le code envoyer par email a l'utilisateur **L'email sera envoyer sur le frontend**
"""

app = FastAPI(
    title = 'FBA Empire API DOCUMENTATION',
    version="1.0.0",
    description=description,
    )


app.include_router(rout)






origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)