from extensions import CriptoConverter, ConvertionExeption
from config import TOKEN, keys
import telebot

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])

def start(massage: telebot.types.Message):
    text_1 = f'Hello, my young investor, {massage.chat.username}!'\
        f'\nHere you can convert some currency. If you want to know which currency you can '\
        f'convert you need to write \n"/value"'
    bot.reply_to(massage, text_1)


@bot.message_handler(commands=['value'])
def values(massage: telebot.types.Message):
    text = f' You can convert these currency:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(massage, text)
    text_2 = 'If you want to start the conversion, you need to write commands in this format: ' \
             '\n<currency name to convert>' \
             '\n<what currency you want to convert to>' \
             '\n<conversion amount>\nthrough a space' \
             '\nExample: Euro Dollar 100'
    bot.reply_to(massage, text_2)


@bot.message_handler(content_types=['text'])
def convert(massage: telebot.types.Message):
    try:
        values = massage.text.split(' ')
        if len(values) != 3:
            raise ConvertionExeption('To many elements. Try one more time.')

        quote, base, amount = values
        total_base = CriptoConverter.get_price(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(massage, f'user error.\n{e}')
    except Exception as e:
        bot.reply_to(massage, f'failed to process command.\n{e}')
    else:
        text = f'Prise of {amount} {quote} in {base} - {float(total_base) * float(amount)}'
        bot.send_message(massage.chat.id, text)


bot.polling(none_stop=True)