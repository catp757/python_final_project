''' Executing this function initiates the application of sentiment
    analysis to be executed over the Flask channel and deployed on
    localhost:5000.
'''
import json
import requests
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

#Initiate the flask app
app = Flask("Emotion Detection")

@app.route("/emotionDetector")
def emotion_detection():
    text_to_analyze = request.args.get('textToAnalyze')

    if (not text_to_analyze) or (text_to_analyze.strip() == ""):
        return "Please enter text to analyze."

    try:
        response = emotion_detector(text_to_analyze)

        # If the function returns None for dominant_emotion, input was invalid
        if response['dominant_emotion'] is None:
            return "Invalid text! Please try again!"

        # Extract emotions and format the response
        return (
            f"For the given statement, the system response is "
            f"'anger': {response['anger']}, 'disgust': {response['disgust']}, "
            f"'fear': {response['fear']}, 'joy': {response['joy']} and "
            f"'sadness': {response['sadness']}. The dominant emotion is {response['dominant_emotion']}."
        )

    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route("/")
def render_index_page():
    ''' This function initiates the rendering of the main application
        page over the Flask channel
    '''
    return render_template('index.html')

if __name__ == "__main__":
    #This functions executes the flask app and deploys it on localhost:5000
    app.run(host="0.0.0.0", port=5050)
