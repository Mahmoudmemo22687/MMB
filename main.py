import flet as ft

def main(page: ft.Page):
    page.title = "لعبة X O"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 300
    page.window_height = 715

    board = [""] * 9
    current_player = "X"
    winner_text = ft.Text("", size=24, weight=ft.FontWeight.BOLD)
    
    def check_winner():
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        for combo in winning_combinations:
            a, b, c = combo
            if board[a] == board[b] == board[c] and board[a] != "":
                return board[a]
        if "" not in board:
            return "تعادل"
        return None

    def handle_click(index):
        nonlocal current_player
        if board[index] == "" and winner_text.value == "":
            board[index] = current_player
            buttons[index].text = current_player
            buttons[index].update()
            
            winner = check_winner()
            if winner:
                winner_text.value = "🎉 الفائز: " + winner if winner != "تعادل" else "😢 تعادل!"
                page.update()
                return
            
            current_player = "O" if current_player == "X" else "X"
            page.update()

    def reset_game(e):
        nonlocal current_player
        for i in range(9):
            board[i] = ""
            buttons[i].text = ""
            buttons[i].update()
        current_player = "X"
        winner_text.value = ""
        page.update()

    buttons = [ft.ElevatedButton(text="", on_click=lambda e, i=i: handle_click(i), width=80, height=80) for i in range(9)]
    
    grid = ft.Column([
        ft.Row(buttons[:3], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(buttons[3:6], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(buttons[6:], alignment=ft.MainAxisAlignment.CENTER),
    ])
    
    reset_button = ft.ElevatedButton(text="إعادة اللعب", on_click=reset_game)
    
    page.add(winner_text, grid, reset_button)

ft.app(target=main)
