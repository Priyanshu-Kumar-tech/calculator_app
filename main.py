import flet as ft


def main(page: ft.Page):

    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.title = "Calculator"
    page.window.width = 425
    page.window.height = 500
    page.window.resizable = False
    page.window.maximizable = False

    history = ft.Text(size=30, color=ft.Colors.GREY_700)
    select_value = ft.Text(0, size=40)

    output_screen = ft.Container(
        # content=ft.Text(value="0", size=40),
        ft.Column(
            controls=[
                ft.Row(
                    history,
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Row(
                    select_value,
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            alignment=ft.MainAxisAlignment.END,  # bottom
            horizontal_alignment=ft.CrossAxisAlignment.END,
        ),
        # alignment=ft.alignment.Alignment(1, 1),
        # alignment=ft.Alignment.BOTTOM_RIGHT,
        border=ft.Border.all(width=1, color=ft.Colors.BLACK_26),
        padding=20,
        width=390,
        height=150,
    )

    buttons = ft.Container(
        ft.Column(
            controls=[
                ft.Row(
                    [
                        ft.Button(
                            content=ft.Icon(ft.Icons.PERCENT),
                            data="%",
                            width=90,
                            height=45,
                            # on_click=calculation,
                        ),
                        ft.Button(
                            content=ft.Text("C", size=18),
                            data="C",
                            width=90,
                            height=45,
                            # on_click=calculation,
                        ),
                        ft.Button(
                            content=ft.Icon(ft.Icons.BACKSPACE, size=15),
                            data="Backspace",
                            width=90,
                            height=45,
                            # on_click=calculation,
                        ),
                        ft.Button(
                            content=ft.Text(
                                "/",
                                size=18,
                            ),
                            data="/",
                            width=90,
                            height=45,
                            # on_click=operation,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Button(
                            content=ft.Text("7", size=18),
                            data="7",
                            width=90,
                            height=45,
                            # on_click=calculation,
                        ),
                        ft.Button(
                            content=ft.Text("8", size=18),
                            data="8",
                            width=90,
                            height=45,
                            # on_click=calculation,
                        ),
                        ft.Button(
                            content=ft.Text("9", size=18),
                            data="9",
                            width=90,
                            height=45,
                            # on_click=calculation,
                        ),
                        ft.Button(
                            content=ft.Icon(ft.Icons.CLOSE),
                            data="*",
                            width=90,
                            height=45,
                            # on_click=operation,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Button(
                            content=ft.Text("4", size=18),
                            data="4",
                            width=90,
                            height=45,
                            # on_click=calculation,
                        ),
                        ft.Button(
                            content=ft.Text("5", size=18),
                            data="5",
                            width=90,
                            height=45,
                            # on_click=calculation,
                        ),
                        ft.Button(
                            content=ft.Text("6", size=18),
                            data="6",
                            width=90,
                            height=45,
                            # on_click=calculation,
                        ),
                        ft.Button(
                            content=ft.Icon(ft.Icons.REMOVE),
                            data="-",
                            width=90,
                            height=45,
                            # on_click=operation,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Button(
                            content=ft.Text("1", size=18),
                            data="1",
                            width=90,
                            height=45,
                            # on_click=calculation,
                        ),
                        ft.Button(
                            content=ft.Text("2", size=18),
                            data="2",
                            width=90,
                            height=45,
                            # on_click=calculation,
                        ),
                        ft.Button(
                            content=ft.Text("3", size=18),
                            data="3",
                            width=90,
                            height=45,
                            # on_click=calculation,
                        ),
                        ft.Button(
                            content=ft.Icon(ft.Icons.ADD),
                            data="+",
                            width=90,
                            height=45,
                            # on_click=operation,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Button(
                            content=ft.Text("+/-", size=18),
                            data="+/-",
                            width=90,
                            height=45,
                            # on_click=calculation,
                        ),
                        ft.Button(
                            content=ft.Text("0", size=18),
                            data="0",
                            width=90,
                            height=45,
                            # on_click=calculation,
                        ),
                        ft.Button(
                            content=ft.Text(".", size=18),
                            data=".",
                            width=90,
                            height=45,
                            # on_click=calculation,
                        ),
                        ft.Button(
                            content=ft.Icon(ft.Icons.DRAG_HANDLE),
                            data="=",
                            width=90,
                            height=45,
                            bgcolor=ft.Colors.ORANGE,
                            # on_click=calculation,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ]
        )
    )

    page.add(output_screen, buttons)


ft.run(main)
