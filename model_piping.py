#!/usr/bin/python2

import os
import re
import json

def avoidKeyError(p):
    try:
        return p['name']
    except KeyError:
        return ""

for filename in os.listdir('scraped_jsons'):
    with open('scraped_jsons/' + filename, 'r') as f:
        
        newf = open("processed_jsons/" + filename, "w+")
        for line in f.readlines():
            recipe = json.loads(line)
            ingredients = ""

            for ing in recipe["recipe"]["ingredients"]:
                ingredients += ing + "\n"
            
            stream = os.popen('echo \'' + ingredients + '\' | bin/parse-ingredients.py --model-file /crf-model/20200716_2000-nyt-ingredients-snapshot-2015-461547e.crfmodel')
            output = stream.read()

            parsed_ingredients = json.loads(output)
            ingredient_names = [avoidKeyError(p) for p in parsed_ingredients]

            for i in range(len(ingredient_names)):
            
                s = ingredient_names[i].split()
                l = []
                for w in s:
                    if w[-1] != '.':
                        l.append(w)
                
                ingredient_names[i] = re.sub(r'[^A-Za-z0-9 ]+', '', ' '.join(l))


            recipe["recipe"]["ingredients"] = ingredient_names
            newf.write(json.dumps(recipe) + '\n')
        
        newf.close()

        