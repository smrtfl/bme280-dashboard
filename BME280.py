# IIO_PATH = "/sys/devices/platform/soc/fe804000.i2c/i2c-1/1-0077/iio:device0/"
IIO_PATH = "/Users/PNikulin/Berufsschule/Mittelstufe/EvP/bme280/inputs/"
HUMIDITY_INPUT_FILE = "in_humidityrelative_input"
PRESSURE_INPUT_FILE = "in_pressure_input"
TEMPERATURE_INPUT_FILE = "in_temp_input"

class BME280:
    def get_temperature(self):
        return self.__string_input_to_float(
            self.__read_file(f"{IIO_PATH}{TEMPERATURE_INPUT_FILE}")
        )

    def get_humidity(self):
        return self.__string_input_to_float(
            self.__read_file(f"{IIO_PATH}{HUMIDITY_INPUT_FILE}")
        )


    def get_pressure(self):
        return self.__string_input_to_float(
            self.__read_file(f"{IIO_PATH}{PRESSURE_INPUT_FILE}")
        )

    @staticmethod
    def __string_input_to_float(string_input):
        return float(string_input) / 1000. if string_input is not None else None


    @staticmethod
    def __read_file(filename):
        try:
            with open(filename, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"File {filename} not found")
        except PermissionError:
            print(f"Permission denied when accessing {filename}")

        return None
