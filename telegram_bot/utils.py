from functools import wraps
from typing import Dict
from telegram import Update
from constants import TG_BOT_MSG_NONO
import logging

logger = logging.getLogger(__name__)

Users = []

def validate_user(func):

    @wraps(func)
    async def wrapper(update: Update, *args, **kwargs):
        if not Users:
            # no users loaded - allow all incoming command
            return await func(update, *args, **kwargs)
        if update.effective_user is None or update.effective_user.id not in Users:
            logger.info(f"{update.effective_user.id} try to use not allowed command")
            reply = update.message if update.message else update.edited_message
            if reply:
                await reply.reply_text(TG_BOT_MSG_NONO)
            return
        return await func(update, *args, **kwargs)

    return wrapper

def load_authorized_users(user_id: Dict) -> None:
    global Users
    Users = user_id
    logger.info("Authorized users loaded")
