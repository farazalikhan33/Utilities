import random

from moviepy.editor import *
from datetime import datetime

# File paths
# audio_path = '09-01-24_18_43_191po9d.mp3'
# subtitle_path = 'words_transcription.srt'
bg_video_path = 'bg_video.mp4'

def random_clip_duration():
    start = random.randrange(0, 700)
    end = start + 57
    return start, end

def time_to_seconds(timestamp):
    h, m, s = map(float, timestamp.split(':'))
    return h * 3600 + m * 60 + s


def update_aspect_ratio(video_clip):
    new_width = 1080
    new_height = 1920
    resized_clip = video_clip.resize(width=new_width, height=new_height)

    x_center = (resized_clip.w - new_width) // 2
    y_center = (resized_clip.h - new_height) // 2

    shift_to_right = 100
    cropped_clip = resized_clip.crop(
        y1=y_center,
        y2=y_center + new_height,
        x1=x_center + shift_to_right,
        x2=x_center + new_width + shift_to_right
    )
    return cropped_clip


def get_bg_video(audio):
    bg_video = VideoFileClip(bg_video_path)

    start_time, end_time = random_clip_duration()
    bg_video = bg_video.subclip(start_time, end_time)

    bg_video = bg_video.set_duration(audio.duration)
    bg_video = update_aspect_ratio(bg_video)
    return bg_video


def compile_text_clip(subtitle_path, audio):
    subtitles = []
    video_clips = []
    with open(subtitle_path, 'r', encoding='utf-8') as file:
        subtitle_lines = file.read().strip().split('\n\n')
        for line in subtitle_lines:
            parts = line.strip().split('\n')
            if len(parts) >= 3:
                start, end = parts[1].split(' --> ')
                text = '\n'.join(parts[2:])
                subtitles.append((start, end, text))

    for i, subtitle in enumerate(subtitles):
        start, end, text = subtitle
        txt_clip = TextClip(text, fontsize=120, color='white', align='center')
        txt_clip = txt_clip.set_start(start).set_end(end)
        video_clips.append(txt_clip)

        # Add blank video for the gap
        if i < len(subtitles) - 1:
            next_start = subtitles[i + 1][0]
            gap_duration = (time_to_seconds(next_start) - time_to_seconds(end))
            if gap_duration > 0:
                blank_clip = ColorClip(size=(txt_clip.size[0], txt_clip.size[1]), color=(0, 0, 0, 0),
                                       duration=gap_duration)
                video_clips.append(blank_clip)

    print("Concatenating")
    final_video = concatenate_videoclips(video_clips, method="chain", bg_color=None, padding=0)
    print("Setting Audio")
    final_video = final_video.set_audio(audio)
    final_video = final_video.set_duration(audio.duration)
    return final_video


def compile_video(audio_path, subtitle_path, post_id, duration=58):
    output_video_path = f'{post_id}_words_output_video.mp4'
    audio = AudioFileClip(audio_path)
    audio = audio.subclip(0, duration)

    final_video = compile_text_clip(subtitle_path, audio)
    bg_video = get_bg_video(audio)
    print("Setting overlay")
    overlay_clip = CompositeVideoClip([bg_video, final_video.set_pos('center')])

    # Write the video file
    print("Writing video")
    overlay_clip.write_videofile(f'Videos/{output_video_path}', codec='libx264', audio_codec='aac',
                                 temp_audiofile='temp-audio.m4a',
                                 remove_temp=True, fps=10, threads=4)
    return output_video_path


if __name__ == '__main__':
    compile_video('09-01-24_18_43_191po9d.mp3', 'words_transcription.srt', post_id='XXX')
