
from hourly import hourly
import main
def alerts(weather_data, stdscr, curses, curr_index, system, fromArg=False):
    height, width = stdscr.getmaxyx()


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

    if 'alerts' in weather_data[0]['alert'] and len(weather_data[0]['alert']['alerts']) > curr_index:
        stdscr.clear()

        # curses.start_color()
        # curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK) #white on black
        # curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE) #black on white
        # curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED) #alert



        curr_alert = weather_data[0]['alert']['alerts'][curr_index]

        title = curr_alert['alertBannerText'].upper()

        stdscr.attron(curses.color_pair(3))


        stdscr.addstr(0, width//2 - len(title)//2, title)
        stdscr.attron(curses.color_pair(1))
  
        stdscr.addstr(1, width//2 - len(f"Issued {curr_alert["issueTimeText"]}")//2, f"Issued {curr_alert["issueTimeText"]}")
        first_location_value = next(iter(curr_alert['refLocs'].values()))
        location_name = first_location_value.get('name', 'Unknown Location')
        stdscr.addstr(2, width//2 - len(location_name)//2, location_name)


        alert_text = curr_alert['text']

        alert_text = alert_text.strip()
        alert_text = alert_text.split()

        lines = []
        current_line = ''

        for word in alert_text:
            if len(word) + len(current_line)+1 < width-4:
                current_line += word
                current_line += " "
            else:
                lines.append(current_line)
                current_line=word + " "

        if current_line:
            lines.append(current_line.strip())
        stdscr.attron(curses.color_pair(2))

        stdscr.addstr(height-3, width-3 - len("-->") //2, "-->" )
        stdscr.addstr(height-3, 3, "<--" )

        print(lines)
        for line in range(0,len(lines)):
            stdscr.addstr(4+line, width//2 -len(lines[line])//2, lines[line])

        stdscr.addstr(6 + len(lines), width//2 - len(f"({curr_index}/{len(weather_data[0]['alert']['alerts'])})"), f"({curr_index+1}/{len(weather_data[0]['alert']['alerts'])})")

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_RIGHT:
            alerts(weather_data, stdscr, curses, curr_index+1, system,fromArg)

        if key == curses.KEY_LEFT and curr_index >0:
            alerts(weather_data, stdscr, curses, curr_index-1, system,fromArg)
        
        if key == curses.KEY_LEFT and curr_index == 0 and fromArg == False:
            # main.main(stdscr)
            return

        
    elif fromArg == False:
        hourly(weather_data, stdscr, curses, system)
    elif fromArg == True and 'alerts' not in weather_data[0]['alert']:
        print('No alerts')
        return

        