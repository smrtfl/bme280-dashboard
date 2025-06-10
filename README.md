# BME280 Dashboard

Terminal dashboard to display BME280 sensor's readings

## Getting Started

1. Clone the project

```sh
git clone https://github.com/smrtfl/bme280-dashboard.git
```

2. Setup Python Virtual Environment (optional)

```sh
python -m venv venv/
source venv/bin/activate
```

3. Start the dashboard

```sh
python main.py
```

### Custom IIO path

Optionally, you could specify IIO path to dir with sensor data

```sh
python main.py --iio-path=path/to/sensor-data
```
