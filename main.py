from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import re

app = FastAPI()

class SentimentRequest(BaseModel):
    sentences: List[str]

positive_words = {
    "love", "great", "excellent", "amazing", "good", "happy",
    "wonderful", "fantastic", "awesome", "nice", "like", "best"
}

negative_words = {
    "hate", "terrible", "bad", "awful", "worst", "sad",
    "angry", "horrible", "disappointed", "poor"
}

def analyze_sentiment(sentence: str) -> str:
    text = sentence.lower()
    words = re.findall(r'\b\w+\b', text)

    positive_score = sum(word in positive_words for word in words)
    negative_score = sum(word in negative_words for word in words)

    if positive_score > negative_score:
        return "happy"
    elif negative_score > positive_score:
        return "sad"
    else:
        return "neutral"

@app.post("/sentiment")
def sentiment_analysis(request: SentimentRequest):
    results = []

    for sentence in request.sentences:
        sentiment = analyze_sentiment(sentence)
        results.append({
            "sentence": sentence,
            "sentiment": sentiment
        })

    return {"results": results}
