document.addEventListener('DOMContentLoaded', () => {
    // Store the original transcription for potential reset
    let originalTranscription = '';
    // Tab switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all tabs
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab
            btn.classList.add('active');
            const tabId = `${btn.dataset.tab}-tab`;
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Text input processing
    const processTextBtn = document.getElementById('process-text-btn');
    const inputText = document.getElementById('input-text');

    processTextBtn.addEventListener('click', () => {
        const text = inputText.value.trim();
        if (text) {
            processInput('text', text);
        } else {
            alert('Please enter some text to transform');
        }
    });

    // Audio recording
    let mediaRecorder;
    let audioChunks = [];
    let recordingTimer;
    let recordingSeconds = 0;
    let recordedAudioBlob = null;
    
    const startRecordingBtn = document.getElementById('start-recording');
    const stopRecordingBtn = document.getElementById('stop-recording');
    const micIcon = document.getElementById('microphone');
    const recordingStatus = document.getElementById('recording-status');
    const recordingTimerDisplay = document.getElementById('recording-timer');
    const redoRecordingBtn = document.getElementById('redo-recording');
    const sendRecordingBtn = document.getElementById('send-recording');

    startRecordingBtn.addEventListener('click', startRecording);
    stopRecordingBtn.addEventListener('click', stopRecording);
    redoRecordingBtn.addEventListener('click', redoRecording);
    sendRecordingBtn.addEventListener('click', sendRecording);
    
    micIcon.addEventListener('click', () => {
        if (!mediaRecorder || mediaRecorder.state === 'inactive') {
            if (redoRecordingBtn.style.display === 'inline-block') {
                // If we're in post-recording state, redo the recording
                redoRecording();
            } else {
                // Otherwise start a new recording
                startRecording();
            }
        } else {
            stopRecording();
        }
    });

    function startRecording() {
        // Hide redo and send buttons, show stop button
        startRecordingBtn.style.display = 'none';
        redoRecordingBtn.style.display = 'none';
        stopRecordingBtn.style.display = 'inline-block';
        sendRecordingBtn.style.display = 'none';
        
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];
                recordedAudioBlob = null; // Reset the stored audio blob
                
                mediaRecorder.addEventListener('dataavailable', event => {
                    audioChunks.push(event.data);
                });
                
                mediaRecorder.start();
                
                // Update UI
                micIcon.classList.add('recording');
                recordingStatus.textContent = 'Recording...';
                stopRecordingBtn.disabled = false;
                
                // Start timer
                recordingSeconds = 0;
                updateRecordingTimer();
                recordingTimer = setInterval(updateRecordingTimer, 1000);
            })
            .catch(error => {
                console.error('Error accessing microphone:', error);
                alert('Could not access your microphone. Please check permissions.');
                // Reset UI if microphone access fails
                startRecordingBtn.style.display = 'inline-block';
                stopRecordingBtn.style.display = 'inline-block';
                stopRecordingBtn.disabled = true;
            });
    }

    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
            
            // Stop all tracks in the stream
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
            
            // Update UI
            micIcon.classList.remove('recording');
            recordingStatus.textContent = 'Recording ready to send';
            
            // Stop timer
            clearInterval(recordingTimer);
            
            mediaRecorder.addEventListener('stop', () => {
                // Store the audio blob but don't process it yet
                recordedAudioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                
                // Show redo and send buttons, hide stop button
                stopRecordingBtn.style.display = 'none';
                stopRecordingBtn.disabled = true;
                redoRecordingBtn.style.display = 'inline-block';
                sendRecordingBtn.style.display = 'inline-block';
            });
        }
    }
    
    function redoRecording() {
        // Reset and start a new recording
        recordedAudioBlob = null;
        startRecording();
    }
    
    function sendRecording() {
        if (recordedAudioBlob) {
            // Process the recorded audio
            processInput('audio', recordedAudioBlob);
            
            // Reset UI
            redoRecordingBtn.style.display = 'none';
            sendRecordingBtn.style.display = 'none';
            startRecordingBtn.style.display = 'inline-block';
            recordingStatus.textContent = 'Processing your recording...';
        } else {
            alert('No recording available to send. Please record audio first.');
        }
    }

    function updateRecordingTimer() {
        recordingSeconds++;
        const minutes = Math.floor(recordingSeconds / 60).toString().padStart(2, '0');
        const seconds = (recordingSeconds % 60).toString().padStart(2, '0');
        recordingTimerDisplay.textContent = `${minutes}:${seconds}`;
    }

    // File upload
    const fileUploadContainer = document.querySelector('.upload-container');
    const fileUploadInput = document.getElementById('file-upload');
    const fileInfo = document.getElementById('file-info');
    const processFileBtn = document.getElementById('process-file-btn');
    
    fileUploadContainer.addEventListener('click', () => {
        fileUploadInput.click();
    });
    
    fileUploadContainer.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUploadContainer.style.borderColor = '#3a86ff';
    });
    
    fileUploadContainer.addEventListener('dragleave', () => {
        fileUploadContainer.style.borderColor = '#ddd';
    });
    
    fileUploadContainer.addEventListener('drop', (e) => {
        e.preventDefault();
        fileUploadContainer.style.borderColor = '#ddd';
        
        if (e.dataTransfer.files.length) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });
    
    fileUploadInput.addEventListener('change', () => {
        if (fileUploadInput.files.length) {
            handleFileUpload(fileUploadInput.files[0]);
        }
    });
    
    function handleFileUpload(file) {
        const allowedTypes = [
            'text/plain',
            'audio/wav',
            'audio/mpeg',
            'audio/flac',
            'audio/x-flac'
        ];
        
        if (!allowedTypes.includes(file.type) && 
            !(file.name.endsWith('.txt') || 
              file.name.endsWith('.wav') || 
              file.name.endsWith('.mp3') || 
              file.name.endsWith('.flac'))) {
            alert('Please upload a .txt, .wav, .mp3, or .flac file');
            return;
        }
        
        fileInfo.textContent = `Selected file: ${file.name} (${formatFileSize(file.size)})`;
        processFileBtn.disabled = false;
        
        processFileBtn.onclick = () => {
            processInput('file', file);
        };
    }
    
    function formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' bytes';
        else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
        else return (bytes / 1048576).toFixed(1) + ' MB';
    }

    // Function to update transcribed text and regenerate output
    function updateTranscribedText(newText, requestId) {
        // Show loading state
        const outputSection = document.getElementById('output-section');
        const loading = document.getElementById('loading');
        const result = document.getElementById('result');
        
        outputSection.style.display = 'block';
        loading.style.display = 'flex';
        result.style.display = 'none';
        
        // Prepare form data
        const formData = new FormData();
        formData.append('text', newText);
        formData.append('is_edited_transcription', 'true');
        
        // Send request to server
        fetch('/process', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Server error');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Display results
            const transformedText = document.getElementById('transformed-text');
            const audioPlayer = document.getElementById('audio-player');
            const downloadAudio = document.getElementById('download-audio');
            
            transformedText.textContent = data.transformed_text;
            audioPlayer.src = data.audio_url;
            
            // Set up download button
            downloadAudio.onclick = () => {
                const a = document.createElement('a');
                a.href = data.audio_url;
                a.download = 'cockpit_voice.wav';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            };
            
            // Hide loading, show result
            loading.style.display = 'none';
            result.style.display = 'block';
            
            // Scroll to results
            outputSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        })
        .catch(error => {
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
            loading.style.display = 'none';
        });
    }
    
    // Process input and handle API calls
    function processInput(type, data) {
        // Show loading state
        const outputSection = document.getElementById('output-section');
        const loading = document.getElementById('loading');
        const result = document.getElementById('result');
        
        outputSection.style.display = 'block';
        loading.style.display = 'flex';
        result.style.display = 'none';
        
        // Prepare form data
        const formData = new FormData();
        
        if (type === 'text') {
            formData.append('text', data);
        } else if (type === 'audio') {
            formData.append('audio', data, 'recording.wav');
        } else if (type === 'file') {
            formData.append('file', data);
        }
        
        // Send request to server
        fetch('/process', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Server error');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Display results
            const transformedText = document.getElementById('transformed-text');
            const audioPlayer = document.getElementById('audio-player');
            const downloadAudio = document.getElementById('download-audio');
            const transcriptionSection = document.getElementById('transcription-section');
            const transcriptionText = document.getElementById('transcription-text');
            
            transformedText.textContent = data.transformed_text;
            audioPlayer.src = data.audio_url;
            
            // Show transcription if available (for audio inputs)
            if (data.transcription_text) {
                transcriptionText.value = data.transcription_text;
                originalTranscription = data.transcription_text;
                transcriptionSection.style.display = 'block';
                
                // Set up the update transcription button
                const updateTranscriptionBtn = document.getElementById('update-transcription');
                updateTranscriptionBtn.onclick = () => {
                    updateTranscribedText(transcriptionText.value, data.request_id);
                };
            } else {
                transcriptionSection.style.display = 'none';
            }
            
            // Set up download button
            downloadAudio.onclick = () => {
                const a = document.createElement('a');
                a.href = data.audio_url;
                a.download = 'cockpit_voice.wav';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            };
            
            // Hide loading, show result
            loading.style.display = 'none';
            result.style.display = 'block';
            
            // Scroll to results
            outputSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        })
        .catch(error => {
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
            loading.style.display = 'none';
        });
    }
});
