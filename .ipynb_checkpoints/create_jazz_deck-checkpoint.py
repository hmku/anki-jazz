import os
import requests
import base64

# CONFIG
deck_name = "Jazz Ear Training"
media_folder = r"C:\Users\Harrison Ku\Downloads\jazz-audio"
anki_connect_url = "http://localhost:8765"

# Step 1: Create the deck
def create_deck(name):
    requests.post(anki_connect_url, json={
        "action": "createDeck",
        "version": 6,
        "params": {"deck": name}
    })

# Step 2: Add a note
def add_note(deck, front, audio_filename):
    audio_path = os.path.join(media_folder, audio_filename)
    with open(audio_path, "rb") as f:
        audio_data = f.read()
        encoded_audio = base64.b64encode(audio_data).decode("utf-8")

    # Upload the audio file to Anki media collection
    requests.post(anki_connect_url, json={
        "action": "storeMediaFile",
        "version": 6,
        "params": {
            "filename": audio_filename,
            "data": encoded_audio
        }
    })

    # Add the note
    requests.post(anki_connect_url, json={
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck,
                "modelName": "Basic",
                "fields": {
                    "Front": os.path.splitext(audio_filename)[0],
                    "Back": f"[sound:{audio_filename}]"
                },
                "options": {
                    "allowDuplicate": False
                },
                "tags": ["jazz-audio"]
            }
        }
    })

# MAIN
create_deck(deck_name)

for filename in os.listdir(media_folder):
    if filename.lower().endswith((".mp3", ".wav", ".ogg")):
        print(f"Adding {filename}...")
        add_note(deck_name, filename, filename)

print("Done!")
