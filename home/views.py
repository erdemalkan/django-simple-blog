from django.shortcuts import render, HttpResponse

def home_view(request):

    if request.user.is_authenticated:
        context = {
            'name': request.user
        }
    else:
        context = {
            'name': 'Anonymous User' 
        }
    
    return render(request, 'home.html', context)