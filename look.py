import time
from telethon.sync import TelegramClient
from telethon.tl import functions, types

# Your Telegram API credentials
api_id = '26970677'
api_hash = '2bed2e0e9f5c04be92e2f130e5978ccc'
phone_number = '66640757623'

# Function to read usernames from a file
def read_usernames(file_path):
    with open(file_path, 'r') as file:
        usernames = [line.strip() for line in file.readlines()]
    return usernames

def send_reactions(client, username):
    # Retrieve the pinned stories for the specified username
    pinned_stories = client(functions.stories.GetPinnedStoriesRequest(
        peer=username,
        offset_id=0,  # Specify the offset ID
        limit=100  # Specify the limit
    ))

    for story in pinned_stories.stories:
        try:
            # Send a reaction to the current story
            result = client(functions.stories.SendReactionRequest(
                peer=client.get_input_entity(username),
                story_id=story.id,
                reaction=types.ReactionEmoji(
                    emoticon='👍'  # Replace with your desired reaction
                ),
                add_to_recent=True
            ))
            print(f"Reaction sent for user {username} to story {story.id}: {result}")

            # Introduce a 3-second delay between reactions
            time.sleep(3)
        except Exception as e:
            print(f"An error occurred for user {username} to story {story.id}: {e}")

            # If an error occurs, move on to the next user
            break

# Initialize the Telegram client with a more descriptive session name
with TelegramClient('your_session_name', api_id, api_hash) as client:
    # First, you need to log in
    if not client.is_user_authorized():
        client.start()

    # Replace 'usernames.txt' with the path to your text file containing usernames
    usernames_file_path = 'usernames.txt'
    usernames = read_usernames(usernames_file_path)

    for username in usernames:
        send_reactions(client, username)
