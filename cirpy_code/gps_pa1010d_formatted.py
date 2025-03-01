import time
import board
import adafruit_gps

# Buffer for partial sentences
buffer = ""

def initialize_gps(i2c, update_rate=1000):
    """
    Initialize the GPS module with the specified update rate.
    :param i2c: I2C connection instance.
    :param update_rate: Update rate in milliseconds (default is 1000ms or 1Hz).
    :return: Initialized GPS instance.
    """
    gps = adafruit_gps.GPS_GtopI2C(i2c)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")  # Enable GGA and RMC
    gps.send_command(f"PMTK220,{update_rate}".encode())  # Set update rate
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

# Main Entry
if __name__ == "__main__":
    i2c = board.I2C()
    gps = initialize_gps(i2c)
    process_gps(gps)
