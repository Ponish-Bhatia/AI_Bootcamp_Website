from django.shortcuts import render
from .models import Img
from .forms import ImageUploadUSA, TextFormClass
from django.conf import settings
from django.http import HttpResponse
import cv2
from matplotlib import pyplot as plt
from website.wsgi import get_predictions
from sklearn.tree import DecisionTreeClassifier
import random
import pandas
from sklearn.preprocessing import LabelEncoder

def text(request):
    if request.method=='GET':
        return render(request, 'textinputpredictio.html', {'form':TextFormClass()})
    elif request.method=="POST":
        pb = LabelEncoder()
        tree = DecisionTreeClassifier()
        df = pandas.read_csv(settings.STATIC_ROOT / 'Book1.csv')
        x_values = df[['fat ', 'protein', 'carbohydrates']]
        y_values = df['healthy']
        y_values = pb.fit_transform(y_values)
        tree.fit(x_values, y_values)
        try:
            j = pandas.DataFrame()
            j['protein'] = [request.POST['proteins']]
            j['fat '] = [request.POST['fats']]
            j['carbohydrates'] = [request.POST['carbohydrates']]
            prc = tree.predict(j)
            if pb.inverse_transform(prc)[0]=="not_healthy":
                return render(request, 'predicted.html', {'pr':"Healthy"})
            else:
                return render(request, 'predicted.html', {'pr':"Not Healthy"})
        except ValueError:
            return render(request, 'textinputpredictio.html', {'form':TextFormClass(), 'er':"Insert an integer in all fields."})

def homepage(request):
    return render(request, 'home.html')

def predict(request):
    if request.method=='GET':
        return render(request, 'prediction.html', {'form':ImageUploadUSA})
    elif request.method=="POST":
        x = ImageUploadUSA(request.POST, request.FILES)
        x.save()
        field_name = 'image'
        obj = Img.objects.last()
        field_object =Img._meta.get_field(field_name)
        field_value = field_object.value_from_object(obj)
        y = cv2.imread(str(settings.MEDIA_ROOT / str(field_value.name)))
        prediction = get_predictions(y)
        return render(request, 'predicted.html', {'pr':prediction, 'q':'notext'})

def creditsuser(request):
    return render(request, 'creditsuser.html')

def pagenotfound404(request, exception):
	return render(request, '404o.html')

def servererror500(request):
	return render(request, '500o.html')

def csrftokendjango403(request, exception):
	return render(request, '403o.html')

def badrequest400(request, exception):
	return render(request, '400o.html')
# def caminputpage(request):
#     return render(request, 'o.html')
