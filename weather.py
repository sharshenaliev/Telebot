import telebot
from pyowm import OWM

token = "1105029676:AAFouNcKmqpe5MOJ5neACqwZD5w7pgLjFMU"
bot = telebot.TeleBot(token)

owm = OWM('4d7eae943b5e49b7962feaf80b0817d5')
mgr1 = owm.geocoding_manager()

@bot.message_handler(commands=['start', 'hi'])
def start_message(message):
    bot.send_message(message.chat.id, 'Введите широту и долготу через запятую:')

@bot.message_handler(content_types=['text'])
def send_sticker_on_sticker(message):
    coor = message.text.split(',')
    if len(coor) == 2:
        try:
            lat = float(coor[0])
            lon = float(coor[1])
            if lat >= -90 and lat <= 90 and lon >= -180 and lon <= 180:
                list_of_locations = mgr1.reverse_geocode(lat, lon)
                l = str(list_of_locations[0]).split(',')
                city = l[1].split('=')
                mgr2 = owm.weather_manager()
                observation = mgr2.weather_at_place(city[1])
                w = observation.weather
                wind = w.wind()
                h = w.humidity
                t = w.temperature('celsius')
                c = w.clouds
                
                bot.send_message(message.chat.id, 'температура - ' + str(t['temp']) + '°')
                bot.send_message(message.chat.id, 'влажность - ' + str(h) + '%')
                bot.send_message(message.chat.id, 'скорость ветра - ' + str(wind['speed']))
                bot.send_message(message.chat.id, 'облачность - ' + str(c) + '%')
            else:
                bot.send_message(message.chat.id, 'Введите широту и долготу через запятую правильно:')
        except:
            bot.send_message(message.chat.id, 'Введите широту и долготу через запятую правильно:')
    else:
        bot.send_message(message.chat.id, 'Введите широту и долготу через запятую правильно:')

bot.polling()
