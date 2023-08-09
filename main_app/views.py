from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse

import requests
import json
import uuid
import os
import boto3
import math

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView

from django.urls import reverse_lazy, reverse
from .models import Profile, Comment, Photo

from .forms import ProfileForm

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin 


# ---------------- Home ----------------------------


def home(request):
  return render(request, 'home.html')


def about(request):
  return render(request, 'about.html')


@login_required
def profile(request):
  try:
    profile = Profile.objects.get(user=request.user)
    context = {'profile': profile}
    if profile:
        profile_form = ProfileForm(instance=profile)
        comments = Comment.objects.filter(user=request.user)
        context['profile_form']=profile_form
        context['comments']=comments
    return render(request, 'user/profile.html', context)
  except Profile.DoesNotExist:
    return redirect('create_profile')


# ---------------- Sign-Up ------------------------


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('create_profile')
    else:
      error_message = 'Invalid sign up - try again!'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


#-------------Create Profile----------------


class ProfileCreate(CreateView):
  model = Profile
  template_name = 'user/create_profile.html'
  fields = ['age', 'gender', 'location', 'is_couch_potato', 'favorites', 'latitude', 'longitude', 'is_active']
  success_url = reverse_lazy('profile')  # Replace 'profile-detail' with your actual URL pattern

  def form_valid(self, form):
      print('form_valid being executed')
      form.instance.user = self.request.user
      print(form)
      return super().form_valid(form)


# -------------------- Matching Functions -------------------------------


class ActivityUpdate(UpdateView):
  model = Profile
  template_name = 'user/update_activity.html'
  fields = ['is_couch_potato', 'chosen_activities']
  success_url = reverse_lazy('match')

  def form_valid(self, form):
      print('form_valid being executed')
      form.instance.user = self.request.user
      return super().form_valid(form)
  
  def get_success_url(self):
        return reverse('match')


# Load The Matching Page
@login_required
def match(request):
  ip = requests.get('https://api.ipify.org?format=json')
  ip_data = json.loads(ip.text)
  res = requests.get('http://ip-api.com/json/'+ip_data["ip"]) #get a json
  location_data_one = res.text #convert JSON to python dictionary
  location_data = json.loads(location_data_one) #loading location data one
  if request.method == 'POST':
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    profile = Profile.objects.get(user=request.user)
    profile.latitude = latitude
    profile.longitude = longitude
    profile.save()
    return HttpResponse(status=200)
  profile = Profile.objects.get(user=request.user)
  context = {'data': location_data, 'ip': ip_data, 'profile': profile }
  return render(request, 'user/match.html', context)


class ActivityUpdate(UpdateView):
  model = Profile
  template_name = 'user/update_activity.html'
  fields = ['is_couch_potato', 'chosen_activities']
  success_url = reverse_lazy('match')

  def form_valid(self, form):
      print('form_valid being executed')
      form.instance.user = self.request.user
      return super().form_valid(form)
  
  def get_success_url(self):
        return reverse('match')


#Formula for the Haversine Distance
def haversine(lat1, lon1, lat2, lon2):
  R = 6371
  dist_lat = math.radians(lat2 - lat1)
  dist_lon = math.radians(lon2 - lon1)
  a = math.sin(dist_lat / 2) * math.sin(dist_lat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dist_lon / 2) * math.sin(dist_lon / 2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
  distance = R*c
  return distance

# Retrieve User latitude and longitude info and Database info and check haversine distance for a 
# certain criteria (is_active, chosen_activities, maximum distance from user)
def calculate_distance(request, profile_id):
  user_profile = Profile.objects.filter(id=profile_id)
  user_latitude = user_profile.latitude
  user_longitude = user_profile.longitude
  user_chosen_activities = user_profile.chosen_activities #needs to be a comma-separated list

  # Filter profiles
  active_profiles = Profile.objects.filter(is_active=True, chosen_activities__in=user_chosen_activities).exclude(id=profile_id)

  nearby_profiles = []
  
  #Check if haversine distance is within a range (5.0km)
  for profile in active_profiles:
    distance = haversine(user_latitude, user_longitude, profile.latitude, profile.longitude)
    if distance < 5.0:
      nearby_profiles.append(profile)

  return render(request, 'match.html', {'nearby_profiles': nearby_profiles})


# ---------------- Update Profile ------------------------
class ProfileUpdate(UpdateView):
  model = Profile
  template_name = 'user/update_profile.html'
  fields = ['gender', 'age', 'location', 'favorites', 'is_active']

  success_url = reverse_lazy('profile')

  def form_valid(self, form):
      print('form_valid being executed')
      form.instance.user = self.request.user
      return super().form_valid(form)
  
  def get_success_url(self):
        return reverse('profile')


# ---------------Comment Section --------------------


class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'user/profile.html'
    context_object_name = 'comments'
    ordering = ['-created_at']
    # Filter comments for the current user
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.get_queryset()
        return context  


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'user/create_comment.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
        
class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'user/edit_comment.html'
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

      
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'user/delete_comment.html'
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    

@login_required
def add_photo(request, user_id):
  photo_file = request.FILES.get('photo_file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, user_id=user_id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
  return redirect('profile')