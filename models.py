from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator



class Personne(Model):

    name = fields.CharField(max_length = 25)
    prenom = fields.CharField(max_length = 25)
    pays = fields.CharField(max_length = 25)
    ville = fields.CharField(max_length = 25)
    email = fields.CharField(max_length = 50)
    numero = fields.CharField(max_length = 30   )
    motPasse = fields.CharField(max_length = 255)
    actif = fields.BooleanField(default = False)
    is_Login = fields.BooleanField(default = False)
    type = fields.CharField(max_length=25)
    date = fields.DatetimeField(auto_now = True)
    
    def __str__(self):
        return self.name
    
    
class Codes(Model):
    user = fields.ForeignKeyField('models.Personne' ,related_name='codes' ,on_delete = fields.CASCADE)
    date = fields.DatetimeField(auto_now = True)
    number = fields.IntField()    


class Ambassadeurs(Model):
    user = fields.ForeignKeyField('models.Personne' ,related_name='ambassadeurs' ,on_delete = fields.CASCADE)
    cotisation = fields.IntField(default = 0)  
    date = fields.DatetimeField(auto_now = True)


class Partenaires(Model):
    user = fields.ForeignKeyField('models.Personne' ,related_name='partenaires' ,on_delete = fields.CASCADE)
    type = fields.CharField(max_length=15)
    cotisation = fields.IntField(default = 0)  
    date = fields.DatetimeField(auto_now = True)


class Mouvements(Model):
    user = fields.ForeignKeyField('models.Personne' ,related_name='mouvements' ,on_delete = fields.CASCADE)
    nombre_action = fields.IntField(default = 0)
    cotisation = fields.IntField(default = 0)
    reste = fields.IntField(default = 0)
    date = fields.DatetimeField(auto_now = True)
    
    
    
class Actionnaires(Model):
    user = fields.ForeignKeyField('models.Personne' ,related_name='actionnaires' ,on_delete = fields.CASCADE)
    nombre_action = fields.IntField(default = 0)
    benefices = fields.IntField(default = 0)
    date = fields.DatetimeField(auto_now = True)



class MembrePleinDroit(Model):
    user = fields.ForeignKeyField('models.Personne' ,related_name='membrePleinDroit' ,on_delete = fields.CASCADE)
    cotisations = fields.IntField(default = 0)
    type = fields.CharField(max_length=15 , default = "new")
    date = fields.DatetimeField(auto_now = True)


class Gerant(Model):
    user = fields.ForeignKeyField('models.Personne' ,related_name='gerant' ,on_delete = fields.CASCADE)
    


Personne_Pydantic = pydantic_model_creator(Personne , name='Personne')
Ambassadeurs_Pydantic = pydantic_model_creator(Ambassadeurs , name='Ambassadeurs')
Partenaires_Pydantic = pydantic_model_creator(Partenaires , name='Partenaires')
Mouvements_Pydantic = pydantic_model_creator(Mouvements , name='Mouvements')
Actionnaires_Pydantic = pydantic_model_creator(Actionnaires , name='Actionnaires')
MembrePleinDroit_Pydantic = pydantic_model_creator(MembrePleinDroit , name='MembrePleinDroit')
Gerant_Pydantic = pydantic_model_creator(Gerant , name='Gerant')



