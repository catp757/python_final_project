import requests
import json

def emotion_detector(text_to_analyse):
    # Define the URL for the emotion analysis API
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'

    # Create the request payload
    myobj = {"raw_document": {"text": text_to_analyse}}

    # Set the request headers
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    # Make the POST request
    response = requests.post(url, json=myobj, headers=header)

    # Convert the response text to a Python dictionary using json.loads()
    try:
        formatted_response = json.loads(response.text)
    except ValueError:
        return "Error: Invalid JSON response"

	# Check for 404 status
    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
		
    # Extract the emotion scores
    try:
        emotion_scores = formatted_response['emotionPredictions'][0]['emotion']
        anger_score = emotion_scores.get('anger', 0)
        disgust_score = emotion_scores.get('disgust', 0)
        fear_score = emotion_scores.get('fear', 0)
        joy_score = emotion_scores.get('joy', 0)
        sadness_score = emotion_scores.get('sadness', 0)
    except (KeyError, IndexError, TypeError):
        return "Error: Malformed response structure"

    # Identify the dominant emotion (emotion with the highest score)
    emotions = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score
    }
    
    dominant_emotion = max(emotions, key=emotions.get)

    # Return the structured result
    return {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score,
        'dominant_emotion': dominant_emotion
    }