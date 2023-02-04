import requests
from datetime import datetime
import webbrowser
import os
from tkinter import *
from tkinter import messagebox

# ENTER YOUR INFO
GENDER = "male"
WEIGHT_KG = 70
HEIGHT_CM = 170
AGE = 26

# CHAT GPT BASED AI
NUTRION_APP_ID = os.environ['NUTRITION_API_ID']
NUTRION_APP_KEY = os.environ['NUTRITION_API_KEY']
NUTRITION_ENDPOINT = " https://trackapi.nutritionix.com/v2/natural/exercise"

SHEETY_POST_URL = "https://api.sheety.co/813216c1c7b89ca2bcd35e1ec6989347/workoutOpenAiChatbasedRecord/workouts"

# using bearer authorization
sheety_bearer_headers = {
    "Authorization": f"Bearer {os.environ['BAERER_AUTHORIZATION']}"

}
# sheety basic authorization
sheety_basic_headers = {
    "Authorization": f"Basic {os.environ['BASIC_AUTHORIZATION']}"
}

nutrition_headers = {
    "x-app-id": NUTRION_APP_ID,
    "x-app-key": NUTRION_APP_KEY,
}
def internet():
    try:
        requests.get(NUTRITION_ENDPOINT)
    except requests.exceptions.ConnectionError:
        messagebox.showinfo(title="No internet Connection", message="Please check your internet connection!!")
        return False
    else:
        return True
def add_data_to_excel_sheet():
    if not internet():
        return
    query = input_entry.get()

    if query:
        nutrition_parameters = {
            "query": query,
            "gender": GENDER,
            "weight_kg": WEIGHT_KG,
            "height_cm": HEIGHT_CM,
            "age": AGE
        }
        exercise_list = []
        exercises = requests.post(NUTRITION_ENDPOINT, json=nutrition_parameters, headers=nutrition_headers).json()['exercises']
        for exercise in exercises:
            exercise_list.append(exercise['name'].title())
            sheety_params = {
                "workout": {
                    "date": datetime.now().strftime("%d/%m/%Y"),
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "exercise": exercise['name'].title(),
                    "duration": exercise['duration_min'],
                    "calories": exercise['nf_calories']
                }
            }
            requests.post(SHEETY_POST_URL, json=sheety_params, headers=sheety_bearer_headers)

        messagebox.showinfo(title="Successfully added", message=f"Your exercise for {' '.join(exercise_list)} has bee added!!")
        input_entry.delete(0, END)
        input_entry.focus()
    else:
        messagebox.showinfo(title="Empty Entry", message="Please fill the entry!")
def open_browser():
    if not internet():
        return
    webbrowser.open(os.environ['URL'], new=1)

############# GUI ##################
window = Tk()
window.title("Work Time")
window.geometry("1200x563+200+100")
window.resizable(False, False)
canvas = Canvas(width=1200, height=563)
canvas.place(x=0, y=0)
img = PhotoImage(file="img.png")
canvas.create_image(600, 280, image=img)
COLOR_1 = "#30babc"
COLOR_2 = "#6fba2a"
COLOR_3 = "#da65b4"
COLOR_4 = "#735a9b"
COLOR_5 = "#97d1ab"

# ENTRY
input_label = Label(text="Tell me what exercise you have done?",  background=COLOR_5, foreground="white", font=("Arial", 22, "bold"))
input_label.place(x=350, y=150)
example_label = Label(text="e.g. (I did 10 hours cycling and 5 minutes push ups)", background=COLOR_5, foreground="white", font=("Arial", 14, "bold"))
example_label.place(x=350, y=185)
input_entry = Entry(width=33, font=("Arial", 22), highlightthickness=2, highlightbackground=COLOR_1, highlightcolor=COLOR_1)
input_entry.place(x=350, y=225)
input_entry.focus()

# BUTTONS
update_button = Button(text="ADD", background=COLOR_2, foreground="white", font=("Arial", 15, "bold"), command=add_data_to_excel_sheet)
update_button.place(x=350, y=290, width=260)
view_button = Button(text="WORKOUT SHEET", background=COLOR_4, foreground="white", font=("Arial", 15, "bold"), command=open_browser)
view_button.place(x=630, y=290, width=260)
window.mainloop()