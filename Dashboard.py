import curses


class Dashboard:

    def __init__(self, stdscr, bme280):
        self.__stdscr = stdscr
        self.__bme280 = bme280

        self.__units = {
            "Temperature": "°C",
            "Humidity": "%",
            "Pressure": "hPa"
        }

        self.__run()


    def __run(self):
        curses.curs_set(0)
        curses.start_color()

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

        self.__stdscr.nodelay(True)
        self.__stdscr.timeout(200)


        while True:
            self.__stdscr.clear()

            title = "BME280 Sensor Readings"
            readings = self.__get_bme280_readings()

            screen_height, screen_width = self.__stdscr.getmaxyx()

            self.__print_dashboard(title, readings, screen_height, screen_width)
            self.__print_bottom("Press 'q' to quit", screen_height, screen_width)

            self.__stdscr.refresh()

            key = self.__stdscr.getch()
            if key == ord('q'):
                break


    def __get_bme280_readings(self):
        data = {
            "Temperature": "N/A",
            "Humidity": "N/A",
            "Pressure": "N/A"
        }
        errors = []

        for key in data.keys():
            try:
                data[key] = f"{self.__bme280.get_temperature()} {self.__units[key]}"
            except Exception as e:
                errors.append(e)

        if errors:
            self.__print_errors(errors)

        return data


    def __print_dashboard(self, title, readings, screen_height, screen_width):
        table_y_offset = screen_height // 2 - len(readings)
        title_y_offset = table_y_offset - 4

        self.__stdscr.addstr(title_y_offset, self.__get_centered_x_offset(title, screen_width), title, curses.A_BOLD)

        max_name_length, max_value_length = 0, 0
        for name, value in readings.items():
            max_name_length = max(max_name_length, len(name))
            max_value_length = max(max_value_length, len(value))

        for i, (name, value) in enumerate(readings.items()):
            name_column = name.ljust(max_name_length)
            value_column = value.center(max_value_length)

            row_y_offset = table_y_offset + i * 2

            self.__stdscr.addstr(
                row_y_offset,
                self.__get_centered_x_offset(name_column + value_column, screen_width),
                name_column
            )
            self.__stdscr.addstr(
                row_y_offset,
                self.__get_centered_x_offset(name_column + value_column, screen_width) + len(name_column) + 5 // 2,
                value_column,
                curses.A_BOLD
            )


    def __print_errors(self, errors):
        for i, error in enumerate(errors):
            self.__stdscr.addstr((i + 1) * 2, 4, str(error), curses.color_pair(1))


    def __print_bottom(self, text, height, width):
        y_offset = max(0, height - 2)
        x_offset = max(0, (width - len(text)) // 2)

        self.__stdscr.addstr(y_offset, x_offset, text)


    @staticmethod
    def __get_centered_x_offset(text, screen_width):
        return (screen_width - len(text)) // 2
