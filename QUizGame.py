import flet as ft
from flet import TextField
import requests
import html
import random
import time
import threading
import os
import asyncio
import json

def main(page: ft.Page) -> None:
    # Initialize game state and tracking variables
    cash = 0
    high = 0
    low = 0
    i = 0
    fase_too = True
    fase_tchaysar = True
    lost = False
    secs = 60
    textanswer = ""
    prev_right = ["", ""]
    cash_builder_list = []
    rand_list = []
    timer_running = True
    
    # Configure main Flet window properties
    page.title = 'The Chase'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.Colors.TRANSPARENT
    page.window.width = 1280
    page.window.height = 720
    page.window.resizable = False
    page.window.maximizable = False
    page.update()
    
    cash_builder_qs = 80
    score = 0
    
    # Function to save the player's score and cash to a local JSON file
    def save_highscore(cash, point):
        try:
            with open("highscores.json", "r", encoding="utf-8") as file:
                highscore = json.load(file)
        
        except FileNotFoundError:
            # Create a new list if the file doesn't exist
            highscore = []
            return "chicken"
        
        except Exception as e:
            return (f"Smth got fricked! Error: {e}")
        
        # Append the new score and write back to the JSON file
        highscore.append({"score": point, "cash": cash})
        print(highscore)
        
        try:
            with open("highscores.json", "w", encoding="utf-8") as file:
                json.dump(highscore, file, indent=4)
        except Exception as e:
            return (f"Smth got fricked! Error: {e}")
        
    # Phase 3: The Final Chase
    def last_phase():
        nonlocal timer_running, secs, cash_builder_qs
        cash_builder_qs = 80

        # Calculates the Chaser's score and determines the final win/loss result
        def phase_chaser():
            nonlocal score, cash, fase_tchaysar
            fase_tchaysar = False
            page.clean()
            page.update()
            
            # Generate a random score for the Chaser using Gaussian distribution
            smth = random.gauss(19, 5)
            smth = max(3, min(25, smth))
            smth = int(smth)
            
            # Compare player score with Chaser score
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
                save_highscore(cash, score)
            else:
                page.clean()
                page.add(
                    ft.Column(
                        controls=[
                            ft.Text(value=f"YOU Lose ${cash} \n you got {score} right, chaser got {smth} right", size=80, color="red")
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                )

        # Retrieves the next question for the Final Chase
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
                # Render the final phase UI for the current question
                finally_therock(
                    dictT["question"],
                    dictT["correct_answer"],
                    dictT["incorrect_answers"],
                    dictT["category"],
                    dictT["difficulty"],
                    timer_text
                )

        # Builds the UI for asking questions in the Final Chase (requires text input)
        def finally_therock(question_text, right, wrong_list, category, difficulty, timer_text):
            nonlocal rand_list, timer_running, secs, score, prev_right, cash_builder_qs
            right = right
            if timer_running == False:
                secs = 120

            # Shuffle answers and format negative questions
            questions = wrong_list
            questions.append(right)
            rand_list = random.sample(questions, len(questions))
            if " not " in question_text.lower():
                question_text += f"\n Options: {rand_list[0]}, {rand_list[1]}, {rand_list[2]}, {rand_list[3]}."

            page.clean()

            # Render question, timer, input field, and previous answer feedback
            page.add(
                ft.Row(
                    controls=[ft.Text(value=f"You have ${cash}", size=18, color='green')],
                    alignment=ft.MainAxisAlignment.END
                ),
                ft.Row(
                    controls=[ft.Text(value=question_text, size=22, expand=True, text_align=ft.TextAlign.CENTER)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[ft.Text(value=f"Category: {category}", size=22, expand=True, text_align=ft.TextAlign.CENTER)],
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
                        ft.Text(value=f'previous answer "{prev_right[1]}", correct answer: "{prev_right[0]}"', size=22, expand=True, color='pink', )
                    ]
                )
            )
            page.update()
            
        secs = 120
        timer_text = ft.Text(value="120 seconds remaining...", size=15, color="red")
        timer_running = True
        
        # Validates user input against the correct answer during the Final Chase
        def check_answer(e):
            nonlocal score, i, cash_builder_qs, prev_right, textanswer
            cash_builder_qs -= 1
            rights = e.control.data

            prev_right = [rights, textanswer]
            print(prev_right)

            if textanswer.lower().strip() == rights.lower().strip():
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
                
                # Check if there are more questions or if time is up
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
                    phase_chaser()
                    return
                page.update()

            response = ""

        # Asynchronous function to run the 120-second countdown timer
        async def s120_sec():
            nonlocal timer_running, secs, timer_text, fase_tchaysar
            await asyncio.sleep(4)
            while secs > 0 and timer_running:
                await asyncio.sleep(1)
                secs -= 1
                timer_text.value = f"{secs} seconds remaining..."
                try:
                    timer_text.update()
                except Exception as e:
                    print(f"Error updating timer{random.randint(1,100)}: {e}")
            timer_running = False
            print("120-second timer finished")
            if fase_tchaysar:
                phase_chaser()

        # Asynchronous function to load "hard" difficulty questions for the Final Chase
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
            # Fetch a pool of hard questions
            cash_builder_list = get_questions(50, 'hard', 'type=multiple')
            await asyncio.sleep(5)
            cash_builder_list += get_questions(30, 'hard', 'type=multiple')
            i = 0
            if cash_builder_list:
                print(f"{len(cash_builder_list)} questions loaded")
                run_next_question2(timer_text)

        # Run both the loading mechanism and timer as Flet background tasks
        page.run_task(load_questions)
        page.run_task(s120_sec)

    # Updates the global textanswer variable as the user types
    def handle_field_change(e):
        nonlocal textanswer
        textanswer = e.control.value

    # Helper function to fetch and format questions from the Open Trivia Database API
    def get_questions(amount, difficulty, typE):
        url = f"https://opentdb.com/api.php?amount={amount}&{difficulty}&{typE}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data['response_code'] == 0:
                results = data['results']
                # Unescape HTML entities (e.g., &quot; to ")
                for q in results:
                    q['question'] = html.unescape(q['question'])
                    q['correct_answer'] = html.unescape(q['correct_answer'])
                    q['incorrect_answers'] = [html.unescape(w) for w in q['incorrect_answers']]
                    q['category'] = html.unescape(q['category'])
                return results
            
            # Fallback styling/responses if API response code is non-zero
            page.decoration = ft.BoxDecoration(
                image=ft.DecorationImage(
                    src="background_image.jpeg",
                    fit=ft.BoxFit.COVER,
                ),
            )
            return [{'question': 'Buddy theres no wifi', 'correct_answer': 'brr', 'incorrect_answers': ['brrr','br','brrrr'], 'category': 'buddy no wifi'}]

        except Exception as e:
            # Error handling for network issues
            print(f"Error: {e}")
            page.decoration = ft.BoxDecoration(
                image=ft.DecorationImage(
                    src="background_image.jpeg",
                    fit=ft.BoxFit.COVER,
                ),
            )
            return [{'question': 'Buddy API is down sorry', 'correct_answer': 'brr', 'incorrect_answers': ['brrr','br','brrrr'], 'category': 'buddy no API','difficulty': 'easy'}]

    # Phase 2: Head-to-Head against the Chaser
    def phase_two():
        nonlocal cash, low, high, page, i, fase_too
        i = 0
        fase_too = False
        h2h_list = []
        page.window.width = 1920
        page.window.height = 720
        l = 0 # Player position on the board
        p = 0 # Chaser position on the board
        page.clean()
        page.update()
        
        # Visual representation of the Chase board
        chase_ladder = [
            ft.Container(height=90, width=600, bgcolor="0xff00ff99"),
            ft.Container(height=90, width=600, bgcolor="0xff00ff99"),
            ft.Container(height=90, width=600, bgcolor="0xff00ff99"),
            ft.Container(height=90, width=600, bgcolor="0xff00ff99"),
            ft.Container(height=90, width=600, bgcolor="0xff00ff99"),
            ft.Container(height=90, width=600, bgcolor="0xff00ff99"),
            ft.Container(height=90, width=600, bgcolor="0xffffd700"), # Bank/Safety
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
        
        # Initializes a multiple-choice question for the Head-to-Head round
        def start_question(question_text, right, wrong_list, category, difficulty):
            nonlocal p, i, l, right_side, left_side, chase_ladder, h2h_list, lost
            questions = wrong_list
            questions.append(right)
            rand_list = random.sample(questions, len(questions))
            
            # Evaluates the player's button selection and simulates the Chaser's turn
            def check_answer(answer):
                nonlocal right, l, p, i, right_side, left_side, chase_ladder, lost
                response = answer.control.data
                
                # Player logic
                if response == right:
                    l += 1 # Move player down the board
                    try:
                        chase_ladder[l].bgcolor = "0xff3380de"
                    except Exception as e:
                        print(f"Error: {e}")
                    
                    # Player reaches home
                    if l >= 6:
                        last_phase()
                        return
                    else:
                        i += 1
                        start_question(h2h_list[i]["question"], h2h_list[i]["correct_answer"],
                                       h2h_list[i]["incorrect_answers"], h2h_list[i]["category"],
                                       h2h_list[i]["difficulty"])

                # Catch condition if Chaser catches player
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
                    
                # Chaser logic: 84% chance of getting it right
                if random.random() <= 0.84:
                    p += 1 # Move Chaser down the board
                    chase_ladder[p].bgcolor = "red"
                    
                    if l == p: # Chaser catches player
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
                    # Chaser gets it wrong, board state remains roughly the same, move to next Q
                    if p <= l or p <= 7:
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

            # UI configuration for displaying the Head-to-Head question and 4 choices
            left_side.content = ft.Column(
                controls=[
                    ft.Row(
                        controls=[ft.Text(value=f"You have ${cash}", size=18, color='green')],
                        alignment=ft.MainAxisAlignment.END
                    ),
                    ft.Row(
                        controls=[ft.Text(value=question_text, size=22, expand=True, text_align=ft.TextAlign.CENTER)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        controls=[ft.Text(value=f"Category: {category}", size=22, expand=True, text_align=ft.TextAlign.CENTER)],
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
            i += 1

        # Sets the initial board positioning depending on user's selected offer
        def head_to_head(diffs):
            nonlocal l, right_side, low, cash, high, chase_ladder, p, i, h2h_list
            chase_ladder[0].bgcolor = "cyan"
            diff = diffs.control.data
            
            # High offer setup
            if diff == "hard":
                chase_ladder[1].bgcolor = "0xff3380de"
                cash = high
                l = 1
                p = -1
            # Low offer setup
            elif diff == "easy":
                chase_ladder[1].bgcolor = "cyan"
                chase_ladder[2].bgcolor = "cyan"
                chase_ladder[3].bgcolor = "0xff3380de"
                cash = low
                l = 3
                p = -1
            # Medium/Standard offer setup
            elif diff == "medium":
                chase_ladder[1].bgcolor = "cyan"
                chase_ladder[2].bgcolor = "0xff3380de"
                l = 2
                p = -1
                
            right_side.update()
            # Retrieve questions specific to the chosen difficulty
            h2h_list = get_questions(30, f"difficulty={diff}", "type=multiple")
            start_question(h2h_list[i]["question"], h2h_list[i]["correct_answer"], h2h_list[i]["incorrect_answers"], h2h_list[i]["category"], h2h_list[i]["difficulty"])

        # UI for picking the Low, Cash (Medium), or High offer before Phase 2 begins
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
                                value="^This gives you a 4 questions advantage.                           This gives you 3.                                                  This gives you 2",
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

    # Phase 1: The Cash Builder Round
    def cash_builder(question_text, right, wrong_list, category, difficulty, timer_text):
        nonlocal rand_list, timer_running, secs, cash, low, high, prev_right

        if timer_running == False:
            secs = 60

        # Debug/Reset function
        def rys(e):
            nonlocal cash, i
            cash = 0
            i = 0
            phase_one()

        # Validates player's text-input answers during Phase 1
        def check_answer(e=None):
            nonlocal cash, i, cash_builder_qs, low, high, prev_right, textanswer
            prev_right = [right, textanswer]

            if textanswer.lower().strip() == right.lower().strip():
                print("\n\n CORRECT \n\n")
                page.clean()
                page.add(
                    ft.Row(
                        controls=[ft.Text(value="CORRECT", size=20)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                )
                page.clean()
                
                # Assign cash based on standard difficulties
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
                i += 1
                cash_builder_qs -= 1
                print(cash_builder_qs)
                if cash_builder_qs > 0:
                    run_next_question(timer_text)
                else:
                    phase_two()
                    return
                page.update()
                
            # Dynamic calculation of High and Low offers for Phase 2 based on cash accumulated
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
        if " not " in question_text.lower():
            question_text += f"\n Options: {rand_list[0]}, {rand_list[1]}, {rand_list[2]}, {rand_list[3]}."

        # UI for Cash Builder questions
        page.add(
            ft.Row(
                controls=[ft.Text(value=f"You have ${cash}", size=18, color='green')],
                alignment=ft.MainAxisAlignment.END
            ),
            ft.Row(
                controls=[ft.Text(value=question_text, size=22, expand=True, text_align=ft.TextAlign.CENTER)],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[ft.Text(value=f"Category: {category}", size=22, expand=True, text_align=ft.TextAlign.CENTER)],
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
                    ft.Text(value=f'previous answer "{prev_right[1]}", correct answer: "{prev_right[0]}"', size=22, expand=True, color='pink')
                ],
            )
        )
        page.update()

    # Retrieves and parses the next Phase 1 question
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

    # Starts Phase 1: Sets up the initial timer and triggers question loading
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

        # Async countdown task for Phase 1
        async def s60_sec():
            nonlocal timer_running, secs, timer_text, fase_too
            while secs > 0 and timer_running:
                await asyncio.sleep(1)
                secs -= 1
                timer_text.value = f"{secs} seconds remaining..."
                try:
                    timer_text.update()
                except Exception as e:
                    print(f"Error updating timer{int(random.random()*100)}: {e}")

            timer_running = False
            print("Timer finished")
            if fase_too:
                phase_two()

        # Async task to pre-load questions for the Cash Builder round
        async def load_questions():
            nonlocal cash_builder_list, i
            cash_builder_list = get_questions(50, "", 'type=multiple')
            time.sleep(5)
            cash_builder_list += get_questions(30, "", 'type=multiple')
            i = 0

            if cash_builder_list:
                run_next_question(timer_text)

        # Start phase one routines
        page.run_task(load_questions)
        page.run_task(s60_sec)

    # Initial Welcome Screen UI
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
                                    end=(1100, 20),
                                    colors=["blue", "white"],
                                )
                            )
                        )
                    )
                ],
            ),
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Row(
            controls=[
                start_button := ft.Button(
                    content=ft.Text(value="START CHASE", size=100, color='blue'),
                    on_click=phase_one
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
    )

if __name__ == '__main__':
    # Execute the application
    ft.run(main)