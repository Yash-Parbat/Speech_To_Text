from flask import Flask, render_template_string, request, jsonify
import speech_recognition as sr
import pyaudio
import threading
import time

app = Flask(__name__)

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        
        # Configure for better performance
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        print("Initializing microphone...")
        self.calibrate_microphone()
    
    def calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        try:
            with self.microphone as source:
                print("Calibrating for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print(f"Calibration complete. Energy threshold: {self.recognizer.energy_threshold}")
        except Exception as e:
            print(f"Calibration warning: {e}")
    
    def recognize_speech(self, timeout=10):
        """Capture and recognize speech"""
        try:
            print("Listening for speech...")
            with self.microphone as source:
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=30)
                print("Audio captured, processing...")
                
                # Use Google Speech Recognition
                text = self.recognizer.recognize_google(audio)
                return {"success": True, "text": text, "engine": "Google"}
                
        except sr.WaitTimeoutError:
            return {"success": False, "error": "Listening timeout - no speech detected"}
        except sr.UnknownValueError:
            return {"success": False, "error": "Could not understand the audio"}
        except sr.RequestError as e:
            return {"success": False, "error": f"Google API error: {e}"}
        except Exception as e:
            return {"success": False, "error": f"Recognition error: {e}"}

# Initialize speech recognizer
speech_engine = SpeechRecognizer()

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Mentor Avatar - Speech-to-Text</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 600px;
            width: 100%;
            text-align: center;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        
        .controls {
            margin-bottom: 30px;
        }
        
        button {
            padding: 15px 30px;
            border: none;
            border-radius: 50px;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.3s;
            margin: 10px;
            min-width: 150px;
        }
        
        .btn-primary {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        
        .btn-primary:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .btn-secondary {
            background: #f8f9fa;
            color: #6c757d;
            border: 2px solid #dee2e6;
        }
        
        .status {
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            font-size: 18px;
            font-weight: 500;
        }
        
        .status.ready {
            background: #e3f2fd;
            color: #1976d2;
            border: 2px solid #bbdefb;
        }
        
        .status.listening {
            background: #e8f5e8;
            color: #2e7d32;
            border: 2px solid #a5d6a7;
            animation: pulse 2s infinite;
        }
        
        .status.processing {
            background: #fff3e0;
            color: #f57c00;
            border: 2px solid #ffcc02;
        }
        
        .status.error {
            background: #ffebee;
            color: #c62828;
            border: 2px solid #ef9a9a;
        }
        
        .results {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            min-height: 100px;
            border: 2px solid #dee2e6;
            text-align: left;
        }
        
        .transcript {
            background: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .transcript-time {
            font-size: 12px;
            color: #666;
            margin-bottom: 5px;
        }
        
        .transcript-text {
            font-size: 16px;
            line-height: 1.5;
            color: #333;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
        
        .empty-state {
            color: #666;
            font-style: italic;
            text-align: center;
            padding: 40px 20px;
        }
        
        .footer {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #dee2e6;
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Mentor Avatar</h1>
        <div class="subtitle">Voice-to-Text Recognition System</div>
        
        <div class="controls">
            <button id="startBtn" class="btn-primary">Start Listening</button>
            <button id="clearBtn" class="btn-secondary">Clear Results</button>
        </div>
        
        <div id="status" class="status ready">
            Click "Start Listening" to begin speech recognition
        </div>
        
        <div class="results" id="results">
            <div class="empty-state">Your transcribed speech will appear here...</div>
        </div>
        
        <div class="footer">
            AI Mentor Avatar - Powered by Speech Recognition
        </div>
    </div>
    
    <script>
        let isListening = false;
        
        const startBtn = document.getElementById('startBtn');
        const clearBtn = document.getElementById('clearBtn');
        const status = document.getElementById('status');
        const results = document.getElementById('results');
        
        startBtn.onclick = toggleListening;
        clearBtn.onclick = clearResults;
        
        function toggleListening() {
            if (isListening) {
                stopListening();
            } else {
                startListening();
            }
        }
        
        function startListening() {
            if (isListening) return;
            
            isListening = true;
            startBtn.textContent = 'Stop Listening';
            startBtn.disabled = true;
            
            status.className = 'status listening';
            status.textContent = 'Listening... Speak now!';
            
            fetch('/recognize', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    addTranscript(result.text);
                    status.className = 'status ready';
                    status.textContent = 'Recognition complete! Click to try again.';
                } else {
                    status.className = 'status error';
                    status.textContent = `Error: ${result.error}`;
                }
                resetButton();
            })
            .catch(error => {
                status.className = 'status error';
                status.textContent = `Network error: ${error.message}`;
                resetButton();
            });
            
            // Enable button after a short delay
            setTimeout(() => {
                startBtn.disabled = false;
            }, 1000);
        }
        
        function stopListening() {
            isListening = false;
            status.className = 'status processing';
            status.textContent = 'Processing audio...';
        }
        
        function resetButton() {
            isListening = false;
            startBtn.textContent = 'Start Listening';
            startBtn.disabled = false;
        }
        
        function clearResults() {
            results.innerHTML = '<div class="empty-state">Your transcribed speech will appear here...</div>';
        }
        
        function addTranscript(text) {
            // Remove empty state if present
            if (results.innerHTML.includes('empty-state')) {
                results.innerHTML = '';
            }
            
            const transcript = document.createElement('div');
            transcript.className = 'transcript';
            transcript.innerHTML = `
                <div class="transcript-time">
                    ${new Date().toLocaleTimeString()}
                </div>
                <div class="transcript-text">${text}</div>
            `;
            
            results.insertBefore(transcript, results.firstChild);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/recognize', methods=['POST'])
def recognize():
    """Handle speech recognition request"""
    try:
        result = speech_engine.recognize_speech(timeout=15)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": f"Server error: {str(e)}"
        })

def main():
    """Main function to run the Flask app"""
    print("=" * 60)
    print("AI MENTOR AVATAR - SPEECH-TO-TEXT")
    print("=" * 60)
    print("Starting Flask server...")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")

if __name__ == "__main__":
    main()
    