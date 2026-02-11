import flet as ft
from flet import TextField
import requests
import html
import random
import time
import threading


def main(page: ft.Page) -> None:
    cash = 0
    i = 0
    secs = 60
    cash_builder_list = []
    randlist = []
    timer_running = True
    page.title = 'The follow'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    cashbuilderqs = 80


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
                    q['incorrect_answers'] = [html.unescape(w) for w in q['incorrect_answers']]
                return results
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []

    def cash_builder(questiontext, right, wronglist, category, difficulty,timer_text):
        nonlocal randlist, timer_running, secs, cash
        if timer_running == False:
            secs = 60


        def rys(e):
            nonlocal cash, i
            cash = 0
            i = 0
            phase_one()

        def check_answer(e):
            nonlocal cash, i, cashbuilderqs
            response = e.control.data

            if response == right:
                print("\n\n CORRECT \n\n")
                page.clean()
                time.sleep(0.05)
                page.add(
                    ft.Row(
                        controls=[ft.Text(value="CORRECT", size=20)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                )
                time.sleep(0.2)
                page.clean()
                if difficulty == "medium":
                    cash += 3000
                elif difficulty == "easy":
                    cash += 1500
                elif difficulty == "hard":
                    cash += 5500

                i += 1
                cashbuilderqs -= 1
                print(cashbuilderqs)
                if cashbuilderqs > 0:
                    run_next_question(timer_text)
                else:
                    pass #next round here
            else:
                print(f"Wrong")
                i+=1
                cashbuilderqs -= 1
                print(cashbuilderqs)
                if cashbuilderqs > 0:
                    run_next_question(timer_text)
                else:
                    pass  #next round here
                page.update()
            if cash <= 6000:
                high = cash * 10
                low = cash / 4
            elif cash <= 11000:
                high = cash * 5
                low = int(cash / 2)
            elif cash <= 16000:
                high = cash * int(random.choice([5, 6, 6, 6, 6]))
                low = 2000
            else:
                high = cash * 9
                low = -1 * int(cash / 2)

        page.clean()
        questions = wronglist
        questions.append(right)
        randlist = random.sample(questions, len(questions))

        page.add(
            ft.Row(
                controls=[ft.Text(value=f"You have ${cash}", size=10, color='green')],
                alignment=ft.MainAxisAlignment.END
            ),
            ft.Row(
                controls=[ft.Text(value=questiontext, size=25)],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[ft.Text(value=f"\nCategory: {category}", size=20)],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[timer_text],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[
                    button_1 := ft.Button(
                        content=ft.Text(randlist[0]),
                        data=randlist[0],
                        on_click=check_answer,
                    ),
                    button_2 := ft.Button(
                        content=ft.Text(randlist[1]),
                        data=randlist[1],
                        on_click=check_answer,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[
                    button_3 := ft.Button(
                        content=ft.Text(randlist[2]),
                        data=randlist[2],
                        on_click=check_answer,
                    ),
                    button_4 := ft.Button(
                        content=ft.Text(randlist[3]),
                        data=randlist[3],
                        on_click=check_answer,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        page.update()

    def run_next_question(timer_text):
        nonlocal i, cash_builder_list
        try:
            dictT = cash_builder_list[i]
        except IndexError as e:
            print(f"Error: {e}")
        cash_builder(
            dictT["question"],
            dictT["correct_answer"],
            dictT["incorrect_answers"],
            dictT["category"],
            dictT["difficulty"],
            timer_text
        )

    def phase_one():
        nonlocal cash_builder_list, i
        timer_text = ft.Text(value="60 seconds remaining...", size=15, color="red")
        def s60_sec():
            nonlocal timer_running, secs, timer_text
            while secs > 0 and timer_running:
                time.sleep(1)
                secs -= 1
                timer_text.value = f"{secs} seconds remaining..."
                try:
                    timer_text.update()
                except Exception as e:
                    print(f"Error: {e}")
            timer_running = False
            print("successs")
            pass #add next phase here

        cash_builder_list = get_questions(50, f'difficulty={random.choice(["easy", "medium", "hard"])}','type=multiple')
        time.sleep(2)
        cash_builder_list_return_of_the_jedi = get_questions(30, f'difficulty={random.choice(["easy", "medium", "hard"])}','type=multiple')
        cash_builder_list.extend(cash_builder_list_return_of_the_jedi)
        i = 0
        if cash_builder_list:
            print(len(cash_builder_list))
            run_next_question(timer_text)
            timer_running = True
            timer_thread = threading.Thread(target=s60_sec, daemon=True)
            timer_thread.start()



    phase_one()


    # h2h_list = get_questions(10, f'difficulty={h2h_type(cash)}','type=multiple')

if __name__ == '__main__':
    ft.run(main)