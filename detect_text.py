import time
import io
import os

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

def logit(tag, start, end):
    print("\n ====== {} TOTAL TIME: {} =====".format(tag,
                                                     ((end - start) * 1000.0)))

# Instantiates a Google Vision client with explicit creds
client = vision.ImageAnnotatorClient(credentials=scoped_credentials)

# MAIN METHOD TO EXPORT
def parse_screenshot(path):
    # 1. Grab the screenshot
    take_screenshot(path)
    # 2. Parse for the block texts
    texts_and_bounds = detect_text_with_bounds(path)
    # 3. Parse into questions and answers
    questions_and_answers = get_questions_and_answers(*texts_and_bounds)
    print("questions and answers: {}".format(questions_and_answers))
    return questions_and_answers


def take_screenshot(path):
    # Grab the screenshot
    START_SCREENGRAB = time.time()
    screenshot(path)
    END_SCREENGRAB = time.time()
    logit("SCREENGRAB", START_SCREENGRAB, END_SCREENGRAB)


def get_questions_and_answers(block_texts, block_bounds):
    """return a dict with `question` and array of `answers`"""
    question = None
    answers = []
    for i, text in enumerate(block_texts):
        bounds = block_bounds[i]
        # the question is the first block
        if (question is None and is_question_block(bounds)):
            question = text
        elif len(answers) <= 3 and not text.isnumeric():
            answers.append(text)
        elif len(answers) == 3:
            break  # reached total num

    return {'question': question, 'answers': answers}


def detect_text_with_bounds(path):
    """
    Detects text in the file with bounds.
    Returns a tuple of the block texts and block bounds
    """
    START_DOC_OCR = time.time()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    END_DOC_OCR = time.time()
    logit("DOC OCR", START_DOC_OCR, END_DOC_OCR)

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
            print('Block Content: {}'.format(block_text))
            # print('Block Bounds:\n {}'.format(block.bounding_box))
            block_texts.append(block_text)
            block_bounds.append(block.bounding_box)

    return (block_texts, block_bounds)


# def detect_text(path):
#     """Detects text in the file."""

#     START_OCR = time.time()
#     with io.open(path, 'rb') as image_file:
#         content = image_file.read()

#     image = types.Image(content=content)

#     response = client.text_detection(image=image)
#     # https://cloud.google.com/vision/docs/reference/rest/v1/images/annotate#textannotation
#     texts = response.text_annotations

#     END_OCR = time.time()
#     logit("OCR", START_OCR, END_OCR)

#     for text in texts:
#         print('\n DESCRIPTION: "{}"'.format(text.description))
#         if hasattr(text, 'bounding_poly'):
#             vertices = ([
#                 '({},{})'.format(vertex.x, vertex.y)
#                 for vertex in text.bounding_poly.vertices
#             ])
#             print('bounds: {}'.format(','.join(vertices)))
#             print("TEXT FULL: {}".format(text))
#         else:
#             print("no bounding_poly")


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
