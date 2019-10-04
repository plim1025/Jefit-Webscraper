# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json

exercise_images = []
exercise_names = []
exercise_info = {}
exercises = {}
exercise_cats = []

h4s = []
ps= [] 

# Iterate through exercise pages
for i in range(39, 131):
    source = requests.get("https://jefit.com/exercises/bodypart.php?page=" + str(i)).text
    soup = BeautifulSoup(source, 'lxml')
    
    h4s = soup.find_all('h4')
    ps = soup.find_all('p')
    img = soup.find_all('img')

    # Webscrape exercises
    a = 0
    for i in h4s:
        h4s[a] = h4s[a].a.text
        exercise_names.append(h4s[a])
        a += 1
        
    for i in ps:
        i = str(i.get_text())
        exercise_cats.append(i)

# Webscrape exercise info
b = 0
for i in exercise_cats:
    if(b+1)%4!=0:
        if(b+1)%4==1:
            exercises["Main Muscle Group"] = i[20:]
        elif(b+1)%4==2:
            exercises["Type"] = i[7:]
        elif(b+1)%4==3:
            exercises["Equipment"] = i[12:]
            exercise_info[exercise_names[(b-2)//4]] = exercises.copy()
    b += 1
        
exercise_info = {'exercise_info' : exercise_info}
with open('exercise_info2.txt', 'w') as f:
    f.write(json.dumps(exercise_info))
    
    # Webscrape exercise images
    c = 0
    for i in img:
        img[c] = 'http://jefit.com/' + img[c]['src'][3:]
        exercise_images.append(img[c])
        c += 1

file_names = []
for i in range(len(exercise_images)):
    file_names.append("exercise_image" + str(i))

j = 1
for item in exercise_images:
    txt = open('%s.jpg' % file_names[j], "wb")
    if "jefit.com/images/exercises/800_600" in item:
        txt.write(requests.get(item).content)
        j += 1
    txt.close()
    