# restaurant/views.py
# description: write view functions to handle URL requests for the restaurant app

from django.shortcuts import render, redirect
import time
import random

def main(request):
    
    template_name = 'restaurant/main.html'
    return render(request, template_name)

def order(request):
    template_name = 'restaurant/order.html'
    daily_specials = ["Virginia Ham Motz, 18", "Corn beef Motz, 18", "Sausage & Gravy, 17.50", "Roast Beef Motz, 18", "Italian and American Tuna Motz, 17.50"]
    context = {
          "special": daily_specials[random.randint(0,len(daily_specials)-1)]
    }
    return render(request, template_name, context)

def confirmation(request):
    template_name = 'restaurant/confirmation.html'

    if request.POST:
        print(request.POST)
        special = request.POST.getlist('special', None)
        bread = request.POST.getlist('bread', None)
        meat = request.POST.getlist('meat', None)
        toppings = request.POST.getlist('toppings', None)
        special_instructions = request.POST.get('special_instructions', None)
        items = [special, bread, meat, toppings]
        flatList = []
        print('items', items)
        total = 0
        for i in range(len(items)):
            if items[i] == []:
                continue
            for item in items[i]:
                splitup = item.split(',')
                total += float(splitup[1])
                flatList.append(splitup[0])
        

        t = time.localtime()
        current_timestamp = time.mktime(t)
        four_hours_in_seconds = 4 * 3600
        new_timestamp = current_timestamp - four_hours_in_seconds

        random_minutes = random.randint(30, 60) * 60 # Generate a random number of minutes between 30 and 60
        final_timestamp = new_timestamp + random_minutes # Add the random minutes to the new timestamp
        final_time = time.localtime(final_timestamp)  # Convert the final timestamp back to local time
        final_time_formatted = time.strftime("%I:%M %p", final_time)  # Format the final time into a readable string
        
        context = {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'phone': request.POST['phone'],
            'items': flatList,
            'total': total,
            'delivery_time': final_time_formatted,
            'special_instructions': special_instructions,
        }

    return render(request, template_name, context)

