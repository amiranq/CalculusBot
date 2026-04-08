import telebot
import requests
from PIL import Image
from io import BytesIO
from API import get_answer
import os
import random
from file_exctrctor import get_teorems

bot = telebot.TeleBot('7558810688:AAE7dX2nVtORhMTEyIDveO3guA7TxhTIt88')


@bot.message_handler(content_types=['photo'])
def save_photo(message):
    # Доп. сообщение, пока не готово основное
    wait_msg = bot.send_message(message.chat.id, "Промыслов призадумался, поэтому придётся подождать :)")
    wait_msg_id = wait_msg.message_id

    text = ""
    if message.caption is not None:
        text = message.caption
    # Получаем наибольшую по размеру фотографию из массива доступных
    photo_size_object = message.photo[-1]  # Берём последнюю, так как она самая большая по размеру
    file_info = bot.get_file(photo_size_object.file_id)

    # Получаем путь к файлу через API Telegram
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"

    # Загружаем изображение
    file_data = requests.get(file_url)

    # Открываем изображение через PIL и сохраняем как JPG
    img = Image.open(BytesIO(file_data.content))
    img.save(f"Images/{message.chat.id}.jpg", "JPEG")  # Сохраняем фото в файл
    ans = get_answer(path=f"Images/{message.chat.id}.jpg", text=text)
    bot.delete_message(message.chat.id, wait_msg_id)
    bot.send_message(message.chat.id, f'{ans}')
    os.remove(f"Images/{message.chat.id}.jpg")


@bot.message_handler(commands=['i_am_tired'])
def site(message):
    images = os.listdir("Prom_images/")
    image = images[random.randint(0, len(images) - 1)]
    bot.send_photo(message.chat.id, photo=Image.open(f"Prom_images/{image}"), caption="Я верю в тебя, сладкий)")


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}\nНапиши мне свой пример или пришли фото!')  # Ответ на команду /start


@bot.message_handler()
def info(message):
    # Доп. сообщение, пока не готово основное
    wait_msg = bot.send_message(message.chat.id, "Промыслов призадумался, поэтому придётся подождать :)")
    wait_msg_id = wait_msg.message_id

    teors = get_teorems(message.text)

    bot.delete_message(message.chat.id, wait_msg_id)
    bot.send_message(message.chat.id, f'{teors if teors else ""}')


# Запуск бота
bot.polling(non_stop=True)
