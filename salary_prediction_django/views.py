from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

def home(request):    
    return render(request, 'index.html')


# custom method for generating predictions
def getPredictions(int_features):

    import numpy as np
    import pickle
    
    file_path = os.path.join(settings.FILES_DIR, 'model.pkl')
    model = pickle.load(open(file_path, 'rb'))
     
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)
        
    return output
    

def result(request):
    msg=""
    if request.method == 'POST':  
        value = list(request.POST.values())[1:]
        int_features = [int(x) for x in value]
        result = getPredictions(int_features)
        print(result)
        msg = "Your Salary Will be: " + str(result)
    return render(request, 'index.html', {'result':msg})


def trainml(request):
    msg=""
    if request.method == 'POST':
        from salary_prediction_django import train
        x = train.train_model()
        msg = "Successfully Trained Model. Test Result is: "+ str(x)
    return render(request, 'train.html', {'test':msg})


def upload(request):
    context ={}
    if request.method == 'POST':
        uploaded_file = request.FILES['dataset']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name,uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)
