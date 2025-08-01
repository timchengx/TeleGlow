from telegram import Update
from telegram.ext import ContextTypes
from constants import TG_BOT_TBD

async def all_on(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(TG_BOT_TBD)

async def all_off(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(TG_BOT_TBD)
