import time
import io
import os
import webbrowser

# load config
import json
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

# Service credentials
# import google.auth
# credentials, project = google.auth.default()
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file(
    data["GOOGLE"]["CREDENTIALS_PATH"])
scoped_credentials = credentials.with_scopes(
    ['https://www.googleapis.com/auth/cloud-platform'])

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# The name of the image file to annotate
from screengrab import screenshot
IMAGE_PATH = os.path.join(
    os.path.dirname(__file__), data["LOCAL"]["IMAGE_PATH"])
from utils import logit

# List of words to clean from the question during google search
WORDS_TO_STRIP = [
    'who', 'what', 'where', 'when', 'of', 'and', 'that', 'have', 'for',
    'on', 'with', 'as', 'this', 'by', 'from', 'they', 'a', 'an', 'and', 'my',
    'in', 'to', '?', ',', 'these'
]

# Instantiates a Google Vision client with explicit creds
client = vision.ImageAnnotatorClient(credentials=scoped_credentials)

# MAIN METHOD TO EXPORT
def parse_screenshot(path, should_launch=True):
    # 1. Grab the screenshot
    take_screenshot(path)
    # 2. Parse for the block texts
    texts_and_bounds = detect_text_with_bounds(path)
    # 3. Parse into questions and answers
    questions_and_answers = get_questions_and_answers(*texts_and_bounds, should_launch=True)
    # print("{}".format(questions_and_answers))
    return questions_and_answers

def take_screenshot(path):
    # Grab the screenshot
    # START_SCREENGRAB = time.time()
    screenshot(path)
    # END_SCREENGRAB = time.time()
    # logit("SCREENGRAB", START_SCREENGRAB, END_SCREENGRAB)

def get_questions_and_answers(block_texts, block_bounds, should_launch=True):
    """
    - return a dict with `question` and array of `answers` (attempt to get 3)
    - launches the question in web browser
    """
    question = block_texts[0]

    # launch in browser as soon as we have the question
    if (should_launch):
        launch_web(question)

    answers = []
    answerIndex = 1 # should only ever be 3 answers (indices 1-3)
    while (answerIndex <= 3 and answerIndex < len(block_texts)):
        answers.append(block_texts[answerIndex]) 
        answerIndex += 1

    # print out answers for debugging
    for i, text in enumerate(answers):
            print("{}: {}".format(i, text))
            
    return {'question': question, 'answers': answers}

# launch with clean question
def launch_web(original_question):
    words = original_question.split()
    words = [word for word in words if word.lower() not in WORDS_TO_STRIP]
    url = "https://www.google.com.tr/search?q={}".format(' '.join(words))
    webbrowser.open_new_tab(url)

def detect_text_with_bounds(path):
    """
    Detects text in the file with bounds.
    Returns a tuple of the block texts and block bounds
    """
    # START_DOC_OCR = time.time()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    # END_DOC_OCR = time.time()
    # logit("DOC OCR", START_DOC_OCR, END_DOC_OCR)

    block_bounds = []
    block_texts = []
    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                # print("paragraph words length: {}".format(len(paragraph.words)))
                block_words.extend(paragraph.words)

            # print("block words length: {}".format(len(block_words)))
            block_words_mapped = list(map(map_words, block_words))

            block_text = ' '.join(block_words_mapped)
            # print('Block Content: {}'.format(block_text))
            # print('Block Bounds:\n {}'.format(block.bounding_box))
            block_texts.append(block_text)
            block_bounds.append(block.bounding_box)

    return (block_texts, block_bounds)

def is_question_block(bounding_box):
    """incredibly quick-and-dirty check to see if this is probably a question"""
    top_left = bounding_box.vertices[0]
    bottom_right = bounding_box.vertices[3]
    return bottom_right.y - top_left.y > 100

def map_words(word):
    characters = list(map(lambda symbol: symbol.text, word.symbols))
    return ''.join(characters)


if __name__ == '__main__':
    # Get the questions and answers
    questions_and_answers = parse_screenshot(IMAGE_PATH)
