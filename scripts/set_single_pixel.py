import requests
import colorsys

def set_pixel_color(host, pixel_id, r, g, b):
    url = f"http://{host}/pixels/{pixel_id}/set_color_rgb"
    params = {'r': r, 'g': g, 'b': b}
    response = requests.get(url, params=params)
    return response

tick_count = 0


def get_rainbow_colors(num_colors):
        colors = []
        for i in range(num_colors):
            hue = i / num_colors
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            colors.append(tuple(int(c * 255) for c in rgb))
        return colors

   



# Example usage
if __name__ == "__main__":
    host = "192.168.4.99:8000"
    pixel_id = 1
    rainbow_colors = get_rainbow_colors(20)
    while True:
        for pixel_id, color in enumerate(rainbow_colors, start=1):
            color = rainbow_colors[(pixel_id + tick_count) % len(rainbow_colors)]
            r, g, b = color
            response = set_pixel_color(host, pixel_id, r, g, b)
            print(f"Pixel {pixel_id}: {response.status_code} - {response.text}")
        tick_count += 1
    # r, g, b = 255, 0, 0  # Red color
    # for pixel_id in range(1, 11):
    #     response = set_pixel_color(host, pixel_id, r, g, b)
    #     print(f"Pixel {pixel_id}: {response.status_code} - {response.text}")
    # response = set_pixel_color(host, pixel_id, r, g, b)
    # print(response.status_code)
    # print(response.text)
    