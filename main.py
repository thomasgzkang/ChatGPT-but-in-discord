from keep_alive import keep_alive
import discord
import openai
import io
import requests

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
    try:
      # Get the question from the message
      question = message.content[4:]
  
      # Send the question to the OpenAI API
      response = openai.Completion.create(engine="text-davinci-003",
                                          prompt=question,
                                          max_tokens=4000)
      response_text = response["choices"][0]["text"]
  
      # Truncate the response to 4,000 characters or fewer
      response_text = response_text[:4000]

    except openai.error.InvalidRequestError:
      await message.channel.send('No token left!')
    else:
      # Send the response back to the Discord channel
      await message.channel.send(response_text)
      
  if message.content.startswith('gen'):
    # Get the description from the message
    description = message.content[4:]

    # Generate an image based on the description
    try:
      image_data = generate_image(description)
    except openai.error.InvalidRequestError:
      await message.channel.send('Your prompt may contain text that is not allowed by our safety system!')
    else:
    # Send the image back to the Discord channel
      await message.channel.send(file=discord.File(image_data, filename='image.png'))

def generate_image(description):
  response = openai.Image.create(
    prompt=description,
    model="image-alpha-001",
    size="1024x1024"
  )

  image_data = io.BytesIO()
  for obj in response["data"]:
    image_url = obj["url"]
    image_content = requests.get(image_url).content
    image_data.write(image_content)

  image_data.seek(0)
  return image_data


    
# Start the Discord client
keep_alive()
client.run(DISCORD_BOT_TOKEN)
