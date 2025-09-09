from django.shortcuts import render
from .models import Project
# Create your views here.

def project_list(request):
    try:
        projects = Project.objects.all()
    except Project.DoesNotExist:
        projects = []
    return render(request, 'projects/projects_list.html', {'projects': projects})



def project_detail(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        project = None
    return render(request, 'projects/projects_detial.html', {'project': project})