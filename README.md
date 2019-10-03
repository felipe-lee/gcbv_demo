# Generic Class-Based Views Demo

Repo to accompany Djangocon 2019 talk, [Generic View? What is that and why would I use it?](https://2019.djangocon.us/talks/generic-view-what-is-that-and-why-would/)

Basically this repo has a sample django project. The website it spins up is just a basic todo site. Honestly the UI is 
not great, and the functionality is...lacking to say the least. Really the purpose of this is to show examples of using 
class-based views (CBVs), and specifically taking advantages of the generic CBVs.

One of the features of this project is that there are CBVs set up to run the entire project and there are function-based
views (FBVs) that contain similar (though not exactly the same) functionality. This makes it so that you can see 
side-by-side (well, top-by-bottom?) examples of both and how you might use generic CBVs to replace some of your FBVs.

## Local Setup
All the commands below assume you have your terminal open and are in the project's root directory.
### Docker
There's a Dockerfile and a docker-compose file set up so you can run this site using docker fairly easily. The 
docker-compose file sets up a postgres container and the settings for this project are set up to point at it. 

#### First Time
1. Run `docker-compose up -d db`
2. Run `docker-compose run --rm django python manage.py migrate`
3. Run `docker-compose up django`


#### After First Time
There are a few different options to how you can run it after you've already set it up.
- Spin up whole project
  ```bash
  docker-compose up
  ```
- Run db first and then django server separately.
  The advantage to this is that you can spin up the server, or jump into the container and not have to think about the 
  db since it'll just be running in the background.
  ```bash
  docker-compose up -d db  
  ```
  - Just launch server
    ```bash
    docker-compose up django
    ```
  - Jump into container
    ```bash
    docker-compose run --rm --service-ports django bash
    ```
    - The service ports bit just makes it so you can run `python manage.py runserver` from within the container and have
    it work properly. If you only plan to run `manage.py` commands and do other things on the command line, then you can
    leave it off.  
  - Run manage.py command
    ```bash
    docker-compose run --rm django python manage.py migrate
    ```
      - Here you can replace `migrate` with any command you need to run.

### Virtual Env
You don't have to use docker, but if you don't, you'll need to edit the settings to point at whatever db you plan to 
use. Simplest would probably be to just use SQLite, like the default settings normally have. 

#### First Time
1. Edit `gcbv_demo/settings.py`, look for the `DATABASES` setting and edit it to whatever you want. You can see the 
django docs for more info: https://docs.djangoproject.com/en/2.2/ref/settings/#databases
2. Set up your virtual environment. For more info see: 
https://tutorial.djangogirls.org/en/django_installation/#virtual-environment
3. Activate the venv (see link above for more info).
4. Run `pip install -r requirements`
5. Run `python manage.py migrate`
6. Run `python manage.py runserver`

#### After First Time
1. Activate your venv.
2. Run `python manage.py runserver`

### Swapping Between CBVs and Function-based Views
The code has been set up to swap between the CBVs and the FBVs. The `settings.py` file has this:
```python
# Use this to trigger using the different view types
VIEW_TYPES = os.environ.get('DJANGO_VIEW_TYPES', 'CBV')
```
What it means is that you can set an environment variable, `DJANGO_VIEW_TYPES` to trigger between CBVs and FBVs. The 
code is set up to default to `CBV`, and if that env var has any other value, it will use FBVs. This is an example of how
the main home page is set up (cut out irrelevant lines):
```python
from common.views import HomeView, home_view

if settings.VIEW_TYPES == 'CBV':
    urlpatterns = [
        path('', HomeView.as_view(), name='home'),
    ]
else:
    urlpatterns = [
        path('', home_view, name='home'),
    ]
```

## Testing
...I...well I didn't write tests for this code... Terrible, I know. Like I pointed out in the beginning of this README,
this repo was more about showing how generic CBVs can be used and comparing them to FBVs. Which, yes, would probably be
very easy to drive home if I set up tests that run on both and work for both, but I just didn't have enough time. Maybe
I'll come back and write them at some point. (We all know that's not happening...)
