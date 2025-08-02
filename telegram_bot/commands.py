import asyncio

from telegram import Update
from telegram.ext import ContextTypes
from constants import TG_BOT_MSG_ON, TG_BOT_MSG_OFF
from bulb import wiz
from telegram_bot.utils import validate_user

@validate_user
async def all_on(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    asyncio.gather(wiz.WizBulbs.turn_on())
    reply = update.message if update.message else update.edited_message
    if reply:
        await reply.reply_text(TG_BOT_MSG_ON)

@validate_user
async def all_off(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    asyncio.gather(wiz.WizBulbs.turn_off())
    reply = update.message if update.message else update.edited_message
    if reply:
        await reply.reply_text(TG_BOT_MSG_OFF)
