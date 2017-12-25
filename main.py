# will take screenshot => output/screenshot.png
from detect_text import parse_screenshot, logit, IMAGE_PATH
from google_search import run_query_all
import time


START_FULL = time.time()

def main():
    q_and_a = parse_screenshot(IMAGE_PATH)
    # START_QUERY_ALL = time.time()
    (question, results) = run_query_all(q_and_a['question'], q_and_a['answers'])

    # END_QUERY_ALL = time.time()
    # logit("QUERY ALL", START_QUERY_ALL, END_QUERY_ALL)
    for (answer, total) in results:
        print("answer: {} === TOTAL: {}".format(answer, total))

if __name__ == '__main__':
    main()

    END_FULL = time.time()
    logit("FULL", START_FULL, time.time())