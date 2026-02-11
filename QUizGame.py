import flet as ft
from flet import TextField
from flet_core.control_event import ControlEvent
import requests
import html
import random
import time
cash = 0


def main(page: ft.Page) -> None:
    page.title = 'The follow'


def get_questions(amount, difficulty, typE):
    url = f"https://opentdb.com/api.php?amount={amount}&{difficulty}&{typE}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        
        if data['response_code'] == 0:
            results = data['results']
            for q in results:
                q['question'] = html.unescape(q['question'])
                q['correct_answer'] = html.unescape(q['correct_answer'])
                q['incorrect_answers'] = [html.unescape(wrongey) for wrongey in q['incorrect_answers']]
            return results
        else:
            print("Error: The API could not return results.")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return []

def h2h_type(cash):
    if cash >= 10000:
        return 'hard'
    elif cash >= 8000:
        return 'medium'
    else:
        return 'easy'
    
def cash_builder(questiontext, right, wronglist, category, difficulty, cash):
    
    questions = wronglist
    questions.append(right)
    randlist = random.sample(questions, len(questions))
    print(
        questiontext,
        f"\nCategory: {category}"
        "\n1: ",
        randlist[0],
        "\n2: ",
        randlist[1],
        "\n3: ",
        randlist[2],
        "\n4: ",
        randlist[3],
        )
    response = input(" -> ")
    if response == str(randlist.index(right)+1) or response.lower() == right.lower():
        print("\n\n CORRECT \n\n")
        if difficulty == "medium":
            cash = 3000
            return cash
        elif difficulty == "easy":
            cash = 1500
            return cash
        elif difficulty == "hard":
            cash = 5500
            return cash
        pass
    else:
        print("\n\n wrong \n\n")
        #wrong booooo
        pass
    


end_time = time.time() + 60
cash_builder_list = get_questions(80, f'difficulty={random.choice(["easy","medium","hard"])}','type=multiple')
i= 0
while time.time() < end_time:
#     time_left = int(end_time - time.time())
#     buttoninflet(f"{time_left} seconds remaining! \n 'Since question started'")
    time.sleep(1)
    dictT = cash_builder_list[i]
    try:
        cash += cash_builder(dictT["question"],dictT["correct_answer"],dictT["incorrect_answers"],dictT["category"],dictT["difficulty"],cash)
    except:
        pass
    print(f"Cash ${cash}")

    i += 1

cash = int(cash)

if cash <= 6000:
    high = cash*10
    low = cash/4
elif cash <= 11000:
    high = cash * 5
    low = int(cash/2)
elif cash <= 16000:
    high = cash * int(random.choice([5,6,6,6,6]))
    low = 2000
else:
    high = cash * 9
    low = -1 * int(cash/2)
    


# h2h_list = get_questions(10, f'difficulty={h2h_type(cash)}','type=multiple')