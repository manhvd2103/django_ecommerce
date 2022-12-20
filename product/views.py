from django.shortcuts import render
from .models import *

def test_view(request):
    return render(request, "pages/index.html")
