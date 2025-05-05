import requests
import json

def emotion_detector(text_to_analyse):
    none_response = {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
    }

    # Return None values for blank input
    if not text_to_analyse or text_to_analyse.strip() == "":
        return none_response

    # Define the URL and headers
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = {"raw_document": {"text": text_to_analyse}}

    try:
        response = requests.post(url, json=myobj, headers=header)
    except requests.exceptions.RequestException:
        # Handle connection error or timeout
        return none_response

    # Handle blank input or invalid API usage
    if response.status_code == 400:
        return none_response

    # Parse valid response
    try:
        formatted_response = json.loads(response.text)
        emotion_scores = formatted_response['emotionPredictions'][0]['emotion']
        anger = emotion_scores.get('anger', 0)
        disgust = emotion_scores.get('disgust', 0)
        fear = emotion_scores.get('fear', 0)
        joy = emotion_scores.get('joy', 0)
        sadness = emotion_scores.get('sadness', 0)

        # Find dominant emotion
        emotions = {
            'anger': anger,
            'disgust': disgust,
            'fear': fear,
            'joy': joy,
            'sadness': sadness
        }
        dominant_emotion = max(emotions, key=emotions.get)

        return {
            'anger': anger,
            'disgust': disgust,
            'fear': fear,
            'joy': joy,
            'sadness': sadness,
            'dominant_emotion': dominant_emotion
        }

    except (ValueError, KeyError, IndexError, json.JSONDecodeError, TypeError):
        return none_response