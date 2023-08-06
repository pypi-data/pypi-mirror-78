import traceback

from telethon import TelegramClient, events, connection

from consts import LVL2H


def prepareClient(name, api_id, api_hash, token, proxy=None, loop=None):
    c = connection.tcpfull.ConnectionTcpFull if not proxy else connection.ConnectionTcpMTProxyAbridged
    return TelegramClient(
        name, api_id, api_hash,
        connection=c,
        proxy=proxy,
        loop=loop,
        auto_reconnect=True,
    ).start(bot_token=token)


class Bot:
    def __init__(self, tg_client, subscribers):
        self._tg_client = tg_client
        self._subscribers = subscribers

    async def on_cmd_list(self, event):
        sid_cur = event.chat_id
        try:
            res = [(project, lvl) for project, (sid, lvl) in self._subscribers._store_iter() if sid == sid_cur]
            if res:
                res.sort(key=lambda o: o[0])
                res = '\n'.join(
                    f'Project `[{p}]` on {", ".join(LVL2H[i] for i in range(1, lvl + 1))}.' for p, lvl in res)
            else:
                res = 'No subscriptions.'
            await event.respond(res)
        except Exception:
            await event.respond(f"**ERROR**\n```{traceback.format_exc()}```")
        raise events.StopPropagation

    async def on_cmd_sub(self, event):
        sid = event.chat_id
        p = event.pattern_match.group(1).split(' ')
        project = p[0]
        lvl = int(p[1]) if len(p) > 1 else 3
        try:
            await self._subscribers.sub(sid, project, lvl)
            s = ', '.join(LVL2H[i] for i in range(1, lvl + 1))
            await event.respond(f"Subscribed for project `[{project}]`({s})!")
        except Exception:
            await event.respond(f"**ERROR**\n```{traceback.format_exc()}```")
        raise events.StopPropagation

    async def on_cmd_unsub(self, event):
        sid = event.chat_id
        project = event.pattern_match.group(1)
        try:
            await self._subscribers.unsub(sid, project)
            await event.respond(f"Unsubscribed from project `[{project}]`!")
        except Exception:
            await event.respond(f"**ERROR**\n```{traceback.format_exc()}```")
        raise events.StopPropagation

    def _prepare_handlers(self):
        self._tg_client.add_event_handler(self.on_cmd_sub, events.NewMessage(pattern='/sub (.+)'))
        self._tg_client.add_event_handler(self.on_cmd_unsub, events.NewMessage(pattern='/unsub (.+)'))
        self._tg_client.add_event_handler(self.on_cmd_list, events.NewMessage(pattern='/list'))

    def init(self):
        self._prepare_handlers()
