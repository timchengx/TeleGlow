from typing import List, Dict, Optional
from pywizlight import wizlight, discovery
import asyncio, logging

logger = logging.getLogger(__name__)

WizBulbs = None

class WizBulbManager:
    def __init__(
        self,
        config_list: Optional[List[dict]] = None,
        wizlight_list: Optional[List[wizlight]] | None = None
    ) -> None:
        self.bulbs: Dict[str, wizlight] = {}

        if wizlight_list is not None:
            for i in wizlight_list:
                self.bulbs[i.ip] = i
        else:
            if config_list is not None:
                for i in config_list:
                    self.bulbs[i["name"]] = wizlight(i["ip"])

    @staticmethod
    async def discover_bulbs(broadcast_space: str = "192.168.1.255") -> List[wizlight]:
        bulbs = await discovery.discover_lights(broadcast_space=broadcast_space)
        return bulbs

    async def turn_on(self) -> None:
        await asyncio.gather(*[bulb.turn_on() for bulb in self.bulbs.values()])

    async def turn_off(self) -> None:
        await asyncio.gather(*[bulb.turn_off() for bulb in self.bulbs.values()])

def init_wiz_bulbs(config: dict) -> None:
    logger.info("Use %s mode to load bulb", config["init_mode"])
    global WizBulbs
    if config["init_mode"] == "discovery" and "discovery_broadcast_ip" in config:
        discovered_bulbs = asyncio.run(WizBulbManager.discover_bulbs())
        WizBulbs = WizBulbManager(wizlight_list=discovered_bulbs)
    elif config["init_mode"] == "static" and "wiz_bulb_ip" in config:
        WizBulbs = WizBulbManager(config_list=config["wiz_bulb_ip"])
    else:
        raise Exception("bulb config invalid")
