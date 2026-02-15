import flet as ft

def main(page: ft.Page) -> None:
    print(page.window.width, page.window.height)
    page.title = 'The follow'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 1920
    page.window.height = 720
    page.window.resizable = False
    page.window.maximizable = False
    page.update()
    def the_chase():
        pass
    low = 9
    cash = 10
    high = 11
    page.add(
        ft.Row(
            controls=[
                # --- LEFT SIDE (Width = 2) ---
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
                    expand=2,  # Takes up 1 "share" of the space
                ),

                # --- RIGHT SIDE (Width = 1) ---
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("I am on the RIGHT!"),
                            ft.TextField(label="Type here")
                        ]
                    ),
                    bgcolor="green",
                    expand=1,  # Takes up 1 "share" of the space (so 50/50 total)
                ),
            ],
            expand=True,  # Make the row fill the whole vertical height
        )
    )



ft.run(main)