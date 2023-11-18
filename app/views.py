from django.shortcuts import render

# Create your views here.
def index(request):
    context ={
         'nama' : 'stefan daeli'
    }
    return render(request,'index.html', context)
