from typing import List, Dict, Optional
from asyncio import run
from pywizlight import wizlight, discovery

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
        for bulb in self.bulbs.values():
            await bulb.turn_on()

    async def turn_off(self) -> None:
        for bulb in self.bulbs.values():
            await bulb.turn_off()
