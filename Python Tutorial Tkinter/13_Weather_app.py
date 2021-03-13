from tkinter import *
import requests
import json

root = Tk()
root.title('Hi')
root.iconbitmap("src//fruit.ico")
root.geometry("500x100")


def zip_():
    api_request = requests.get("https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zip"
                               "Code="+str(zipcode.get())+"&distance=5&API_KEY=E0E44A5B-6868-4141-A81A-F5075E697991")

    try:
        api = json.loads(api_request.content)

        text = str(api[0]["ReportingArea"]) + ", Air Quality: " + str(api[0]["AQI"]) \
               + " (" + str(api[0]["Category"]["Name"]) + ")"

        weather_color = "green"
        if str(api[0]["Category"]["Name"]) == "Good":
            weather_color = "green"
        elif str(api[0]["Category"]["Name"]) == "Moderate":
            weather_color = "#FFFF00"
        elif str(api[0]["Category"]["Name"]) == "Unhealthy for Sensitive Groups":
            weather_color = "#ff9900"
        elif str(api[0]["Category"]["Name"]) == "Unhealthy":
            weather_color = "#FF0000"
        elif str(api[0]["Category"]["Name"]) == "Very Unhealthy":
            weather_color = "#990066"
        elif str(api[0]["Category"]["Name"]) == "Hazardous":
            weather_color = "#660000"

        Label(root, text=text, font=("Helvetica", 15), background=weather_color).grid(row=1, column=0)
        root.configure(background=weather_color)

    except Exception as e:
        print(f"Error: {e}")


zipcode = Entry(root)
zipcode.grid(row=0, column=0, stick=W+E+N+S)

zip_btn = Button(root, text="Look up Zipcode", command=zip_)
zip_btn.grid(row=0, column=1, stick=W+E+N+S)

mainloop()
