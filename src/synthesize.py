import sys
import os
from elevenlabs import play, save, VoiceSettings
from elevenlabs.client import ElevenLabs


api_key = os.getenv("ELEVEN_LABS_API_KEY")
client = ElevenLabs(api_key=api_key)

def synthesize_text(text, output_path="pilot_voice.wav"):
    print("Synthesizing voice...")
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="foUTQvYz9ikkh3w3dxSh",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
        
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=1,
            use_speaker_boost=True,
            speed=1.0,
        )
        
    )
    
    save(audio, output_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python synthesize.py [input_text_file] [optional_output_audio_file]")
        sys.exit(1)

    input_text_path = sys.argv[1]
    output_audio_path = sys.argv[2] if len(sys.argv) > 2 else "pilot_voice.wav"

    with open(input_text_path, "r", encoding="utf-8") as f:
        text = f.read()

    synthesize_text(text, output_path=output_audio_path)