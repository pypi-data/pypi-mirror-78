from .models import CustomModelAdmin
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib import LogEntry, ADDITION, CHANGE, DELETION
import telebot
import os

bot = telebot.TeleBot(os.getenv('TELEGRAM_LOG_BOT_TOKEN', None))
chat_id = os.getenv('TELEGRAM_LOG_CHAT_ID', None)


@receiver(post_save, sender=LogEntry)
def bot_message(sender, instance, **kwargs):
    message = LogEntry.objects.last()
    bot.send_message(chat_id, str(message.change_message))
