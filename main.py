#!/usr/bin/env python
import asyncio, logging, yaml, sys, signal, os

from bulb.wiz import init_wiz_bulbs
from constants import TG_BOT_DESCRIPTION, TG_BOT_COMMANDS

from telegram.ext import Application, CommandHandler

formatter = logging.Formatter("%(asctime)s - [%(levelname)-8s] %(message)s [%(module)s/%(funcName)s]")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logger.setLevel(log_level)

# set higher logging level for httpx to avoid all GET and POST requests flood
logging.getLogger("httpx").setLevel(logging.WARNING)


application = None
bulb_manager = None
config = None

async def bot_init(token: str) -> Application:
    application = Application.builder().token(token).build()

    from telegram_bot.commands import all_on, all_off   # load after bulb manager init
    application.add_handler(CommandHandler("all_on", all_on))
    application.add_handler(CommandHandler("all_off", all_off))

    await application.bot.set_my_short_description(TG_BOT_DESCRIPTION)
    await application.bot.set_my_commands(TG_BOT_COMMANDS)

    return application

async def start_telegram_bot(config: dict = {}) -> None:
    try:
        application = await bot_init(config["token"])

        await application.initialize()
        await application.updater.start_webhook(
            listen='0.0.0.0',
            port=config["port"],
            webhook_url=config["webhook_url"]
        )
        await application.start()

        def shutdown_handler():
            logger.info("Shutdown initiated")
            stop_event.set()

        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, shutdown_handler)

        stop_event = asyncio.Event()
        await stop_event.wait()

    except Exception as e:
        logger.critical(f"init fail: {e}")
        sys.exit(1)

    finally:
        if application:
            await application.updater.stop()
            await application.stop()
            await application.shutdown()

async def start_app(config: dict) -> None:
    await init_wiz_bulbs(config["bulb"])
    await start_telegram_bot(config["telegram"])

def main() -> None:
    try:
        with open("./config.yml", "r") as f:
            config = yaml.safe_load(f)
            logging.debug(config)
        logger.info("Config file loaded")

        if "telegram" not in config or "bulb" not in config:
            raise Exception("config invalid")

        logger.info("Initializing")
        asyncio.run(start_app(config))

    except Exception as e:
        logger.critical(f"init fail: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
