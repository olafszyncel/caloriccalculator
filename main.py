import math
import sys


howmuch = 0  # global variable, howmuch someone want to lose weigh per week in grams

def main():
    todo = welcome()
    answers = questions(todo)  # list of gender, weight, goal, tall, age, activity
    cal = calories(
        todo, answers[0], answers[1], answers[3], answers[4], answers[5], howmuch
    )
    # telling how many calories someone should eat
    print(f"You should eat {cal} calories")

    # if someone chose losing or gaining weigh we are telling in what time he will do it
    if todo == 1:
        week = time(answers[2], answers[1], howmuch)
        dividerSmall()
        print(f"You will spend {week} losing weight")
    elif todo == 3:
        week = time(answers[2], answers[1], howmuch)
        dividerSmall()
        print(f"You will spend {week} gaining weight")


# function that gets basic information about person, and returns todo
def welcome():
    global howmuch
    dividerBig()
    print("WELCOME IN THE CALORIER APP")
    dividerBig()
    name = input("What's your name? ")
    print(f"Hi, {name}")

    dividerBig()
    print("Tell us, what would you like to do with your weight?")
    print("1.   loose weight")
    print("2.   maintain weight")
    print("3.   increase weight")
    todo = getInteger(3)  # variable which stores what someone want to do (lose/maintain/increase weigh)

    dividerBig()
    # if someone want to lose/gain weigh, function asking user for theoretical
    # goal loosing/gaining weigh in one week, from 1 to 1000 grams
    if todo == 1:
        print("How much weight you would like to lose per week?")
        print(
            "Remember, to lose weight in a healthy way, \nyou should not lose more than 1 kg per week"
        )
        print("enter the weight in grams")
        howmuch = getInteger(1000)
    elif todo == 3:
        print("How much weight would you like to gain per week?")
        print(
            "Remember, to increase your weight in a healthy way, \nyou should not gain more than 1 kg per week"
        )
        print("enter the weight in grams")
        howmuch = getInteger(1000)
    dividerBig()
    return todo


# input function which checking answers, function get number which
# should be maximal accebtable and returns number inputed
def getInteger(n):
    x = 0
    while x < 1 or x > n:
        try:
            x = int(input("your choice -->"))
        except:
            print("Invalid input")
    return x


# function taking answers from user, and returns them
def questions(todo):
    print(
        "To tell you how many calories you should be consuming, \nwe need to ask you a few more questions"
    )
    dividerSmall()
    print("What is your gender?")
    print("1.   Female")
    print("2.   Male")
    gender = getInteger(2)  # variable storing gender of user
    dividerSmall()
    print("How much you weigh in kilograms?")
    weight = getInteger(600)  # variable storing current weigh of user

    # if user in welcome function chose that he/she want to lose/gain weigh, that segment ask for goal weigh
    if todo == 1 or todo == 3:
        dividerSmall()
        print("how much you want to weigh in kilograms?")
        goal = getInteger(140)  # variable storing goal weigh of user
    else:
        goal = weight

    dividerSmall()
    print("How tall are you in centimeters?")
    tall = getInteger(250)  # variable storing tall of user
    dividerSmall()
    print("How old are you?")
    age = getInteger(120)   # variable storing users age
    dividerSmall()
    print("What is your activity level?")
    print("1.   No activity")
    print("2.   Light: exercise 1-3 times per week")
    print("3.   Moderate: exercise 4-5 times per week")
    print("4.   Active: daily exercise")
    print("5.   Very Active: daily intense exercise")
    print("6.   Extra Active: very intense exercise every day")
    activity = getInteger(6)    # variable storing users activity level in 6 point scale
    dividerBig()
    return [gender, weight, goal, tall, age, activity]


# function calculating the amount of calories, that user should eat per day to maintain the goal
# function return this amount
def calories(todo, gender, weight, tall, age, activity, howmuch):
    actConst = [1.2, 1.4, 1.6, 1.8, 2.0, 2.2]   # list of constant variables storing values of activity level
    cal = 0.0 # declaring a variable that stores amount of calories

    # calculating the amount of calories for WOMAN
    if gender == 1:
        cal = 665 + (9.56 * weight) + (1.85 * tall) - (4.67 * age)
    # calculating the amount of calories for MAN
    if gender == 2:
        cal = 66 + (13.75 * weight) + (5 * tall) - (6.75 * age)

    # multiplying the basal metabolism with level of users activity
    cal = cal * actConst[activity - 1]

    # when user chose losing weigh - subtraction calories to achieve the target
    if todo == 1:
        cal = cal - (7700 * howmuch) / (1000 * 7)
    # when user chose gaining weigh - addition calories to achieve the target
    if todo == 3:
        cal = cal + (7700 * howmuch) / (1000 * 7)

    # if calories are less than 800 is high probability that this is not healthy or in programe has an error
    if cal < 800:
        sys.exit("Sorry, an error has occurred :\\ \nContact with us here, is our email: olaf@falseemail.com"
        )

    return round(cal)


# function takes current weigh, goal weigh and how much user want to
# lose/gain weigh per week and returns string of number of weeks
def time(goal, weight, howmuch):
    week = int(abs(math.ceil((weight - goal) * 1000 / howmuch)))    # maybe math.ceil after abs?
    return f"{week} weeks" if week > 1 else f"{week} week"


def dividerBig():
    print("=====================================================================")


def dividerSmall():
    print("---------------------------------------------------------------------")


if __name__ == "__main__":
    main()