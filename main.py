from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: List[str]

positive_words = {
    "love","great","excellent","amazing","good","happy",
    "wonderful","fantastic","awesome","nice","like",
    "best","enjoy","pleasant","brilliant","perfect",
    "super","positive","delight","smile","glad"
}

negative_words = {
    "hate","terrible","bad","awful","worst","sad",
    "angry","horrible","disappointed","poor",
    "negative","pain","annoying","upset","cry",
    "frustrated","dislike","disaster","fail","problem"
}

def analyze_sentiment(sentence: str) -> str:
    text = sentence.lower()

    # strong phrase detection first
    if any(phrase in text for phrase in ["not good", "very bad", "really bad", "so sad"]):
        return "sad"
    if any(phrase in text for phrase in ["very good", "really good", "so happy", "love it"]):
        return "happy"

    words = re.findall(r'\b\w+\b', text)

    pos_score = sum(1 for word in words if word in positive_words)
    neg_score = sum(1 for word in words if word in negative_words)

    if pos_score > neg_score:
        return "happy"
    elif neg_score > pos_score:
        return "sad"
    else:
        return "neutral"

@app.post("/sentiment")
def sentiment_analysis(request: SentimentRequest):
    return {
        "results": [
            {
                "sentence": sentence,
                "sentiment": analyze_sentiment(sentence)
            }
            for sentence in request.sentences
        ]
    }
