import requests
import html
import random
import time



cash = 0



def get_questions(amount, difficulty, typE):
    url = f"https://opentdb.com/api.php?amount={amount}&{difficulty}&{typE}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        
        if data['response_code'] == 0:
            return data['results']
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
    if response == str(randlist.index(right)+1) or response == right:
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
cash_builder_list = get_questions(60, f'difficulty={random.choice(["easy","medium","hard"])}','type=multiple')
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

# h2h_list = get_questions(10, f'difficulty={h2h_type(cash)}','type=multiple')