import os
from flask import Flask, render_template, request, jsonify, send_from_directory
import tempfile
import uuid
import time
from werkzeug.utils import secure_filename
from src.cockpitvoice import run_pipeline

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'cockpitvoice_outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Ensure upload and output directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'wav', 'mp3', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Generate a unique ID for this request using UUID and timestamp
    timestamp = int(time.time())
    request_id = f"{timestamp}_{str(uuid.uuid4())}"
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], request_id)
    os.makedirs(output_dir, exist_ok=True)
    
    transformed_filename = "transformed.txt"
    transcription_filename = "transcription.txt"
    audio_filename = "cockpit_voice.wav"
    
    try:
        if 'file' in request.files:
            # Handle file upload
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{request_id}_{filename}")
                file.save(filepath)
                input_data = filepath
            else:
                return jsonify({'error': 'Invalid file type'}), 400
        elif 'audio' in request.files:
            # Handle recorded audio
            audio = request.files['audio']
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{request_id}_recording.wav")
            audio.save(filepath)
            input_data = filepath
        elif 'text' in request.form:
            # Handle direct text input or edited transcription
            input_data = request.form['text']
            
            # Check if this is an edited transcription
            is_edited_transcription = 'is_edited_transcription' in request.form and request.form['is_edited_transcription'] == 'true'
            
            # If it's an edited transcription, we'll skip the transcription step
            if is_edited_transcription:
                # Create a temporary file with the edited transcription
                temp_text_path = os.path.join(output_dir, transcription_filename)
                with open(temp_text_path, "w", encoding="utf-8") as f:
                    f.write(input_data)
        else:
            return jsonify({'error': 'No input provided'}), 400
        
        # Run the pipeline
        run_pipeline(
            input_data=input_data,
            output_dir=output_dir,
            transformed_output=transformed_filename,
            audio_output=audio_filename
        )
        
        # Read the transformed text
        transformed_path = os.path.join(output_dir, transformed_filename)
        with open(transformed_path, 'r', encoding='utf-8') as f:
            transformed_text = f.read()
        
        # Check if there's a transcription file (for audio inputs)
        transcription_text = None
        transcription_path = os.path.join(output_dir, transcription_filename)
        if os.path.exists(transcription_path):
            with open(transcription_path, 'r', encoding='utf-8') as f:
                transcription_text = f.read()
        
        # Return paths to the output files
        response_data = {
            'success': True,
            'transformed_text': transformed_text,
            'audio_url': f'/outputs/{request_id}/{audio_filename}',
            'request_id': request_id
        }
        
        # Add transcription if available
        if transcription_text:
            response_data['transcription_text'] = transcription_text
            
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/outputs/<path:request_id>/<path:filename>')
def serve_output(request_id, filename):
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], request_id)
    return send_from_directory(output_dir, filename)




if __name__ == '__main__':
    app.run(debug=True)
