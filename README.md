# Project 3 - FitMeIn
## Description
At week nine of the Software Engineering Immersive course at General Assembly, we were challenged to work for seven days as a team for this project. We were requested to architect, design and collaboratively build a full-stack web app using Python and Django.

So here it is, our [FitMeIn](https://fitmein-social-3cd33888ee92.herokuapp.com/) app!

## Working Team
Meet the team: [Angelica Sandrini](https://github.com/gellisun) | [Hannah Curran](https://github.com/hannahcurran) | [James Carter](https://github.com/JamesC215) | [Lucas Neno](https://github.com/casneno)

There was a great synergy from the beginning, we went through the planning all together and decided that we wanted to build a social network for couch potatoes who need some motivation to exercise.

During the planning we also decided that we would be working with a mix of pair/mob programming and solo programming depending on the needs and functionalities.

## Technology Used

<div align="left">
	<code><img width="30" src="https://raw.githubusercontent.com/tomchen/stack-icons/master/logos/html-5.svg" alt="HTML" title="HTML"/></code>
	<code><img width="30" src="https://raw.githubusercontent.com/tomchen/stack-icons/master/logos/css-3.svg" alt="CSS" title="CSS"/></code>
	<code><img width="40" src="https://raw.githubusercontent.com/tomchen/stack-icons/master/logos/bootstrap.svg" alt="Bootstrap" title="Bootstrap"/></code>
	<code><img width="40" src="https://raw.githubusercontent.com/tomchen/stack-icons/master/logos/javascript.svg" alt="JavaScript" title="JavaScript"/></code>
	<code><img width="40" src="https://raw.githubusercontent.com/tomchen/stack-icons/master/logos/python.svg" alt="Python" title="Python"/></code>
  <code><img width="30" src="https://raw.githubusercontent.com/tomchen/stack-icons/master/logos/django.svg" alt="Django" title="Django"/></code>
</div><br>
<div align="left">
	<code><img width="80" src="https://raw.githubusercontent.com/tomchen/stack-icons/master/logos/git.svg" alt="Git" title="Git"/></code>
	<code><img width="40" src="https://raw.githubusercontent.com/tomchen/stack-icons/master/logos/github-icon.svg" alt="GitHub" title="GitHub"/></code>
</div>

## Brief
- Connect to and perform data operations on a PostgreSQL database (the default SQLLite3 database is not acceptable).
- If consuming an API, have at least one data entity (Model) in addition to the built-in User model.
- If not consuming an API, have at least two data entities (Models) in addition to the built-in User model.
- Have full-CRUD data operations across any combination of the app's models (excluding the User model).
- Authenticate users using Django's built-in authentication.
- Implement authorization by restricting access to the Creation, Updating & Deletion of data resources.

## Planning
During the planning phase, we thought about the delegation of tasks across the team, too. [Angelica Sandrini](https://github.com/gellisun) volunteered to be GitHub master, controlling the pull requests from the rest of the team and sorting out merge conflicts as and when they arose. [Lucas Neno](https://github.com/casneno) took charge of the location API, as you will see a bit further down below. [Hannah Curran](https://github.com/hannahcurran) and I worked together on a few functionalities, of which one was the ability to upload and add a profile picture. We all worked on various CSS features, too.
### Brainstorming
We decided to use [lucid.com](https://www.lucidchart.com/pages/) to brainstorm all sorts of ideas using a notes chart/brainstorming pad. We used this for a variety of functions, including the app idea, the name and what functionality we would like it to achieve. Each member of the team contributed, and then we took a vote on our favourite ideas.

![Initial brainstorming on the project](/main_app/static/images/README/Brainstorming.png "Initial brainstorming on the project")
### Wireframe
For the wireframe, again, we used [lucid.com](https://www.lucidchart.com/pages/), where we all contributed to create the mobile-first design as you see below. The idea behind this is self-explanatory - most users of the web browse with their phones, and so we wanted to create our app using mobile-first design.

![Mobile](/main_app/static/images/README/mobile-wireframe.png "Wireframe for mobile")<br>

After we had created the wireframe for the mobile first design, we moved onto the browser page section, where we would ultimately use media queries to achieve the look of this wireframe. You can see screenshots of this, below.

![Web](/main_app/static/images/README/web-wireframe.png "Wireframe for web")
### ERD
Again, we used [lucid.com](https://www.lucidchart.com/pages/) to create the ERD as seen below.

![ERD](/main_app/static/images/README/erd.png "ERD")

## Code Process

I worked a little bit of paired programming with [Angelica Sandrini](https://github.com/gellisun) and we tried to take care of the profile creation. The biggest challenge we faced with this was at first to understand how to make a 1:1 relationship work.
This and the CSS were the bits where I was most involved in, namely on the home/landing pages and also on the login page.

```Python
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
```
### API
Amongst one of the features is the API call of which Lucas was in charge: our program matches two or more users using their GPS/IP location by means of the HTLM5 Geolocation API.  When first prompted, the user provides data on which activities he would like to perform and this information is stored in his profile.  The program then makes a JavaScript call to the API that takes the user's 'latitude' and 'longitude', it then passes on those values through an URL to the back-end which are then parsed and stored in the database.  Finally, a filter is applied to every active profile in the database that has selected similar activities to that of the user, and calculates the distance between these profiles and the user, returning a table of profiles within a certain range that have the same activity interests as our user.

```JavaScript
const displayCoord = document.getElementById("displayCoord")
const latitudeDisplay = document.getElementById("latitude")
const longitudeDisplay = document.getElementById("longitude")

displayCoord.addEventListener("click", getLocation)

function getLocation(event) {
    event.preventDefault()
    console.log('click')
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(success, error);
    } else {
        alert("Geolocation is not available in your browser.");
    }
}

function success(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    console.log('success')
    console.log(latitude)

    window.location.assign(`http://localhost:8000/my_match/${latitude}/${longitude}/`)

}
```
```Python
def haversine(lat1, lon1, lat2, lon2):
  R = 6371
  dist_lat = math.radians(lat2 - lat1)
  dist_lon = math.radians(lon2 - lon1)
  a = math.sin(dist_lat / 2) * math.sin(dist_lat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dist_lon / 2) * math.sin(dist_lon / 2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
  distance = R*c
  return distance

def find_match(request, profile_id):
  profile = Profile.objects.get(id=profile_id)
  user_latitude = profile.latitude
  user_longitude = profile.longitude
  user_chosen_activities = profile.chosen_activities
  active_profiles = Profile.objects.filter(is_active=True, chosen_activities__contains=user_chosen_activities).exclude(id=profile.id)
  matched_profiles = []
  matched_distance = [] 
  #Check if haversine distance is within a range (5.0km)
  for profile in active_profiles:
    distance = haversine(user_latitude, user_longitude, profile.latitude, profile.longitude)  
    if distance < 5000.0:
      matched_profiles.append(profile)
      matched_distance.append(distance)
  print(matched_profiles)
  print(matched_distance)
  return render(request, 'user/my_matches.html', {'profile':profile, 'matched_profiles':matched_profiles, 'matched_distance':matched_distance, 'user_latitude':user_latitude, 'user_longitude':user_longitude})
```

## Challenges
The most time consuming challenge we faced as a team was pulling down from the main remote repo after major changes and functionalities were made. Also, as the functionalities we wanted to implement were different from what we did during class and labs, that meant that we all had to go through a lot of documentation in order to implement them, causing us to use a lot of our time studying.

## Wins
Throughout our group project, we accomplished some important goals as a team. We implemented a few features and have a functioning app. Although there were challenges, we were able to pull through and created a supportive space. By working together and talking openly, we set up a solid start for a great social fitness app!

To work as part of a team who all had a positive attitude despite the challenges.

## Key Learnings
We all can say we learnt a lot about Git and GitHub collaboration, as we found the workflow around this difficult as it was very new to us all.
Additionally, tackling real-world challenges, such as integrating authentication, an API and balancing front-end aesthetics with back-end functionality, enhanced our technical skills in different ways.
Also, using our base knowledge of Django/Python that we learned about in our classroom lessons, but also using documentation from the Internet to allow us to implement features that we have not learned about before.

## Future Improvements
- At the moment there’s a bug with the photo upload (it uploads to all users and once uploaded cannot be changed) and the comments are not linked to the profile for which they are added.
- We would like the app to show all the connections made and improve its social feature.
- We would like it to also be a place where, based on the user's location, fitness events in the area can be suggested.
- We would like to add functionality to also find recipes and eating habits and suggestions to improve the user's health.
- We finally but not lastly would like to improve its style and UI/UX.
