from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from textblob import TextBlob

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

def analyze_sentiment(sentence: str) -> str:
    polarity = TextBlob(sentence).sentiment.polarity

    if polarity > 0.1:
        return "happy"
    elif polarity < -0.1:
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
