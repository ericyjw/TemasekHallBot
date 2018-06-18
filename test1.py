import telebot
import time
from telebot import types

bot_token = '594412308:AAHmqPmz4pJGIB_Wx85TQr8pmD9rcTobVYI'

bot = telebot.TeleBot(token=bot_token)
chatID_matricNum_dict = {}



@bot.message_handler(commands=['enter_matriculation_number'])
def send_welcome(message):
	##message.chat.id is the identification number in telegram terms of the user
	##do we need to validate it?
	sent = bot.send_message(message.chat.id, 'In your next message, enter your matriculation number') #sent is the message entered by the person which will be their matric number
	#goes to the next step or next function
	bot.register_next_step_handler(sent, saveNum)

def saveNum(message):
	#to find the previous input of the message.chat.id and message.txt and delete it in dictionary and textfile
	#this is to rewrite the previous input matric number by them, we don't want to have 2 matric number per telegram identification number
	openFile = open("matricNum.txt", 'r')
	lines = openFile.readlines()
	openFile.close()
	openFile = open("matricNum.txt", 'w')
	##removes the initial wrong chatID and the matric number
	for line in lines:
		if line.split()[0] != message.chat.id:
			openFile.write(line)
	openFile.close()
	open('matricNum.txt' ,'a').write(str(message.chat.id) + ' ' + message.text + '\n')
	##replaces the one in the dictionary as well
	chatID_matricNum_dict[message.chat.id] = message.text
	bot.send_message(message.chat.id, 'Your new matric number is saved!')
	
	
	
@bot.message_handler(commands=['start']) #this function will happen when the user types in /start
def send_welcome(message):
	bot.reply_to(message, 'Hi Temasekians I am your Dinner Number Generator')
	matricNum = bot.send_message(message.chat.id, 'Do enter your matriculation number')
	bot.register_next_step_handler(matricNum, saveFunc)

def saveFunc(message):
	open('matricNum.txt', 'a+').write(str(message.chat.id) + ' ' + message.text + '\n') #appends into a text file named message.text, make sure you have this message.txt in the same folder
	chatID_matricNum_dict[message.chat.id] = message.text                               #saves it in a dictionary too, just in case for later use
	bot.send_message(message.chat.id, 'Saved. Thank you for being a part of this')
	bot.send_message(message.chat.id, str(chatID_matricNum_dict[message.chat.id]))	    #sends a message containing their matriculation number
		
	

while (True):
	try:
		bot.polling()
	except Exception:
		time.sleep(15)

