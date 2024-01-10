import os
import requests
from pprint import pprint
import telegram
import random
import time
#______________________________
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()

while True:

    api_key = os.getenv("API_KEY")

    params_nasa = {
        "count" : "1",
        "api_key" : api_key,
        
    }

    response_nasa = requests.get(f'https://api.nasa.gov/planetary/apod', params=params_nasa )
    response_nasa.raise_for_status()

    name_nasa = 0

    for slovar_nasa in response_nasa.json():
        response = requests.get(slovar_nasa['url'])
        response.raise_for_status()
        name_nasa = name_nasa + 1
        number_of_name = f"picture{name_nasa}.jpeg"
        with open(f"img_nasa/{number_of_name}", "wb") as file:
            file.write(response.content)

    max_random_number_nasa = len(response_nasa.json())

    #______________________________________________________________________________________


    response_all_spaceX = requests.get(f"https://api.spacexdata.com/v3/launches")
    response_all_spaceX.raise_for_status()

    name_spaceX = 0

    for launch in reversed(response_all_spaceX.json()):
        if launch['links']['flickr_images'] != []:
            response_latest_spaceX = launch
            break

    for link_spaceX in response_latest_spaceX['links']['flickr_images']:
        response = requests.get(link_spaceX)
        response.raise_for_status()
        name_spaceX = name_spaceX + 1
        number_of_name = f"picture{name_spaceX}.jpeg"
        with open(f"img_spaceX/{number_of_name}", "wb") as file:
            file.write(response.content)

    max_random_number_spaceX = len(response_latest_spaceX['links']['flickr_images'])

    random_company = random.choice(["nasa" , "spaceX"])

    response_latest_time_spaceX = response_latest_spaceX['launch_date_local'].replace("T" , " Time -> ")

    if random_company == "nasa":
        random_picture = random.randint(1, max_random_number_nasa)
        description = response_nasa.json()[0]['explanation']
        picture_text = GoogleTranslator(source='auto', target='ru').translate(description)
    else:
        random_picture = random.randint(1 , max_random_number_spaceX)
        picture_text = f"Крайний запуск ракеты SpaceX. Cовершен: {response_latest_time_spaceX}"

    

    #____________________________________________________________________________________________________________________________
    #Work with telegram
    
    telegtam_bot_token=os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID")
    photo_path = f'img_{random_company}/picture{random_picture}.jpeg'

    bot = telegram.Bot(token=telegtam_bot_token)

    if len(picture_text) > 950:
        picrure_text_residue = "  ↑  " + picture_text[950:-1]
        picture_text = picture_text[0:950] + "..."
        bot.send_photo(chat_id=telegram_chat_id, photo=open(photo_path, 'rb'), caption=f"{picture_text}")
        bot.send_message(chat_id=telegram_chat_id, text=f"{picrure_text_residue}")
    else:
        bot.send_photo(chat_id=telegram_chat_id, photo=open(photo_path, 'rb'), caption=f"{picture_text}")

    time.sleep(5)#time to next send

