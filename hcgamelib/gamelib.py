from .const import *
from typing import Union, Dict
import json, websocket, time, random, os, sys, threading, logging, traceback

def roll(list_: list):
    try: return random.choice(list_)
    except: return None
            
class Game:
    def __init__(self, nick: str, channel_ws_dict: Dict[str, Union[websocket.WebSocket, websocket.WebSocketApp]], prefix: str='|', owner: list=['AAfFKK','VEbeHK','coBad2','eYFDHl'], status: dict=True):
        """"""
        self.nick = nick
        self.cwd = channel_ws_dict
        self.prefix = prefix
        self.owner = owner
        self.status = status
        self.games = list()
        self.game_dict = {'werewolves': self.werewolves, 'uno': self.uno}
        self.running = {'werewolves': False, 'uno': False}
        self.init_dict = {'werewolves': self._init_werewolves, 'uno': self._init_uno}
        """
        self.LINE = {
            "真心话": self._truth,
            "结算": self._atLast,
            "结束游戏": self._endTruth,
            "*bom": self._bom,
        }
        """
    class AlreadyStartedError(Exception):
        def __init__(self, game):
            self.message = f'{game} already started'
            super().__init__(self.message)
    class AlreadyEndedError(Exception):
        def __init__(self, game):
            self.message = f'{game} already ended'
            super().__init__(self.message)
    """
    def _bom(self) -> str:
        if not bombs[5]:
            if not self.nick in bombs[1]:
                bombs[1].append(nick)
                return "已成功添加机器人进入游戏！"
            else:
                return "机器人已经加入过了！"
        else:
            return "这局已经开始了，等下局吧~"

    def _truth(self) -> str:
        if not truthList[0]:
            truthList[0] = True
            return GAMEMENU
        else:
            return "已经在玩了哦╮(╯_╰)╭"

    def _atLast(self) -> str:
        if truthList[0]:
            if len(truthList[2]) < 2: return "有句话叫什么，一个巴掌拍不响(°o°；)"
            else:
                sort = sorted(truthList[1].items(), key=lambda x: x[1])
                loser, winner = sort[0], sort[-1]
                fin = "\n".join([
                    f"本轮参与人数：{len(truthList[1])}。",
                    f"最大：{winner[1]}（{winner[0]}），",
                    f"最小：{loser[1]}（{loser[0]}）。",
                    f"@{winner[0]} 向@{loser[0]} 提问，@{loser[0]} 回答。"
                ])
                truthList[1] = {}
                truthList[2] = []
                return fin
        else:
            return "真心话还没开始你在结算什么啊(▼皿▼#)"

    def _endTruth(self) -> str:
        if truthList[0]:
            truthList[0] = False
            return "好吧好吧，结束咯(一。一;;）"
        return "真心话还没开始你在结束什么啊(▼皿▼#)"
"""
    def dsend(self, msg: str, channel: str=True) -> None:
        if channel != True and self.status != True and not self.status.get(channel, None):
            return
        if channel == True:
            for chan in self.cwd:
                if self.status.get(chan, None):
                    self.dsend(msg, chan)
        elif channel in self.cwd:
            ws = self.cwd[channel]
            try:
                ws.send(json.dumps({'cmd':'chat','text':str(msg)}))
            except:
                time.sleep(5)
                self.dsend(msg, channel)
        else:
            raise ValueError

    def handle(self,data):
        channel = data.get('channel', None)
        for game in self.games:
            if self.status == True or self.status.get(channel, None):
                game(data)

    def start(self, name):
        """name must be in ['werewolves', 'uno']"""
        if name in self.game_dict:
            game = self.game_dict[name]
            if not self.running[name]:
                self.games.append(game)
                self.running[name] = True
                self.init_dict[name]()
            else:
                raise self.AlreadyStartedError(name)
        else:
            raise ValueError("name must be in ['werewolves', 'uno']")
    
    def end(self, name):
        """name must be in ['werewolves', 'uno']"""
        if name in self.game_dict:
            game = self.game_dict[name]
            if self.running[name]:
                self.games.remove(game)
                self.running[name] = False
                self.init_dict[name]()
            else:
                raise self.AlreadyEndedError(name)
        else:
            raise ValueError("name must be in ['werewolves', 'uno']")

    def _init_uno(self):
        unos[0] = False
        unos[1] = []
        unos[2] = []
        unos[6] = {}

    def uno(self, wss):
        # UNO
        def initialize_card():
            unos[3] = []
            for j in "红黄蓝绿":
                for i in range(1, 10):
                    unos[3].append(j + str(i))
                    unos[3].append(j + str(i))
                for i in ["+2", "禁", "转向"]:
                    unos[3].append(j + i)
                    unos[3].append(j + i)
                unos[3].append(j + "0")
            for i in range(4):
                unos[3].append("+4")
                unos[3].append("变色")
        def endUno():
            unos[0] = False
            unos[1] = []
            unos[2] = []
            unos[6] = {}
        def no_card(num):
            if len(unos[3]) < num:
                initialize_card()
                for i in unos[2]:
                    for j in i:
                        unos[3].remove(j)
                self.dsend('牌没了，已重新洗牌。')
        def sort_uno(cards: list) -> list:
            return sorted(cards,key=lambda x: UNO_SORT[x])
        if wss.get('cmd') == 'chat':
            msg = wss['text']
            sender = wss['nick']
            channel = wss['channel']
            if msg == "uno":
                if unos[0]:
                    self.dsend("游戏已经开始了，等下一轮吧。", channel)
                elif sender in unos[1]:
                    self.dsend("你已经加入了！", channel)
                else:
                    unos[1].append(sender)
                    unos[6].update({sender: channel})
                    self.dsend(f"{sender}加入成功，现在有{len(unos[1])}人。")
                    if len(unos[1]) == 8:
                        _start_uno()
            elif (msg == "开始u" or len(unos[1]) == 8) and not unos[0] and sender in unos[1] and channel == unos[6][sender]:
                def _start_uno():
                    if len(unos[1]) == 8:
                        self.dsend('人数达到上限，游戏自动开始！')
                    unos[0] = True
                    initialize_card()
                    for i in range(len(unos[1])):
                        playerCard = []
                        for j in range(7):
                            addCard = random.choice(unos[3])
                            playerCard.append(addCard)
                            unos[3].remove(addCard)
                        unos[2].append(playerCard)
                        self.dsend(f"/w {unos[1][i]} 这是你的牌：{'，'.join(sort_uno(playerCard))}", unos[6][unos[1][i]])
                    unos[4] = random.choice(unos[1])
                    while unos[5] == "+4":
                        unos[5] = random.choice(unos[3])
                    unos[3].remove(unos[5])
                    self.dsend(f"牌发完啦，{UNORULE}\n初始牌是=={unos[5]}==，请`{unos[4]}`先出！")
                if len(unos[1]) >= 2:
                    _start_uno()
                else:
                    self.dsend("人数不够！", channel)
            elif msg == "结束u" and sender in unos[1] and unos[0] and channel == unos[6][sender]:
                endUno()
                self.dsend("结束了...")
            elif msg[:2] == "u " and sender == unos[4] and channel == unos[6][sender]:
                msgList = msg.split(" ")
                card = msgList[1]
                id_ = unos[1].index(sender)
                nextid = (id_ + 1) % len(unos[1])
                next2id_ = (id_ + 2) % len(unos[1])
                if card == "check":
                    return self.dsend(f"/w {sender} 现在牌面上的牌是=={unos[5]}==，这是你的牌：{'，'.join(sort_uno(unos[2][id_]))}", unos[6][sender])
                elif card == '.':
                    addCard = random.choice(unos[3])
                    unos[3].remove(addCard)
                    if addCard[0] == unos[5][0] or addCard[1:] == unos[5][1:] or unos[5] == '变色':
                        unos[5] = addCard
                        if addCard[1:] == '禁':
                            unos[4] = unos[1][next2id_]
                            self.dsend(f'`{sender}`补到了{addCard}并将其打出，`{unos[1][nextid]}`跳过1轮，轮到`{unos[4]}`！')
                        elif addCard[1:] == '+2':
                            unos[4] = unos[1][next2id_]
                            no_card(2)
                            for i in range(2):
                                addCard_ = random.choice(unos[3])
                                unos[2][nextid].append(addCard_)
                                unos[3].remove(addCard_)
                            self.dsend(f'`{sender}`补到了=={addCard}==并将其打出，`{unos[1][nextid]}`加2张，轮到`{unos[4]}`！')
                            self.dsend(f"/w {unos[1][nextid]} 你新增了2张牌，这是你现在的牌：{'，'.join(sort_uno(unos[2][nextid]))}。", unos[6][unos[1][nextid]])
                        elif addCard[1:] == '转向':
                            unos[1].reverse()
                            unos[2].reverse()
                            unos[4] = unos[1][(-id_)%len(unos[1])]
                            id_ = (-id_-1)%len(unos[1])
                            self.dsend(f'`{sender}`补到了{addCard}并将其打出，==顺序转换==，轮到`{unos[4]}`！')
                        else:
                            unos[4] = unos[1][nextid]
                            self.dsend(f'`{sender}`补到了=={addCard}==并将其打出，轮到`{unos[4]}`！')
                    else:
                        unos[4] = unos[1][nextid]
                        unos[2][id_].append(addCard)
                        self.dsend(f'`{sender}`补了一张牌，轮到`{unos[4]}`！')
                        self.dsend(f"/w {sender} 你新增了1张牌，这是你现在的牌： {'，'.join(sort_uno(unos[2][id_]))}。", unos[6][sender])
                    return
                elif not card in unos[2][id_]:
                    return self.dsend("你没有那张牌！", channel)
                elif card == "+4":
                    for i in unos[2][id_]:
                        if i[0] == unos[5][0]:
                            return self.dsend("不符合规则！", channel)
                    if len(msgList) < 3:
                        return self.dsend("缺少参数！", channel)
                    if not msgList[2] in "红黄蓝绿":
                        return self.dsend("参数错误！", channel)
                    unos[5] = msgList[2] + "?"
                    unos[4] = unos[1][next2id_]
                    no_card(4)
                    for i in range(4):
                        addCard = random.choice(unos[3])
                        unos[2][nextid].append(addCard)
                        unos[3].remove(addCard)
                    self.dsend(f"`{sender}`出了+4（王牌），`{unos[1][nextid]}`加四张，颜色变为=={msgList[2]}==，轮到`{unos[4]}`！")
                    self.dsend(f"/w {unos[1][nextid]} 你新增了4张牌，这是你现在的牌：{'，'.join(sort_uno(unos[2][nextid]))}。", unos[6][unos[1][nextid]])
                elif card == "变色":
                    if len(msgList) < 3:
                        return self.dsend("缺少参数！", channel)
                    if msgList[2] not in "红黄蓝绿":
                        return self.dsend("参数错误！", channel)
                    unos[4] = unos[1][nextid]
                    unos[5] = msgList[2] + "?"
                    self.dsend(f"`{sender}`出了变色牌，颜色变为=={msgList[2]}==，轮到`{unos[4]}`！")
                elif card[0] == unos[5][0] or card[1:] == unos[5][1:] or unos[5] == "变色":
                    unos[5] = card
                    if card[1:] == "禁":
                        unos[4] = unos[1][next2id_]
                        self.dsend(f"`{sender}`出了{card}，`{unos[1][nextid]}`跳过1轮，轮到`{unos[4]}`！")
                    elif card[1:] == "+2":
                        unos[4] = unos[1][next2id_]
                        no_card(2)
                        for i in range(2):
                            addCard = random.choice(unos[3])
                            unos[2][nextid].append(addCard)
                            unos[3].remove(addCard)
                        self.dsend(f"`{sender}`出了=={card}==，`{unos[1][nextid]}`加2张，轮到`{unos[4]}`！")
                        self.dsend(f"/w {unos[1][nextid]} 你新增了2张牌，这是你现在的牌：{'，'.join(sort_uno(unos[2][nextid]))}。", unos[6][unos[1][nextid]])
                    elif card[1:] == "转向":
                        unos[1].reverse()
                        unos[2].reverse()
                        unos[4] = unos[1][(-id_)%len(unos[1])]
                        id_ = (-id_-1)%len(unos[1])
                        self.dsend(f"`{sender}`出了{card}，==顺序转换==，轮到`{unos[4]}`！")
                    else:
                        unos[4] = unos[1][nextid]
                        self.dsend(f"`{sender}`出了=={card}==，轮到`{unos[4]}`！")
                elif card not in ["+4", "变色"]:
                    return self.dsend("不符合规则！", channel)
                unos[2][id_].remove(card)
                if len(unos[2][id_]) == 1:
                    self.dsend(f"`{sender}`==UNO==了！！！")
                elif len(unos[2][id_]) == 0:
                    endUno()
                    self.dsend(f"`{sender}`获胜，游戏结束。")
                    return
                no_card(1)

    def poker(self):
        pass

    def bomber(self):
        pass

    def truth(self):
        pass

    def chess(self):
        pass
    
    def _init_werewolves(self):
        werewolf[0].clear()
        werewolf[0]["uwu"]=False

    def werewolves(self,wss):
        # nick:昵称 state:状态
        def chan(nick,state=False):
            werewolf[0]["state"][state].append(werewolf[0]["state"][not state].pop(werewolf[0]["state"][not state].index(nick)))
            werewolf[0]["core"][nick][3]=state
            if not state and nick in werewolf[0]["msg"]:
                time.sleep(1)
                self.dsend(f"/me >\n这时 [{nick}](https://){roll(werewolf[3][9])}的遗言被发现了\n[{nick}]：[{werewolf[0]['msg'][nick]}]")
        try:
            if "cmd" in wss:
                cmd=wss["cmd"]
                channel = wss.get('channel',None)
                if cmd=="chat":
                    nick=wss["nick"]
                    text=wss["text"]
                    if text==f"{self.prefix}help":
                        self.dsend(f"/me >\n·\n[【{werewolf[8]['game']}】](https://)\n开发者：纸片君ee(PAPEREE)\n贡献者：jiangmuran(jmr)\n移植者：Doppelganger(DPG)\n版本号：awa.1.09\n·\n使用手册\n查看帮助：{self.prefix}help\n查看规则：{self.prefix}rule\n获取权限：{self.prefix}root\n开始游戏：{self.prefix}start", channel)
                    elif text==f"{self.prefix}rule":
                        note=str()
                        if werewolf[0]["uwu"]:
                            note+=f"\n·\n卡牌设置({len(werewolf[0]['group'])}人局)：\n[【{werewolf[2][1][0]}】](https://)x{werewolf[0]['group'].count(1)}\n[【{werewolf[2][2][0]}】](https://)x{werewolf[0]['group'].count(2)}\n[【{werewolf[2][3][0]}】](https://)x{werewolf[0]['group'].count(3)}\n[【{werewolf[2][4][0]}】](https://)x{werewolf[0]['group'].count(4)}"
                        true="".join([f"[【{werewolf[2][_][0]}】](https://)" for _ in werewolf[2] if _ and werewolf[2][_][-1]])
                        false="".join([f"[【{werewolf[2][_][0]}】](https://)" for _ in werewolf[2] if _ and not werewolf[2][_][-1]])

                        self.dsend(f"/me >\n·\n主要卡牌：\n{true}/[【{werewolf[2][0][True]}】](https://)\n{false}/[【{werewolf[2][0][False]}】](https://)\n{note}\n·\n限制时长：\n[【{werewolf[2][2][0]}】](https://)1分钟\n[【{werewolf[2][3][0]}】](https://)2分钟\n[【{werewolf[2][4][0]}】](https://)1分钟\n白天投票共4分钟\n·\n游戏特性：\n[【{werewolf[2][1][0]}】](https://)擅长推理\n[【{werewolf[2][2][0]}】](https://)记性很好\n[【{werewolf[2][3][0]}】](https://)杀人不受限制\n[【{werewolf[2][4][0]}】](https://)不会猝死", channel)

                    elif text[:5]==f"{self.prefix}root":
                        if wss.get('trip') in self.owner:
                            if text==f"{self.prefix}root":
                                self.dsend(f"/me >\n[{nick}](https://)成功获取root权限", channel)

                                time.sleep(1)
                                self.dsend(f"/w {nick} >\n·\n可变更项：\n卡牌(card) 阵营(camp) 药水(potion) 牌组(group) 其他(other)\n·\n变更说明：\n卡牌：牌序(1~4) 牌名(str) 阵营(1/0)\n阵营：正方阵营名(str) 反方阵营名(str)\n药水：好坏(1/0) 药名(str) 状态(str)\n牌组：牌序(1~4)\n其他：发起者称呼(str) 玩家称呼(str) 游戏名(str)", channel)

                            else:
                                try:
                                    slices=[_.split(" ") for _ in text.split("\n")]
                                    order=slices[0][-1]
                                    note="变更执行成功"

                                    if order=="card":
                                        for _ in slices[1:]:
                                            if int(_[0]):
                                                werewolf[2][int(_[0])]=[_[1],werewolf[2][int(_[0])][1],bool(int(_[2]))]

                                    elif order=="camp":
                                        werewolf[2][0]={True:slices[1][0],False:slices[1][1]}

                                    elif order=="potion":
                                        for _ in slices[1:]:
                                            werewolf[7][bool(int(_[0]))]=[_[1],_[2]]

                                    elif order=="group":
                                        uwu=[int(_) for _ in slices[1] if _ in ["1","2","3","4"]]
                                        werewolf[1]=uwu

                                        if werewolf[0].get("group"):
                                            werewolf[0]["group"]=uwu

                                    elif order=="other":
                                        werewolf[8]={'op':slices[1][0],'core':slices[1][1],'game':slices[1][2]}

                                    else:
                                        note="找不到此变更项"

                                    self.dsend(f'/me >\n{note}', channel)

                                except:
                                    self.dsend("/me >\n执行时出现错误", channel)
                        else:
                            self.dsend(f"/me quq", channel)

                    elif text==f"{self.prefix}start":
                        if werewolf[0]["uwu"]:
                            if werewolf[0].get('core'):
                                self.dsend(f"/me >\n[【{werewolf[8]['game']}】](https://)已经开始了", channel)

                            else:
                                self.dsend(f"/me >\n[【{werewolf[8]['op']}】](https://)正在清点村里人数", channel)

                        else:
                            werewolf[0]={"uwu":True,"owner":{'nick':nick, 'channel': channel},"group":werewolf[1],"time":round(time.time()),"round":0,"temp":{},"core":{},"state":{True:[],False:[]},"sudden":[],"prophet":[],"werewolf":{"skip":False,"core":[],"wait":[],"kill":[],"dead":[]},"witch":{"med":{True:[True,True],False:[False,True]},"temp":[],"allow":[]},"day":{"wait":[],"kill":[],"dead":[]},"msg":{},"now":[]}
                            self.dsend(f"/me >\n新的[【{werewolf[8]['op']}】](https://)诞生了 美好的夜晚要开始了")

                            time.sleep(1)
                            uvu=" ".join([str(uwu) for uwu in werewolf[1]])
                            self.dsend(f"/w {nick} >\n·\n[【{werewolf[8]['op']}】](https://)[{nick}](https://)\n现在你可以选择改变牌组 否则为默认\n·\n卡牌详情：\n1.[【{werewolf[2][1][0]}】](https://)\n2.[【{werewolf[2][2][0]}】](https://)\n3.[【{werewolf[2][3][0]}】](https://)\n4.[【{werewolf[2][4][0]}】](https://)\n·\n默认牌组({len(werewolf[1])}人局)：\n{uvu}\n·\n设置方法：\n/w {self.nick} 牌组", channel)

                            time.sleep(0.5)
                            self.dsend(f"/me >\n[【{werewolf[8]['op']}】](https://)开始清点村里人数 请用{self.prefix}1报数")
                    
                            # 自动判断人数
                            def auto():

                                # 主循环
                                def loop():
                                    # nick:昵称 state:状态
                                    def chan(nick,state=False):
                                        werewolf[0]["state"][state].append(werewolf[0]["state"][not state].pop(werewolf[0]["state"][not state].index(nick)))
                                        werewolf[0]["core"][nick][3]=state
                                        if not state and nick in werewolf[0]["msg"]:
                                            time.sleep(1)
                                            self.dsend(f"这时 [{nick}]{roll(werewolf[3][9])}的遗言被发现了\n[{nick}]：[{werewolf[0]['msg'][nick]}]")
                                    try:
                                        while self.running['werewolves']:
                                            werewolf[0]["round"]+=1
                                            werewolf[0]["werewolf"]["skip"]=False
                                            werewolf[0]["day"]={"wait":[],"kill":[],"dead":werewolf[0]["day"]["dead"]}

                                            ava=list(werewolf[0]["core"].values())
                                            werewolf[0]["state"]={True:[uvu[0] for uvu in ava if uvu[3]],False:[uvu[0] for uvu in ava if not uvu[3]]}

                                            time.sleep(4)
                                            self.dsend(f"/me >\n[【回合{werewolf[0]['round']}】](https://)天黑请闭眼")

                                            for awa in werewolf[0]["core"]:
                                                uwu=werewolf[0]["core"][awa]

                                                if uwu[1]==2:
                                                    time.sleep(2)
                                                    self.dsend(f"/me >\n[【{werewolf[2][2][0]}】](https://)请睁眼")

                                                    if uwu[3]:
                                                        alive=[uvu for uvu in werewolf[0]["state"][True] if uvu!=uwu[0]]
                                                        random.shuffle(alive)
                                                        ovo=" ".join([f"[{uvu}](https://)" for uvu in alive])
                                                        owo="\n".join([f"[【{werewolf[2][werewolf[0]['core'][uvu][1]][0]}】](https://)/[【{werewolf[2][0][werewolf[0]['core'][uvu][2]]}】](https://)[{uvu}](https://)" for uvu in werewolf[0]["prophet"]])
                                                        

                                                        werewolf[0]["now"]=[uwu[1],uwu[0]]

                                                        time.sleep(1)
                                                        self.dsend(f"/w {uwu[0]} >\n·\n[【{werewolf[2][2][0]}】](https://)/[【{werewolf[2][0][True]}】](https://)[{uwu[0]}](https://)\n现在你可以选择一位村民得知身份\n请在1分钟内做出选择\n·\n已知身份：\n你自己{owo}\n·\n选择方法：\n/w {self.nick} 对象\n·\n可选对象：\n{ovo}", uwu[4])

                                                        for _ in range(60):
                                                            time.sleep(1)

                                                            if werewolf[0]["now"][0]!=uwu[1]:
                                                                break

                                                        else:
                                                            chan(uwu[0])
                                                            werewolf[0]["sudden"].append(uwu[0])

                                                            time.sleep(1)
                                                            self.dsend(f"/me >\n[【{werewolf[2][2][0]}】](https://)[{uwu[0]}](https://)在今晚{roll(werewolf[3][1])} 突然猝死")

                                                    else:
                                                        time.sleep(random.randint(10,50))
                                                        self.dsend(f"/me >\n[【{werewolf[2][2][0]}】](https://){roll(werewolf[4][4])}")

                                                elif uwu[3]==3 and not werewolf[0]["werewolf"]["skip"]:
                                                    time.sleep(2)
                                                    self.dsend(f"/me >\n[【{werewolf[2][3][0]}】](https://)请睁眼")

                                                    if uwu[3]:
                                                        alive=list(werewolf[0]["state"][True])
                                                        random.shuffle(alive)
                                                        ovo=" ".join([f"[{uvu}](https://)" for uvu in alive])

                                                        note=[uvu for uvu in werewolf[0]["core"] if werewolf[0]["core"][uvu][1]==3 and werewolf[0]["core"][uvu][3]]
                                                        werewolf[0]["werewolf"]={"skip":True,"core":note,"wait":note,"kill":[],"dead":werewolf[0]["werewolf"]["dead"]}
                                                        werewolf[0]["now"]=[uwu[3],werewolf[0]["werewolf"]["core"]]

                                                        for uvu in werewolf[0]["werewolf"]["core"]:
                                                            time.sleep(1)
                                                            owo=" ".join([f"[{aua}](https://)" for aua in werewolf[0]["werewolf"]["core"] if aua!=uvu])

                                                            if owo:
                                                                owo=f"\n·\n你的同伴：\n{owo}"

                                                            self.dsend(f"/w {uvu} >\n·\n[【{werewolf[2][3][0]}】](https://)/[【{werewolf[2][0][False]}】](https://)[{uvu}](https://)\n现在你可以选择一位村民杀死\n狼群只有意见统一才会行动\n请在2分钟内做出选择{owo}\n·\n选择方法：\n/w {self.nick} 对象\n·\n可选对象：\n{ovo}", werewolf[0]["core"][uvu][4])

                                                        for times in range(120):
                                                            time.sleep(1)

                                                            if werewolf[0]["now"][0]!=uwu[1]:
                                                                break

                                                        else:
                                                            for uvu in werewolf[0]["werewolf"]["core"]:
                                                                if uvu not in werewolf[0]["werewolf"]["wait"]:
                                                                    time.sleep(1)
                                                                    self.dsend(f"/w {uvu} >\n今晚你的同伴猝死了\n{roll(werewolf[5][6])}的狼群忙于为TA送葬 没有行动", werewolf[0]["core"][uvu][4])

                                                            for uvu in werewolf[0]["werewolf"]["wait"]:
                                                                chan(uvu)
                                                                werewolf[0]["sudden"].append(uvu)

                                                                time.sleep(1)
                                                                self.dsend(f"/me >\n[【{werewolf[2][3][0]}】](https://)[{uvu}](https://)在今晚{roll(werewolf[3][1])} 突然猝死")

                                                    else:
                                                        time.sleep(random.randint(20,40))
                                                        self.dsend(f"/me >\n狼群中的狼{roll(werewolf[5][7])}")

                                                elif uwu[1]==4:
                                                    time.sleep(2)
                                                    self.dsend(f"/me >\n[【{werewolf[2][4][0]}】](https://)请睁眼")

                                                    if uwu[3]:
                                                        werewolf[0]["witch"]={"med":werewolf[0]["witch"]["med"],"temp":[],"allow":[]}
                                                        med=[uvu for uvu in werewolf[0]["witch"]["med"] if werewolf[0]["witch"]["med"][uvu][1]]

                                                        if med:
                                                            werewolf[0]["now"]=[uwu[1],uwu[0]]
                                                            dead=[uvu for uvu in werewolf[0]["state"][False] if uvu not in werewolf[0]["sudden"]]
                                                            alive=[uvu for uvu in werewolf[0]["state"][True] if uvu!=uwu[0]]

                                                            ovo=" ".join([werewolf[7][werewolf[0]["witch"]["med"][uvu][0]][0] for uvu in med])
                                                            owo=str()

                                                            if dead and True in med:
                                                                werewolf[0]["witch"]["allow"].extend(dead)
                                                                random.shuffle(dead)
                                                                owo+="\n可救："+" ".join([f"[{uvu}](https://)" for uvu in dead])

                                                            if alive and False in med:
                                                                werewolf[0]["witch"]["allow"].extend(alive)
                                                                random.shuffle(alive)
                                                                owo+="\n可杀："+" ".join([f"[{uvu}](https://)" for uvu in alive])

                                                            time.sleep(1)
                                                            self.dsend(f"/w {uwu[0]} >\n·\n[【{werewolf[2][4][0]}】](https://)/[【{werewolf[2][0][False]}】](https://)[{uwu[0]}](https://)\n现在你可以选择一位村民使用药水\n请在1分钟内做出选择\n·\n选择方法：\n/w {self.nick} 对象\n·\n所剩药水：\n{ovo}\n·\n可选对象：{owo}", uwu[4])

                                                            for times in range(60):
                                                                time.sleep(1)

                                                                if werewolf[0]["now"][0]!=uwu[1]:
                                                                    break

                                                            else:
                                                                time.sleep(1)
                                                                self.dsend(f"/me >\n黑夜里 只剩[【{werewolf[2][4][0]}】](https://)四处飞行的身影")

                                                        else:
                                                            time.sleep(1)
                                                            self.dsend(f"/w {uwu[0]} >\n·\n[【{werewolf[2][4][0]}】](https://)[{uwu[0]}](https://)\n虽然轮到你行动 但你已经用完了药水", uwu[4])

                                                            time.sleep(2)
                                                            self.dsend(f"/me >\n[【{werewolf[2][4][0]}】](https://)在研究能{roll(werewolf[6][0])}的药水")

                                                    else:
                                                        time.sleep(random.randint(10,50))
                                                        self.dsend(f"/me >\n[【{werewolf[2][4][0]}】](https://){roll(werewolf[6][4])}")


                                            time.sleep(4)
                                            self.dsend(f"/me >\n[【回合{werewolf[0]['round']}】](https://)天亮了")

                                            alive=list(werewolf[0]["state"][True])
                                            random.shuffle(alive)
                                            ovo=" ".join([f"[{uvu}](https://)" for uvu in alive])
                                            owo=str()

                                            if not werewolf[0]["witch"]["temp"] or werewolf[0]["witch"]["temp"][-1]:
                                                owo="是一个平安夜\n"

                                            if isinstance(werewolf[0]["werewolf"]["kill"],str):
                                                owo=f"[{werewolf[0]['werewolf']['kill']}](https://)被[【{werewolf[2][3][0]}】](https://)杀死了\n"

                                            if werewolf[0]["witch"]["temp"]:
                                                owo+=f"[{werewolf[0]['witch']['temp'][2]}](https://)被使用[{werewolf[7][werewolf[0]['witch']['temp'][-1]][0]}](https://)的[【{werewolf[2][4][0]}】](https://)[{werewolf[7][werewolf[0]['witch']['temp'][-1]][1]}](https://)了\n"

                                            time.sleep(2)
                                            self.dsend(f"/me >\n[【公告】](https://)昨晚{owo}")

                                            werewolf[0]["stats"]=[[uvu for uvu in werewolf[0]["core"] if werewolf[0]["core"][uvu][2] and werewolf[0]["core"][uvu][3]],[uvu for uvu in werewolf[0]["core"] if not werewolf[0]["core"][uvu][2] and werewolf[0]["core"][uvu][3]]]

                                            if not all(werewolf[0]["stats"]):
                                                break

                                            werewolf[0]["now"]=[0,werewolf[0]["state"][True]]
                                            werewolf[0]["day"]={"wait":list(werewolf[0]["state"][True]),"kill":[],"dead":werewolf[0]["day"]["dead"]}
                                            
                                            time.sleep(2)
                                            self.dsend(f"/me >\n·\n投票环节：\n每人一票 得票数最高的[【{werewolf[8]['core']}】](https://)会被处死\n请在4分钟内做出选择\n·\n选择方法：\n/w {self.nick} 对象\n·\n可选对象：\n{ovo}")

                                            for times in range(240):
                                                time.sleep(1)

                                                if not werewolf[0]["day"]["wait"]:
                                                    break

                                                elif times==180:
                                                    self.dsend(f"/me >\n白天仅剩1分钟了")

                                            else:
                                                for uvu in werewolf[0]["day"]["wait"]:
                                                    if werewolf[0]["core"][uvu][1]!=4:
                                                        chan(uvu)
                                                        werewolf[0]["sudden"].append(uvu)

                                                        time.sleep(2)
                                                        self.dsend(f"/me >\n[【{werewolf[2][werewolf[0]['core'][uvu][1]][0]}】](https://)[{uvu}](https://)在白天{roll(werewolf[3][1])} 突然猝死")

                                            if werewolf[0]["day"]["kill"]:
                                                time.sleep(2)
                                                aua=max(set(werewolf[0]["day"]["kill"]),key=werewolf[0]["day"]["kill"].count)

                                                try:
                                                    chan(aua)
                                                    werewolf[0]["day"]["dead"].append(aua)
                                                    self.dsend(f"/me >\n[【公告】](https://)投票结果统计完成\n{roll(werewolf[3][3])}的[【{werewolf[8]['core']}】](https://)们处死了[{aua}](https://)")

                                                except:
                                                    self.dsend(f"/me >\n[【公告】](https://)投票结果统计完成\n{roll(werewolf[3][3])}的[【{werewolf[8]['core']}】](https://)们{roll(werewolf[3][0])}处死[{aua}](https://)\n但当发现时 [{aua}](https://)已经猝死在家中了")

                                                alive=list(werewolf[0]["state"][True])
                                                random.shuffle(alive)
                                                ovo=" ".join([f"[{uvu}](https://)" for uvu in alive])

                                                time.sleep(2)
                                                self.dsend(f"/me >\n目前留在村子里的人有：\n{ovo}")

                                            werewolf[0]["stats"]=[[uvu for uvu in werewolf[0]["core"] if werewolf[0]["core"][uvu][2] and werewolf[0]["core"][uvu][3]],[uvu for uvu in werewolf[0]["core"] if not werewolf[0]["core"][uvu][2] and werewolf[0]["core"][uvu][3]]]
                        
                                            if not all(werewolf[0]["stats"]):
                                                break
                                        
                                        if not self.running['werewolves']:
                                            self._init_werewolves()
                                            sys.exit(0)
                                            
                                        time.sleep(4)
                                        winner=werewolf[0]["stats"].index([])

                                        if winner:
                                            self.dsend(f"/me >\n不知什么时候 天气变得晴朗\n大家清楚地感受到 邪恶从村子里消失了")

                                        else:
                                            self.dsend(f"/me >\n这个村子正在发生异变\n血色笼罩村庄 时不时传来邪恶的声音")
                                            
                                        uwu=[[f"[{_}]" for _ in werewolf[0]["stats"][not int(winner)]],
                                        [f"[{_}]" for _ in werewolf[0]["core"] if werewolf[0]["core"][_][2]==winner and not werewolf[0]["core"][_][3]],
                                        [f"[{_}]" for _ in werewolf[0]["core"] if werewolf[0]["core"][_][2]==(not winner)],
                                        [f"[{_}]" for _ in werewolf[0]["prophet"]],
                                        [f"[{_}]" for _ in werewolf[0]["werewolf"]["dead"]],
                                        [f"\n【{werewolf[2][4][0]}】[{werewolf[7][werewolf[0]['witch']['med'][_][0]][1]}]了：[{werewolf[0]['witch']['med'][_][-1]}]" for _ in werewolf[0]["witch"]["med"] if not werewolf[0]["witch"]["med"][_][1]],
                                        [f"[{_}]" for _ in werewolf[0]["day"]["dead"]]]

                                        note=[str() for _ in range(3)]

                                        for _ in range(len(uwu)):
                                            if uwu[_]:
                                                if not _:
                                                    note[0]+=f"\n存活({len(werewolf[0]['stats'][not winner])})："+" ".join(uwu[_])

                                                elif _==1:
                                                    note[0]+=f"\n死亡({len(uwu[_])})："+" ".join(uwu[_])

                                                elif _==2:
                                                    note[1]+=f"\n死亡({len(uwu[_])})："+" ".join(uwu[_])

                                                else:
                                                    if _==3:
                                                        note[2]+=f"\n【{werewolf[2][2][0]}】知道了："+" ".join(uwu[_])

                                                    elif _==4:
                                                        note[2]+=f"\n【{werewolf[2][3][0]}】杀死了："+" ".join(uwu[_])

                                                    elif _==5:
                                                        note[2]+="".join(uwu[_])

                                                    elif _==6:
                                                        note[2]+=f"\n投票处死了："+" ".join(uwu[_])

                                        else:
                                            if note[2]:
                                                note[2]=f"\n·\n特殊数据：{note[2]}"

                                        time.sleep(2)
                                        self.dsend(f"/me >\n[【{werewolf[2][0][not winner]}】](https://)阵亡 [【{werewolf[2][0][winner]}】](https://)胜利")

                                        minutes=divmod(round(time.time()-werewolf[0]["time"]),60)
                                        self.dsend(f"/me >\n·\n[【统计数据】](https://)\n时长：{minutes[0]}分钟 {minutes[1]}秒\n回合数：{werewolf[0]['round']}\n·\n[【{werewolf[2][0][winner]}】](https://)(胜){note[0]}\n·\n【{werewolf[2][0][not winner]}】(败){note[1]}{note[2]}")

                                        time.sleep(1)
                                        self.dsend(f"/me >\n本局结束 撒花-")

                                        self._init_werewolves()

                                        sys.exit(0)
                                    except:
                                        logging.error(traceback.format_exc())

                                while self.running['werewolves']:
                                    if len(werewolf[0]["temp"])==len(werewolf[0]["group"]):
                                        werewolf[0]["notice"]="@"+" @".join(werewolf[0]["temp"].keys())+" "
                                        self.dsend(f"/me >\n{werewolf[0]['notice']}\n人数到齐 开始抽牌 请注意查看私聊")

                                        tmp = list(werewolf[0]["temp"].keys())
                                        random.shuffle(tmp)

                                        for _ in tmp:
                                            note=werewolf[0]["group"][tmp.index(_)]
                                            werewolf[0]["core"][_]=[_,note,werewolf[2][note][2],True,werewolf[0]["temp"][_]]

                                            time.sleep(1)
                                            self.dsend(f"/w {_} >\n·\n你的卡牌：\n[【{werewolf[2][note][0]}】](https://)/[【{werewolf[2][0][werewolf[2][note][2]]}】](https://)\n·\n你的任务：\n{werewolf[2][note][1]}\n·\n获胜条件：\n[【{werewolf[2][0][not werewolf[2][note][2]]}】](https://)全员阵亡\n·\n设置遗言(死亡前有效)：\n/w {self.nick} msg(换行)遗言", werewolf[0]["temp"][_])

                                        time.sleep(2)
                                        self.dsend(f"/me >\n发牌完毕 [【{werewolf[8]['game']}】](https://)正式开始")

                                        # 开启多线程
                                        threading.Thread(target=loop).start()
                                        break

                                    else:
                                        time.sleep(2)

                                sys.exit(0)

                            # 开启多线程
                            threading.Thread(target=auto).start()


                    elif werewolf[0]["uwu"]:
                        if not werewolf[0]["core"]:
                            if text==f"{self.prefix}1":
                                if nick in werewolf[0]["temp"]:
                                    self.dsend(f"/me >\n[{nick}](https://)已经在花名册中了", channel)

                                else:
                                    werewolf[0]["temp"].update({nick:channel})
                                    self.dsend(f"/me >\n[{nick}](https://){roll(werewolf[3][6])}了村子 村里有{len(werewolf[0]['temp'])}人了")

                            

                elif cmd=="info" and wss.get('type')=="whisper":

                    if "from" in wss and isinstance(wss["from"], str):
                        nick=wss["from"]
                        text=wss["text"]
                        uwu=text[text.find(':')+2:]

                        if werewolf[0]["uwu"]:
                            msg=uwu.split("\n",1)
                            if not werewolf[0]["core"]:
                                if nick == werewolf[0]["owner"]["nick"] and channel == werewolf[0]["owner"]["channel"]:
                                    allow=[int(_) for _ in uwu.split(' ') if _ in ["1","2","3","4"]]

                                    if allow==werewolf[0]["group"]:
                                        self.dsend(f"/w {nick} >\n牌组和原先相同 不变更", channel)

                                    elif len(allow)<len(werewolf[0]["temp"]):
                                        self.dsend(f"/w {nick} >\n花名册的人数已经超过牌数了", channel)

                                    else:
                                        werewolf[0]["group"]=sorted(allow)
                                        self.dsend(f"/me >\n[【{werewolf[8]['op']}】](https://)更改了[【{werewolf[8]['core']}】](https://)身份牌数目")

                                        time.sleep(1)
                                        self.dsend(f"/me >\n现卡牌设置({len(allow)}人局)：\n1.[【{werewolf[2][1][0]}】](https://)x{allow.count(1)}\n2.[【{werewolf[2][2][0]}】](https://)x{allow.count(2)}\n3.[【{werewolf[2][3][0]}】](https://)x{allow.count(3)}\n4.[【{werewolf[2][4][0]}】](https://)x{allow.count(4)}")

                            elif msg[0]=="msg" and nick in werewolf[0]["state"][True]:
                                if len(msg)<2 and not msg[1].strip():
                                    self.dsend(f"/w {nick} >\n请写下你的遗言",channel)

                                elif "$" in text:
                                    self.dsend(f"/w {nick} >\n如果说 遗言不允许LaTeX？",channel)

                                else:
                                    if nick in werewolf[0]["msg"]:
                                        self.dsend(f"/w {nick} >\n遗言更新成功",channel)

                                    else:
                                        self.dsend(f"/w {nick} >\n遗言添加成功",channel)

                                    werewolf[0]["msg"][nick]=msg[1]


                            elif werewolf[0].get('now'):
                                if nick in werewolf[0]["day"]["wait"]:
                                    if uwu in werewolf[0]["state"][True]:
                                        werewolf[0]["day"]["wait"].pop(werewolf[0]["day"]["wait"].index(nick))
                                        werewolf[0]["day"]["kill"].append(uwu)
                                        aua=f"[{uwu}](https://)"

                                        if uwu==nick:
                                            aua="你自己"

                                        self.dsend(f"/w {nick} >\n你将写有{aua}名字的纸片塞进投票箱", channel)

                                        time.sleep(2)
                                        self.dsend(f"/me >\n投票箱中多了一张{roll(werewolf[3][4])}的纸片")

                                    elif uwu in werewolf[0]["state"][False]:
                                        self.dsend(f"/w {nick} >\n你没必要{roll(werewolf[3][7])}死者", channel)

                                    else:
                                        werewolf[0]["day"]["wait"].pop(werewolf[0]["day"]["wait"].index(nick))
                                        self.dsend(f"/w {nick} >\n你{roll(werewolf[3][5])} 放弃了投票", channel)

                                        time.sleep(2)
                                        self.dsend(f"/me >\n有一张纸片{roll(werewolf[3][8])}")

                                elif nick==werewolf[0]["now"][1] or isinstance(werewolf[0]["now"][1],list) and nick in werewolf[0]["werewolf"]["wait"]:
                                    if werewolf[0]["now"][0]==2:
                                        if uwu==nick:
                                            self.dsend(f"/w {nick} >\n不允许[【{werewolf[2][2][0]}】](https://)选择自己", channel)

                                        else:
                                            if uwu in werewolf[0]["state"][True]:
                                                if uwu in werewolf[0]["prophet"]:
                                                    self.dsend(f"/w {nick} >\n你已经预言过[{uwu}](https://)的身份了\nTA是[【{werewolf[2][werewolf[0]['core'][uwu][1]][0]}】](https://) 属于[【{werewolf[2][0][werewolf[0]['core'][uwu][2]]}】](https://)", channel)

                                                    time.sleep(2)
                                                    self.dsend(f"/me >\n不幸的[【{werewolf[2][2][0]}】](https://){roll(werewolf[4][0])}")

                                                else:
                                                    werewolf[0]["prophet"].append(uwu)
                                                    self.dsend(f"/w {nick} >\n[{uwu}](https://)是[【{werewolf[2][werewolf[0]['core'][uwu][1]][0]}】](https://) 属于[【{werewolf[2][0][werewolf[0]['core'][uwu][2]]}】](https://)", channel)

                                                    aua=roll(werewolf[4][1])

                                                    if not werewolf[0]['core'][uwu][2]:
                                                        aua=roll(werewolf[4][2])

                                                    time.sleep(2)
                                                    self.dsend(f"/me >\n盯着水晶球的[【{werewolf[2][2][0]}】](https://){aua}")

                                            elif uwu in werewolf[0]["state"][False]:
                                                self.dsend(f"/w {nick} >\n你没必要{roll(werewolf[3][7])}死者", channel)

                                            else:
                                                self.dsend(f"/w {nick} >\n你{roll(werewolf[3][0])}今晚放弃预言 睡个好觉", channel)

                                                time.sleep(2)
                                                self.dsend(f"/me >\n[【{werewolf[2][2][0]}】](https://)睡得很{roll(werewolf[4][3])}")

                                            werewolf[0]["now"]=[0,None]

                                    elif werewolf[0]["now"][0]==3:
                                        if uwu in werewolf[0]["state"][True]:
                                            werewolf[0]["werewolf"]["wait"].pop(werewolf[0]["werewolf"]["wait"].index(nick))
                                            werewolf[0]["werewolf"]["kill"].append(uwu)

                                            aua=f"[{uwu}](https://)"

                                            if uwu==nick:
                                                aua=f"自己 {roll(werewolf[5][4])}"

                                            elif uwu in werewolf[0]["werewolf"]["core"]:
                                                aua=f"同伴[{uwu}](https://) 这样{roll(werewolf[5][5])}"

                                            self.dsend(f"/w {nick} >\n你{roll(werewolf[3][0])}杀{aua}", channel)

                                            for uvu in werewolf[0]["werewolf"]["wait"]:
                                                if uvu==uwu:
                                                    aua="你"

                                                time.sleep(1)
                                                self.dsend(f"/w {uvu} >\n你的同伴[{nick}](https://){roll(werewolf[3][0])}杀{aua}", werewolf[0]["core"][uvu][4])

                                        elif uwu in werewolf[0]["state"][False]:
                                            self.dsend(f"/w {nick} >\n你没必要{roll(werewolf[3][7])}死者", channel)

                                        else:
                                            werewolf[0]["werewolf"]["wait"].pop(werewolf[0]["werewolf"]["wait"].index(nick))
                                            self.dsend(f"/w {nick} >\n你{roll(werewolf[3][0])}今晚做件好事 放过人类", channel)

                                            for uvu in werewolf[0]["werewolf"]["wait"]:
                                                time.sleep(1)
                                                self.dsend(f"/w {uvu} >\n你的同伴[{nick}](https://){roll(werewolf[3][3])}了", werewolf[0]["core"][uvu][4])

                                        if not werewolf[0]["werewolf"]["wait"]:
                                            aua="你们意见不相同 因此没有杀人"

                                            if werewolf[0]["werewolf"]["kill"] and werewolf[0]["werewolf"]["kill"].count(uwu)==len(werewolf[0]["werewolf"]["kill"]):
                                                chan(uwu)
                                                werewolf[0]["werewolf"]["dead"].append(uwu)
                                                werewolf[0]["werewolf"]["kill"]=uwu

                                                aua=f"你们杀死了[{uwu}](https://)\nTA是[【{werewolf[0]['core'][uwu][1]}】](https://) 属于[【{werewolf[0]['core'][uwu][2]}】](https://)"

                                                if uwu in werewolf[0]["werewolf"]["core"]:
                                                    aua=f"你们杀死了同伴[{uwu}](https://)"

                                            for uvu in werewolf[0]["werewolf"]["core"]:
                                                time.sleep(1)

                                                if uvu==uwu:
                                                    self.dsend(f"/w {uvu} >\n今晚 你被杀死了", werewolf[0]["core"][uvu][4])

                                                else:
                                                    self.dsend(f"/w {uvu} >\n今晚 {aua}", werewolf[0]["core"][uvu][4])

                                            time.sleep(2)

                                            if uwu in werewolf[0]["core"] and not werewolf[0]["core"][uwu][5]:
                                                self.dsend(f"/me >\n[【公告】](https://){roll(werewolf[3][2])} 只听见[{uwu}](https://)的{roll(werewolf[5][0])}和几声狼嚎\n当[{roll(werewolf[0]['state'][True])}](https://)跑去查看情况的时候 只发现[{uwu}](https://){roll(werewolf[5][1])}的尸体")

                                            else:
                                                self.dsend(f"/me >\n能听见远处狼群{roll(werewolf[5][2])}的声音")

                                            werewolf[0]["now"]=[0,None]

                                    elif werewolf[0]["now"][0]==4:
                                        if uwu==nick:
                                            self.dsend(f"/w {nick} >\n不允许[【{werewolf[2][4][0]}】](https://)自己喝下药水", channel)

                                        elif uwu in werewolf[0]["sudden"]:
                                            self.dsend(f"/w {nick} >\n你没必要{roll(werewolf[3][7])}猝死的人", channel)

                                        else:
                                            if uwu in werewolf[0]["witch"]["allow"]:
                                                state=not werewolf[0]["core"][uwu][3]
                                                uvu=werewolf[0]["witch"]["med"][state]

                                                self.dsend(f"/w {nick} >\n你使用{werewolf[7][uvu[0]][0]}成功{werewolf[7][uvu[0]][1]}了[{uwu}](https://)", channel)

                                                chan(uwu,state)
                                                werewolf[0]["witch"]["temp"]=[uwu,state]
                                                werewolf[0]["witch"]["med"][state][1]=False

                                                aua=f"获得了新生"

                                                if not state:
                                                    aua=f"陷入了永眠"

                                                time.sleep(2)
                                                self.dsend(f"/me >\n[【公告】](https://){roll(werewolf[3][2])} 村子里{roll(werewolf[6][1])}\n[{roll(werewolf[0]['state'][True])}](https://)挨家挨户地传话道 [{uwu}](https://){roll(werewolf[6][2])}地{aua}")

                                                werewolf[0]["now"]=[0,None]
                                                
                                            elif uwu in werewolf[0]["core"]:
                                                self.dsend(f"/w {nick} >\n你没有能给[{uwu}](https://)使用的药", channel)

                                            else:
                                                self.dsend(f"/w {nick} >\n你{roll(werewolf[3][0])}今晚放弃投药 等待机会", channel)

                                                time.sleep(2)
                                                self.dsend(f"/me >\n[【{werewolf[2][4][0]}】](https://)笑得很{roll(werewolf[6][3])}")
                                                werewolf[0]["now"]=[0,None]

                                elif nick in werewolf[0]["state"][True]:
                                    self.dsend(f"/w {nick} >\n现在不是你的场合 快去睡觉——", channel)

                                elif nick in werewolf[0]["state"][False]:
                                    self.dsend(f"/w {nick} >\n你已经死了", channel)
        except:
            logging.error(traceback.format_exc())
