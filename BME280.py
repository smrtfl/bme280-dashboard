FALLBACK_IIO_PATH = "/sys/devices/platform/soc/fe804000.i2c/i2c-1/1-0077/iio:device0/"
HUMIDITY_INPUT_FILE = "in_humidityrelative_input"
PRESSURE_INPUT_FILE = "in_pressure_input"
TEMPERATURE_INPUT_FILE = "in_temp_input"


class BME280:

    def __init__(self, iio_path=None):
        self.iio_path = iio_path or FALLBACK_IIO_PATH


    def get_temperature(self):
        return self.__string_input_to_float(
            self.__read_file(f"{self.iio_path}{TEMPERATURE_INPUT_FILE}")
        )


    def get_humidity(self):
        return self.__string_input_to_float(
            self.__read_file(f"{self.iio_path}{HUMIDITY_INPUT_FILE}")
        )


    def get_pressure(self):
        return self.__string_input_to_float(
            self.__read_file(f"{self.iio_path}{PRESSURE_INPUT_FILE}")
        )


    @staticmethod
    def __string_input_to_float(string_input):
        return float(string_input) / 1000. if string_input is not None else None


    @staticmethod
    def __read_file(filename):
        with open(filename, 'r') as f:
            return f.read().strip()
