from fastapi import FastAPI
from PIL import Image
import io
from datetime import datetime

app = FastAPI()

def is_daytime(image_path):
    # Your existing code for is_daytime function goes here
    x1 = 1249
    y1 = 41
    x2 = 1878
    y2 = 119

    reader = easyocr.Reader(['en'])

    image = Image.open(image_path)
    cropped_image = image.crop((x1, y1, x2, y2))
    cropped_image = cropped_image.convert('RGB')

    with io.BytesIO() as output:
        cropped_image.save(output, format="JPEG")
        image_bytes = output.getvalue()

    # Perform text detection on cropped image
    result = reader.readtext(image_bytes)

    output_text1 = result[0][1]  # Extract '08 47.21' from the first element of the list
    output_text2 = result[1][1]  # Extract 'AM' from the second element of the list

    input_string = output_text1

    # Split the input string based on spaces and dots
    parts = input_string.split()

    # Extract hours, minutes, and seconds
    hours = int(parts[1].split('.')[0])
    minutes = int(parts[1].split('.')[1])
    seconds = int(parts[1].split('.')[2])

    # Format the time as hh:mm:ss
    formatted_time = f'{hours:02}:{minutes:02}:{seconds:02}'

    # Split the formatted time
    time_parts = formatted_time.split(':')

    # Extract hours, minutes, and seconds
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    seconds = int(time_parts[2])

    # Determine if it's 'AM' or 'PM'
    is_am = output_text2 == 'AM'

    # Adjust hours if it's 'PM' (add 12 hours)
    if not is_am:
        hours += 12

    # Create a datetime object with the adjusted time
    final_time = datetime(1, 1, 1, hours, minutes, seconds)

    # Check if the time is between 6 AM and 6 PM
    is_between_6am_and_6pm = 6 <= final_time.hour < 18

    return is_between_6am_and_6pm

@app.get("/")
def read_root():
    return {"message": "Welcome to your FastAPI application!"}

@app.post("/is_daytime/")
async def check_daytime(image_path: str):
    is_day = is_daytime(image_path)
    return {"is_daytime": is_day}
