def build_button_table(buttons, cols):
    button_table = [
        buttons[i : i + cols] for i in range(0, len(buttons), cols)
    ]
    return button_table
