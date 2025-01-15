from django.shortcuts import render

# Create your views here.

#Home_view

def home_view(req):
    return render(req,'home.html')