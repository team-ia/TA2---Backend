
from kanren.constraints import neq
from kanren import run
from kanren import lall
from kanren import facts
from kanren import Relation
from kanren import var
import json
import csv
import time
x = var()
z = var()
recipe_list=[]
cleared_recipe_list=[]
enfermedades_list=[]
tipos_enfermedades_list=[]
enfermedades_ingredientes_list_buenos=[]
enfermedades_ingredientes_list_malos=[]
ingredient_list=[]

#Relations
ingredienteDe = Relation()
buenoPara = Relation()
maloPara = Relation()
platilloTipo = Relation()




def read_recipes_dataset():
    with open('recipes.json') as recipesJson:
      recipes=json.load(recipesJson)
      ## print(recipes,end='\n')
      for item,value in recipes.items():
        recipe_details={"title":None,"ingredients":None,"instructions":None}
        ## print(item,":",value)
        recipe_details['title']=value.get("title","")
        recipe_details['ingredients'] =value.get("ingredients","")
        recipe_details['instructions'] =value.get("instructions","")
        recipe_list.append(recipe_details)
  #  print(recipe_list[0]['ingredients'][0])
  #  print(len(recipe_list))

def read_enfermedades_csv():
    with open('enfermedades.csv') as enfermedadesCsv:
        csv_reader=csv.reader(enfermedadesCsv,delimiter=',')
        line_count=0
        for row in csv_reader:
         enfermedades_details={"nombre":None,"tipo":None}
         if line_count == 0:
            line_count += 1
         else:
            enfermedades_details['nombre']=row[0]
            enfermedades_details['tipo']=row[1]
            enfermedades_list.append(enfermedades_details)
            if row[1] not in tipos_enfermedades_list: tipos_enfermedades_list.append(row[1])
   # print(enfermedades_list)

def read_good_ingredients():
    with open('enfermedades_ingredientes_buenos.csv') as enfermedadesCsv:
        csv_reader=csv.reader(enfermedadesCsv,delimiter=',')
        line_count=0
        for row in csv_reader:
         enfermedades_details={"enfermedad":None,"ingredient":[]}
         if line_count == 0:
            line_count += 1
         else:
            enfermedades_details['enfermedad']=row[0]
            for ingredient in row[1:]:
                if  ingredient:
                    enfermedades_details['ingredient'].append(ingredient)
                    if ingredient.lower() not in ingredient_list: ingredient_list.append(ingredient.lower())
            enfermedades_ingredientes_list_buenos.append(enfermedades_details)
   # print(enfermedades_ingredientes_list_buenos[0])
    #print(ingredient_list)
    
def read_bad_ingredients():   
    with open('enfermedades_ingredientes_malos.csv') as enfermedadesCsv:
     csv_reader=csv.reader(enfermedadesCsv,delimiter=',')
     line_count=0
     for row in csv_reader:
        enfermedades_details={"enfermedad":None,"ingredient":[]}
        if line_count == 0:
            line_count += 1
        else:
            enfermedades_details['enfermedad']=row[0]
            for ingredient in row[1:]:
                if  ingredient:
                    enfermedades_details['ingredient'].append(ingredient)
                    if ingredient.lower() not in ingredient_list: ingredient_list.append(ingredient.lower())
            enfermedades_ingredientes_list_malos.append(enfermedades_details)
   # print(enfermedades_ingredientes_list_buenos[0])
    #print(ingredient_list)


def clear_data():
    for recipe_detail in recipe_list:
        cleared_recipe_list_detail={"title":None,"ingredients":[],"instructions":None}
        cleared_recipe_list_detail['title']=recipe_detail['title']
        cleared_recipe_list_detail['instructions']=recipe_detail['instructions']
        for ingredient1 in recipe_detail['ingredients']:
            for ingredient2 in ingredient_list:
            #    print(ingredient1 + "------>" + ingredient2)
                if ingredient2.lower() in ingredient1.lower() and ingredient2!="teaspoon":
               ## print(ingredient1.find(ingredient2))
              ##  print(ingredient1 + "------>" + ingredient2)
                 cleared_recipe_list_detail['ingredients'].append(ingredient2)
              #  print(cleared_recipe_list_detail)
                 cleared_recipe_list.append(cleared_recipe_list_detail)
    print(len(ingredient_list))
                #time.sleep(2.4)
#print(cleared_recipe_list[0])
#print(cleared_recipe_list[1])
#print(cleared_recipe_list[2])
#print(cleared_recipe_list[3])
                
#facts(platilloTipo, ("Pan al Ajo", "Entrada"), ("Pan al Ajo picante", "Entrada"), ("Pizza", "Plato de Fondo"))
def fact_ingredient_recipe():
    for recipe in cleared_recipe_list:
        for ingredient in recipe['ingredients']:
   #     print(recipe['title'] + "--->" + ingredient.lower())
       #  facts(ingredienteDe, (ingredient.lower(), recipe['title']))
         facts(ingredienteDe, (ingredient.lower(), recipe['title']))

 
##facts(ingredienteDe, ("Ajo", "Pan al Ajo"), ("Aji", "Pan al Ajo picante"),
##("Ajo", "Pan al Ajo picante"), ("Tomate", "Pizza"))
def fact_enfermedad_ingredient_bueno():
    for enfermedad_ingredient in enfermedades_ingredientes_list_buenos:
        for ingredient in enfermedad_ingredient["ingredient"]:
          # print(enfermedad_ingredient["enfermedad"] + "--->" + ingredient.lower())
            facts(buenoPara, (ingredient.lower(),enfermedad_ingredient["enfermedad"]))

def fact_enfermedad_ingredient_malo():
    for enfermedad_ingredient in enfermedades_ingredientes_list_malos:
        for ingredient in enfermedad_ingredient["ingredient"]:
         # print(enfermedad_ingredient["enfermedad"] + "--->" + ingredient.lower())
         facts(maloPara, (ingredient.lower(),enfermedad_ingredient["enfermedad"])) 
    
#facts(buenoPara, ("Ajo", "Faringitis"), ("naranja", "Faringitis"), ("Perejil", "Faringitis"))
#facts(maloPara, ("Aji", "Faringitis"), ("Cafe", "Faringitis"))

def RecomendadoPara(x, y):
    w = var()
    return lall(buenoPara(w, y), ingredienteDe(w, x))

#def RecomendadoPara(x, y, z):
 #   w = var()
 #   return lall(platilloTipo(x, z), buenoPara(w, y), ingredienteDe(w, x))

def NoRecomendadoPara(x, y):
    w = var()
    return lall(maloPara(w, y), ingredienteDe(w, x))


#def NoRecomendadoPara(x, y, z):
 #   w = var()
  #  return lall(platilloTipo(x, z), maloPara(w, y), ingredienteDe(w, x))

def test():
    print(set(run(100, x, RecomendadoPara(x,"Faringitis"))))
    print('\n')
    print('\n')
    print('\n')
    print(set(run(100, x, NoRecomendadoPara(x,"Faringitis"))))
    print('\n')
    print('\n')
    print('\n')
    print('\n')
    print(set(run(100, x, RecomendadoPara(x,"Faringitis")))-set(run(100, x, NoRecomendadoPara(x,"Faringitis"))))
    print(set(run(100, x, RecomendadoPara(x,"Faringitis"))).intersection(set(run(100, x, NoRecomendadoPara(x,"Faringitis")))))

def process_data():
    read_recipes_dataset()
    read_enfermedades_csv()
    read_good_ingredients()
    read_bad_ingredients()
    clear_data()

def fact_definition():
    fact_ingredient_recipe()
    fact_enfermedad_ingredient_bueno()
    fact_enfermedad_ingredient_malo()
#print(set(run(100, x, RecomendadoPara(x,"Faringitis"))))
#print(set(run(100, x, RecomendadoPara(x, "Faringitis", "Entrada"))) -
 #       set(run(100, x, NoRecomendadoPara(x, "Faringitis", "Entrada"))))
def operation(str_list,al_list):
    good_recipes=set()
    bad_recipes=set()
    alergic=set()
    for recipe in str_list:
       good_recipes.update(set(run(100, x, RecomendadoPara(x,recipe))))
       bad_recipes.update(set(run(100, x, NoRecomendadoPara(x,recipe))))
    
    for ingredient in al_list:
       alergic.update(set(run(100,x,lall(ingredienteDe(ingredient,x)))))
        
    result=good_recipes-bad_recipes-alergic    
      #result=(set(run(100, x, RecomendadoPara(x,str)))-set(run(100, x, NoRecomendadoPara(x,str))))
   # print(result)
    return result
 
def mainP():
      process_data()
      fact_definition()
      print("acabe")
     # test()
mainP()
