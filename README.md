🧠 AI Mentor Avatar – Speech-to-Text Web App
A sleek and interactive Flask-based web application that captures live speech from your microphone, transcribes it using Google Speech Recognition, and displays the results on a beautifully designed frontend.

🚀 Features
🎤 Real-time voice-to-text recognition

🌐 Web-based interface with responsive design

✅ Uses Google’s speech recognition engine

📦 Built with Flask, JavaScript, HTML, and CSS

⚙️ Automatic microphone calibration for noise

🔁 Reset/Clear transcript functionality

📱 Mobile-friendly UI

🖼️ Demo UI Snapshot
The interface features a modern gradient design with large buttons, real-time status updates, and a transcript viewer that shows the recognized speech.

🧰 Tech Stack
Component	Technology
Backend	Flask (Python)
Frontend	HTML, CSS, JavaScript
Speech Recognition	speech_recognition (Google API)
Audio Interface	PyAudio

📦 Prerequisites
Make sure the following are installed:

Python 3.7+

PortAudio (required for pyaudio)

Virtualenv (recommended)

🔧 Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/your-username/ai-mentor-avatar.git
cd ai-mentor-avatar
Set up and activate a virtual environment:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
If you don’t have a requirements.txt, use:

bash
Copy
Edit
pip install Flask speechrecognition pyaudio
(Optional) Install PyAudio with system support:

Linux (Debian/Ubuntu):

bash
Copy
Edit
sudo apt-get install portaudio19-dev python3-pyaudio
Windows: Use pre-built wheels from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

▶️ Running the App
Once everything is installed:

bash
Copy
Edit
python app.py
The server will start at:
📍 http://localhost:5000

🗣️ How It Works
Click Start Listening.

Speak clearly into your microphone.

The system captures and sends your audio to the backend.

The backend processes the audio using Google Speech Recognition.

The transcribed text is sent back and displayed on the page.

🧪 Troubleshooting
❗ Microphone not working?

Ensure system microphone permissions are granted.

Try running the app with administrative privileges.

📁 File Structure
csharp
Copy
Edit
.
├── app.py                # Main Flask application
├── templates             # (Not used, since HTML is inline)
├── static                # (Optional for external CSS/JS)
└── README.md             # Project documentation
📜 License
MIT License © 2025 Yash Parbat

🙋‍♂️ Author
Created with ❤️ by Yash Parbat
