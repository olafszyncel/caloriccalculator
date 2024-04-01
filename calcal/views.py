from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

from .models import User, Profile, Breakfast, Lunch, Dinner

import datetime, json, requests



def index(request):
    return render(request, "calcal/index.html")
        
def profile(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == "POST":
        weight = float(request.POST["weight"])
        tall = int(request.POST["tall"])
        birth = int(request.POST["birth"])
        gender = request.POST["gender"]
        act = int(request.POST["activity"])
        match act:
            case 1:
                activity = 1.2
            case 2:
                activity = 1.4
            case 3:
                activity = 1.6
            case 4: 
                activity = 1.8
            case 5:
                activity = 2.0
            case 6:
                activity = 2.2
            case 7:
                activity = 2.4

        rate = request.POST["rate"]
        goal_weight = request.POST["gw"]

        year = int(datetime.date.today().year)
        age = year - birth
        if gender == "Female":
            caloric = int(665 + (9.56 * weight) + (1.85 * tall) - (4.67 * age)) * activity
        elif gender == "Male":
            caloric = int(66 + (13.75 * weight) + (5 * tall) - (6.75 * age)) * activity
        if goal_weight != "maintain":
            goal_weight = int(goal_weight)

        if goal_weight > weight:
            caloric = caloric + (7700 * int(rate)/1000) / (1000 * 7)
        else:
            caloric = caloric - (7700 * int(rate)/1000) / (1000 * 7)
        try:
            profile = Profile.objects.get(user=user)
            profile.weight = weight
            profile.tall = tall
            profile.year_birth = str(birth)
            profile.activity_lvl = act
            profile.gender = gender
            profile.goal_weight = goal_weight
            profile.rate = rate
            profile.caloric = caloric
        except:
            profile = Profile(
                user = user,
                weight = weight,
                tall = tall,
                year_birth = str(birth),
                activity_lvl =act,
                gender = gender,
                goal_weight = goal_weight,
                rate = rate,
                caloric = caloric
            )
        profile.save()
        return render(request, "calcal/profile.html", {
            "profile": profile,
            "message": "Successfully save you profile details!"
        })

    
    try:
        profile = Profile.objects.get(user=user)
    except:
        profile = None
    return render(request, "calcal/profile.html", {
        "profile": profile,
    })

def menu(request):
    if request.method == 'POST':
        query = request.POST["query"]
        gram = request.POST["amount"]
        meal = request.POST["meal"]
        day = request.POST["single-day"]
        day = day[-1:]
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        response = requests.get(api_url, headers={'X-Api-Key': '2o5Ie9y6Nn10L3cr3Tmbbg==IZ9m4PN7njKspjwh'})
        try:
            api = json.loads(response.content)
            user = User.objects.get(pk=request.user.id)
            match meal:
                case "Breakfast":
                     breakfast = Breakfast(
                        user = user,
                        product = api[0]["name"],
                        product_weight = gram,
                        caloric = round(api[0]["calories"]),
                        fat = round(api[0]["fat_total_g"]),
                        carbs = round(api[0]["carbohydrates_total_g"]),
                        protein = round(api[0]["protein_g"]),
                        day = day
                     )
                     breakfast.save()
                case "Lunch":
                    lunch = Lunch(
                        user = user,
                        product = api[0]["name"],
                        product_weight = gram,
                        caloric = round(api[0]["calories"]),
                        fat = round(api[0]["fat_total_g"]),
                        carbs = round(api[0]["carbohydrates_total_g"]),
                        protein = round(api[0]["protein_g"]),
                        day = day
                     )
                    lunch.save()
                case "Dinner":
                    dinner = Dinner(
                        user = user,
                        product = api[0]["name"],
                        product_weight = gram,
                        caloric = round(api[0]["calories"]),
                        fat = round(api[0]["fat_total_g"]),
                        carbs = round(api[0]["carbohydrates_total_g"]),
                        protein = round(api[0]["protein_g"]),
                        day = day
                     )
                    dinner.save()
        except Exception as e:
            api = "Something must go wrong, try again!"
            return render(request, "calcal/menu.html", {
                "message": api
            })
        b = Breakfast.objects.filter(user=user, day=day)
        l= Lunch.objects.filter(user=user, day=day)
        d = Dinner.objects.filter(user=user, day=day)
        return render(request, "calcal/menu.html")
    # method is get
    return render(request, "calcal/menu.html")
    

def weekday(request, day):
    user = User.objects.get(pk=request.user.id)
    b = Breakfast.objects.filter(user=user, day=day)
    l = Lunch.objects.filter(user=user, day=day)
    d = Dinner.objects.filter(user=user, day=day)

    return JsonResponse([
        [breakfast.serialize() for breakfast in b],
        [lunch.serialize() for lunch in l],
        [dinner.serialize() for dinner in d]], safe=False)

def delete_product(request, meal, meal_id):
    match meal:
        case 0:
            p = Breakfast.objects.get(pk=meal_id)
        case 1:
            p = Lunch.objects.get(pk=meal_id)
        case 2:
            p = Dinner.objects.get(pk=meal_id)
    p.delete()
    return HttpResponseRedirect(reverse(menu))

def login_view(request):
    #if user is authenticated redirect to index

    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "calcal/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "calcal/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    #if user is authenticated redirect to index

    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "calcal/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "calcal/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "calcal/register.html")
