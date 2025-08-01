import asyncio

from telegram import Update
from telegram.ext import ContextTypes
from constants import TG_BOT_TBD
from bulb import wiz

async def all_on(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    asyncio.gather(wiz.WizBulbs.turn_on())
    await update.message.reply_text(TG_BOT_TBD)

async def all_off(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    asyncio.gather(wiz.WizBulbs.turn_off())
    await update.message.reply_text(TG_BOT_TBD)
