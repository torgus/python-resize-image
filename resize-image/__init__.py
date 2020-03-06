import logging

import azure.functions as func
import io
import sys
from PIL import Image

# Final image composite size
FINAL_COMPOSITE_MAX_HEIGHT = 600
FINAL_COMPOSITE_MAX_WIDTH = 600

def main(blobin: func.InputStream, blobout: func.Out[bytes], context: func.Context):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {blobin.name}\n"
                 f"Blob Size: {blobin.length} bytes\n"
                 f"Context: {context}")
    input_image = blobin
    try:
        base_image = Image.open(input_image)
    except OSError as e:
        print(f'EXCEPTION: Unable to read input as image. {e}')
        sys.exit(254)
    except Exception as e:
        print(f'EXCEPTION: {e}')
        sys.exit(255)
    if base_image.width > FINAL_COMPOSITE_MAX_WIDTH or base_image.height > FINAL_COMPOSITE_MAX_HEIGHT:
        if base_image.height > base_image.width:
            factor = 900 / base_image.height
        else:
            factor = 900 / base_image.width
        resized_image = base_image.resize((int(base_image.width * factor), int(base_image.height * factor)))
    img_byte_arr = io.BytesIO()
    resized_image.convert('RGB').save(img_byte_arr, format='JPEG')
    blobout.set(img_byte_arr.getvalue())