import ast

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

    history = ft.Text(
        size=30, color=ft.Colors.GREY_700, max_lines=1, overflow=ft.TextOverflow.FADE
    )
    select_value = ft.Text("0", size=40, max_lines=1, overflow=ft.TextOverflow.FADE)

    expression = ""
    current_value = "0"

    def format_value(value):
        if value is None:
            return "0"
        if isinstance(value, float):
            value = round(value, 12)
            if value.is_integer():
                return str(int(value))
            return format(value, ".12g")
        return str(value)

    def update_display():
        value_to_show = (
            current_value if len(current_value) <= 12 else current_value[:12]
        )
        select_value.value = value_to_show
        history.value = expression[:18] if len(expression) > 18 else expression
        page.update()

    def safe_evaluate(expr):
        expr = expr.replace(" ", "")
        tree = ast.parse(expr, mode="eval")

        def eval_node(node):
            if isinstance(node, ast.Constant):
                return node.value
            if isinstance(node, ast.UnaryOp):
                value = eval_node(node.operand)
                if isinstance(node.op, ast.USub):
                    return -value
                if isinstance(node.op, ast.UAdd):
                    return +value
            if isinstance(node, ast.BinOp):
                left = eval_node(node.left)
                right = eval_node(node.right)
                if isinstance(node.op, ast.Add):
                    return left + right
                if isinstance(node.op, ast.Sub):
                    return left - right
                if isinstance(node.op, ast.Mult):
                    return left * right
                if isinstance(node.op, ast.Div):
                    return left / right
                if isinstance(node.op, ast.Pow):
                    return left**right
                if isinstance(node.op, ast.Mod):
                    return left % right
            raise ValueError("Unsupported expression")

        return eval_node(tree.body)

    def clear_all():
        nonlocal expression, current_value
        expression = ""
        current_value = "0"
        history.value = ""
        update_display()

    def append_digit(value):
        nonlocal current_value

        if value == ".":
            if "." in current_value:
                return
            if current_value == "-":
                current_value += "0."
            elif current_value == "0":
                current_value = "0."
            else:
                current_value += "."
            update_display()
            return

        if current_value == "0":
            current_value = value
        else:
            current_value += value
        update_display()

    def apply_operator(op):
        nonlocal expression, current_value

        if op == "-" and current_value == "0" and not expression:
            current_value = "-"
            update_display()
            return

        if expression and expression[-1] in "+-*/":
            expression = expression[:-1] + op
            update_display()
            return

        if current_value in ("", "0") and op not in ("-",):
            return

        expression += current_value + op
        current_value = "0"
        update_display()

    def toggle_sign():
        nonlocal current_value
        if current_value == "0":
            return
        current_value = format_value(-float(current_value))
        update_display()

    def backspace():
        nonlocal current_value
        if current_value in ("0", ""):
            return
        current_value = current_value[:-1]
        if not current_value:
            current_value = "0"
        update_display()

    def calculate_percentage():
        nonlocal current_value
        try:
            current_value = format_value(float(current_value) / 100)
        except ValueError:
            current_value = "0"
        update_display()

    def calculate_result():
        nonlocal expression, current_value

        if not expression:
            return

        value = expression + current_value
        if value.endswith(("+", "-", "*", "/")):
            value = value[:-1]

        try:
            result = safe_evaluate(value)
            history.value = f"{value[:18]} =" if len(value) > 18 else f"{value} ="
            current_value = format_value(result)
            expression = ""
            select_value.value = current_value[:12]
            page.update()
        except (SyntaxError, ZeroDivisionError, ValueError):
            history.value = "Error"
            current_value = "0"
            expression = ""
            update_display()

    def get_value(e):
        value = e.control.data

        if value.isdigit():
            append_digit(value)
        elif value in "+-*/":
            apply_operator(value)
        elif value == ".":
            append_digit(value)
        elif value == "C":
            clear_all()
        elif value == "Backspace":
            backspace()
        elif value == "=":
            calculate_result()
        elif value == "+/-":
            toggle_sign()
        elif value == "%":
            calculate_percentage()

    def handle_key(key, code=None):
        key = str(key or "")
        code = str(code or "")

        variants = set()
        for value in (key, code):
            if not value:
                continue
            cleaned = value.strip()
            variants.add(cleaned)
            variants.add(cleaned.lower())
            variants.add(cleaned.upper())
            variants.add(cleaned.replace(" ", ""))
            variants.add(cleaned.replace("_", ""))
            variants.add(cleaned.replace("-", ""))
            variants.add(cleaned.replace(" ", "").lower())
            variants.add(cleaned.replace("_", "").lower())
            variants.add(cleaned.replace("-", "").lower())
            variants.add(cleaned.replace(" ", "").upper())
            if cleaned.startswith("Numpad"):
                variants.add("numpad" + cleaned[6:])
            if cleaned.startswith("KP_"):
                variants.add(cleaned[3:])
            if cleaned.startswith("KP") and len(cleaned) > 2:
                variants.add(cleaned[2:])

        numpad_map = {
            "0": "0",
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8",
            "9": "9",
            "numpad0": "0",
            "numpad1": "1",
            "numpad2": "2",
            "numpad3": "3",
            "numpad4": "4",
            "numpad5": "5",
            "numpad6": "6",
            "numpad7": "7",
            "numpad8": "8",
            "numpad9": "9",
            "kp0": "0",
            "kp1": "1",
            "kp2": "2",
            "kp3": "3",
            "kp4": "4",
            "kp5": "5",
            "kp6": "6",
            "kp7": "7",
            "kp8": "8",
            "kp9": "9",
            "decimal": ".",
            "numpaddecimal": ".",
            "kpdecimal": ".",
            "period": ".",
            "dot": ".",
            "numpadadd": "+",
            "add": "+",
            "kpadd": "+",
            "numpadsubtract": "-",
            "subtract": "-",
            "minus": "-",
            "kpsubtract": "-",
            "numpadmultiply": "*",
            "multiply": "*",
            "asterisk": "*",
            "kpmultiply": "*",
            "numpaddivide": "/",
            "divide": "/",
            "slash": "/",
            "kpdivide": "/",
            "numpadenter": "=",
            "enter": "=",
            "equals": "=",
            "equal": "=",
            "kpenter": "=",
            "backspace": "BACKSPACE",
            "delete": "DELETE",
            "escape": "ESCAPE",
            "c": "CLEAR",
            "percent": "PERCENT",
            "mod": "PERCENT",
        }

        for token in variants:
            mapped = numpad_map.get(token.lower())
            if mapped is not None:
                if mapped in ("BACKSPACE", "DELETE", "ESCAPE", "CLEAR", "PERCENT"):
                    if mapped == "BACKSPACE":
                        backspace()
                    elif mapped == "DELETE":
                        backspace()
                    elif mapped == "ESCAPE":
                        clear_all()
                    elif mapped == "CLEAR":
                        clear_all()
                    elif mapped == "PERCENT":
                        calculate_percentage()
                    return
                key = mapped
                break

        if key in "0123456789":
            append_digit(key)
        elif key in "+-*/":
            apply_operator(key)
        elif key == ".":
            append_digit(key)
        elif key == "=":
            calculate_result()

    def on_keyboard(e):
        handle_key(e.key, getattr(e, "code", None))

    output_screen = ft.Container(
        ft.Column(
            controls=[
                ft.Row(
                    [history],
                    alignment=ft.MainAxisAlignment.END,
                    width=360,
                ),
                ft.Row(
                    [select_value],
                    alignment=ft.MainAxisAlignment.END,
                    width=360,
                ),
            ],
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.END,
        ),
        border=ft.Border.all(width=1, color=ft.Colors.BLACK_26),
        padding=20,
        width=390,
        height=150,
    )

    point_btn = ft.Button(
        content=ft.Text(".", size=18),
        data=".",
        width=90,
        height=45,
        on_click=get_value,
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
                            on_click=get_value,
                        ),
                        ft.Button(
                            content=ft.Text("C", size=18),
                            data="C",
                            width=90,
                            height=45,
                            on_click=get_value,
                        ),
                        ft.Button(
                            content=ft.Icon(ft.Icons.BACKSPACE, size=15),
                            data="Backspace",
                            width=90,
                            height=45,
                            on_click=get_value,
                        ),
                        ft.Button(
                            content=ft.Text("/", size=18),
                            data="/",
                            width=90,
                            height=45,
                            on_click=get_value,
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
                            on_click=get_value,
                        ),
                        ft.Button(
                            content=ft.Text("8", size=18),
                            data="8",
                            width=90,
                            height=45,
                            on_click=get_value,
                        ),
                        ft.Button(
                            content=ft.Text("9", size=18),
                            data="9",
                            width=90,
                            height=45,
                            on_click=get_value,
                        ),
                        ft.Button(
                            content=ft.Icon(ft.Icons.CLOSE),
                            data="*",
                            width=90,
                            height=45,
                            on_click=get_value,
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
                            on_click=get_value,
                        ),
                        ft.Button(
                            content=ft.Text("5", size=18),
                            data="5",
                            width=90,
                            height=45,
                            on_click=get_value,
                        ),
                        ft.Button(
                            content=ft.Text("6", size=18),
                            data="6",
                            width=90,
                            height=45,
                            on_click=get_value,
                        ),
                        ft.Button(
                            content=ft.Icon(ft.Icons.REMOVE),
                            data="-",
                            width=90,
                            height=45,
                            on_click=get_value,
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
                            on_click=get_value,
                        ),
                        ft.Button(
                            content=ft.Text("2", size=18),
                            data="2",
                            width=90,
                            height=45,
                            on_click=get_value,
                        ),
                        ft.Button(
                            content=ft.Text("3", size=18),
                            data="3",
                            width=90,
                            height=45,
                            on_click=get_value,
                        ),
                        ft.Button(
                            content=ft.Icon(ft.Icons.ADD),
                            data="+",
                            width=90,
                            height=45,
                            on_click=get_value,
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
                            on_click=get_value,
                        ),
                        ft.Button(
                            content=ft.Text("0", size=18),
                            data="0",
                            width=90,
                            height=45,
                            on_click=get_value,
                        ),
                        point_btn,
                        ft.Button(
                            content=ft.Icon(ft.Icons.DRAG_HANDLE),
                            data="=",
                            width=90,
                            height=45,
                            bgcolor=ft.Colors.ORANGE,
                            on_click=get_value,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ]
        )
    )

    page.on_keyboard_event = on_keyboard
    page.add(output_screen, buttons)


ft.run(main)
