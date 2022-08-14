from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')

def team(request):
    return render(request, 'cms/team.html')

@login_required
def overview(request):
    return render(request, "overview.html")