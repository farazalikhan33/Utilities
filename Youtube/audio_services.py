import sys
import time
from datetime import datetime
import subprocess
import json
import whisper_timestamped as whisper

sys.path.append('tiktok_voice_main')

from tiktok_voice_main.main import tts


def split_content(content):
    chunks = list()
    temp = str()
    content_list = content.split()

    for word in content_list:
        if len(temp) < 290:
            temp += word + ' '
        else:
            chunks.append(temp)
            temp = ' ' + word + ' '

    if temp != chunks[-1]:
        chunks.append(temp)

    for i, chunk in enumerate(chunks):
        print(f'Chunk {i + 1}')
        print(chunk)
        print('-' * 5)
    return chunks


def stitch_audio(content, post_id):
    current_date = datetime.now()
    formatted_date = current_date.strftime("%d-%m-%y_%H_%M")
    chunks = split_content(content)
    filename = f"{formatted_date}_{post_id}.mp3"
    for chunk in chunks:
        print(f'TTS for {chunk}')
        tts(
            session_id="73782eef66d5ab64bf83342be9623375",
            text_speaker="en_us_006",
            req_text=chunk,
            filename=f'Audios/{filename}',
        )
        time.sleep(2)
    return filename


def speed_up_audio_ffmpeg(input_file, output_file, speed=1.5):
    # Run ffmpeg command to speed up the audio
    command = f'ffmpeg -i "{input_file}" -filter:a "atempo={speed}" -vn "{output_file}"'
    subprocess.run(command, shell=True)


def transcribe_audio_sentences():
    audio = whisper.load_audio("09-01-24_18_43_191po9d.mp3")
    model = whisper.load_model("tiny", device="cpu")
    result = whisper.transcribe(model, audio, language="en")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    with open('transcription.srt', 'a') as srt_file:
        for i, segment in enumerate(result['segments']):
            start, end = segment['start'], segment['end']
            srt_file.write(f'{i + 1}\n')
            srt_file.write(f"00:00:{str(int(start)).replace('.', ',')} --> 00:00:{str(int(end)).replace('.', ',')}\n")
            srt_file.write(f'{segment["text"].strip()}\n\n')


def transcribe_audio_words(audio_file="09-01-24_18_43_191po9d.mp3", post_id=''):
    srt_file_path = f'{post_id}_words_transcription.srt'
    word_count = 0
    audio = whisper.load_audio(f'Audios/{audio_file}')
    model = whisper.load_model("tiny", device="cpu")
    result = whisper.transcribe(model, audio, language="en")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    with open(f'Subs/{srt_file_path}', 'a') as srt_file:
        print(f'writing to {srt_file_path}')
        for segment in result['segments']:
            for word in segment['words']:
                word_count += 1
                start, end = word['start'], word['end']
                srt_file.write(f'{word_count}\n')
                srt_file.write(f"00:00:{str(float(start))} --> 00:00:{str(float(end))}\n")
                srt_file.write(f'{word["text"].upper().strip()}\n\n')
    print(f'Written to {srt_file_path}')
    return srt_file_path


def generate_audio_and_transcription(content, post_id):
    audio_file = stitch_audio(content, post_id)
    srt_file = transcribe_audio_words(audio_file, post_id)
    return audio_file, srt_file
