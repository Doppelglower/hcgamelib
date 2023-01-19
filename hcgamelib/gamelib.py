from .const import *
from typing import Union
import json, websocket, time, random, os, sys, threading

class Game:
    def __init__(self, ws: Union[websocket.WebSocket, websocket.WebSocketApp], nick: str):
        """"""
        self.nick = nick
        self.ws = ws
        self.games = list()
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
            self.message = f'{game} already started.'
            super().__init__(self.message)
    class AlreadyEndedError(Exception):
        def __init__(self, game):
            self.message = f'{game} already ended.'
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
    def dsend(self, msg: str) -> None:
        self.ws.send(json.dumps({'cmd':'chat','text':str(msg)}))

    def handle(self,data):
        for game in self.games:
            game(data)

    def uno(self):
        pass

    def poker(self):
        pass

    def bomber(self):
        pass

    def truth(self):
        pass

    def chess(self):
        pass

    def werewolves(self,wss):
        def start():
            if self.werewolves not in self.games:
                self.games.append(self.werewolves)
            else:
                raise self.AlreadyStartedError('Werewolves')
        def end():
            if self.werewolves in self.games:
                self.games.remove(self.werewolves)
            else:
                raise self.AlreadyEndedError('Werewolves')
        if "cmd" in wss:
            cmd=wss["cmd"]
            if cmd=="chat":
                time.sleep(1)
                nick=wss["nick"]
                text=wss["text"]
                if text=="|help":
                    self.dsend(f"/me >\n·\n[【狼人杀】](https://)生存\n开发者：纸片君ee(PAPEREE)\n移植者：Doppelganger(DPG)\n版本号：awa.1.00\n开发进度：95.0001%\n·\n[【手册】](https://)\n查看帮助：|help\n查看规则：|rule\n获取权限：|root\n开始生存：|uwu")
                elif text=="|rule":
                    aua=str()
                    if werewolf[0]["uwu"]:
                        aua+=f"\n·\n卡牌设置({len(werewolf[0]['num'])}人局)：\n[【{werewolf[2][1][0]}】](https://)x{werewolf[0]['num'].count(1)}\n[【{werewolf[2][2][0]}】](https://)x{werewolf[0]['num'].count(2)}\n[【{werewolf[2][3][0]}】](https://)x{werewolf[0]['num'].count(3)}\n[【{werewolf[2][4][0]}】](https://)x{werewolf[0]['num'].count(4)}"
                    true="".join([f"[【{werewolf[2][uwu][0]}】](https://)" for uwu in werewolf[2] if uwu and werewolf[2][uwu][-1]])
                    false="".join([f"[【{werewolf[2][uwu][0]}】](https://)" for uwu in werewolf[2] if uwu and not werewolf[2][uwu][-1]])

                    self.dsend(f"/me >\n·\n主要卡牌：\n{true}/[【{werewolf[2][0][True]}】](https://)\n{false}/[【{werewolf[2][0][False]}】](https://)\n{aua}\n·\n限制时长：\n[【{werewolf[2][2][0]}】](https://)1分钟\n[【{werewolf[2][3][0]}】](https://)2分钟\n[【{werewolf[2][4][0]}】](https://)1分钟\n白天投票共4分钟\n·\n生存特性：\n[【{werewolf[2][1][0]}】](https://)擅长推理\n[【{werewolf[2][2][0]}】](https://)记性很好\n[【{werewolf[2][3][0]}】](https://)杀人不受限制\n[【{werewolf[2][4][0]}】](https://)不会猝死")

                elif text[:5]=="|root":
                    if wss.get('trip') in OWNER:
                        if text=="|root":
                            self.dsend(f"/me >\n[{nick}](https://)成功获取root权限")

                            time.sleep(1)
                            self.dsend(f"/w {nick} >\n·\n可变更项：\n卡牌(werewolf[2]) 其他(other)\n·\n详细说明：\n卡牌：牌序(1~4) 牌名(str) 阵营(bool)\n其他：正方阵营名(str) 反方阵营名(str) 村长称呼(str)")

                        else:
                            try:
                                slices=[uwu.split(" ") for uwu in text.split("\n")]

                                if slices[0][-1]=="card":
                                    for new in slices[1:]:
                                        werewolf[2][int(new[0])]=[new[1],werewolf[2][int(new[0])][1],True if new[2]=="True" else False]

                                    self.dsend(f"/me >\n变更执行成功")

                                elif slices[0][-1]=="other":
                                    werewolf[2][0]={True:slices[1][0],False:slices[1][1],None:slices[1][2]}
                                    self.dsend(f"/me >\n变更执行成功")

                                else:
                                    self.dsend(f"/me >\n找不到此变更项")

                            except:
                                self.dsend(f"/w {nick} >\n执行时出现错误")

                    else:
                        self.dsend(f"/me quq")

                elif text=="|uwu":
                    if werewolf[0]["uwu"]:
                        if werewolf[0].get('user'):
                            self.dsend(f"/me >\n[【狼人杀】](https://)生存已经开始了")

                        else:
                            self.dsend(f"/me >\n[【{werewolf[2][0][None]}】](https://)正在清点村里人数")

                    else:
                        werewolf[0]={"uwu":True,"owner":nick,"num":werewolf[1],"time":time.time(),"round":0,"temp":[],"user":{},"sudden":[],"prophet":[],"werewolf":{"skip":False,"user":[],"wait":[],"kill":[],"dead":[]},"witch":{"med":{True:[True,True,"解药","救活"],False:[False,True,"毒药","杀死"]},"temp":[],"allow":[]},"day":{"wait":[],"kill":[],"dead":[]},"now":[]}
                        self.dsend(f"/me >\n新的[【{werewolf[2][0][None]}】](https://)诞生了 美好的夜晚要开始了")

                        time.sleep(1)
                        uvu=" ".join([str(uwu) for uwu in werewolf[1]])
                        self.dsend(f"/w {nick} >\n·\n[【{werewolf[2][0][None]}】](https://)[{nick}](https://)\n现在你可以选择改变牌组 否则为默认\n·\n卡牌详情：\n1.[【{werewolf[2][1][0]}】](https://)\n2.[【{werewolf[2][2][0]}】](https://)\n3.[【{werewolf[2][3][0]}】](https://)\n4.[【{werewolf[2][4][0]}】](https://)\n·\n默认牌组({len(werewolf[1])}人局)：\n{uvu}\n·\n设置方法：\n/w {self.nick} 牌组")

                        time.sleep(0.5)
                        self.dsend(f"/me >\n[【{werewolf[2][0][None]}】](https://)开始清点村里人数 请用1报数")

                elif werewolf[0]["uwu"]:
                    if not werewolf[0]["user"]:
                        if text=="1":
                            if nick in werewolf[0]["temp"]:
                                self.dsend(f"/me >\n[{nick}](https://)已经在花名册中了")

                            else:
                                werewolf[0]["temp"].append(nick)
                                self.dsend(f"/me >\n[{nick}](https://){random.choice(werewolf[3][6])}了村子 村里有{len(werewolf[0]['temp'])}人了")

                        if len(werewolf[0]["temp"])==len(werewolf[0]["num"]):
                            time.sleep(1)
                            werewolf[0]["notice"]="@"+" @".join(werewolf[0]["temp"])+" "
                            self.dsend(f"/me >\n{werewolf[0]['notice']}\n·\n人数到齐 开始抽牌 请注意查看私聊")

                            random.shuffle(werewolf[0]["temp"])

                            for uwu in werewolf[0]["temp"]:
                                uvu=werewolf[0]["num"][werewolf[0]["temp"].index(uwu)]
                                werewolf[0]["user"][uwu]=[uwu,werewolf[2][uvu][0],werewolf[2][0][werewolf[2][uvu][2]],uvu,werewolf[2][uvu][2],True]

                                time.sleep(1)
                                self.dsend(f"/w {uwu} >\n·\n你的卡牌：\n[【{werewolf[2][uvu][0]}】](https://)/[【{werewolf[2][0][werewolf[2][uvu][2]]}】](https://)\n·\n你的任务：\n{werewolf[2][uvu][1]}\n·\n获胜条件：\n[【{werewolf[2][0][not werewolf[2][uvu][2]]}】](https://)全员阵亡")

                            time.sleep(2)
                            self.dsend(f"/me >\n发牌完毕 [【狼人杀】](https://)生存正式开始")

                            # nick:昵称,state:状态
                            def change(nick,state=False):
                                werewolf[0]["state"][state].append(werewolf[0]["state"][not state].pop(werewolf[0]["state"][not state].index(nick)))
                                werewolf[0]["user"][nick][5]=state

                            # 主循环
                            def loop():
                                while True:
                                    werewolf[0]["round"]+=1
                                    werewolf[0]["werewolf"]["skip"]=False
                                    werewolf[0]["day"]={"wait":[],"kill":[],"dead":werewolf[0]["day"]["dead"]}

                                    ava=list(werewolf[0]["user"].values())
                                    werewolf[0]["state"]={True:[uvu[0] for uvu in ava if uvu[5]],False:[uvu[0] for uvu in ava if not uvu[5]]}

                                    time.sleep(4)
                                    self.dsend(f"/me >\n[【回合{werewolf[0]['round']}】](https://)天黑请闭眼")

                                    print(werewolf[0])

                                    for awa in list(werewolf[0]["user"].keys()):
                                        uwu=werewolf[0]["user"][awa]

                                        if uwu[3]==2:
                                            time.sleep(2)
                                            self.dsend(f"/me >\n[【{werewolf[2][2][0]}】](https://)请睁眼")

                                            if uwu[5]:
                                                alive=[uvu for uvu in werewolf[0]["state"][True] if uvu!=uwu[0]]
                                                random.shuffle(alive)
                                                ovo=" ".join([f"[{uvu}](https://)" for uvu in alive])
                                                owo="\n".join([f"[【{werewolf[0]['user'][uvu][1]}】](https://)/[【{werewolf[0]['user'][uvu][2]}】](https://)[{werewolf[0]['user'][uvu][0]}](https://)" for uvu in werewolf[0]["prophet"]])

                                                werewolf[0]["now"]=[uwu[3],uwu[0]]

                                                time.sleep(1)
                                                self.dsend(f"/w {uwu[0]} >\n·\n[【{werewolf[2][2][0]}】](https://)/[【{werewolf[2][0][True]}】](https://)[{uwu[0]}](https://)\n现在你可以选择一位村民得知身份\n请在1分钟内做出选择\n·\n已知身份：\n你自己{owo}\n·\n选择方法：\n/w {self.nick} 对象\n·\n可选对象：\n{ovo}")

                                                for times in range(60):
                                                    time.sleep(1)

                                                    if werewolf[0]["now"][0]!=uwu[3]:
                                                        break

                                                else:
                                                    change(awa)
                                                    werewolf[0]["sudden"].append(awa)

                                                    time.sleep(1)
                                                    self.dsend(f"/me >\n[【{werewolf[2][2][0]}】](https://)[{awa}](https://)在今晚{random.choice(werewolf[3][1])} 突然猝死")

                                            else:
                                                time.sleep(random.randint(10,50))
                                                self.dsend(f"/me >\n[【{werewolf[2][2][0]}】](https://){random.choice(werewolf[4][4])}")

                                        elif uwu[3]==3 and not werewolf[0]["werewolf"]["skip"]:
                                            time.sleep(2)
                                            self.dsend(f"/me >\n[【{werewolf[2][3][0]}】](https://)请睁眼")

                                            if uwu[5]:
                                                alive=list(werewolf[0]["state"][True])
                                                random.shuffle(alive)
                                                ovo=" ".join([f"[{uvu}](https://)" for uvu in alive])

                                                note=[uvu for uvu in werewolf[0]["user"] if werewolf[0]["user"][uvu][3]==3 and werewolf[0]["user"][uvu][5]]
                                                werewolf[0]["werewolf"]={"skip":True,"user":note,"wait":note,"kill":[],"dead":werewolf[0]["werewolf"]["dead"]}
                                                werewolf[0]["now"]=[uwu[3],werewolf[0]["werewolf"]["user"]]

                                                for uvu in werewolf[0]["werewolf"]["user"]:
                                                    time.sleep(1)
                                                    owo=" ".join([f"[{aua}](https://)" for aua in werewolf[0]["werewolf"]["user"] if aua!=uvu])

                                                    if owo:
                                                        owo=f"\n·\n你的同伴：\n{owo}"

                                                    self.dsend(f"/w {uvu} >\n·\n[【{werewolf[2][3][0]}】](https://)/[【{werewolf[2][0][False]}】](https://)[{uvu}](https://)\n现在你可以选择一位村民杀死\n狼群只有意见统一才会行动\n请在2分钟内做出选择{owo}\n·\n选择方法：\n/w {self.nick} 对象\n·\n可选对象：\n{ovo}")

                                                for times in range(120):
                                                    time.sleep(1)

                                                    if werewolf[0]["now"][0]!=uwu[3]:
                                                        break

                                                else:
                                                    for uvu in werewolf[0]["werewolf"]["user"]:
                                                        if uvu not in werewolf[0]["werewolf"]["wait"]:
                                                            time.sleep(1)
                                                            self.dsend(f"/w {uvu} >\n今晚你的同伴猝死了\n{random.choice(werewolf[5][6])}的狼群忙于为TA送葬 没有行动")

                                                    for uvu in werewolf[0]["werewolf"]["wait"]:
                                                        change(uvu)
                                                        werewolf[0]["sudden"].append(uvu)

                                                        time.sleep(1)
                                                        self.dsend(f"/me >\n[【{werewolf[2][3][0]}】](https://)[{uvu}](https://)在今晚{random.choice(werewolf[3][1])} 突然猝死")

                                            else:
                                                time.sleep(random.randint(20,40))
                                                self.dsend(f"/me >\n狼群中的狼{random.choice(werewolf[5][7])}")

                                        elif uwu[3]==4:
                                            time.sleep(2)
                                            self.dsend(f"/me >\n[【{werewolf[2][4][0]}】](https://)请睁眼")

                                            if uwu[5]:
                                                werewolf[0]["witch"]={"med":werewolf[0]["witch"]["med"],"temp":[],"allow":[]}
                                                med=[uvu for uvu in werewolf[0]["witch"]["med"] if werewolf[0]["witch"]["med"][uvu][1]]

                                                if med:
                                                    werewolf[0]["now"]=[uwu[3],uwu[0]]
                                                    dead=[uvu for uvu in werewolf[0]["state"][False] if uvu not in werewolf[0]["sudden"]]
                                                    alive=[uvu for uvu in werewolf[0]["state"][True] if uvu!=uwu[0]]

                                                    ovo=" ".join([werewolf[0]["witch"]["med"][uvu][2] for uvu in med])
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
                                                    self.dsend(f"/w {uwu[0]} >\n·\n[【{werewolf[2][4][0]}】](https://)/[【{werewolf[2][0][False]}】](https://)[{uwu[0]}](https://)\n现在你可以选择一位村民使用药水\n请在1分钟内做出选择\n·\n选择方法：\n/w {self.nick} 对象\n·\n所剩药水：\n{ovo}\n·\n可选对象：{owo}")

                                                    for times in range(60):
                                                        time.sleep(1)

                                                        if werewolf[0]["now"][0]!=uwu[3]:
                                                            break

                                                    else:
                                                        time.sleep(1)
                                                        self.dsend(f"/me >\n黑夜里 只剩[【{werewolf[2][4][0]}】](https://)四处飞行的身影")

                                                else:
                                                    time.sleep(1)
                                                    self.dsend(f"/w {uwu[0]} >\n·\n[【{werewolf[2][4][0]}】](https://)[{uwu[0]}](https://)\n虽然轮到你行动 但你已经用完了药水")

                                                    time.sleep(2)
                                                    self.dsend(f"/me >\n[【{werewolf[2][4][0]}】](https://)在研究能{random.choice(werewolf[6][0])}的药水")

                                            else:
                                                time.sleep(random.randint(10,50))
                                                self.dsend(f"/me >\n[【{werewolf[2][4][0]}】](https://){random.choice(werewolf[6][4])}")


                                    time.sleep(4)
                                    self.dsend(f"/me >\n[【回合{werewolf[0]['round']}】](https://)天亮了")

                                    print(werewolf[0])

                                    alive=list(werewolf[0]["state"][True])
                                    random.shuffle(alive)
                                    ovo=" ".join([f"[{uvu}](https://)" for uvu in alive])
                                    owo=str()

                                    if not werewolf[0]["witch"]["temp"] or werewolf[0]["witch"]["temp"][3]:
                                        owo="是一个平安夜\n"

                                    if isinstance(werewolf[0]["werewolf"]["kill"],str):
                                        owo=f"[{werewolf[0]['werewolf']['kill']}](https://)被[【{werewolf[2][3][0]}】](https://)杀死了\n"

                                    if werewolf[0]["witch"]["temp"]:
                                        owo+=f"[{werewolf[0]['witch']['temp'][2]}](https://)被使用{werewolf[0]['witch']['temp'][0]}的[【{werewolf[2][4][0]}】](https://){werewolf[0]['witch']['temp'][1]}了\n"

                                    time.sleep(2)
                                    self.dsend(f"/me >\n[【公告】](https://)昨晚{owo}")

                                    werewolf[0]["stats"]=[[uvu for uvu in werewolf[0]["user"] if werewolf[0]["user"][uvu][4] and werewolf[0]["user"][uvu][5]],[uvu for uvu in werewolf[0]["user"] if not werewolf[0]["user"][uvu][4] and werewolf[0]["user"][uvu][5]]]

                                    if not all(werewolf[0]["stats"]):
                                        break

                                    werewolf[0]["day"]={"wait":list(werewolf[0]["state"][True]),"kill":[],"dead":werewolf[0]["day"]["dead"]}
                                    werewolf[0]["now"]=[0,werewolf[0]["state"][True]]

                                    time.sleep(2)
                                    self.dsend(f"/me >\n·\n投票环节：\n每人一票 得票数最高的村民会被处死\n请在4分钟内做出选择\n·\n选择方法：\n/w {self.nick} 对象\n·\n可选对象：\n{ovo}")

                                    for times in range(240):
                                        time.sleep(1)

                                        if not werewolf[0]["day"]["wait"]:
                                            break

                                        elif times==180:
                                            self.dsend(f"/me >\n白天仅剩1分钟了")

                                    else:
                                        for uvu in werewolf[0]["day"]["wait"]:
                                            if werewolf[0]["user"][uvu][3]!=4:
                                                change(uvu)
                                                werewolf[0]["sudden"].append(uvu)

                                                time.sleep(2)
                                                self.dsend(f"/me >\n[【{werewolf[0]['user'][uvu][1]}】](https://)[{uvu}](https://)在白天{random.choice(werewolf[3][1])} 突然猝死")

                                    if werewolf[0]["day"]["kill"]:
                                        time.sleep(2)
                                        aua=max(set(werewolf[0]["day"]["kill"]),key=werewolf[0]["day"]["kill"].count)

                                        try:
                                            change(aua)
                                            werewolf[0]["day"]["dead"].append(aua)
                                            self.dsend(f"/me >\n[【公告】](https://)投票结果统计完成\n{random.choice(werewolf[3][3])}的人们处死了[{aua}](https://)")

                                        except:
                                            self.dsend(f"/me >\n[【公告】](https://)投票结果统计完成\n{random.choice(werewolf[3][3])}的人们{random.choice(werewolf[3][0])}处死[{aua}](https://)\n但当发现时 [{aua}](https://)已经猝死在家中了")

                                        alive=list(werewolf[0]["state"][True])
                                        random.shuffle(alive)
                                        ovo=" ".join([f"[{uvu}](https://)" for uvu in alive])

                                        time.sleep(2)
                                        self.dsend(f"/me >\n目前留在村子里的人有：\n{ovo}")

                                    werewolf[0]["stats"]=[[uvu for uvu in werewolf[0]["user"] if werewolf[0]["user"][uvu][4] and werewolf[0]["user"][uvu][5]],[uvu for uvu in werewolf[0]["user"] if not werewolf[0]["user"][uvu][4] and werewolf[0]["user"][uvu][5]]]
                
                                    if not all(werewolf[0]["stats"]):
                                        break

                                time.sleep(4)
                                winner=werewolf[0]["stats"].index([])

                                uwu=[eb for eb in werewolf[0]["user"] if werewolf[0]["user"][eb][4]==winner and not werewolf[0]["user"][eb][5]]
                                uvu=[eb for eb in werewolf[0]["user"] if werewolf[0]["user"][eb][4]==(not winner)]
                                awa=" ".join([eb for eb in werewolf[0]["prophet"]])
                                ava=" ".join([eb for eb in werewolf[0]["werewolf"]["dead"]])
                                aua=" ".join([eb for eb in werewolf[0]["day"]["dead"]])
                                quq="".join([f"\n[【{werewolf[2][4][0]}】](https://){werewolf[0]['witch']['med'][eb][3]}了：{werewolf[0]['witch']['med'][eb][-1]}" for eb in werewolf[0]["witch"]["med"] if not werewolf[0]["witch"]["med"][eb][1]])
                                ovo=" ".join(uvu)
                                owo=" ".join(werewolf[0]['stats'][not int(winner)])
                                ouo=str()
                                note=str()

                                if winner:
                                    self.dsend(f"/me >\n大家清楚地感受到 邪恶从村子里消失了")

                                else:
                                    self.dsend(f"/me >\n这个村子正在发生异变\n血色笼罩村庄 时不时传来邪恶的声音")

                                if uwu:
                                    uwu=f"\n死亡({len(uwu)})："+" ".join(uwu)

                                else:
                                    uwu=str()

                                if ovo:
                                    ouo=f"\n死亡({len(uvu)})：{ovo}"

                                if awa:
                                    note+=f"\n[【{werewolf[2][2][0]}】](https://)知道了：{awa}"

                                if ava:
                                    note+=f"\n[【{werewolf[2][3][0]}】](https://)杀死了：{ava}"

                                if aua:
                                    note+=f"\n投票处死了：{aua}"

                                if note:
                                    note=f"\n·\n特殊数据：{note}"

                                time.sleep(2)
                                self.dsend(f"/me >\n[【{werewolf[2][0][not winner]}】](https://)阵亡 [【{werewolf[2][0][winner]}】](https://)胜利")

                                minutes=divmod(round(time.time()-werewolf[0]["time"]),60)
                                self.dsend(f"/me >\n·\n[【统计】](https://)\n时长：{minutes[0]}分钟 {minutes[1]}秒\n回合数：{werewolf[0]['round']}\n·\n[【{werewolf[2][0][winner]}】](https://)(胜)\n存活({len(werewolf[0]['stats'][winner])})：{owo}{uwu}\n·\n[【{werewolf[2][0][not winner]}】](https://)(败){ouo}{note}")

                                time.sleep(1)
                                self.dsend(f"/me >\n本局结束 撒花-")

                                werewolf[0].clear()
                                werewolf[0]["uwu"]=False

                                sys.exit(0)

                            # 开启多线程
                            threading.Thread(target=loop).start()

            elif cmd=="info" and wss.get('type')=="whisper":
                time.sleep(1)

                if "from" in wss:
                    nick=str(wss["from"])
                    text=wss["text"]
                    uwu=text[text.find(':')+2:]

                    if werewolf[0]["uwu"]:
                        if not werewolf[0]["user"]:
                            if nick==werewolf[0]["owner"]:
                                allow=[int(uwu) for uwu in uwu.split(' ') if uwu in ["1","2","3","4"]]

                                if allow==werewolf[0]["num"]:
                                    self.dsend(f"/w {nick} >\n牌组和原先相同 不变更")

                                elif len(allow)<4:
                                    self.dsend(f"/w {nick} >\n设定的有效牌至少要有4张")

                                elif len(allow)<=len(werewolf[0]["temp"]):
                                    self.dsend(f"/w {nick} >\n花名册的人数已经达到/超过牌数了")

                                else:
                                    werewolf[0]["num"]=sorted(allow)
                                    self.dsend(f"/me >\n[【{werewolf[2][0][None]}】](https://)更改了村民身份牌数目")

                                    time.sleep(1)
                                    self.dsend(f"/me >\n现卡牌设置({len(allow)}人局)：\n1.[【{werewolf[2][1][0]}】](https://)x{allow.count(1)}\n2.[【{werewolf[2][2][0]}】](https://)x{allow.count(2)}\n3.[【{werewolf[2][3][0]}】](https://)x{allow.count(3)}\n4.[【{werewolf[2][4][0]}】](https://)x{allow.count(4)}")

                        elif werewolf[0]["now"]:
                            if nick in werewolf[0]["day"]["wait"]:
                                if uwu in werewolf[0]["state"][True]:
                                    del werewolf[0]["day"]["wait"][werewolf[0]["day"]["wait"].index(nick)]
                                    werewolf[0]["day"]["kill"].append(uwu)
                                    aua=f"[{uwu}](https://)"

                                    if uwu==nick:
                                        aua="你自己"

                                    self.dsend(f"/w {nick} >\n你将写有{aua}名字的纸片塞进投票箱")

                                    time.sleep(2)
                                    self.dsend(f"/me >\n投票箱中多了一张{random.choice(werewolf[3][4])}的纸片")

                                elif uwu in werewolf[0]["state"][False]:
                                    self.dsend(f"/w {nick} >\n你没必要{random.choice(werewolf[3][7])}死者")

                                else:
                                    del werewolf[0]["day"]["wait"][werewolf[0]["day"]["wait"].index(nick)]
                                    self.dsend(f"/w {nick} >\n你{random.choice(werewolf[3][5])} 放弃了投票")

                                    time.sleep(2)
                                    self.dsend(f"/me >\n有一张纸片{random.choice(werewolf[3][8])}")

                            elif nick==werewolf[0]["now"][1] or isinstance(werewolf[0]["now"][1],list) and nick in werewolf[0]["werewolf"]["wait"]:
                                if werewolf[0]["now"][0]==2:
                                    if uwu==nick:
                                        self.dsend(f"/w {nick} >\n不允许[【{werewolf[2][2][0]}】](https://)选择自己")

                                    else:
                                        if uwu in werewolf[0]["state"][True]:
                                            if uwu in werewolf[0]["prophet"]:
                                                self.dsend(f"/w {nick} >\n你已经预言过[{uwu}](https://)的身份了\nTA是[【{werewolf[0]['user'][uwu][1]}】](https://) 属于[【{werewolf[0]['user'][uwu][2]}】](https://)")

                                                time.sleep(2)
                                                self.dsend(f"/me >\n不幸的[【{werewolf[2][2][0]}】](https://){random.choice(werewolf[4][0])}")

                                            else:
                                                werewolf[0]["prophet"].append(uwu)
                                                self.dsend(f"/w {nick} >\n[{uwu}](https://)是[【{werewolf[0]['user'][uwu][1]}】](https://) 属于[【{werewolf[0]['user'][uwu][2]}】](https://)")

                                                aua=random.choice(werewolf[4][1])

                                                if not werewolf[0]['user'][uwu][4]:
                                                    aua=random.choice(werewolf[4][2])

                                                time.sleep(2)
                                                self.dsend(f"/me >\n盯着水晶球的[【{werewolf[2][2][0]}】](https://){aua}")

                                        elif uwu in werewolf[0]["state"][False]:
                                            self.dsend(f"/w {nick} >\n你没必要{random.choice(werewolf[3][7])}死者")

                                        else:
                                            self.dsend(f"/w {nick} >\n你{random.choice(werewolf[3][0])}今晚放弃预言 睡个好觉")

                                            time.sleep(2)
                                            self.dsend(f"/me >\n[【{werewolf[2][2][0]}】](https://)睡得很{random.choice(werewolf[4][3])}")

                                        werewolf[0]["now"]=[0,None]

                                elif werewolf[0]["now"][0]==3:
                                    if uwu in werewolf[0]["state"][True]:
                                        del werewolf[0]["werewolf"]["wait"][werewolf[0]["werewolf"]["wait"].index(nick)]
                                        werewolf[0]["werewolf"]["kill"].append(uwu)

                                        aua=f"[{uwu}](https://)"

                                        if uwu==nick:
                                            aua=f"自己 {random.choice(werewolf[5][4])}"

                                        elif uwu in werewolf[0]["werewolf"]["user"]:
                                            aua=f"同伴[{uwu}](https://) 这样{random.choice(werewolf[5][5])}"

                                        self.dsend(f"/w {nick} >\n你{random.choice(werewolf[3][0])}杀{aua}")

                                        for uvu in werewolf[0]["werewolf"]["wait"]:
                                            if uvu==uwu:
                                                aua="你"

                                            time.sleep(1)
                                            self.dsend(f"/w {uvu} >\n你的同伴[{nick}](https://){random.choice(werewolf[3][0])}杀{aua}")

                                    elif uwu in werewolf[0]["state"][False]:
                                        self.dsend(f"/w {nick} >\n你没必要{random.choice(werewolf[3][7])}死者")

                                    else:
                                        del werewolf[0]["werewolf"]["wait"][werewolf[0]["werewolf"]["wait"].index(nick)]
                                        self.dsend(f"/w {nick} >\n你{random.choice(werewolf[3][0])}今晚做件好事 放过人类")

                                        for uvu in werewolf[0]["werewolf"]["wait"]:
                                            time.sleep(1)
                                            self.dsend(f"/w {uvu} >\n你的同伴[{nick}](https://){random.choice(werewolf[3][3])}了")

                                    if not werewolf[0]["werewolf"]["wait"]:
                                        aua="你们意见不相同 因此没有杀人"

                                        if werewolf[0]["werewolf"]["kill"] and werewolf[0]["werewolf"]["kill"].count(uwu)==len(werewolf[0]["werewolf"]["kill"]):
                                            change(uwu)
                                            werewolf[0]["werewolf"]["dead"].append(uwu)
                                            werewolf[0]["werewolf"]["kill"]=uwu

                                            aua=f"你们杀死了[{uwu}](https://)\nTA是[【{werewolf[0]['user'][uwu][1]}】](https://) 属于[【{werewolf[0]['user'][uwu][2]}】](https://)"

                                            if uwu in werewolf[0]["werewolf"]["user"]:
                                                aua=f"你们杀死了同伴[{uwu}](https://)"

                                        for uvu in werewolf[0]["werewolf"]["user"]:
                                            time.sleep(1)

                                            if uvu==uwu:
                                                self.dsend(f"/w {uvu} >\n今晚 你被杀死了")

                                            else:
                                                self.dsend(f"/w {uvu} >\n今晚 {aua}")

                                        time.sleep(2)

                                        if uwu in werewolf[0]["user"] and not werewolf[0]["user"][uwu][5]:
                                            self.dsend(f"/me >\n[【公告】](https://){random.choice(werewolf[3][2])} 只听见[{uwu}](https://)的{random.choice(werewolf[5][0])}和几声狼嚎\n当[{random.choice(werewolf[0]['state'][True])}](https://)跑去查看情况的时候 只发现[{uwu}](https://){random.choice(werewolf[5][1])}的尸体")

                                        else:
                                            self.dsend(f"/me >\n能听见远处狼群{random.choice(werewolf[5][2])}的声音")

                                        werewolf[0]["now"]=[0,None]

                                elif werewolf[0]["now"][0]==4:
                                    if uwu==nick:
                                        self.dsend(f"/w {nick} >\n不允许[【{werewolf[2][4][0]}】](https://)自己喝下药水")

                                    elif uwu in werewolf[0]["sudden"]:
                                        self.dsend(f"/w {nick} >\n你没必要{random.choice(werewolf[3][7])}猝死的人")

                                    else:
                                        if uwu in werewolf[0]["witch"]["allow"]:
                                            state=not werewolf[0]["user"][uwu][5]
                                            uvu=werewolf[0]["witch"]["med"][state]
                                            self.dsend(f"/w {nick} >\n你使用{uvu[2]}成功{uvu[3]}了[{uwu}](https://)")

                                            change(uwu,state)
                                            werewolf[0]["witch"]["temp"]=[uvu[2],uvu[3],uwu,state]
                                            werewolf[0]["witch"]["med"][state][1]=False

                                            aua=f"获得了新生"

                                            if not state:
                                                aua=f"陷入了永眠"

                                            time.sleep(2)
                                            self.dsend(f"/me >\n[【公告】](https://){random.choice(werewolf[3][2])} 村子里{random.choice(werewolf[6][1])}\n[{random.choice(werewolf[0]['state'][True])}](https://)挨家挨户地传话道 [{uwu}](https://){random.choice(werewolf[6][2])}地{aua}")

                                            werewolf[0]["now"]=[0,None]
                                            
                                        elif uwu in werewolf[0]["user"]:
                                            self.dsend(f"/w {nick} >\n你没有能给[{uwu}](https://)使用的药")

                                        else:
                                            self.dsend(f"/w {nick} >\n你{random.choice(werewolf[3][0])}今晚放弃投药 等待机会")

                                            time.sleep(2)
                                            self.dsend(f"/me >\n[【{werewolf[2][4][0]}】](https://)笑得很{random.choice(werewolf[6][3])}")
                                            werewolf[0]["now"]=[0,None]

                            elif nick in werewolf[0]["state"][True]:
                                self.dsend(f"/w {nick} >\n现在不是你的场合 快去睡觉——")

                            elif nick in werewolf[0]["state"][False]:
                                self.dsend(f"/w {nick} >\n你已经死了")