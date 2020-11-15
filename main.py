from flask import Flask, request, jsonify , Response
from flask_restful import Resource, Api
import json
from menu import *
app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
    main()
     
def main():
    mainP()


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


@app.route('/tipo_enfermedades',methods=['GET'])
def tipos_enfermedades():
    #x=json.dumps(enfermedades_list)
    #print(len(enfermedades_list))
   # print(enfermedades_list)
    return jsonify( tipos_enfermedades_list)

@app.route('/enfermedades',methods=['POST'])
def enfermedades():
    result=[]
    print("llegue")
    tipo=request.json['tipo']
    for enfermedades in enfermedades_list:
        if enfermedades['tipo']==tipo:result.append(enfermedades['nombre'])
    return jsonify(result)

@app.route('/platillos/<pos>',methods=['POST'])
def platillo(pos):
    result=[]
    #print("llegue")
    enfermedades=list(request.json['enfermedades'])
    alergias=list(request.json['alergias'])
    result=operation(enfermedades,alergias)
    
    recipe_list=[]
    for recipe in result:
        recipe_details={"title":None,"instructions":None}
        recipe_details["title"]=recipe
        recipe_details['instructions']=next(r for r in cleared_recipe_list if r['title']==recipe)['instructions'] 
        recipe_list.append(recipe_details)
        
    #print(len(list(result)))
    resp=list(recipe_list)[int(pos)*10:int(pos)*10+10]
    r=Response(json.dumps(resp),mimetype='application/json')
    return r

@app.route('/ingredients',methods=['GET'])
def ingredientes():
    result=ingredient_list

    return jsonify(result)