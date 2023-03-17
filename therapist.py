import gradio as gr
import openai, config, subprocess, ffmpeg, sys, os
#openai.api_key = config.OPENAI_API_KEY
openai.api_key = "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"

messages = [{"role": "system", "content": 'You are a therapist. Respond to all input in 25 words or less.'}]
#messages = [{"role": "system", "content": 'You are a Spanish translator. Respond by translating the English to Spanish.'}]

def transcribe(audio):
    global messages

    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    subprocess.call(["say", system_message['content']])

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript

ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch()
ui.launch()