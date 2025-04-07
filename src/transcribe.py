import whisper
import sys
import warnings

# Suppress specific warning from Whisper
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

def transcribe_audio(audio_path):
    print("Loading Whisper model...")
    model = whisper.load_model("base")  # options: tiny, base, small, medium, large
    
    print(f"Transcribing: {audio_path}")
    result = model.transcribe(audio_path)
    
    return result["text"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py [audio_file] [optional_output_file]")
        sys.exit(1)

    audio_file = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "transcription.txt"

    # Transcribe and write to file
    transcript = transcribe_audio(audio_file)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    print(f"Transcription saved to: {output_path}")