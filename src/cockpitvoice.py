from transcribe import transcribe_audio
from text_transformation import transform_text
from synthesize import synthesize_text
import sys


def run_pipeline(audio_file, transformed_output="transformed.txt", audio_output="cockpit_voice.wav"):
    print("🔈 Step 1: Transcribing...")
    transcript = transcribe_audio(audio_file)

    temp_text_path = "transcription.txt"
    with open(temp_text_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    print("✍️ Step 2: Transforming text...")
    transformed = transform_text(transcript)
    with open(transformed_output, "w", encoding="utf-8") as f:
        f.write(transformed)

    print("🗣️ Step 3: Synthesizing voice...")
    synthesize_text(transformed, output_path=audio_output)

    print("✅ Done! Output saved to: {audio_output}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cockpitvoice.py [audio_file] [optional_transformed_text] [optional_audio_output]")
        sys.exit(1)

    audio_file = sys.argv[1]
    transformed_path = sys.argv[2] if len(sys.argv) > 2 else "transformed.txt"
    voice_path = sys.argv[3] if len(sys.argv) > 3 else "cockpit_voice.wav"

    run_pipeline(audio_file, transformed_path, voice_path)
