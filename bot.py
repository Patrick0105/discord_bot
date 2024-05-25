import discord
from discord.ext import commands
import requests
import os
def notify_send(msg):
    url = 'https://notify-api.line.me/api/notify'
    token = (os.getenv('LINE_NOTIFY_TOKEN'))
    headers = {
        'Authorization': 'Bearer ' + token  # 設定權杖
    }
    data = {
        'message': msg  # 設定要發送的訊息
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        print('LINE 通知發送失敗')

# 初始化機器人並設置 intents
intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# 當用戶進入或離開語音頻道時觸發的事件
@bot.event
async def on_voice_state_update(member, before, after):
    # 如果用戶進入語音頻道
    if before.channel is None and after.channel is not None:
        try:
            notify_send(f'{member.name} 進入了語音頻道 {after.channel.name}')
        except Exception as e:
            print(f'LINE 通知發送失敗: {e}')
    # 如果用戶從一個語音頻道移動到另一個語音頻道
    elif before.channel is not None and after.channel is not None and before.channel != after.channel:
        try:
            notify_send(f'{member.name} 從 {before.channel.name} 移動到了 {after.channel.name}')
        except Exception as e:
            print(f'LINE 通知發送失敗: {e}')

# 啟動機器人
bot.run(os.getenv('BOT_TOKEN'))  # 替換為你的機器人 Token
