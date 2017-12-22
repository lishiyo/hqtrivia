HQ Trivia Hack
===============

Inspired by [this medium post](https://hackernoon.com/i-hacked-hq-trivia-but-heres-how-they-can-stop-me-68750ed16365) but uses Pillow for screenshotting and Google Vision API for OCR parsing instead.

Usage:
```
workon venv 
pip install -r requirements.txt

// either create config.json and credentials.json (service credentials)
// or grab from git-secret
git secret reveal 

// connect iphone to Mac
// position quicktime player at top left -> select New Movie Recording
// open recording button dropdown -> switch Movie recording to iphone

// run the full script and compare which has the most results
python main.py
```

### 1 - Grab screenshot

USAGE: `from screengrab import screenshot`

- Quicktime must be positioned at top left
- Uses PILLOW imagegrab - bounding box grabs only question + the multiple choice answers

### 2 - OCR detect text

USAGE: `from detect_text import parse_screenshot`

Process screenshot into question + answers.

Google Cloud Vision: uses [api-project](https://console.cloud.google.com/apis/dashboard?project=api-project-244156348570&authuser=1&duration=PT1H) for creds:
https://googlecloudplatform.github.io/google-cloud-python/latest/vision/index.html
https://cloud.google.com/vision/docs/detecting-fulltext

`py detect_text.py` returns dict:
```
{
    question: 'After Texas , what U . S . state produces the most crude oil ?'
    answers: ['Oklahoma', 'North Dakota', 'Alaska']
}
```
### 3 - Using Google Custom search, run three custom searches with question + answer.

USAGE: `from google_search import run_query_all`

https://developers.google.com/custom-search/json-api/v1/overview

Compare the total num results for each answer:
```
answer: Oklahoma === TOTAL: 1,180,000
answer: North Dakota === TOTAL: 1,360,000
answer: Alaska === TOTAL: 1,330,000
```