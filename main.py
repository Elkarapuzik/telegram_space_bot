import os
from pprint import pprint
import random
import time
#______________________________
import requests
import telegram
from deep_translator import GoogleTranslator
from termcolor import cprint
from dotenv import load_dotenv

load_dotenv()

def delete_files_in_folder(folder_path):
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename) 
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    cprint(f'Ошибка при удалении файла {file_path}. {e}', 'red')




#______________________________________________________________________________________
#Nasa

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
    #spaceX


    response_all_spaceX = requests.get(f"https://api.spacexdata.com/v3/launches")
    response_all_spaceX.raise_for_status()

    name_spaceX = 0

    all_spaceX_pictures = []

    for launch in reversed(response_all_spaceX.json()):
        if launch['links']['flickr_images'] != []:
            all_spaceX_pictures.append(launch)  
            
    random_spaceX_launch = random.choice(all_spaceX_pictures)

    for link_spaceX in random_spaceX_launch['links']['flickr_images']:
        response = requests.get(link_spaceX)
        response.raise_for_status()
        name_spaceX = name_spaceX + 1
        number_of_name = f"picture{name_spaceX}.jpeg"
        with open(f"img_spaceX/{number_of_name}", "wb") as file:
            file.write(response.content)

    max_random_number_spaceX = len(random_spaceX_launch['links']['flickr_images'])

    random_company = random.choice(["nasa" , "spaceX"])

    response_latest_time_spaceX = random_spaceX_launch['launch_date_local'].replace("T" , " Время -> ")

    if random_company == "nasa":
        random_picture = random.randint(1, max_random_number_nasa)
        description = response_nasa.json()[0]['explanation']
        picture_text = GoogleTranslator(source='auto', target='ru').translate(description)
    else:
        random_picture = random.randint(1 , max_random_number_spaceX)
        description = GoogleTranslator(source='auto', target='ru').translate(random_spaceX_launch['details'])
        picture_text = f"""\
Запуск ракеты SpaceX.
{description}

Запуск совершен
                                 │
                                 ╰─>{response_latest_time_spaceX}"""

    #____________________________________________________________________________________________________________________________
    #Work with telegram
    
    telegtam_bot_token=os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID")
    photo_path = f'img_{random_company}/picture{random_picture}.jpeg'

    bot = telegram.Bot(token=telegtam_bot_token)

    if len(picture_text) > 950:
       
        try:
            picrure_text_residue = f"  ^^^  || {picture_text[950:-1]} || "
            picture_text = f"{picture_text[0:950]}..."
            bot.send_photo(chat_id=telegram_chat_id, photo=open(photo_path, 'rb'), caption=f"{picture_text}")
            bot.send_message(chat_id=telegram_chat_id, text=f"{picrure_text_residue}", parse_mode="MarkdownV2")
        except telegram.error.BadRequest:
            picrure_text_residue = f"  ^^^   {picture_text[950:-1]}  "
            picture_text = f"{picture_text[0:950]}..."
            bot.send_photo(chat_id=telegram_chat_id, photo=open(photo_path, 'rb'), caption=f"{picture_text}")
            bot.send_message(chat_id=telegram_chat_id, text=f"{picrure_text_residue}")
            cprint("Parse mode error" , 'red')
    else:
        bot.send_photo(chat_id=telegram_chat_id, photo=open(photo_path, 'rb'), caption=f"{picture_text}")

    time.sleep(5)#time to next send

    delete_files_in_folder("img_spaceX")
    delete_files_in_folder("img_nasa")
