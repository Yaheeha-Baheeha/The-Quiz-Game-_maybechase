import flet as ft


def main(page: ft.Page):
    textanswer = ""
    page.theme_mode = ft.ThemeMode.LIGHT
    def check_answer():
        if "yay" == textanswer:
            print("yippe")
        else:
            print("noooo")
    
    def handle_field_change(e: ft.Event[ft.TextField]):
        nonlocal textanswer
        textanswer = e.control.value

    page.add(
        ft.Row( controls = [
            ft.TextField(
                on_change=handle_field_change,
                label="Response",
                hint_text="skill issue",
            ),
            button := ft.Button(
                content=ft.Text("confirm"),
                on_click=check_answer,
                )
        ])
    )
    

ft.run(main)