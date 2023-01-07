from keep_alive import keep_alive
import discord
import openai

# Replace these values with your own
DISCORD_BOT_TOKEN = ''
OPENAI_API_KEY = ''

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

# Set the intents that you want the client to be able to receive
intents = discord.Intents.all()

# Create a new Discord client
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
  if message.content.startswith('rim'):
    # Get the question from the message
    question = message.content[4:]

    # Send the question to the OpenAI API
    response = openai.Completion.create(engine="text-davinci-003", prompt=question, max_tokens=4000)
    response_text = response["choices"][0]["text"]

    # Truncate the response to 4,000 characters or fewer
    response_text = response_text[:4000]

    # Send the response back to the Discord channel
    await message.channel.send(response_text)


# Start the Discord client
keep_alive()
client.run(DISCORD_BOT_TOKEN)
