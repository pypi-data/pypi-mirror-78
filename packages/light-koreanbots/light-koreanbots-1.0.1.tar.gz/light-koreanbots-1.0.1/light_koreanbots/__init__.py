"""
MIT License

Copyright (c) 2020 eunwoo1104

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import aiohttp
import asyncio
import logging

__version__ = "1.0.1"


class LKBClient:
    """
    light_koreanbots의 클라이언트입니다.
    모든 인자들은 keyword 형태로 전달되어야 합니다.
    :param bot: `discord.Client` 또는 `discord.ext.commands.Bot` 또는 이 두개 중에서 하나를 상속받은 클래스이어야 합니다.
    :param token: str. Koreanbots 토큰입니다.
    :param loop: asyncio 이벤트 루프입니다. 꼭 넣을 필요는 없습니다. 기본값은 asyncio.get_event_loop() 입니다.
    :param run_update: bool. 만약에 `False`일 경우 업데이트 태스크가 생성되지 않습니다. 기본값은 True 입니다.
    :param use_v2: bool. 나중을 위한 코드입니다. 지금은 기본값인 `False`로 둬야 합니다.
    """
    base_url_v1 = "https://api.koreanbots.dev/v1/bots/servers"
    base_url_v2 = "https://api.koreanbots.dev/v2/bots/servers" # v2 준비용

    def __init__(self, *, bot, token, loop=asyncio.get_event_loop(), run_update: bool = True, use_v2: bool = False):
        self.bot = bot
        self.token = token
        self.loop = loop
        self.logger = logging.getLogger('discord')
        self.base_url = self.base_url_v2 if use_v2 else self.base_url_v1
        self.before = 0
        if run_update:
            self.loop.create_task(self.__update())

    async def update(self):
        """
        Koreanbots에 길드 카운트를 업데이트하는 코루틴 함수입니다.
        :return: 리턴값 없음.
        """
        self.logger.debug("Posting guild count now...")
        if self.before == len(self.bot.guilds):
            self.logger.debug("Same guild count. Canceled.")
            return
        header = {"Content-Type": "	application/json", "token": self.token}
        body = {"servers": len(self.bot.guilds)}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, headers=header, json=body) as resp:
                ret = await resp.json()
                if ret["code"] == 200:
                    self.before = len(self.bot.guilds)
                    self.logger.info("Guild count post success.")
                elif ret["code"] == 429:
                    self.logger.debug("Rate limited, skipping.")
                else:
                    self.logger.error(f"Failed guild post count with code {ret['code']}. Message: {ret['message']}")

    async def __update(self):
        await self.bot.wait_for("ready")
        while not self.bot.is_closed():
            await self.update()
            await asyncio.sleep(60)
