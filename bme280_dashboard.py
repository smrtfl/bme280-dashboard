#!/usr/bin/env python3

import curses
from BME280 import BME280

def get_centered_x_offset(text, screen_width):
    return (screen_width - len(text)) // 2

def print_bottom(text, stdscr, height, width):
    y_offset = max(0, height - 2)
    x_offset = max(0, (width - len(text)) // 2)

    stdscr.addstr(y_offset, x_offset, text)

def dashboard(stdscr):
    bme280 = BME280()

    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(200)

    while True:
        stdscr.clear()

        title = "BME280 Sensor Readings"

        readings = {
            "Temperature": f"{temperature:.2f} °C" if (temperature := bme280.get_temperature()) is not None else "N/A",
            "Humidity": f"{humidity:.2f} %" if (humidity := bme280.get_humidity()) is not None else "N/A",
            "Pressure": f"{pressure:.2f} hPa" if (pressure := bme280.get_pressure()) is not None else "N/A"
        }

        screen_height, screen_width = stdscr.getmaxyx()

        table_y_offset = screen_height // 2 - len(readings)
        title_y_offset = table_y_offset - 4

        stdscr.addstr(title_y_offset, get_centered_x_offset(title, screen_width), title, curses.A_BOLD)

        max_name_length, max_value_length = 0, 0
        for name, value in readings.items():
            max_name_length = max(max_name_length, len(name))
            max_value_length = max(max_value_length, len(value))

        for i, (name, value) in enumerate(readings.items()):
            name_column = name.ljust(max_name_length)
            value_column = value.center(max_value_length)

            row_y_offset = table_y_offset + i * 2
            
            stdscr.addstr(
                row_y_offset,
                get_centered_x_offset(name_column + value_column, screen_width),
                name_column
            )
            stdscr.addstr(
                row_y_offset,
                get_centered_x_offset(name_column + value_column, screen_width) + len(name_column) + 5 // 2,
                value_column,
                curses.A_BOLD
            )


        print_bottom("Press 'q' to quit", stdscr, screen_height, screen_width)

        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q'):
            break


if __name__ == "__main__":
    curses.wrapper(dashboard)
