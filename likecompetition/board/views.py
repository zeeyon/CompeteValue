from django.shortcuts import render

def result(request):
    return render(request, 'result.html')
