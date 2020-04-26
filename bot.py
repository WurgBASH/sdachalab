#! /usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater,CallbackQueryHandler,RegexHandler,ConversationHandler,Job 
import telegram
import os
import time
import imageio
import io
import telegram
import turtle
from time import sleep

t = turtle.Turtle()
t.pu()
t.setpos(0, 0)
t.seth(-90)
t.speed(0)
t.pd()

l = 200


inst = [-1, 0, -1]

#logging.basicConfig(level=logging.DEBUG)

TOKEN = "1151849911:AAHGIIGJuvGLp7DMhaij3uFJ5kmp1T99lfY"
PORT = int(os.environ.get('PORT', '43760'))
updater = Updater(token=TOKEN)
#-------------------------------------- 
dispatcher = updater.dispatcher

ANSWER1 = 1
ANSWER2 = 2
ANSWER3 = 3
#--------------------------------------
def Reset(i, p):
	t.clear()
	t.pu()
	t.setpos(-p, 0)
	t.pd()
	t.lt(-45*i)

def Draw():
	t.fd(l)
	for i in range(len(inst)):
		if(inst[i] == -1):
			t.lt(90)
			cv = turtle.getcanvas()
			cv.postscript(file="tmp/file_name"+str(i)+".ps", colormode='color')
		elif(inst[i] >= 1):
			t.rt(90*inst[i])
			cv = turtle.getcanvas()
			cv.postscript(file="tmp/file_name"+str(i)+".ps", colormode='color')
		t.fd(l)
		cv = turtle.getcanvas()
		cv.postscript(file="tmp/file_name"+str(i)+".ps", colormode='color')



def handleMessage(bot,update):
	msg = update.message.text
	chat_id = update.message.chat_id

def start(bot,update):
	msg = update.message.text
	chat_id = update.message.chat_id
	bot.send_message(chat_id, text='Привіт 😊, сьогодні я продемонструю вам побудову фракталу Крива Леві - цей фрактал був запропонований французьким математиком Полем Леві.')
	bot.send_message(chat_id, text='Фрактал будується наступним чином:\n🔹 Беруть половину квадрата виду /\\ \n🔹 Кожну сторону отриманої фігури замінюють таким же фрагментом.')
	bot.send_message(chat_id, text='Введіть кількість ітерацій, щоб я зміг побудувати фрактал 👇')
	return ANSWER1

def fraktal(bot,update):
	msg = update.message.text
	chat_id = update.message.chat_id
	for i in range(5):
		Reset(i, l)
		
		temp = inst
		temp.append(i+1)
		revTemp = inst[::-1]
		for o in range(len(inst)-1):
			temp.append(revTemp[o+1])

		inst = temp
		del(temp)
		del(revTemp)
		l /= 1.5

	Draw()
	buf = io.BytesIO()

	with imageio.get_writer('tmp/gw.gif', mode='I') as writer:
		for i in range(len(inst)):
			image = imageio.imread("tmp/file_name"+str(i)+".ps")
			writer.append_data(image)

	bot.send_animation(chat_id, animation=open('tmp/gw.gif','rb')) 




def cancel(bot,update):
	return ConversationHandler.END
#--------------------------------------
conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, handleMessage), CommandHandler('start', start)],

        states={
            ANSWER1: [MessageHandler(Filters.text, question4)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
dispatcher.add_handler(conv_handler)
dispatcher.add_handler(MessageHandler(Filters.text, handleMessage))



#--------------------------------------
if __name__ == '__main__':
	updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
	updater.bot.set_webhook("https://agrotender-1.herokuapp.com/" + TOKEN)
	updater.idle()
