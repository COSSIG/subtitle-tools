# TODO:
# Extracion of audio from video file; - DONE
# Automatic transcription of audio file (ENGLISH); - DONE
# Writing the transcription to a subtitle file (.ass) - DONE
# Correcting the subtitle output in accordance to manual transcriptions provided should there be any
# Direct use from CLI; should implement options
# Setting subtitle styles - font, font size, etc

#   Bonus goal: writing the transcription to an Arctime Project file (.atpj) which is based on JSON


import whisper
import pysubs2
import os
import os.path
import subprocess


def assess_media_format(media_dir:str) -> str:

    # A list of commonly seen audio formats
    aud_extension_names = ["pcm", "wav", "mp3", "flac", "ogg"]  # It is welcomed to add more to this list.
    vid_extension_names = ["mp4", "mkv", "mov", "wmv", "mpeg", "rmvb", "flv", "m4v", "avi", "webm"]

    media_format: str = media_dir.split(".")[-1].lower()  # this doesn't resolve cases such as ".d.ts" though...

    if media_format in aud_extension_names:
        return "audio"
    elif media_format in vid_extension_names:
        return "video"
    else:
        return "other"

def extract_audio(video_dir: str):
    # extracting audio from video file with ffmpeg, saving it to a local directory.
    # extracted wav matches the requirements of openai-whisper
    extraction_command = ["ffmpeg", "-i", video_dir, "-map", "0:a", "-acodec", "pcm_s16le", "-ar", "16000",
                          "-ac", "1", "-f", "wav", "audio_temp.wav"]
    subprocess.run(extraction_command)


# Transcribing audio with openai-whisper, and convert the transcript to the pysubs2 subtitle object.
def generate_subtitles(media_dir:str, model:whisper.Whisper) -> pysubs2.SSAFile:
    auto_text = model.transcribe(media_dir, verbose=True)
    return pysubs2.load_from_whisper(auto_text)


if __name__ == "__main__":
    has_transcription: bool = False

    media_where: str = input("Input media file directory:")
    if not os.path.exists(media_where):  # TODO: a fuzzy match to existing files and dirs
        print("The file or directory does not exist.")
        exit(0)
    else:
        media_format: str = assess_media_format(media_where)
        if media_format == "other":
            print("The file format is not supported.")  # TODO: an option to manually override this assertion
            exit(0)
        elif media_format == "video":
            print("The file is a video file. Extracting audio...")
            extract_audio(media_where)

    subtitle_filename: str = media_where.split("/")[-1] + ".ass"  
    # this will result in file names like "x.mp3.ass"
    # more logic will be added to make this not happen

    model_spec: str = "small"  # probably need an implementation to check if the spec is a valid one
    
    model_used = whisper.load_model(model_spec)

    if media_format == "audio":
        subs = generate_subtitles(media_where, model_used)
    elif media_format == "video":
        subs = generate_subtitles("audio_temp.wav", model_used)

    subs.save(subtitle_filename)
    os.remove("audio_temp.wav")
 