from watchdog.events import DirModifiedEvent, FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer

FALLBACK_IIO_PATH = "/sys/devices/platform/soc/fe804000.i2c/i2c-1/1-0077/iio:device0/"
HUMIDITY_INPUT_FILE = "in_humidityrelative_input"
PRESSURE_INPUT_FILE = "in_pressure_input"
TEMPERATURE_INPUT_FILE = "in_temp_input"


class BME280InputChangeEventHandler(FileSystemEventHandler):

    def __init__(self, bme280_instance):
        self.bme280_instance = bme280_instance


    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent):
        if str(event.src_path).rsplit('/', 1)[-1] in [sensor.input_file for sensor in self.bme280_instance.sensors.values()]:
            self.bme280_instance.update_file_readings(event.src_path)


class BME280Sensor:

    def __init__(self, value, input_file):
        self.value: float | None = value 
        self.input_file = input_file


class BME280:

    def __init__(self, iio_path=None):
        self.__iio_path = iio_path or FALLBACK_IIO_PATH
        self.__event_handler = BME280InputChangeEventHandler(self)
        self.__observer = Observer()

        self.sensors = {
            "temperature": BME280Sensor(None, TEMPERATURE_INPUT_FILE),
            "humidity": BME280Sensor(None, HUMIDITY_INPUT_FILE),
            "pressure": BME280Sensor(None, PRESSURE_INPUT_FILE),
        }

        self.__observer.schedule(self.__event_handler, self.__iio_path, recursive=False)

        for sensor_name in self.sensors.keys():
            self.__update_sensor_value(sensor_name)

        self.__observer.start()


    def get_sensor_filepath(self, sensor):
        return f"{self.__iio_path}{sensor.input_file}"


    def update_file_readings(self, filename):
        sensor_name = next((name for name, sensor in self.sensors.items() if sensor.input_file == filename.rsplit('/', 1)[-1]), None)
        self.__update_sensor_value(sensor_name)


    def __update_sensor_value(self, sensor_name):
        sensor = self.sensors[sensor_name]

        try:
            sensor.value = self.__string_input_to_float(
                self.__read_file(f"{self.__iio_path}{sensor.input_file}")
            )
        except:
            sensor.value = None


    @staticmethod
    def __string_input_to_float(string_input):
        return float(string_input) / 1000. if string_input is not None else None


    @staticmethod
    def __read_file(filename):
        with open(filename, 'r') as f:
            return f.read().strip()
