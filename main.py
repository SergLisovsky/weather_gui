import tkinter as tk
import customtkinter as ctk
import datetime
import locale
from PIL import Image
import requests
from tkinter import messagebox

API_KEY = '9b74b5d8b3971a9c41c5aee20dbafcb8'
API_URL = 'https://api.openweathermap.org/data/2.5/weather'
UNITS = 'metric'
LANG = 'uk'
# FILE_EXCEL = 'data.xlsx'

root = ctk.CTk()
root.title('Weather App')
root.iconphoto(False, tk.PhotoImage(file="weather_icon.png"))
root.geometry("800x500+700+300")
root.resizable(False, False)
root.configure(fg_color="#fb8c00")


def get_date_time(ts, timezone, dt_format="%H:%M:%S"):
    tz = datetime.timezone(datetime.timedelta(seconds=timezone))
    return datetime.datetime.fromtimestamp(ts, tz=tz).strftime(dt_format)


def get_weather(event=""):
    params = {
        "appid": API_KEY,
        "units": UNITS,
        "lang": LANG,
        "q": search_entry.get()
    }
    try:
        r = requests.get(API_URL, params=params)
        weather = r.json()
        print_weather(weather)
    except:
        print_weather({"cod": 0, "message": "Не вдалося отримати дані"})


def print_weather(data):
    search_entry.delete(0, "end")
    if data['cod'] != 200:
        messagebox.showerror("Помилка", data['message'].ljust(50))
        content_frame.pack_forget()
        start_content_frame.pack(fill="both", expand=True)
        city_label.configure(text="")
    else:
        start_content_frame.pack_forget()
        content_frame.pack(fill="both", expand=True)
        city = f"{data['name']}, {data['sys']['country']}"
        city_label.configure(text=city)
        city_cnt_label.configure(text=city)
        temp_label.configure(text=f"{data['main']['temp']} °С")
        sunrise_time = get_date_time(data['sys']['sunrise'], data['timezone'])
        sunset_time = get_date_time(data['sys']['sunset'], data['timezone'])
        data_text = f"""Розташування: {city}
Температура: {data['main']['temp']} °С
Атм. тиск: {data['main']['pressure']} гПа
Вологість: {data['main']['humidity']}%
Швидкість вітру: {data['wind']['speed']} м/с
Погодні умови: {data['weather'][0]['description']}
Схід сонця: {sunrise_time}
Захід сонця: {sunset_time}"""
        data_textbox.configure(state="normal")
        data_textbox.delete("0.0", "end")
        data_textbox.insert("1.0", data_text)
        data_textbox.configure(state="disabled")



top_frame = ctk.CTkFrame(root, width=800, height=50, fg_color="#212121", corner_radius=0)
top_frame.pack(fill="x")

city_font = ctk.CTkFont(size=15)
city_label = ctk.CTkLabel(top_frame, text="", text_color="#fff", font=city_font)
city_label.place(x=20, y=10)

search_entry = ctk.CTkEntry(top_frame, placeholder_text="Введіть місто...")
search_entry.place(x=520, y=10)

search_btn = ctk.CTkButton(top_frame, text="Пошук", width=100, command=get_weather)
search_btn.place(x=670, y=10)

search_entry.bind("<Return>", get_weather)

start_content_frame = ctk.CTkFrame(root, corner_radius=0, fg_color="#fb8c00")
start_content_frame.pack(fill="both", expand=True)

welcome_font = ctk.CTkFont(size=30)
welcome_label = ctk.CTkLabel(start_content_frame, text="Ласкаво просимо до програми показу погоди", text_color="#fff", font=welcome_font)
welcome_label.place(relx=0.5, rely=0.5, anchor="center")

content_frame = ctk.CTkFrame(root, corner_radius=0, fg_color="#fb8c00")
# content_frame.pack(fill="both", expand=True)

locale.setlocale(locale.LC_TIME, "uk")
curr_date = datetime.datetime.now().strftime("%a, %B %d")
date_font = ctk.CTkFont(size=20)
date_label = ctk.CTkLabel(content_frame, text=curr_date, text_color="#fff", font=date_font)
date_label.place(relx=0.5, y=30, anchor="center")

city_cnt_label = ctk.CTkLabel(content_frame, text="Назва міста", text_color="#fff", font=date_font)
city_cnt_label.place(relx=0.5, y=60, anchor="center")

weather_icon = ctk.CTkImage(light_image=Image.open("weather_icon.png"), size=(150, 150))
weather_icon_label = ctk.CTkLabel(content_frame, text="", image=weather_icon)
weather_icon_label.place(x=30, y=120)

temp_font = ctk.CTkFont(size=50)
temp_label = ctk.CTkLabel(content_frame, text="25 °С", text_color="#fff", font=temp_font)
temp_label.place(x=200, y=150)

data_textbox_font = ctk.CTkFont(size=15, weight="bold")
data_textbox = ctk.CTkTextbox(content_frame, fg_color="#e65100", text_color="#fff", width=300, height=250,
                              font=data_textbox_font, spacing3=5, wrap="word", activate_scrollbars=False)
data_textbox.place(x=450, y=150)

# data_textbox.insert("0.0", data_text)
data_textbox.configure(state="disabled")
root.mainloop()

