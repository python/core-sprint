"""

1. Download and save the html page from slido as "qa.html" (manual download): https://app.sli.do/event/d4ifvw2o/live/questions
2. `python3-m pip install beautifulsoup4` (in a virtualenv)
3. `python scrapeslido.py`
4. csv is created as "q_a_export.csv"
"""

from bs4 import BeautifulSoup
from dataclasses import dataclass

import csv

@dataclass
class Question:

    author_name: str
    upvote_count: int
    question_text: str
    question_date: str

def main():

    with open("./qa.html", "rb") as file:
        html = file.read()
    if html is not None:
        soup = BeautifulSoup(html, 'html.parser')
        question_items = soup.find_all("div", class_="card question-item")
        questions = []
        for question_item in question_items:
            question_text = question_item.select("div.question-item__body > span.Linkify")[0].text
            upvote_count = int(question_item.select("div.score > button > span")[0].text)
            author_name = question_item.select("div.question-item__author")[0].text
            question_date = question_item.select("div.question-item__date")[0].text
            q = Question(author_name, upvote_count, question_text, question_date)
            questions.append(q)

        with open("q_a_export.csv", "w+") as csvfile:
            writer = csv.writer(csvfile)
            for q in questions:
                writer.writerow([q.question_date, q.upvote_count, q.author_name, q.question_text])

main()