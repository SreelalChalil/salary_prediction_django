from django.shortcuts import render
from django.conf import settings
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
    
    value = list(request.POST.values())[1:]
    int_features = [int(x) for x in value]
    result = getPredictions(int_features)
    print(result)
    msg = "Your Salary Will be: " + str(result)
    return render(request, 'index.html', {'result':msg})
