import requests
import colorsys
import time

def set_pixel_color(host, pixel_id, r, g, b):
    url = f"http://{host}/pixels/{pixel_id}/set_color_rgb"
    params = {'r': r, 'g': b, 'b': g}
    response = requests.get(url, params=params)
    return response

def get_rainbow_colors(num_colors):
    colors = []
    for i in range(num_colors):
        hue = i / num_colors
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        colors.append(tuple(int(c * 255) for c in rgb))
    return colors

def generate_pixel_payload(rainbow_colors, tick_count):
    payload = {}
    for pixel_id, color in enumerate(rainbow_colors):
        adjusted_id = (pixel_id + tick_count) % len(rainbow_colors)
        r, g, b = rainbow_colors[adjusted_id]
        payload[str(pixel_id)] = [r, g, b]
    return payload

# Example usage
if __name__ == "__main__":
    host = "192.168.4.99:8000"
    rainbow_colors = get_rainbow_colors(20)
    tick_count = 0

    while True:
        start_time = time.time()

        # Generate the payload for all pixels
        payload = generate_pixel_payload(rainbow_colors, tick_count)

        # Send the request in one POST call
        response = requests.post(f"http://{host}/pixels/set_pixels", json=payload)

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")

        tick_count += 1

        # Ensure a minimum interval between updates
        elapsed_time = time.time() - start_time
        sleep_duration = max(0, 0.05 - elapsed_time)  # Target 20 updates per second
        time.sleep(sleep_duration)
