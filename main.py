import curses
from curses import wrapper
import json
import requests
import sys
import alerts
import daily
import hourly
import configparser
import argparse




units = {
    'metric':{
        'wind': 'km/h',
        'temperature': '°C'
    },
    'imperial':{
        'wind': 'mi/h',
        'temperature': '°F'
    }
}


parser = argparse.ArgumentParser(description="Meteo: Curses-based weather app for Canadian weather.", formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-p,","--print", action="store_true", help="Prints the weather to the terminal, no curses")
parser.add_argument("--location", type=str, help="Override location in the config file. (if your location includes spaces, use quotations)")
parser.add_argument("--system", type=str, help="override unit system in the config file, (metric, imperial)")
parser.add_argument("--alerts", action="store_true", help="display the alerts screen")
parser.add_argument("--current-conditions", action="store_true", help="display the current conditions screen")
parser.add_argument("--daily", action="store_true", help="display the daily forecast")
parser.add_argument("--hourly", action="store_true", help="display the hourly forecast")


args = parser.parse_args()
def setup():
    global weather_data, parser, args, system, location




    config =  configparser.ConfigParser()

    config.read('config.ini')

    lat = ''
    lon= ''


    if args.location:
        location = args.location
    else:
        location = f"{config['weather']['city']}, {config['weather']['province']}"
        
    if args.system:
        system = args.system
    else:
        system = config['weather']['units']


    try:
        headers = {'User-Agent': 'MyApp/1.0 (your-email@example.com)'}
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": location,
                "format": "json",
                "email": "jmi06@example.com"
            }
        )
        locresponse = response.json()
        # print(f"https://nominatim.openstreetmap.org/search?city={location}&format=json&email=jmi06@example.com")
        # print(locresponse)
        lat = locresponse[0]['lat']
        lon = locresponse[0]['lon']

    except Exception as e:
        print('piss', e)

    try:
        response = requests.get(f"https://weather.gc.ca/api/app/v3/en/Location/{lat},{lon}?type=city")
        weather_data = response.json()
    except Exception as e:
        print("error with getting weather", e)
        sys.exit(1)


def no_tui():
    # CURRENT CONDITIONS
    location = ""
    timestamp = ""
    temperature = "Temp: N/A"
    feels_like = "Feels Like: N/A"
    wind = "Wind: N/A"
    humidity = "Humidity: N/A"
    condition = ""
    sunset = "Sunset: N/A"
    sunrise = "Sunrise: N/A"
    aqhi = "Air Quality: N/A"
    dewpoint = "Dew Point: N/A"
    try:
        location = f"{weather_data[0]['displayName']}, {str(weather_data[0]['observation']['provinceCode']).upper()}"
        timestamp = weather_data[0]['observation']["timeStampText"]
        temperature = f"Temp: {weather_data[0]['observation']["temperature"][system]}{units[system]['temperature']}"
        feels_like = f"Feels Like: {weather_data[0]['observation']["temperature"][system]}{units[system]['temperature']}"
        wind = f"Wind: {weather_data[0]['observation']["windSpeed"][system]}{units[system]['wind']} {weather_data[0]['observation']["windDirection"]}"
        humidity = f"Humidity: {weather_data[0]['observation']["humidity"]}%"
        condition = weather_data[0]['observation']['condition']
        sunset = f"Sunset: {weather_data[0]['riseSet']['set']['time12h']}"
        sunrise = f"Sunrise: {weather_data[0]['riseSet']['rise']['time12h']}"
        aqhi = f"Air Quality: {weather_data[0]['aqhi']['riskText']}"
        dewpoint = f"Dewpoint: {weather_data[0]['observation']["dewpoint"][system]}{units[system]['temperature']}"
    except:
        pass

    def cc():
        print(F"CURRENT CONDITIONS FOR {location}".strip())
        print(condition)
        print(timestamp)
        print(temperature)
        print(feels_like)
        print(wind)
        print(humidity)
        print(sunset)
        print(sunrise)
        print(aqhi)
        print(dewpoint)
    

    def hourly():
        for i in range(0,15):

            pop = weather_data[0]['hourlyFcst']['hourly'][i]["precip"]
            if pop:
                pop = "P.O.P: " + pop + "%"

            string = f"{weather_data[0]['hourlyFcst']['hourly'][i]["time"]}: {weather_data[0]['hourlyFcst']['hourly'][i]["temperature"][system]}{units[system]['temperature']} {weather_data[0]['hourlyFcst']['hourly'][i]["condition"]} {pop}"
            print(string)

    def daily():
        for i in range(0,7):
            string = f"{weather_data[0]['dailyFcst']['daily'][i]["date"]}: {weather_data[0]['dailyFcst']['daily'][i]["temperature"][system]}{units[system]['temperature']} {weather_data[0]['dailyFcst']['daily'][i]['temperatureText']} {weather_data[0]['dailyFcst']['daily'][i]["summary"]}"
            print(string)

    def alerts():
        if 'alerts' not in weather_data[0]['alert']:
            print(F"NO ACTIVE ALERTS IN YOUR REGION")
        else:
            print(F"{len(weather_data[0]['alert']['alerts'])} ACTIVE ALERT(S) IN YOUR REGION")
            print("python3 main.py --alerts FOR MORE INFORMATION")


        return 
    
    if args.current_conditions:
        cc()
    if args.hourly:
        print(F"HOURLY FORECAST FOR {location}")
        hourly()
    if args.daily:
        print(F"DAILY FORECAST FOR {location}")
        daily()
    if args.alerts:
        alerts()

    if args.current_conditions == False and args.hourly == False and args.daily == False and args.alerts == False:
        cc()
        print()
        print(F"HOURLY FORECAST FOR {location}")
        hourly()
        print()
        print(F"DAILY FORECAST FOR {location}")
        daily()
        print()
        alerts()


def main(stdscr):
    global  weather_data, system, location, units, args




    stdscr.clear()



    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK) #white on black
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE) #black on white
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED) #alert


    if args.daily:
        daily(weather_data, stdscr, curses, system, True)
        return
    elif args.alerts:   

        alerts.alerts(weather_data, stdscr, curses, 0, system, True)
        return

    elif args.hourly:

        hourly(weather_data, stdscr, curses, system, True)
        return


    height, width = stdscr.getmaxyx()
    location = ""
    timestamp = ""
    temperature = "Temp: N/A"
    feels_like = "Feels Like: N/A"
    wind = "Wind: N/A"
    humidity = "Humidity: N/A"
    condition = ""
    sunset = "Sunset: N/A"
    sunrise = "Sunrise: N/A"
    aqhi = "Air Quality: N/A"
    dewpoint = "Dew Point: N/A"
    try:
        location = f"{weather_data[0]['displayName']}, {str(weather_data[0]['observation']['provinceCode']).upper()}"
        timestamp = weather_data[0]['observation']["timeStampText"]
        temperature = f"Temp: {weather_data[0]['observation']["temperature"][system]}{units[system]['temperature']}"
        feels_like = f"Feels Like: {weather_data[0]['observation']["temperature"][system]}{units[system]['temperature']}"
        wind = f"Wind: {weather_data[0]['observation']["windSpeed"][system]}{units[system]['wind']} {weather_data[0]['observation']["windDirection"]}"
        humidity = f"Humidity: {weather_data[0]['observation']["humidity"]}%"
        condition = weather_data[0]['observation']['condition']
        sunset = f"Sunset: {weather_data[0]['riseSet']['set']['time12h']}"
        sunrise = f"Sunrise: {weather_data[0]['riseSet']['rise']['time12h']}"
        aqhi = f"Air Quality: {weather_data[0]['aqhi']['riskText']}"
        dewpoint = f"Dewpoint: {weather_data[0]['observation']["dewpoint"][system]}{units[system]['temperature']}"
    except:
        pass

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(0, width//2 - len(location) //2, location )
    stdscr.addstr(1, width//2 - len(timestamp) //2, timestamp )
    stdscr.addstr(3, width//2 - len("Current") //2, "Current" )
    stdscr.addstr(height-3, width-3 - len("-->") //2, "-->" )

    
    
    stdscr.attron(curses.color_pair(1))


    stdscr.addstr(5, width//4 - len(temperature) //2, temperature )

    if condition:
        stdscr.addstr(4, width//2 - len(condition) //2, condition )
        

    if weather_data[0]['observation']["temperature"][system]:
        stdscr.addstr(6, width//4 - len(feels_like) //2, feels_like )
    else:
        stdscr.addstr(6, width//4 - len("Feels Like: N/A") //2, "Feels Like: N/A" )

    if weather_data[0]['observation']["windSpeed"][system] and weather_data[0]['observation']["windDirection"]:
        stdscr.addstr(7, width//4 - len(wind) //2, wind )
    else:
        stdscr.addstr(7, width//4 - len("Wind: N/A") //2, "Wind: N/A" )

    if weather_data[0]['observation']['humidity']:
        stdscr.addstr(8, width//4 - len(humidity) //2, humidity )
    else:
        stdscr.addstr(8, width//4 - len("Humidity: N/A") //2, "Humidity: N/A" )

    stdscr.addstr(6, 3*width//4 - len(sunrise)//2 , sunrise )
    stdscr.addstr(7, 3*width//4 - len(sunset)//2 , sunset )
    

    if 'riskText' in weather_data[0]['aqhi']:
        stdscr.addstr(5, 3*width//4 - len(aqhi)//2 , aqhi )
    else:
        stdscr.addstr(5, 3*width//4 - len("Air Quality: N/A")//2 , "Air Quality: N/A" )


    if weather_data[0]['observation']['dewpoint'][system]:
        stdscr.addstr(8, 3*width//4 - len(dewpoint) //2, dewpoint )
    else:
        stdscr.addstr(8, 3*width//4 - len("dew point: N/A") //2, "Dew Point: N/A" )

    stdscr.attron(curses.color_pair(3))

    if weather_data[0]['alert']:
        stdscr.addstr(10, width//2-len("     ALERT(S) ACTIVE IN YOUR REGION     ")//2,"     ALERT(S) ACTIVE IN YOUR REGION     " )

    stdscr.refresh()
    key = stdscr.getch()

    if key == curses.KEY_RIGHT:
        alerts.alerts(weather_data, stdscr, curses, 0, system)
        return main(stdscr)



if __name__ == "__main__":
    setup()
    if args.print:
        no_tui()
    else:
        wrapper(main)
