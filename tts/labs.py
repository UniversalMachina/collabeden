from elevenlabslib import *

def voiceover(voice="Josh",text="That was a good test",index=0):

    user = ElevenLabsUser("your-key-here(you can ask me for the key)")
    print("getting voice")
    voice = user.get_voices_by_name(voice)[0]  # This is a list because multiple voices can have the same name
    # audio_bytes=voice.generate_audio_bytes("Test.")
    # while True:
    #     try:
    attempts = 0
    max_attempts = 5

    while attempts < max_attempts:
        try:

            print("generating audio")
            audioData = voice.generate_audio_bytes(text)
            break

        except:
            # If an error occurs, print the error message and try again
            print("An error occurred. Retrying...")
            attempts += 1


    import os
    print("getting audio index")
    folder_path = os.getcwd()  # Get the current working directory
    # Use glob to get a list of all the mp3 files in the folder
    filename = os.path.join(folder_path + f"file{index}.mp3")
        #     break
        # except:
        #     print(text)
        #     import re
        #
        #     text = re.sub(r'[^A-Za-z0-9,. ]+', '', text)
        #     print("An error occurred while Recording...")

    attempts = 0
    max_attempts = 5

    while attempts < max_attempts:
        try:
            file = open(filename, "wb")
            file.write(audioData)
            file.close()
            # If the code executes successfully, break out of the loop
            break
        except:
            print("An error occurred. Retrying...")
            attempts += 1
    if attempts == max_attempts:
        print("Max attempts reached. Exiting loop.")



    # print(voice.get_settings())
voiceover()