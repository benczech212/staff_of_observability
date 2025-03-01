import requests

def set_pixel_color(host, pixel_id, r, g, b):
    url = f"http://{host}/pixels/{pixel_id}/set_color_rgb"
    params = {'r': r, 'g': g, 'b': b}
    response = requests.get(url, params=params)
    return response

tick_count = 0



# Example usage
if __name__ == "__main__":
    host = "example.com"
    pixel_id = 1

    r, g, b = 255, 0, 0  # Red color
    for pixel_id in range(1, 11):
        response = set_pixel_color(host, pixel_id, r, g, b)
        print(f"Pixel {pixel_id}: {response.status_code} - {response.text}")
    response = set_pixel_color(host, pixel_id, r, g, b)
    print(response.status_code)
    print(response.text)