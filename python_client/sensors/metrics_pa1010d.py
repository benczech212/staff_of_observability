from prometheus_client import Gauge, start_http_server
import time
import board
import adafruit_gps
from sensors.base_sensor import BaseSensor

class PA1010D_Sensor(BaseSensor):
    def __init__(self, instance_name="GPS"):
        self.instance_name = instance_name
        self.metrics = {}
        # Initialize the GPS module
        try:
            i2c = board.I2C()
            self.gps = self.initialize_gps(i2c)
        except Exception as e:
            print(f"Error initializing GPS module: {e}")
            raise

        # Labels and metrics
        self.base_labels = {'sensor': 'PA1010D', 'instance': instance_name}
        self.metrics = {
            'latitude': self.get_or_create_metric_gauge('sensor_gps_latitude','Latitude in decimal degrees', {'geo': 'Lat', 'unit': 'Degrees'}),
            'longitude': self.get_or_create_metric_gauge('sensor_gps_longitude','Longitude in decimal degrees', {'geo': 'Lng', 'unit': 'Degrees'}),
            'altitude': self.get_or_create_metric_gauge('sensor_altitude','Altitude in meters', {'unit': 'Meters'}),
            'fix_quality': self.get_or_create_metric_gauge('sensor_gps_fix_quality','Fix quality (0 = invalid, 1 = GPS fix, 2 = DGPS fix)'),
            'satellites': self.get_or_create_metric_gauge('sensor_gps_satellites','Number of satellites in view'),
            'speed': self.get_or_create_metric_gauge('sensor_speed','Speed over ground (knots)', {'unit': 'Knots'}),
        }

        # self.metrics = {
        #     'latitude': Gauge(
        #         'sensor_gps_latitude',
        #         'Latitude in decimal degrees',
        #         list(self.base_labels.keys()) + ['geo', 'unit']
        #     ).labels(**self.base_labels, geo='Lat', unit="Degrees"),
        #     'longitude': Gauge(
        #         'sensor_gps_longitude',
        #         'Longitude in decimal degrees',
        #         list(self.base_labels.keys()) + ['geo', 'unit']
        #     ).labels(**self.base_labels, geo='Lng', unit="Degrees"),
        #     'altitude': Gauge(
        #         'sensor_altitude',
        #         'Altitude in meters',
        #         list(self.base_labels.keys()) + ['unit']
        #     ).labels(**self.base_labels,unit="Meters"),
        #     'fix_quality': Gauge(
        #         'sensor_gps_fix_quality',
        #         'Fix quality (0 = invalid, 1 = GPS fix, 2 = DGPS fix)',
        #         list(self.base_labels.keys())
        #     ).labels(**self.base_labels),
        #     'satellites': Gauge(
        #         'sensor_gps_satellites',
        #         'Number of satellites in view',
        #         list(self.base_labels.keys())
        #     ).labels(**self.base_labels),
        #     'speed': Gauge(
        #         'sensor_speed_knots',
        #         'Speed over ground (knots)',
        #         list(self.base_labels.keys())+['unit']
        #     ).labels(**self.base_labels,unit="Knots"),
        # }

    def initialize_gps(self, i2c):
        """
        Initialize the GPS module.
        """
        gps = adafruit_gps.GPS_GtopI2C(i2c)
        gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")  # Enable GGA and RMC
        gps.send_command(b"PMTK220,1000")  # Set update rate to 1 Hz
        return gps

    def read_and_buffer_data(gps, buffer_size=32):
        """
        Read data from the GPS and assemble complete NMEA sentences.
        :param gps: GPS instance.
        :param buffer_size: Maximum number of bytes to read.
        :return: A list of complete NMEA sentences.
        """
        global buffer
        data = gps.read(buffer_size)
        if data is not None:
            buffer += "".join([chr(b) for b in data])
            sentences = buffer.split("\r\n")
            buffer = sentences.pop()  # Keep the incomplete part for the next read
            return sentences
        return []

    def is_valid_nmea_sentence(sentence):
        """
        Validate the basic structure of an NMEA sentence.
        :param sentence: NMEA sentence string.
        :return: True if valid, False otherwise.
        """
        if not sentence.startswith("$"):
            return False
        if "*" in sentence:
            checksum_data, checksum = sentence.split("*", 1)
            return len(checksum) == 2 and checksum.isalnum()
        return False

    def parse_nmea_sentence(sentence):
        """
        Parse an NMEA sentence into its components.
        :param sentence: NMEA sentence string.
        :return: A dictionary with the parsed data or an error message.
        """
        try:
            if len(sentence) < 6 or not sentence.startswith("$"):
                return {"type": "error", "message": "Invalid sentence structure", "raw_sentence": sentence}

            if sentence.startswith("$GNGGA"):
                return parse_gga(sentence)
            elif sentence.startswith("$GNRMC"):
                return parse_rmc(sentence)
            elif sentence.startswith("$GNVTG"):
                return parse_vtg(sentence)
            elif sentence.startswith("$PMTK"):
                return {"type": "unrecognized", "sentence": sentence}  # Handle PMTK as unrecognized for now
            else:
                return {"type": "unrecognized", "sentence": sentence}
        except Exception as e:
            return {
                "type": "error",
                "message": str(e),
                "raw_sentence": sentence,
            }

    def parse_gga(sentence):
        """
        Parse a GGA (Global Positioning System Fix Data) sentence.
        :param sentence: NMEA GGA sentence.
        :return: Dictionary with parsed GGA data or an error message.
        """
        fields = sentence.split(",")
        expected_fields = 11
        if len(fields) < expected_fields:
            return {
                "type": "error",
                "message": f"Incomplete GGA sentence, expected {expected_fields} fields, got {len(fields)}",
                "raw_sentence": sentence,
            }

        return {
            "type": "GGA",
            "time": fields[1],
            "latitude": fields[2],
            "latitude_dir": fields[3],
            "longitude": fields[4],
            "longitude_dir": fields[5],
            "fix_quality": fields[6],
            "num_satellites": fields[7],
            "horizontal_dilution": fields[8],
            "altitude": fields[9],
            "altitude_units": fields[10],
        }

    def parse_rmc(sentence):
        """
        Parse an RMC (Recommended Minimum Specific GNSS Data) sentence.
        :param sentence: NMEA RMC sentence.
        :return: Dictionary with parsed RMC data or an error message.
        """
        fields = sentence.split(",")
        expected_fields = 10
        if len(fields) < expected_fields:
            return {
                "type": "RMC",
                "error": f"Incomplete sentence, expected {expected_fields} fields, got {len(fields)}",
                "raw_sentence": sentence,
            }

        return {
            "type": "RMC",
            "time": fields[1],
            "status": fields[2],
            "latitude": fields[3],
            "latitude_dir": fields[4],
            "longitude": fields[5],
            "longitude_dir": fields[6],
            "speed_over_ground": fields[7],
            "course_over_ground": fields[8],
            "date": fields[9],
        }

    def parse_vtg(sentence):
        """
        Parse a VTG (Course Over Ground and Ground Speed) sentence.
        :param sentence: NMEA VTG sentence.
        :return: Dictionary with parsed VTG data.
        """
        fields = sentence.split(",")
        if len(fields) < 8:
            return {
                "type": "error",
                "message": "Incomplete VTG sentence",
                "raw_sentence": sentence,
            }

        return {
            "type": "VTG",
            "true_course": fields[1],
            "true_course_unit": fields[2],
            "magnetic_course": fields[3],
            "magnetic_course_unit": fields[4],
            "speed_knots": fields[5],
            "speed_knots_unit": fields[6],
            "speed_kmh": fields[7],
            "speed_kmh_unit": fields[8],
        }

    def process_gps(gps):
        """
        Continuously read and process GPS data.
        :param gps: Initialized GPS instance.
        """
        timestamp = time.monotonic()
        try:
            while True:
                sentences = read_and_buffer_data(gps)
                for sentence in sentences:
                    if is_valid_nmea_sentence(sentence):
                        parsed_data = parse_nmea_sentence(sentence)
                        if parsed_data.get("type") == "error":
                            print(f"Error: {parsed_data.get('message', 'Unknown error')}, Sentence: {parsed_data.get('raw_sentence', 'N/A')}")
                        elif parsed_data.get("type") == "unrecognized":
                            print(f"Unrecognized Sentence: {parsed_data.get('sentence')}")
                        else:
                            print(parsed_data)
                    else:
                        print(f"Invalid Sentence Structure: {sentence}")

                if time.monotonic() - timestamp > 5:
                    gps.send_command(b"PMTK605")  # Request firmware version
                    timestamp = time.monotonic()
        except KeyboardInterrupt:
            print("Program interrupted by user.")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def update_metrics(self):
        """Update the GPS metrics."""
        try:
            # Read GPS data
            self.gps.update()
            data = self.gps
            # print(data)

            # Update Prometheus metrics
            self.metrics['latitude'].set(data.latitude)
            self.metrics['longitude'].set(data.longitude)
            self.metrics['altitude'].set(data.altitude_m)
            self.metrics['fix_quality'].set(data.fix_quality)
            self.metrics['satellites'].set(data.satellites)
            self.metrics['speed'].set(data.speed_knots)
        except Exception as e:
            print(f"Error updating GPS metrics: {e}")

            
