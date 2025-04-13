# Cockpit Voice

Cockpit Voice is an open source web application that transforms text or audio recordings into a prototypical pilot's voice. The application uses speech-to-text, text transformation, and text-to-speech technologies to create an authentic pilot voice experience.

## Features

- **Text Input**: Enter text directly to transform into pilot speech
- **Audio Recording**: Record audio through your microphone
- **File Upload**: Upload audio files (WAV, MP3, FLAC) or text files
- **Editable Transcription**: Edit the transcribed text before transformation
- **Audio Playback**: Listen to the transformed pilot voice
- **Download**: Save the generated audio file

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Speech-to-Text**: OpenAI Whisper
- **Text Transformation**: OpenAI GPT-4
- **Text-to-Speech**: ElevenLabs

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/clintonjules/CockpitVoice.git
   cd CockpitVoice
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up API keys as environment variables:
   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   export ELEVEN_LABS_API_KEY="your_elevenlabs_api_key"
   ```
   On Windows, use `set` instead of `export`.

## Usage

1. Start the Flask application:
   ```bash
   python app.py
   ```

   If port 5000 is already in use (common on macOS with AirPlay Receiver), you can specify a different port:
   ```bash
   python -c "from app import app; app.run(debug=True, port=5001)"
   ```
   
   Or modify the `app.py` file to change the default port:
   ```python
   if __name__ == '__main__':
       app.run(debug=True, port=5001)
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000  # or the custom port you specified, e.g., http://127.0.0.1:5001
   ```

3. Use the web interface to:
   - Enter text directly
   - Record audio through your microphone
   - Upload audio or text files

4. Process your input to transform it into pilot voice

5. Listen to the result and download the audio file if desired

## Project Structure

- `app.py`: Main Flask application
- `src/`: Core functionality modules
  - `cockpitvoice.py`: Main pipeline orchestration
  - `transcribe.py`: Audio transcription using Whisper
  - `text_transformation.py`: Text transformation using GPT-4
  - `synthesize.py`: Voice synthesis using ElevenLabs
- `static/`: Frontend assets (JavaScript, CSS)
- `templates/`: HTML templates
- `uploads/`: Temporary storage for uploaded files
- `cockpitvoice_outputs/`: Output directory for transformed text and audio

## API Keys

This application requires API keys from:

1. **OpenAI**: For GPT-4 text transformation and Whisper transcription
2. **ElevenLabs**: For voice synthesis

These keys should be set as environment variables and are not included in the repository.
