import json
import telebot
from telebot import types
import time
import datetime


def vuvod_type_1(text, otstup):
    for word in text:
        print(otstup + word, end='', flush=True)
        time.sleep(0.01)

def vuvod_type_2(text, otstup):
    lines = text.splitlines()
    for line in lines:
        print(otstup + line)
        time.sleep(0.1)

def create_bot(json_file: str):
    try:
        with open(json_file, 'r', encoding='utf-8') as config_file:
            config_data = json.load(config_file)
    except:
        # Записати об'єкт JSON у файл
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump({"bot": {"token": "enter the token"}}, file, ensure_ascii=False, indent=4)
        vuvod_type_1(f"створено {json_file}", otstup="")
        print()
        with open(json_file, 'r', encoding='utf-8') as config_file:
            config_data = json.load(config_file)
    return config_data

def start_bot(data):
    token = data['bot']['token']
    if token == "enter the token":
        vuvod_type_1(f"Введіть свій токін", otstup="")
        exit()
    else:
        bot = telebot.TeleBot(token)
        time.sleep(3)
        now = datetime.datetime.now()
        formatted_time = now.strftime("[%H:%M:%S]")
        vuvod_type_1(text=f"Успішний запуск! | {formatted_time}\n\n", otstup="")
        
        
        @bot.message_handler(content_types=['text'])
        def handle_text(message):
            text = message.text
            command = text.split()[0]
            if text.startswith('/'):
                if command in data['command']:
                    action_list = data['command'][command]
            else:
                if command in data['reaction_on_text']:
                    action_list = data['reaction_on_text'][command]
            for action in action_list:
                try:
                    if 'time.sleep' in action:
                        time.sleep(action['time.sleep'])
                    if 'delete' in action:
                        message_id = message.message_id
                        delete_id = eval(action['delete'])
                        bot.delete_message(message.chat.id, delete_id)
                    if 'text' in action:
                        response_text = action['text']
                        if 'buttons' in action:
                            buttons = []
                            for button in action['buttons']:
                                if 'type' in button:
                                    if button['type'] == 'url':
                                        buttons.append(telebot.types.InlineKeyboardButton(button['name'], url=button['url']))
                                    elif button['type'] == 'callback':
                                        buttons.append(telebot.types.InlineKeyboardButton(button['name'], callback_data=button['calldata']))
                            if buttons:
                                markup = telebot.types.InlineKeyboardMarkup()
                                markup.add(*buttons)
                                bot.send_message(message.chat.id, response_text, reply_markup=markup)
                            else:
                                bot.send_message(message.chat.id, response_text)
                    if 'photo' in action:
                        photo_url = action['photo']
                        if 'buttons' in action:
                                buttons = []
                                for button in action['buttons']:
                                    if 'type' in button:
                                        if button['type'] == 'url':
                                            buttons.append(telebot.types.InlineKeyboardButton(button['name'], url=button['url']))
                                        elif button['type'] == 'callback':
                                            buttons.append(telebot.types.InlineKeyboardButton(button['name'], callback_data=button['calldata']))
                                if buttons:
                                    markup = telebot.types.InlineKeyboardMarkup()
                                    markup.add(*buttons)
                                    if 'caption' in action: caption = action['caption']; bot.send_photo(message.chat.id, photo_url, caption=caption,  reply_markup=markup)
                                    else: bot.send_photo(message.chat.id, photo_url, caption=caption,  reply_markup=markup)
                        else:
                            if 'caption' in action: caption = action['caption']; bot.send_photo(message.chat.id, photo_url, caption=caption)
                            else: bot.send_photo(message.chat.id, photo_url)
                    if 'video' in action:
                        video_url = action['video']
                        if 'buttons' in action:
                            buttons = []
                            for button in action['buttons']:
                                if 'type' in button:
                                    if button['type'] == 'url':
                                        buttons.append(telebot.types.InlineKeyboardButton(button['name'], url=button['url']))
                                    elif button['type'] == 'callback':
                                        buttons.append(telebot.types.InlineKeyboardButton(button['name'], callback_data=button['calldata']))
                            if buttons:
                                markup = telebot.types.InlineKeyboardMarkup()
                                markup.add(*buttons)
                                if 'caption' in action: caption = action['caption']; bot.send_photo(message.chat.id, video_url, caption=caption,  reply_markup=markup)
                                else: bot.send_photo(message.chat.id, video_url, caption=caption,  reply_markup=markup)
                        else:
                            if 'caption' in action: caption = action['caption']; bot.send_photo(message.chat.id, video_url, caption=caption)
                            else: bot.send_photo(message.chat.id, photo_url)
                    if 'file' in action:
                        video_url = action['file']
                        if 'buttons' in action:
                            buttons = []
                            for button in action['buttons']:
                                if 'type' in button:
                                    if button['type'] == 'url':
                                        buttons.append(telebot.types.InlineKeyboardButton(button['name'], url=button['url']))
                                    elif button['type'] == 'callback':
                                        buttons.append(telebot.types.InlineKeyboardButton(button['name'], callback_data=button['calldata']))
                            if buttons:
                                markup = telebot.types.InlineKeyboardMarkup()
                                markup.add(*buttons)
                                if 'caption' in action: caption = action['caption']; bot.send_photo(message.chat.id, video_url, caption=caption,  reply_markup=markup)
                                else: bot.send_photo(message.chat.id, video_url, caption=caption,  reply_markup=markup)
                        else:
                            if 'caption' in action: caption = action['caption']; bot.send_photo(message.chat.id, video_url, caption=caption)
                            else: bot.send_photo(message.chat.id, photo_url)
                except Exception as e: vuvod_type_1(text=e, otstup="")

        @bot.callback_query_handler(func=lambda call: True)
        def handle_callback(call):
            if call.data in data['callback']:
                actions = data['callback'][call.data]
                for action in actions:
                    try:
                        if 'time.sleep' in action:
                            time.sleep(action['time.sleep'])
                        if 'delete' in action:
                            message_id = call.message.message_id
                            delete_id = eval(action['delete'])
                            bot.delete_message(call.message.chat.id, delete_id)
                        if 'text' in action:
                            response_text = action['text']
                            if 'buttons' in action:
                                buttons = []
                                for button in action['buttons']:
                                    if 'type' in button:
                                        if button['type'] == 'url':
                                            buttons.append(telebot.types.InlineKeyboardButton(button['name'], url=button['url']))
                                        elif button['type'] == 'callback':
                                            buttons.append(telebot.types.InlineKeyboardButton(button['name'], callback_data=button['calldata']))
                                if buttons:
                                    markup = telebot.types.InlineKeyboardMarkup()
                                    markup.add(*buttons)
                                    bot.send_message(call.message.chat.id, response_text, reply_markup=markup)
                            else:
                                bot.send_message(call.message.chat.id, response_text)
                        if 'photo' in action:
                            photo_url = action['photo']
                            if 'buttons' in action:
                                buttons = []
                                for button in action['buttons']:
                                    if 'type' in button:
                                        if button['type'] == 'url':
                                            buttons.append(telebot.types.InlineKeyboardButton(button['name'], url=button['url']))
                                        elif button['type'] == 'callback':
                                            buttons.append(telebot.types.InlineKeyboardButton(button['name'], callback_data=button['calldata']))
                                if buttons:
                                    markup = telebot.types.InlineKeyboardMarkup()
                                    markup.add(*buttons)
                                    if 'caption' in action: caption = action['caption']; bot.send_photo(call.message.chat.id, photo_url, caption=caption,  reply_markup=markup)
                                    else: bot.send_photo(call.message.chat.id, photo_url, caption=caption,  reply_markup=markup)
                            else:
                                if 'caption' in action: caption = action['caption']; bot.send_photo(call.message.chat.id, photo_url, caption=caption)
                                else: bot.send_photo(call.message.chat.id, photo_url)
                        if 'video' in action:
                            video_url = action['video']
                            if 'buttons' in action:
                                buttons = []
                                for button in action['buttons']:
                                    if 'type' in button:
                                        if button['type'] == 'url':
                                            buttons.append(telebot.types.InlineKeyboardButton(button['name'], url=button['url']))
                                        elif button['type'] == 'callback':
                                            buttons.append(telebot.types.InlineKeyboardButton(button['name'], callback_data=button['calldata']))
                                if buttons:
                                    markup = telebot.types.InlineKeyboardMarkup()
                                    markup.add(*buttons)
                                    if 'caption' in action: caption = action['caption']; bot.send_photo(call.message.chat.id, video_url, caption=caption,  reply_markup=markup)
                                    else: bot.send_photo(call.message.chat.id, video_url, caption=caption,  reply_markup=markup)
                            else:
                                if 'caption' in action: caption = action['caption']; bot.send_photo(call.message.chat.id, video_url, caption=caption)
                                else: bot.send_photo(call.message.chat.id, photo_url)
                        if 'file' in action:
                            video_url = action['file']
                            if 'buttons' in action:
                                buttons = []
                                for button in action['buttons']:
                                    if 'type' in button:
                                        if button['type'] == 'url':
                                            buttons.append(telebot.types.InlineKeyboardButton(button['name'], url=button['url']))
                                        elif button['type'] == 'callback':
                                            buttons.append(telebot.types.InlineKeyboardButton(button['name'], callback_data=button['calldata']))
                                if buttons:
                                    markup = telebot.types.InlineKeyboardMarkup()
                                    markup.add(*buttons)
                                    if 'caption' in action: caption = action['caption']; bot.send_photo(call.message.chat.id, video_url, caption=caption,  reply_markup=markup)
                                    else: bot.send_photo(call.message.chat.id, video_url, caption=caption,  reply_markup=markup)
                            else:
                                if 'caption' in action: caption = action['caption']; bot.send_photo(call.message.chat.id, video_url, caption=caption)
                                else: bot.send_photo(call.message.chat.id, photo_url)
                    except Exception as e: vuvod_type_1(text=e, otstup="")

    bot.polling(timeout=999,long_polling_timeout=999)