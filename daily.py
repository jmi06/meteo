import hourly

def daily(weather_data, stdscr, curses, system, fromArg=False):
    print(weather_data)
    stdscr.clear()
    stdscr.attron(curses.color_pair(2))


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

    height, width = stdscr.getmaxyx()
    location = f"{weather_data[0]['displayName']}, {str(weather_data[0]['observation']['provinceCode']).upper()}"
    
    stdscr.addstr(0, width//2 - len(location) //2, location )
    stdscr.addstr(height-3, width-3 - len("-->") //2, "-->" )
    stdscr.addstr(height-3, 3, "<--" )
    
    stdscr.addstr(3, width//2 - len("Daily") //2, "Daily" )
    stdscr.attron(curses.color_pair(1))
    for i in range(0,7):
        string = f"{weather_data[0]['dailyFcst']['daily'][i]["date"]}: {weather_data[0]['dailyFcst']['daily'][i]["temperature"][system]}{units[system]['temperature']} {weather_data[0]['dailyFcst']['daily'][i]['temperatureText']} {weather_data[0]['dailyFcst']['daily'][i]["summary"]}"
        stdscr.addstr(5+i, width //2 -len(string)//2, string)

    curses.update_lines_cols()

    stdscr.refresh()
    key=stdscr.getch()
    if key == curses.KEY_LEFT and fromArg == False:
        
        hourly.hourly(weather_data, stdscr, curses, system, fromArg=False)

    return
