import json, discord, openai
from discord.ext import commands

chat_log = []

with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["TOKEN"]

openai.api_key = config["API_KEY"]

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="!help", url="https://twitch.tv/gothamchess"))
    print(f"{bot.user} is online with the ID {bot.user.id}")
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
      pass
    elif message.content.startswith("$"):
      pass
    else:
      if isinstance(message.channel, discord.DMChannel):
        num = 1
        while num != 0:
          chat_log.append({"role": "user", "content": message.content})

          response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=chat_log
                )

          gpt_response = response["choices"][0]["message"]["content"]

          chat_log.append({"role": "assistant", "content": gpt_response})

          await message.channel.send(response["choices"][0]["message"]["content"])
          num -= 1
          if num == 0:
            break
    await bot.process_commands(message)
    
bot.run(TOKEN)
