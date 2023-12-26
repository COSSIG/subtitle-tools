# TODO:
# Extracion of audio from video file;
# Automatic transcription of audio file (ENGLISH);
# Writing the transcription to a subtitle file (.ass)
#   Bonus goal: writing the transcription to an Arctime Project file (.atpj) which is based on JSON
# Correcting the subtitle output in accordance to manual transcriptions provided should there be any

# In this process styles will be set. For example: font, font size, etc.

import whisper
import pysubs2


# Transcribing audio with openai-whisper, and convert the transcript to the pysubs2 subtitle object.
# ...You will do exception handling, won't you
def generate_subtitles(audio_dir:str, model:whisper.Whisper) -> pysubs2.SSAFile:
    auto_text = model.transcribe(audio_dir, verbose=True)
    return pysubs2.load_from_whisper(auto_text)


if __name__ == "__main__":
    has_transcription: bool = False  # we will do the fuzzy search later
    audio_where: str = input("Input audio file directory:")
    subtitle_filename: str = audio_where.split("/")[-1] + ".ass"  
    # this will result in file names like "x.mp3.ass"
    # more logic will be added to make this not happen

    model_spec: str = "small"  # probably need an implementation to check if the spec is a valid one
    
    model_used = whisper.load_model(model_spec)
    subs = generate_subtitles(audio_where, model_used)

    subs.save(subtitle_filename)