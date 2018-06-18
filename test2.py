import telebot
import time
from telebot import types
from telebot import util

bot_token = '594412308:AAHmqPmz4pJGIB_Wx85TQr8pmD9rcTobVYI'

bot = telebot.TeleBot(bot_token)
chatID_matricNum_dict = {}



@bot.message_handler(commands=['enter_matriculation_number'])
def send_welcome(message):
	##message.chat.id is the identification number in telegram terms of the user
	##do we need to validate it?
	sent = bot.send_message(message.chat.id, 'In your next message, enter your matriculation number') #sent is the message entered by the person which will be their matric number
	#goes to the next step or next function
	bot.register_next_step_handler(sent, saveNum)

def saveNum(message):
	checkAndEditFile(message)
	#chatID_matricNum_dict[message.chat.id] = message.text
	bot.send_message(message.chat.id, 'Your new matric number is saved!')

def checkAndEditFile(message):
	#to find the previous input of the message.chat.id and message.txt and delete it in dictionary and textfile
	#this is to rewrite the previous input matric number by them, we don't want to have 2 matric number per telegram identification number
	openFile = open("matricNum.txt", 'r')
	lines = openFile.readlines()
	newMatricList = []
	for line in lines:
		if line.split()[0] != str(message.chat.id):
			newMatricList.append(line)
	openFile.close()
	openFile = open("matricNum.txt", 'w')
	##removes the initial wrong chatID and the matric number
	for line in newMatricList:
		openFile.write(line)
	openFile.close()
	open('matricNum.txt' ,'a+').write(str(message.chat.id) + ' ' + message.text + '\n')
	##replaces the one in the dictionary as well
	chatID_matricNum_dict[message.chat.id] = message.text

def validateMatricNum(message):
	matricNum = str(message.text)
	bot.send_message(message.chat.id, matricNum)
	if (len(matricNum) != 9 or matricNum[0].upper() != 'A' or matricNum[-1].isalpha() == False or matricNum[1:-1].isdigit() == False):
 		bot.send_message(message.chat.id, "Your Matric Number is Invalid")
		bot.send_message(message.chat.id, "Please enter /start again to reenter your matriculation number")
	else:
		saveFunc(message)
		

@bot.message_handler(commands=['start']) #this function will happen when the user types in /start
def send_welcome(message):
	#bot.reply_to(message, 'Hi Temasekian {} {} I am your Dinner Number Generator'.format("Eric", "Yang"))
	bot.send_message(message.chat.id, 'Hi Temasekian {} {} I am your Dinner Number Generator'.format(str(message.from_user.first_name), str(message.from_user.last_name)))
	matricNum = bot.send_message(message.chat.id, 'Do enter your matriculation number')
	bot.register_next_step_handler(matricNum, validateMatricNum)
	

def saveFunc(message):
	checkAndEditFile(message)
	chatID_matricNum_dict[message.chat.id] = message.text                       #saves it in a dictionary too, just in case for later use
	bot.send_message(message.chat.id, 'Your matriculation ID is saved as {}.'.format(str(chatID_matricNum_dict[message.chat.id])))	
	bot.send_message(message.chat.id, 'Thank you for using this Bot.')   
	#sends a message containing their matriculation number
		

while (True):
	try:
		bot.polling()	
	except Exception:
		time.sleep(15)

