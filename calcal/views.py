from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

from .models import User, Profile, Breakfast, Lunch, Dinner

import datetime, json, requests


# render main page
def index(request):
    return render(request, "calcal/index.html")

@login_required(login_url="/login")
def profile(request):
    user = User.objects.get(pk=request.user.id)
    # section that get date from user input and save in the profile class
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

        # function that get current year
        year = int(datetime.date.today().year)
        age = year - birth
        if gender == "Female":
            caloric = int(665 + (9.56 * weight) + (1.85 * tall) - (4.67 * age)) * activity
        elif gender == "Male":
            caloric = int(66 + (13.75 * weight) + (5 * tall) - (6.75 * age)) * activity
        if goal_weight != "maintain":
            goal_weight = int(goal_weight)

        if goal_weight > weight:
            caloric = round(caloric + (7700 * int(rate)/1000) / (1000 * 7))
        else:
            caloric = round(caloric - (7700 * int(rate)/1000) / (1000 * 7))
        
        # if user already has profile just edit them
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
        # if user dont have profile yet, just create them
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

    # if request method is get, render profile html with user data if their exist
    try:
        profile = Profile.objects.get(user=user)
    except:
        profile = None
    return render(request, "calcal/profile.html", {
        "profile": profile,
    })

@login_required(login_url="/login")
def menu(request):
    try:
        user = User.objects.get(pk=request.user.id)
        profile = Profile.objects.get(user=user)
        profile_weight = float(profile.weight)
        # calculate macro needs
        if profile.activity_lvl < 3:
            profile_protein = [round(profile_weight * 0.8), profile_weight]
        else:
            profile_protein = [round(profile_weight * 1.2), profile_weight * 2]
        profile_fat = [round(profile.caloric * 0.25 / 9), round(profile.caloric * 0.3 / 9)]
        profile_carbs = [(profile.caloric - profile_protein[0]*4 - profile_fat[0]*9) / 4, (profile.caloric - profile_protein[1]*4 - profile_fat[1]*9) / 4]
    except:
        # if user wants to go to this section, but dont fill his profile render
        return render(request, "calcal/profile.html", {
        "message": "First, fill your profile details!",
    })
    # add meal to database
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
        except Exception:
            return render(request, "calcal/menu.html", {
                "message": "Something must go wrong, try again!"
            })
        return render(request, "calcal/menu.html", {
            "profile": profile,
            "profile_protein": profile_protein,
            "profile_carbs": profile_carbs,
            "profile_fat": profile_fat
        })
    # if method is get
    return render(request, "calcal/menu.html", {
        "profile": profile,
        "profile_protein": profile_protein,
        "profile_carbs": profile_carbs,
        "profile_fat": profile_fat
    })
    
# function that response data for user single day menu
@login_required(login_url="/login")
def weekday(request, day):
    user = User.objects.get(pk=request.user.id)
    b = Breakfast.objects.filter(user=user, day=day)
    l = Lunch.objects.filter(user=user, day=day)
    d = Dinner.objects.filter(user=user, day=day)

    return JsonResponse([
        [breakfast.serialize() for breakfast in b],
        [lunch.serialize() for lunch in l],
        [dinner.serialize() for dinner in d]], safe=False)

# function delete menu data from data base
@login_required(login_url="/login")
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

# function that creates list of items for shopping
@login_required(login_url="/login")
def shopping(request):
    user = User.objects.get(pk=request.user.id)
    b = Breakfast.objects.filter(user=user)
    l = Lunch.objects.filter(user=user)
    d = Dinner.objects.filter(user=user)
    product_list = {}
    for food in b:
        product = food.product.lower()
        if product in product_list:
            product_list[product] += food.product_weight
        else:
            product_list[product] = food.product_weight
    for food in l:
        product = food.product.lower()
        if product in product_list:
            product_list[product] += food.product_weight
        else:
            product_list[product] = food.product_weight
    for food in d:
        product = food.product.lower()
        if product in product_list:
            product_list[product] += food.product_weight
        else:
            product_list[product] = food.product_weight
    return render(request, "calcal/shopping.html", {
        "list": product_list
    })

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
