# Meteo: Curses-based weather app for Canadian weather

Meteo is a curses based, TUI client for Canadian weather. 

![alt text](https://github.com/jmi06/meteo/blob/main/images/alert.png "Alert example")

![alt text](https://github.com/jmi06/meteo/blob/main/images/currentconditions.png "Alert example")

```

usage: main.py [-h] [-p,] [--location LOCATION] [--system SYSTEM] [--alerts] [--current-conditions] [--daily]
               [--hourly]

Curses-based weather app for Canadian weather

options:
  -h, --help            show this help message and exit
  -p,, --print          Prints the weather to the terminal, no curses
  --location LOCATION   Override location in the config file. (if your location includes spaces, use quotations)
  --system SYSTEM       override unit system in the config file, (metric, imperial)
  --alerts              display the alerts screen
  --current-conditions  display the current conditions screen
  --daily               display the daily forecast
  --hourly              display the hourly forecast

```