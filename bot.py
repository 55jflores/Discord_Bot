import os
import discord
from pic_transformation import filter_image, cartoon_image
from classify_names import predict

image_types = ["png", "jpeg", "jpg","JPG"]

def main(my_secret_api):
  # Connecting to discord 
  client = discord.Client()
  
  # Event when bot starts up
  @client.event
  async def on_ready():
    print('We have logged in as {0.user}'.format(client))

  # Event when a message is sent
  @client.event
  async def on_message(message):
    # If message is bots
    if message.author == client.user:
      return

    msg = message.content
    # Filter transformation: Takes in image and filter color
    if (message.attachments and msg):
      # Grabbing names of colors
      colors = msg 
      # Grab an image
      for attachment in message.attachments:
        if any(attachment.filename.lower().endswith(image) for image in image_types):
              await attachment.save('images_folder/'+attachment.filename)
      
      if(msg.startswith('cartoon') or msg.startswith('Cartoon')):
        await message.channel.send(f'Will take a moment...')
        cartoon_image('images_folder/'+attachment.filename)
      else:
        # Call transformation function
        filter_image(colors,'images_folder/'+attachment.filename)

      # Send transformed image
      await message.channel.send(file=discord.File('images_folder/new_image.jpg'))
      
      # Removing files to save space
      os.remove('images_folder/'+attachment.filename)      
      os.remove('images_folder/new_image.jpg')
    
    elif msg.startswith('$hello') or msg.startswith('$Hello'):
      user = str(message.author)[:-5]
      bot = str(client.user)[:-5]
      await message.channel.send(f'Hello {user}! Greetings from {bot} bot.')
    elif msg.startswith('$classify'):
      # Grabbing last name
      users_name = msg.split("$classify ",1)[1]
      # Grabbing top 3 classes and their percentages
      top_classes = predict(users_name)

      await message.channel.send(f'{users_name} \n======================== \n{top_classes[0][0]}: {top_classes[0][1]}% \n{top_classes[1][0]}: {top_classes[1][1]}% \n{top_classes[2][0]}: {top_classes[2][1]}%')
      
  # Running bot
  client.run(my_secret_api)

if __name__ == "__main__":
  my_secret_api = "env variable that holds api token goes here"
  main(my_secret_api)
