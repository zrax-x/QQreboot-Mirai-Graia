# coding: utf-8
# README: https://graia-document.vercel.app/docs/intro

from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio

from graia.application.message.elements.internal import Plain, At
from graia.application.message.elements.internal import Image as GiImage

from graia.application.friend import Friend
from graia.application.group import Group, Member, MemberPerm
from graia.application.interrupt import InterruptControl
from graia.application.interrupt.interrupts import GroupMessageInterrupt
from graia.broadcast.interrupt.waiter import Waiter
from graia.application.event.messages import GroupMessage

import time
import datetime
from Qndxx import getCurQndxxLink
from nsfw import *
from checkImg import *
# import paddlehub as hub
# from checkText import checkTextwithModule
from smartChat import xiaoice


test_group = 557116842
use_group = 1054423346
reboot_id = 2683944199
reboot_psd = "MINGreboot558"
# reboot_id = 193174244
push_hour = 12

inTiming = False

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
# inc = InterruptControl(bcc)

app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:9099", # 填入 httpapi 服务运行的地址
        authKey="INITKEYXBpVyzgt", # 填入 authKey
        account = reboot_id, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)


def myMenu():
    print("[Log] menu")
    menu = '''
*小茗女友*暂时支持的功能如下：
1. 每日青年大学习推送
2. 瑟图检测，提出警告
3. pron型违规语句检测
4. 虚拟女友
5. /setu (懂的都懂，质量不好不要骂，随机找的)
6. /qbhn
7. /yjny
8. /cycny
当前*小茗女友*还在开发当中哦~ 敬请期待~
'''
    return menu


def getNextDelay():
    cur_time = datetime.datetime.now()
    h = cur_time.hour
    if h >= push_hour:
        next_time = datetime.datetime(
            cur_time.year, 
            cur_time.month, 
            cur_time.day + 1, 
            push_hour, 0, 0, 0)
    else:
        next_time = datetime.datetime(
            cur_time.year, 
            cur_time.month, 
            cur_time.day, 
            push_hour, 0, 0, 0)
    return (next_time - cur_time).seconds

#### ------------------------------------------------------------------

@bcc.receiver("TempMessage")
async def temp_message_listener(
    message: MessageChain, 
    app: GraiaMiraiApplication, 
    group: Group, temp: Member):
    await app.sendTempMessage(group, temp, MessageChain.create([
        Plain("我还在开发当中哦，敬请期待~")
    ]))


@bcc.receiver("GroupMessage")
async def group_message_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):

    global inTiming
    if not inTiming and group.id == use_group and message.asDisplay().startswith("/ffff"):
        inTiming = True
        # delay = getNextDelay()
        # print("[log]距离下次推送{}秒".format(delay))
        # delay_msg = "距离下次推送青年大学习还有{}秒.".format(delay)
        # await app.sendGroupMessage(group, MessageChain.create([
        #     Plain(delay_msg)
        # ]))
        # await asyncio.sleep(delay)
        title_link = getCurQndxxLink()
        if len(title_link) == 2:
            title, link = title_link
        send_msg = "欢迎来到今天的青年大学习交流环节~\n" + \
                    "今天的主题是：《" + title + '》\n' + \
                    "请点击" + link + "\n开始学习吧！~"
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(send_msg)
        ]))
        # inTiming = False

    if group.id in [test_group, use_group] and message.asDisplay().startswith("/menu"):
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), Plain(myMenu())
        ]))
    
    elif group.id in [test_group, use_group] and message.asDisplay().startswith("/qndxx"):
        delay = getNextDelay()
        delay_msg = "距离下次自动推送青年大学习还有{}秒.".format(delay)
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(delay_msg)
        ]))

    elif group.id in [test_group, use_group] and message.asDisplay().startswith("/setu"):
        img_url = await searchImgfromMicroSoft()
        print("[Log]", img_url)
        # img_file = download_img(img_url)
        # print("[Log]", img_file)
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), GiImage.fromNetworkAddress(img_url)
        ]))
    
    elif group.id in [test_group, use_group] and message.asDisplay().startswith("/qbhn"):
        img_path = await searchImgQbhnLocal()
        print("[Log]", img_path)
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), GiImage.fromLocalFile(img_path)
        ]))

    elif group.id in [test_group, use_group] and message.asDisplay().startswith("/yjny"):
        await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain("正在尝试搜索，请稍等~")
            ]))
        img_url = await searchVmgirls()
        if img_url:
            img_path = download_img(img_url, header_yjny)
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), GiImage.fromLocalFile(img_path)
            ]))
        else:
            img_path = download_img(img_url, header_yjny)
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain("检索失败，重新尝试~")
            ]))
    
    elif group.id in [test_group, use_group] and message.asDisplay().startswith("/cycny"):
        files = os.listdir(myconfigs['cycny_dir'])
        rnd_file = files[random.randint(0, len(files)-1)]
        img_path = os.path.join(myconfigs['cycny_dir'], rnd_file)
        await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), GiImage.fromLocalFile(img_path), Plain("卡哇伊~")
            ]))

    if group.id in [test_group, use_group] and message.has(GiImage):
        for img in message.get(GiImage):
            if img.url:
                img_file = download_img(img.url)
                print(img_file)
                if falsePositive(img_file):
                    continue
                global nsfw
                checkres = nsfw.infer(img_file)
                topres = checkres[0]
                topType = topres['type']
                topP = topres['prob']
                secondType = checkres[1]['type']
                secondP = checkres[1]['prob']
                print("[Log]: \n"+repr(checkres))
                if topType in ['porn', 'hentai']:
                    if topP >= 0.5:
                        await app.sendGroupMessage(group, MessageChain.create([
                            At(member.id), Plain("警告⚠，您发送了一张铯图，请注意您的行为~")
                        ]))
                    elif secondType in ['porn', 'hentai', 'sexy']:
                        if topP + secondP >= 0.7:
                            await app.sendGroupMessage(group, MessageChain.create([
                                At(member.id), Plain("警告⚠，您发送了一张铯图，请注意您的行为~")
                            ]))
                elif topType == 'sexy':
                    await app.sendGroupMessage(group, MessageChain.create([
                        At(member.id), Plain("很好👍，您发送了一张sexy图，请继续~😍")
                    ]))
    
    # if group.id in [test_group, use_group] and message.has(Plain):
    #     global porn_detection_lstm
    #     text = message.get(Plain)[0].text
    #     print(repr(text))
    #     res = checkTextwithModule(text, porn_detection_lstm)
    #     if res:
    #         await app.sendGroupMessage(group, MessageChain.create([
    #                 At(member.id), Plain("警告⚠，您发送了一条违规语句，请注意您的行为~")
    #             ]))

    if group.id in [test_group, use_group] and message.has(At) and message.get(At)[0].target == reboot_id:
        if message.has(Plain):
            text = message.get(Plain)[0].text
            reply = xiaoice(text)
            if reply:
                await app.sendGroupMessage(group, MessageChain.create([
                    At(member.id), Plain(reply)
                ]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain("你艾特我干嘛啊？")
            ]))

nsfw = NSFWEstimator(myconfigs['nsfw_path'])
print("[Log] load img model done!")
# porn_detection_lstm = hub.Module(name="porn_detection_lstm")
# print("[Log] load Text model done!")
app.launch_blocking()
