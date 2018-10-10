from django.shortcuts import render, redirect
from .models import Client, Site, Zone, Camera, Event
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import AddCameraForm, AddSiteForm, AddZoneForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.contrib.auth import logout
from django.contrib.auth.views import logout as logout_msg
from django.template import RequestContext



@login_required
def index(request):
    
    return render(request, 'index.html')

def logout_view(request):
    logout_msg(request)
    return render(request, 'index.html', {'data': 'Déconnecté'})

@login_required
def settings(request):
    
    return render(request, 'settings.html') 
   

@login_required
def reports(request):
    

    site_list = Site.objects.filter(client=request.user.id).values('id')
    #zone_list = Zone.objects.filter(site=list(site_list))
    sites = []
    for x in list(site_list):
        sites.append(x['id'])

    zone_list = Zone.objects.filter(site__in=sites).values('id')
    zones = []
    for x in list(zone_list):
        zones.append(x['id'])

    cameras_list = Camera.objects.filter(zone__in=zones).values('id')
    cameras = []
    for x in list(cameras_list):
        cameras.append(x['id'])

    events_list = Event.objects.filter(camera__in=cameras).order_by('-time')

    context = {
        'events' : events_list
            }
    return render(request, 'reports.html', context)  

@login_required
def sites(request):
    site_list = Site.objects.filter(client=request.user.id)
    context = {
        'sites' : site_list
            }
    return render(request, 'sites.html', context)    

@login_required
def zones(request):
    site_list = Site.objects.filter(client=request.user.id).values('id')
    #zone_list = Zone.objects.filter(site=list(site_list))
    sites = []
    for x in list(site_list):
        sites.append(x['id'])

    zone_list = Zone.objects.filter(site__in=sites)
    context = {
        'zones' : zone_list
            }
    return render(request, 'zones.html', context) 

@login_required
def cams(request):
    
    site_list = Site.objects.filter(client=request.user.id).values('id')
    #zone_list = Zone.objects.filter(site=list(site_list))
    sites = []
    for x in list(site_list):
        sites.append(x['id'])

    zone_list = Zone.objects.filter(site__in=sites).values('id')
    zones = []
    for x in list(zone_list):
        zones.append(x['id'])

    cameras_list = Camera.objects.filter(zone__in=zones)


    #place = Camera.objects.get(name='kansas')

    

    context = {
        'cameras' : cameras_list,
    }

    if 'settings' in request.path:
        return render(request, 'cams_settings.html', context)  
    return render(request, 'cams.html', context)  
       



def add_camera(request):
    
 
    if request.method == "POST":
        form = AddCameraForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            return redirect('/ainet/')
        else:

            return render(request, "camera_form.html", {'form': form})
 
    else:
 
        form = AddCameraForm()
        return render(request, "camera_form.html", {'form': form})  


def add_zone(request):
    
 
    if request.method == "POST":
        form = AddZoneForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            return redirect('/ainet/zones')
        else:

            return render(request, "zone_form.html", {'form': form})
 
    else:
 
        form = AddZoneForm()
        return render(request, "zone_form.html", {'form': form})          

def add_site(request):
    current_user = request.user
    current_client = Client.objects.filter(id=current_user.id)

 
    if request.method == "POST":
        form = AddSiteForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.client = current_client[0]
            model_instance.save()
            return redirect('/ainet/sites')
        else:

            return render(request, "site_form.html", {'form': form})
 
    else:
 
        form = AddSiteForm()
        return render(request, "site_form.html", {'form': form})      

 

class DeleteSite(SuccessMessageMixin, DeleteView):
    model = Site
    success_url = '/ainet/sites'
    success_message = "deleted..."

class DeleteZone(SuccessMessageMixin, DeleteView):
    model = Zone
    success_url = '/ainet/zones'
    success_message = "deleted..."    

class DeleteCamera(SuccessMessageMixin, DeleteView):
    model = Camera
    success_url = '/ainet/cams_settings'
    success_message = "deleted..."    

def delete(self, request, *args, **kwargs):
    self.object = self.get_object()
    name = self.object.name
    request.session['name'] = name  # name will be change according to your need
    message = request.session['name'] + ' deleted successfully'
    messages.success(self.request, message)
    return super(DeleteView, self).delete(request, *args, **kwargs)  

class UpdateSite(UpdateView):

    model = Site
    form_class = AddSiteForm
    template_name = 'site_form.html'
    success_url = '/ainet/sites'    

class UpdateZone(UpdateView):

    model = Zone
    form_class = AddZoneForm
    template_name = 'zone_form.html'
    success_url = '/ainet/zones'            

class UpdateCamera(UpdateView):

    model = Camera
    form_class = AddCameraForm
    template_name = 'camera_form.html'
    success_url = '/ainet/cams_settings'               
