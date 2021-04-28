"""
WSGI config for website project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from sklearn.tree import DecisionTreeClassifier
from django.core.wsgi import get_wsgi_application
import pandas
import random
import easyocr
from django.conf import settings
from sklearn.preprocessing import LabelEncoder
import cv2

pb = LabelEncoder()

tree = DecisionTreeClassifier()

df = pandas.read_csv(settings.STATIC_ROOT / 'Book1.csv')
x_values = df[['fat ', 'protein', 'carbohydrates']]
y_values = df['healthy']
y_values = pb.fit_transform(y_values)
tree.fit(x_values, y_values)
reader = easyocr.Reader(['en'])
def get_predictions(img):
    a = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresholded = cv2.threshold(a,150,255,cv2.THRESH_BINARY)
    n = reader.readtext(thresholded)
    o = [g[1] for g in n]
    for n in o:
        if 'fat' in n.lower():
            if 'saturated' in n.lower():
                o.remove(n)
            elif 'trans' in n.lower():
                o.remove(n)
            elif 'poly'in n.lower():
                o.remove(n)
            elif 'mono'in n.lower():
                o.remove(n)
            else:
                pass
        elif 'carb' in n.lower():
            pass
        elif 'prot' in n.lower():
            pass
        else:
            o.remove(n)
    test=pandas.DataFrame()
    for n in o:
        if 'fat' in n.lower():
            test['fat '] = [n[int(n.find('fat'))+4:int(n.find('fat'))+6]]
        elif 'carb' in n.lower():
            test['carbohydrates'] = [n[int(n.find('carbohydrates'))+14:int(n.find('carbohydrates'))+16]]
        elif 'prot' in n.lower():
            test['protein'] = [n[int(n.find('protein')+8):int(n.find('protein'))+10]]
    iit = True
    while iit:
        try:
            pr = tree.predict(test)
            iit = False
        except ValueError:
            for a in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
                if a in str(test['fat '][0]):
                    test['fat '][0] = random.randint(1,10)
                elif a in str(test['carbohydrates'][0]):
                    test['carbohydrates'][0] = random.randint(1,10)
                elif a in str(test['protein'][0]):
                    test['protein'][0] = random.randint(1,10)
    if pb.inverse_transform(pr)[0]=='healthy':
        return 'Healthy'
    else:
        return 'Not Healthy'


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

application = get_wsgi_application()
