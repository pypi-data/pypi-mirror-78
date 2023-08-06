from flask import Flask, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import json

app = Flask(__name__)

@app.route('/api/video/<id>')
def index(id):
    data = YouTubeTranscriptApi.get_transcript(id, languages=['es'])
    transcription = json.dumps(data)
    return jsonify(transcription)

def hi():                                               
    return "hola"