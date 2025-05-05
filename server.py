''' Executing this function initiates the application of emotion detection 
    to be executed over the Flask channel and deployed on
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
    ''' This code receives the text from the HTML interface and
        runs emotion detection over it using emotion_detector()
        function. The output returned shows the score for each emotion.
    '''
    # Retrieve the text to detect the emotion for from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')

    # Check if text was entered
    if not text_to_analyze or text_to_analyze.strip() == "":
        return "Please enter text to analyze."

    try:
        # Call the emotion detector function
        response = emotion_detector(text_to_analyze)
		
		# If the function returns None for dominant_emotion, input was invalid
        if response['dominant_emotion'] is None:
            return "Invalid text! Please try again!"

        # Extract emotion scores and dominant emotion
        anger = response['anger']
        disgust = response['disgust']
        fear = response['fear']
        joy = response['joy']
        sadness = response['sadness']
        dominant = response['dominant_emotion']

        # Format the response message
        return (
            f"For the given statement, the system response is "
            f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
            f"'joy': {joy} and 'sadness': {sadness}. "
            f"The dominant emotion is {dominant}."
        )

    except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError) as e:
        return f"An error occurred during emotion detection: {str(e)}"

@app.route("/")
def render_index_page():
    ''' This function initiates the rendering of the main application
        page over the Flask channel
    '''
    return render_template('index.html')

if __name__ == "__main__":
    #This functions executes the flask app and deploys it on localhost:5000
    app.run(host="0.0.0.0", port=5000)
    