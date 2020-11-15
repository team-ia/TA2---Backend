from flask_marshmallow import Marshmallow

ma = Marshmallow()

class Enfermedad():
    nombre=""
    tipo=""
    
    def __init__(self,nombre,tipo):
        self.nombre=nombre
        self.tipo=tipo
        
    def __repr__(sefl):
        return f'Enfermedad({self.nombre})'
   
    def __str__(self):
        return f'{self.nombre}' 
    
    