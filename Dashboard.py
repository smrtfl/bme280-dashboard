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
        self.__stdscr.timeout(1000)

        title = "BME280 Sensor Readings"
        screen_height, screen_width = self.__stdscr.getmaxyx()
        readings = self.__get_bme280_readings()

        self.__print_content(title, readings, screen_height, screen_width)

        while True:
            should_reprint = False

            if (new_readings := self.__get_bme280_readings()) != readings:
                readings = new_readings
                should_reprint = True

            if (new_dimensions := self.__stdscr.getmaxyx()) != (screen_height, screen_width):
                screen_height, screen_width = new_dimensions
                should_reprint = True

            if should_reprint:
                self.__print_content(title, readings, screen_height, screen_width)

            key = self.__stdscr.getch()
            if key == ord('q'):
                break


    def __print_content(self, title, readings, screen_height, screen_width):
        self.__stdscr.clear()

        self.__print_dashboard(title, readings, screen_height, screen_width)
        self.__print_bottom("Press 'q' to quit", screen_height, screen_width)

        self.__stdscr.refresh()


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
        column_gap = 10

        self.__stdscr.addstr(title_y_offset, self.__get_centered_x_offset(title, screen_width), title, curses.A_BOLD)

        max_name_length, max_value_length = 0, 0
        for name, value in readings.items():
            max_name_length = max(max_name_length, len(name))
            max_value_length = max(max_value_length, len(value))

        for i, (name, value) in enumerate(readings.items()):
            name_column = name.ljust(max_name_length)
            value_column = value.ljust(max_value_length)

            row_text = (" " * column_gap).join([name_column, value_column])

            row_y_offset = table_y_offset + i * 2

            self.__stdscr.addstr(
                row_y_offset,
                self.__get_centered_x_offset(row_text, screen_width),
                name_column 
            )
            self.__stdscr.addstr(
                row_y_offset,
                self.__get_centered_x_offset(row_text, screen_width) + len(name_column) + column_gap,
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
