from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # This dictionary is passed to the template engine
    context_dict = {}
    context_dict['welcome'] = "Welcome to Rate My Recipe!"
    
    return render(request, 'rango/index.html', context=context_dict)



def categories(request):
    return HttpResponse("This is the categories page")
