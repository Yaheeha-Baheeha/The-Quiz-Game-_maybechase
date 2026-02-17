import flet as ft
from flet import TextField
import requests
import html
import random
import time
import threading
import os
import asyncio

def main(page: ft.Page) -> None:
    cash = 0
    high = 0
    low = 0
    i = 0
    lost = False
    secs = 60
    textanswer = ""
    prev_right = ["",""]
    cash_builder_list = []
    rand_list = []
    timer_running = True
    page.title = 'The Chase'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 1280
    page.window.height = 720
    page.window.resizable = False
    page.window.maximizable = False
    page.update()
    cash_builder_qs = 80
    score = 0

    def last_phase():
        nonlocal timer_running, secs


        def phase_chaser():
            nonlocal score, cash
            page.clean()
            page.update()
            smth = random.gauss(19, 5)
            smth = max(3 , min(25, smth))
            smth = int(smth)
            if score > smth:
                page.clean()
                page.add(
                    ft.Column(
                        controls=[
                            ft.Text(value=f"YOU WIN ${cash} \n you got {score} right, chaser got {smth} right", size=80, color="green")
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                )
                page.update()
            else:
                page.clean()
                page.add(
                    ft.Column(
                        controls=[
                            ft.Text(value=f"YOU Loose ${cash} \n you got {score} right, chaser got {smth} right",size=80, color="red")
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                )

        def run_next_question2(timer_text):
            nonlocal i, cash_builder_list, timer_running
            if timer_running == False:
                phase_chaser()
            else:
                try:
                    dictT = cash_builder_list[i]
                except IndexError as e:
                    print(f"Error: {e}")
                    phase_two()
                    timer_running = False
                    return
                finally_therock(
                    dictT["question"],
                    dictT["correct_answer"],
                    dictT["incorrect_answers"],
                    dictT["category"],
                    dictT["difficulty"],
                    timer_text
                )


        def finally_therock(question_text, right, wrong_list, category, difficulty, timer_text):
            nonlocal rand_list, timer_running, secs, score, prev_right,cash_builder_qs
            cash_builder_qs = 80
            right = right
            if timer_running == False:
                secs = 120




            page.clean()

            page.add(
                ft.Row(
                    controls=[ft.Text(value=f"You have ${cash}", size=18, color='green')],
                    alignment=ft.MainAxisAlignment.END
                ),
                ft.Row(
                    controls=[ft.Text(value=question_text, size=22, expand = True,text_align=ft.TextAlign.CENTER,)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[ft.Text(value=f"Category: {category}", size=22, expand = True, text_align=ft.TextAlign.CENTER,)],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    controls=[timer_text],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    controls=[
                        ft.TextField(
                            on_change=handle_field_change,
                            label="Response",
                            hint_text="skill issue",
                        ),
                        button := ft.Button(
                            content=ft.Text("confirm"),
                            data=right,
                            on_click=check_answer,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    controls=[
                        ft.Text(value=f'previous answer "{prev_right[1]}", correct answer: "{prev_right[0]}"', size=22, expand = True, color='pink', )
                    ]
                )
            )
            page.update()
        secs = 120
        timer_text = ft.Text(value="120 seconds remaining...", size=15, color="red")
        timer_running = True
        def check_answer(e):
            nonlocal score, i, cash_builder_qs, prev_right, textanswer

            rights = e.control.data

            prev_right = [rights, textanswer]
            print(prev_right)
            if textanswer.lower() == rights.lower():
                print("\n\n CORRECT \n\n")
                page.clean()
                page.add(
                    ft.Row(
                        controls=[ft.Text(value="CORRECT", size=20)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                )
                page.update()
                page.clean()
                score += 1

                i += 1
                cash_builder_qs -= 1
                print(cash_builder_qs)
                if cash_builder_qs > 0:
                    run_next_question2(timer_text)
                else:
                    phase_chaser()
                    return
            else:
                print(f"Wrong")
                i += 1
                cash_builder_qs -= 1
                print(cash_builder_qs)
                if cash_builder_qs > 0:
                    run_next_question2(timer_text)
                else:
                    phase_chaser(score)
                    return
                page.update()

            response = ""

        async def s120_sec():
            nonlocal timer_running, secs, timer_text
            while secs > 0 and timer_running:
                await asyncio.sleep(1)
                secs -= 1
                timer_text.value = f"{secs} seconds remaining..."
                try:
                    timer_text.update()
                except Exception as e:
                    print(f"Error updating timer: {e}")
            timer_running = False
            print("120-second timer finished")
            phase_chaser()

        async def load_questions():
            nonlocal cash_builder_list, i
            page.clean()
            page.add(
                ft.Column(
                    controls=[
                        ft.Text(value="wait....", size=120, color="red")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            )
            cash_builder_list = get_questions(50, 'hard', 'type=multiple')
            time.sleep(5)
            cash_builder_list += get_questions(30, 'hard', 'type=multiple')
            i = 0
            if cash_builder_list:
                print(f"{len(cash_builder_list)} questions loaded")
                run_next_question2(timer_text)

        page.run_task(load_questions)
        page.run_task(s120_sec)





    def handle_field_change(e):
        nonlocal textanswer
        textanswer = e.control.value

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
                    q['category'] = html.unescape(q['category'])
                return results
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []

    def phase_two():
        nonlocal cash, low, high, page, i
        i = 0
        h2h_list = []
        page.window.width = 1920
        page.window.height = 720
        l = 0
        p = 0
        page.clean()
        page.update()
        chase_ladder = [
            ft.Container(height=90, width=600, bgcolor="0xff0022ff"),
            ft.Container(height=90, width=600, bgcolor="0xff0022ff"),
            ft.Container(height=90, width=600, bgcolor="0xff0022ff"),
            ft.Container(height=90, width=600, bgcolor="0xff0022ff"),
            ft.Container(height=90, width=600, bgcolor="0xff0022ff"),
            ft.Container(height=90, width=600, bgcolor="0xff0022ff"),
            ft.Container(height=90, width=600, bgcolor="0xff0022ff"),
        ]
        right_side = ft.Container(
            content=ft.Column(
                controls=[
                    chase_ladder[0],
                    chase_ladder[1],
                    chase_ladder[2],
                    chase_ladder[3],
                    chase_ladder[4],
                    chase_ladder[5],
                    chase_ladder[6],

                ],
                spacing=1,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            bgcolor="black",
            expand=1,
        )
        def start_question(question_text, right, wrong_list, category, difficulty):
            nonlocal p, i, l, right_side, left_side, chase_ladder, h2h_list, lost
            questions = wrong_list
            questions.append(right)
            rand_list = random.sample(questions, len(questions))
            def check_answer(answer):
                nonlocal right, l, p, i, right_side, left_side, chase_ladder,lost
                response = answer.control.data
                if response == right:
                    l += 1
                    try:
                        chase_ladder[l].bgcolor = "0xff3380de"
                    except Exception as e:
                        print(f"Error: {e}")
                    if l >= 6:
                        last_phase()
                        return
                    else:
                        i+=1
                        start_question(h2h_list[i]["question"], h2h_list[i]["correct_answer"],
                                       h2h_list[i]["incorrect_answers"], h2h_list[i]["category"],
                                       h2h_list[i]["difficulty"])


                elif l == p:
                    page.clean()
                    page.add(
                        ft.Column(
                            controls=[
                                ft.Text(value="you got caught", size=120, color="red")
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    )
                    page.update()
                    lost = True
                if random.random() <= 0.84:
                    p += 1
                    chase_ladder[p].bgcolor = "red"
                    if l == p:
                        page.clean()
                        page.add(
                            ft.Column(
                                controls=[
                                    ft.Text(value="you got caught", size=120, color="red")
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        )
                        page.update()
                        lost = True
                    else:
                        i += 1
                        start_question(h2h_list[i]["question"], h2h_list[i]["correct_answer"],
                                       h2h_list[i]["incorrect_answers"], h2h_list[i]["category"],
                                       h2h_list[i]["difficulty"])
                else:
                    if p <= l or p<=7:
                        i += 1
                        start_question(h2h_list[i]["question"], h2h_list[i]["correct_answer"],
                                       h2h_list[i]["incorrect_answers"], h2h_list[i]["category"],
                                       h2h_list[i]["difficulty"])
                    else:
                        page.clean()
                        page.add(
                            ft.Column(
                                controls=[
                                    ft.Text(value="you got caught", size=120, color="red")
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        )
                        page.update()
                        lost = True
                if lost == False:
                    right_side.update()


            left_side.content = ft.Column(
                controls = [
                    ft.Row(
                        controls=[ft.Text(value=f"You have ${cash}", size=18, color='green')],
                        alignment=ft.MainAxisAlignment.END
                    ),
                    ft.Row(
                        controls=[ft.Text(value=question_text, size=22, expand = True, text_align=ft.TextAlign.CENTER,)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        controls=[ft.Text(value=f"Category: {category}", size=22, expand = True, text_align=ft.TextAlign.CENTER,)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        controls=[
                            button_1 := ft.Button(
                                content=ft.Text(rand_list[0]),
                                data=rand_list[0],
                                on_click=check_answer,
                            ),
                            button_2 := ft.Button(
                                content=ft.Text(rand_list[1]),
                                data=rand_list[1],
                                on_click=check_answer,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        controls=[
                            button_3 := ft.Button(
                                content=ft.Text(rand_list[2]),
                                data=rand_list[2],
                                on_click=check_answer,
                            ),
                            button_4 := ft.Button(
                                content=ft.Text(rand_list[3]),
                                data=rand_list[3],
                                on_click=check_answer,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            )
            left_side.update()
            i+=1

        def head_to_head(diffs):
            nonlocal l, right_side, low, cash, high, chase_ladder, p, i, h2h_list
            chase_ladder[0].bgcolor = "cyan"
            diff = diffs.control.data
            if diff == "hard":
                chase_ladder[1].bgcolor = "0xff3380de"
                cash = high
                l = 1
                p = -1
            elif diff == "easy":
                chase_ladder[1].bgcolor = "cyan"
                chase_ladder[2].bgcolor = "cyan"
                chase_ladder[3].bgcolor = "0xff3380de"
                cash = low
                l = 3
                p = -1
            elif diff == "medium":
                chase_ladder[1].bgcolor = "cyan"
                chase_ladder[2].bgcolor = "0xff3380de"
                l = 2
                p = -1
            right_side.update()
            h2h_list = get_questions(30, f"difficulty={diff}", "type=multiple")
            start_question(h2h_list[i]["question"],h2h_list[i]["correct_answer"],h2h_list[i]["incorrect_answers"],h2h_list[i]["category"],h2h_list[i]["difficulty"])


        left_side = ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(value="Choose your offer", size=120)
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                ft.Row(
                                    controls=[
                                        low_offer := ft.Button(
                                            content=ft.Text(value=f"Low offer: \n$ {low}", size=60),
                                            data='easy',
                                            on_click=head_to_head
                                        ),
                                        cash_offer := ft.Button(
                                            content=ft.Text(value=f"Cash offer: \n$ {cash}", size=60),
                                            data='medium',
                                            on_click=head_to_head
                                        ),
                                        high_offer := ft.Button(
                                            content=ft.Text(value=f"High offer: \n$ {high}", size=60),
                                            data='hard',
                                            on_click=head_to_head
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            value="^This gives you a 4 questions advantage.                          This gives you 3.                                                  This gives you 2",
                                            size=20)
                                    ]
                                )
                            ]
                        ),
                        bgcolor="blue",
                        expand=2,
                    )

        page.add(
            ft.Row(
                controls=[
                    left_side,
                    right_side,
                ],
                expand=True,
            )
        )
        page.update()






    def cash_builder(question_text, right, wrong_list, category, difficulty, timer_text):
        nonlocal rand_list, timer_running, secs, cash, low, high, prev_right

        if timer_running == False:
            secs = 60


        def rys(e):
            nonlocal cash, i
            cash = 0
            i = 0
            phase_one()

        def check_answer():
            nonlocal cash, i, cash_builder_qs, low, high, prev_right, textanswer
            prev_right = [right, textanswer]
            if textanswer == right.lower():
                print("\n\n CORRECT \n\n")
                page.clean()
                page.add(
                    ft.Row(
                        controls=[ft.Text(value="CORRECT", size=20)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                )
                page.clean()
                if difficulty == "medium":
                    cash += 3000
                elif difficulty == "easy":
                    cash += 1500
                elif difficulty == "hard":
                    cash += 5500

                i += 1
                cash_builder_qs -= 1
                print(cash_builder_qs)
                if cash_builder_qs > 0:
                    run_next_question(timer_text)
                else:
                    phase_two()
                    return
            else:
                print(f"Wrong")
                i+=1
                cash_builder_qs -= 1
                print(cash_builder_qs)
                if cash_builder_qs > 0:
                    run_next_question(timer_text)
                else:
                    phase_two()
                    return
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

            response = ""

        page.clean()
        questions = wrong_list
        questions.append(right)
        rand_list = random.sample(questions, len(questions))

        page.add(
            ft.Row(
                controls=[ft.Text(value=f"You have ${cash}", size=18, color='green')],
                alignment=ft.MainAxisAlignment.END
            ),
            ft.Row(
                controls=[ft.Text(value=question_text, size=22, expand = True, text_align=ft.TextAlign.CENTER,)],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[ft.Text(value=f"Category: {category}", size=22, expand = True, text_align=ft.TextAlign.CENTER,)],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[timer_text],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[
                    ft.TextField(
                        on_change=handle_field_change,
                        label="Response",
                        hint_text="skill issue",
                    ),
                    button := ft.Button(
                        content=ft.Text("confirm"),
                        data=textanswer,
                        on_click=check_answer,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[
                    ft.Text(value=f'previous answer "{prev_right[1]}", correct answer: "{prev_right[0]}"', size=22, expand = True, color='pink')
                ],

            )
        )
        page.update()

    def run_next_question(timer_text):
        nonlocal i, cash_builder_list, timer_running
        if timer_running == False:
            phase_two()
        else:
            try:
                dictT = cash_builder_list[i]
            except IndexError as e:
                print(f"Error: {e}")
                phase_two()
                timer_running = False
                return
            cash_builder(
                dictT["question"],
                dictT["correct_answer"],
                dictT["incorrect_answers"],
                dictT["category"],
                dictT["difficulty"],
                timer_text
            )

    def phase_one():
        nonlocal cash_builder_list, i, secs, timer_running
        page.clean()
        page.add(
            ft.Column(
                controls=[
                    ft.Text(value="wait...", size=120, color="red")
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )
        page.update()

        timer_text = ft.Text(value="60 seconds remaining...", size=15, color="red")
        secs = 60
        timer_running = True

        async def s60_sec():
            nonlocal timer_running, secs, timer_text
            while secs > 0 and timer_running:
                await asyncio.sleep(1)
                secs -= 1
                timer_text.value = f"{secs} seconds remaining..."
                try:
                    timer_text.update()
                except Exception as e:
                    print(f"Error updating timer: {e}")

            timer_running = False
            print("Timer finished")
            phase_two()


        async def load_questions():
            nonlocal cash_builder_list, i
            cash_builder_list = get_questions(50, "", 'type=multiple')
            time.sleep(5)
            cash_builder_list += get_questions(30, "", 'type=multiple')
            i = 0

            if cash_builder_list:
                run_next_question(timer_text)

        page.run_task(load_questions)
        page.run_task(s60_sec)

    page.add(
        ft.Row(
            ft.Text(
                spans=[
                    ft.TextSpan(
                        text="The Chase",
                        style=ft.TextStyle(
                            size=150,
                            weight=ft.FontWeight.BOLD,
                            foreground=ft.Paint(
                                gradient=ft.PaintLinearGradient(
                                    begin=(0, 1200),
                                    end=(1100,20),
                                    colors=["blue", "white"],
                                )
                            )
                        )
                    )
                ],
            ),
            alignment = ft.MainAxisAlignment.CENTER,
        ),
        ft.Row(
            controls=[
                start_button := ft.Button(
                    content = ft.Text(value="START CHASE", size=100, color='blue'),
                    on_click = phase_one
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
    )


if __name__ == '__main__':
    ft.run(main)