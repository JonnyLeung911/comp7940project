from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import configparser
import logging
import redis
from ChatGPT_HKBU import HKBU_ChatGPT
import requests




#注意组建的导入目录,导入功能
from function.redis_handler import save_data, get_data
from function.tv_show_reviews import write_review, read_review
from function import hiking_route_sharing


def equiped_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def main():
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    # updater = Updater(token=(os.environ['ACCESS_TOKEN']),  use_context=True)
    dispatcher = updater.dispatcher
    global redis1
    redis1 = redis.Redis(host=(config['REDIS']['HOST']),
        password=(config['REDIS']['PASSWORD']),
        port=(config['REDIS']['REDISPORT']))
        
# You can set this logging module, so you will know when
# and why things do not work as expected Meanwhile, update your config.ini as:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    
# register a dispatcher to handle message: here we register an echo dispatcher
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)
    
    # dispatcher for chatgpt
    global chatgpt
    chatgpt = HKBU_ChatGPT(config)
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command),equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)
      
#在此添加回复的命令
# on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("Hello", hello))      #register a new command_handler
    
    

    # 注册数据库保存命令处理函数
    dispatcher.add_handler(CommandHandler("save", save_data))
    dispatcher.add_handler(CommandHandler("get", get_data))
    # 注册电影命令处理函数
    dispatcher.add_handler(CommandHandler("save_review", save_review))
    dispatcher.add_handler(CommandHandler("get_review", get_review))
    #注册路径分享命令
    # dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('save_hiking_route_description', hiking_route_sharing.save_hiking_route_description))
    dispatcher.add_handler(CommandHandler('share_hiking_route', hiking_route_sharing.share_hiking_route))

    
# To start the bot:
    updater.start_polling()
    updater.idle()
    
def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)
    # Define a few command handlers. These usually take the two arguments update and
    # context. Error handlers also receive the raised TelegramError object in error.

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')

def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0] # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')
        
def hello(update:Update, context: CallbackContext) -> None:
    name = context.args[0]
    reply_message = f"Good day,{name}!"
    update.message.reply_text(reply_message)
    
    
    
#电影评论功能
def save_review(update, context):
    try:
        tv_show = context.args[0]
        review = ' '.join(context.args[1:])
        
        write_review(tv_show, review)
        
        update.message.reply_text('Review saved successfully.')
    except IndexError:
        update.message.reply_text('Usage: /save_review <tv_show> <review>')

def get_review(update, context):
    try:
        tv_show = context.args[0]
        
        review = read_review(tv_show)
        
        if review:
            update.message.reply_text(f"Review for {tv_show}: {review}")
        else:
            update.message.reply_text(f"No review found for {tv_show}.")
    except IndexError:
        update.message.reply_text('Usage: /get_review <tv_show>')
        
        
        
        
         

        
if __name__ == '__main__':
    main()