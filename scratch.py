import flet as ft
from flet import TextField
from flet_core.control_event import ControlEvent

def main(page: ft.Page) -> None:
    cash = 0
    cash_talk = "abcdefghijklmnopqrstuvwxyz"
    page.title = 'The follow'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    qtextfield = "\n \n fancyquestionwowoow"
    page.add(
        ft.Row(
            controls=[ft.Text(value=cash_talk, size = 20)],
            alignment = ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            controls=[ft.Text(value=qtextfield, size = 20)],
            alignment = ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            button := ft.Button(
                content="buttoj",
                data=0,
                on_click=1 + 1,
            ),
            message := ft.Text()
        )
    )

if __name__ == '__main__':
    ft.run(main)
