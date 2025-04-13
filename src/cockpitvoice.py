import os
from src.transcribe import transcribe_audio
from src.text_transformation import transform_text
from src.synthesize import synthesize_text
import sys

def run_pipeline(input_data, output_dir="cockpitvoice_outputs", transformed_output="transformed.txt", audio_output="cockpit_voice.wav"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    transformed_output = os.path.join(output_dir, transformed_output)
    audio_output = os.path.join(output_dir, audio_output)

    if os.path.isfile(input_data) and input_data.lower().endswith(('.wav', '.mp3', '.flac')):
        print("Step 1: Transcribing...")
        transcript = transcribe_audio(input_data)

        temp_text_path = os.path.join(output_dir, "transcription.txt")
        with open(temp_text_path, "w", encoding="utf-8") as f:
            f.write(transcript)
    elif os.path.isfile(input_data):
        print("Step 1: Reading text from file...")
        with open(input_data, "r", encoding="utf-8") as f:
            transcript = f.read()
    else:
        print("Step 1: Using provided text...")
        transcript = input_data

    print("Step 2: Transforming text...")
    transformed = transform_text(transcript)
    with open(transformed_output, "w", encoding="utf-8") as f:
        f.write(transformed)

    print("Step 3: Synthesizing voice...")
    synthesize_text(transformed, output_path=audio_output)

    print(f"Done. Outputs saved to: {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cockpitvoice.py [audio_file|text|text_file] [optional_output_dir] [optional_transformed_text] [optional_audio_output]")
        sys.exit(1)

    input_data = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "cockpitvoice_outputs"
    transformed_path = sys.argv[3] if len(sys.argv) > 3 else "transformed.txt"
    voice_path = sys.argv[4] if len(sys.argv) > 4 else "cockpit_voice.wav"

    run_pipeline(input_data, output_dir, transformed_path, voice_path)
