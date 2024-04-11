from hoshino import Service, logger
from httpx import AsyncClient, Response
from nonebot import get_bot
from json import loads
from os import path
from pathlib import Path

with open(Path(path.dirname(__file__)) / "config.json","r" , encoding="utf-8") as f:
    URL = loads(f.read())["url"]

sv = Service("钓鱼", enable_on_default=True, visible=True)
client = AsyncClient()
bot = get_bot()

async def event_filter(group_id: int):
    # resp = await bot.get_group_member_list(group_id=group_id)
    # if bot.self_id in subs and main in [i["user_id"] for i in resp]:
    #     return True
    return True

@sv.on_fullmatch(("开始钓鱼", "结束钓鱼", "停止钓鱼", "钓鱼记录", "钓鱼统计"))
async def fish_handle(bot, ev):
    text = ev.message.extract_plain_text()
    if not text:
        return
    data = {"user_id": f"OneBot 11_{ev.user_id}", "message": text}
    try:
        resp: Response = await client.post(URL, json=data, timeout=60)
    except Exception as e:
        logger.error(str(e))
        return
    if resp.status_code == 200:
        message = resp.text
        if not message:
            return
        # if "header" in state:
        #     message = "".join([state["header"], message])
        await bot.send(ev, message)
        # matcher.stop_propagation()
