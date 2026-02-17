import flet as ft
from flet import TextField
import requests
import html
import random
import time
import threading
import os
import asyncio
def main(page: ft.Page):
    page.add(
        ft.Row(
            controls=[ft.Text(value=f"You have $", size=18, color='green')],
            alignment=ft.MainAxisAlignment.END
        ),
        ft.Row(
            controls=[
                ft.Text(
                    value="12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890",
                    size=22,
                    text_align=ft.TextAlign.CENTER,
                    expand=True
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
ft.run(main)