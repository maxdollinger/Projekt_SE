from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')

def team(request):
    return render(request, 'cms/team.html')

@login_required
def manage_reportings(request):
    return render(request, "manage_reports.html")