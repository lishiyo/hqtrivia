HQ Trivia Hack
===============

Inspired by [this medium post](https://hackernoon.com/i-hacked-hq-trivia-but-heres-how-they-can-stop-me-68750ed16365) but uses Pillow for screenshotting and Google Vision API for OCR parsing instead.

Usage:
```
workon venv 
pip install -r requirements.txt

// download a credentials.json service credentials file from a Google Vision-enabled Cloud Platform project (see OCR section below)
// then create config.json following config.json.sample

// connect iphone to Mac
// position quicktime player at top left -> select New Movie Recording
// open recording button dropdown -> switch Movie recording to iphone

// run the full script:
// - will launch browser to google search of the question
// - in terminal, prints out the search results count for each q+a search (usually, take the  one with largest count)
python main.py
```

### 1 - Grab screenshot

USAGE: `from screengrab import screenshot`

- Quicktime player must be positioned at top left of screen, on iPhone recording
- Uses PILLOW imagegrab - bounding box grabs only question + the multiple choice answers

### 2 - OCR detect text

USAGE: `from detect_text import parse_screenshot`

- Processes screenshot into question + answers
- Launches browser to google search of the question

This uses Google Cloud Vision api, so make sure you've downloaded a service account file from a Google Cloud project that has [enabled Google Cloud Vision](https://cloud.google.com/vision/docs/before-you-begin). See "using a service account": https://cloud.google.com/vision/docs/auth

Then add the path of that service account json file `config.json` as `CREDENTIALS_PATH`.

`py detect_text.py` returns a dict:
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

Notes:
- if the question is a "not" question ("which of these is NOT...") take the one with the lowest count
- it's not unusual for the answer to be the second largest