# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from transformers import pipeline

CLASSIFIER = pipeline('sentiment-analysis', device=0)

def sentiment_analysis(sentence):
    return CLASSIFIER(sentence)[0]# ["label"] == "NEGATIVE"