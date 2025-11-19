import daily
import alerts
import main
def hourly(weather_data, stdscr, curses, system, fromArg=False):
    stdscr.clear()
    stdscr.attron(curses.color_pair(2))

    height, width = stdscr.getmaxyx()
    location = f"{weather_data[0]['displayName']}, {str(weather_data[0]['observation']['provinceCode']).upper()}"
    


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

    
    stdscr.addstr(0, width//2 - len(location) //2, location )
    



    stdscr.addstr(3, width//2 - len("Hourly") //2, "Hourly" )

    
    stdscr.addstr(height-3, width-3 - len("-->") //2, "-->" )
    stdscr.addstr(height-3, 3, "<--" )
    stdscr.attron(curses.color_pair(1))



    for i in range(0,15):

        pop = weather_data[0]['hourlyFcst']['hourly'][i]["precip"]
        if pop:
            pop = "P.O.P: " + pop + "%"

        string = f"{weather_data[0]['hourlyFcst']['hourly'][i]["time"]}: {weather_data[0]['hourlyFcst']['hourly'][i]["temperature"][system]}{units[system]['temperature']} {weather_data[0]['hourlyFcst']['hourly'][i]["condition"]} {pop}"
        stdscr.addstr(5+i, width //2 -len(string)//2, string)

    curses.update_lines_cols()

    stdscr.refresh()
    key=stdscr.getch()

    if key == curses.KEY_RIGHT and fromArg == False:
        daily.daily(weather_data, stdscr, curses, system)
    if key == curses.KEY_LEFT and fromArg == False and 'alerts' in weather_data[0]['alert']:
        
        alerts.alerts(weather_data, stdscr, curses, 0, system, fromArg=False)

    if key == curses.KEY_LEFT and fromArg == False and 'alerts' not in weather_data[0]['alert']:
        # main.main(stdscr, weather_data)
        return

    return
