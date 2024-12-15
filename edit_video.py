from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import os
import random


def detect_cuts(threshold=30.0):
    video_folder = "video_model"
    video_name = "model.mp4"
    video_path = os.path.join(video_folder, video_name)

    video_clip = VideoFileClip(video_path)
    total_frames = int(video_clip.duration * video_clip.fps)

    cut_timestamps = []
    prev_frame = None

    for idx, frame in enumerate(video_clip.iter_frames()):
        if idx == 0:
            prev_frame = frame
            continue

        frame_diff = abs(frame.mean() - prev_frame.mean())

        if frame_diff > threshold:
            cut_timestamp = video_clip.duration * idx / total_frames
            cut_timestamps.append(min(cut_timestamp, video_clip.duration))

        prev_frame = frame

    cut_timestamps.insert(0, 0.0)
    cut_timestamps.append(video_clip.duration)

    video_clip.close()

    return cut_timestamps


def transform_timecode(timecode):
    parts = timecode.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])
    frames = int(parts[3])

    total_seconds = hours * 3600 + minutes * 60 + seconds

    transformed = total_seconds + frames / 100.0

    return transformed


with open('timecodes.txt', 'r') as file:
    timecodes = file.readlines()


cut_timestamps = detect_cuts()
# cut_timestamps = [transform_timecode(tc.strip()) for tc in timecodes]
print("Detected cuts at timestamps:", cut_timestamps)


def create_new_video(timestamps, video_folder="videos", output_path="output_video.mp4"):
    video_clips = []

    for i in range(len(timestamps) - 1):
        random_clip = VideoFileClip(os.path.join(
            video_folder, random.choice(os.listdir(video_folder))))

        print("i = ", i)
        print("Clip: ", random_clip.filename)
        start_time = random.uniform(
            0, random_clip.duration - (timestamps[i+1] - timestamps[i]))
        end_time = start_time + (timestamps[i+1] - timestamps[i])
        print("Start time: ", start_time)
        print("End time: ", end_time)

        segment_clip_1 = random_clip.subclip(
            start_time, end_time)

        video_clips.append(segment_clip_1)
        segment_clip_1.close()

    final_clip = concatenate_videoclips(
        video_clips, method="compose")
    final_clip.write_videofile(output_path)
    final_clip.close()


create_new_video(cut_timestamps)


def replace_audio(video_path, music_path, output_path):
    video_clip = VideoFileClip(video_path)
    music_clip = VideoFileClip(music_path)

    video_clip_with_music = video_clip.set_audio(music_clip.audio)
    video_clip_with_music.write_videofile(output_path)

    video_clip.close()
    music_clip.close()


model_video_path = "video_model/model.mp4"
output_video_path = "output_video.mp4"
output_path = "output_video_with_music.mp4"

# replace_audio(output_video_path, model_video_path, output_path)


def replace_audio_with_mp3(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    audio_clip = audio_clip.subclip(0, video_clip.duration)

    video_clip_with_music = video_clip.set_audio(audio_clip)
    video_clip_with_music.write_videofile(output_path)

    video_clip.close()
    audio_clip.close()


audio_path = "video_music/music.mp3"
video_path = "output_video.mp4"
output_path = "output_video_with_music.mp4"

replace_audio_with_mp3(video_path, audio_path, output_path)
