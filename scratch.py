import flet as ft
from flet_core.border_radius import horizontal


def main(page: ft.Page) -> None:
    l = 2
    print(page.window.width, page.window.height)
    page.title = 'The follow'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 1920
    page.window.height = 720
    page.window.resizable = False
    page.window.maximizable = False
    page.update()

    low = 9
    cash = 10
    high = 11

    chase_ladder = [
        ft.Container(height=90, width=600, bgcolor="white"),
        ft.Container(height=90, width=600, bgcolor="white"),
        ft.Container(height=90, width=600, bgcolor="white"),
        ft.Container(height=90, width=600, bgcolor="white"),
        ft.Container(height=90, width=600, bgcolor="white"),
        ft.Container(height=90, width=600, bgcolor="white"),
        ft.Container(height=90, width=600, bgcolor="white"),
    ] #and this (remember)
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
                        bgcolor="green",
                        expand=1,
                    )   #also this (remember)
    def the_chase():
        nonlocal l,right_side, low, cash, high, chase_ladder
        chase_ladder[1].bgcolor="red"           #ts very important (remember)
        chase_ladder[2].bgcolor="blue"
        right_side.update()



    page.add(
        ft.Row(
            controls=[
                ft.Container(
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
                                        content=ft.Text(value=f"Low offer: {low}", size=60),
                                        data=low,
                                        on_click=the_chase
                                    ),
                                    cash_offer := ft.Button(
                                        content=ft.Text(value=f"Cash offer: {cash}", size=60),
                                        data=cash,
                                        on_click=the_chase
                                    ),
                                    high_offer := ft.Button(
                                        content=ft.Text(value=f"High offer: {high}", size=60),
                                        data=high,
                                        on_click=the_chase
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
                ),

                right_side,   #dont forget ts (remember)
            ],
            expand=True,
        )
    )
    page.update()



ft.run(main)