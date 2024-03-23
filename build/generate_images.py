import os
from openai import OpenAI
import time
import requests

def generate_images(chapters, output_dir, size, openai_api_key):
    client = OpenAI(api_key=openai_api_key)

    os.makedirs(output_dir, exist_ok=True)
    img_num = 1
    for chapter in chapters:
        try:
            response = client.images.generate(
                prompt=chapter,
                n=1,
                size=size,
                model="dall-e-3"
            )
        except Exception as e:
            print(f"Something gone wrong during image generation: {e}")
            continue

        for i, image_data in enumerate(response.data):
            image_url = image_data.url
            try:
                image_response = requests.get(image_url)
                image_response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print(f"HTTP connection failed: {errh}")
                continue
            except requests.exceptions.ConnectionError as errc:
                print(f"Failed to connect : {errc}")
                continue
            except requests.exceptions.Timeout as errt:
                print(f"Receiving data timeout: {errt}")
                continue
            except requests.exceptions.RequestException as err:
                print(f"There is something wrong with your request: {err}")
                continue

            with open(os.path.join(output_dir, f"image_{img_num}.png"), "wb") as f:
                f.write(image_response.content)
                print(f"Obraz {img_num} został pomyślnie pobrany i zapisany jako 'image_{img_num}.png'")
                img_num += 1


        print("Poczekaj 5s")
        time.sleep(5)