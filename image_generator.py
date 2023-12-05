from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

def generate_advertisement_collage(base_prompt, scenes, collage_dimensions=(3, 1)):
    """
    Generates a collage of images for an advertisement based on a base prompt.
    
    :param base_prompt: Base description of the advertisement.
    :param scenes: Number of different scenes to generate.
    :param collage_dimensions: Dimensions of the collage (columns, rows).
    :return: Collage image.
    """
    client = OpenAI(api_key='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')
    images = []  # Inițializarea listei de imagini

    for i in range(scenes):
        try:
            prompt = f"{base_prompt}, scene {i + 1} of {scenes}"
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            images.append(image)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    collage_width = collage_dimensions[0] * 1024
    collage_height = collage_dimensions[1] * 1024
    collage = Image.new('RGB', (collage_width, collage_height))

    for i, image in enumerate(images):
        x = i % collage_dimensions[0] * 1024
        y = i // collage_dimensions[0] * 1024
        collage.paste(image, (x, y))

    return collage
