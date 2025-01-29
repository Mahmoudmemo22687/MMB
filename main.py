import flet as ft
import random

def main(page: ft.Page):
    page.title = "لعبة X O مع روبوت"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 300
    page.window_height = 400

    board = [""] * 9
    human = "X"
    ai = "O"
    winner_text = ft.Text("", size=24, weight=ft.FontWeight.BOLD)
    
    def check_winner():
        """التحقق من الفائز أو التعادل"""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # صفوف
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # أعمدة
            [0, 4, 8], [2, 4, 6]  # قطرين
        ]
        for combo in winning_combinations:
            a, b, c = combo
            if board[a] == board[b] == board[c] and board[a] != "":
                return board[a]
        if "" not in board:
            return "تعادل"
        return None

    def minimax(new_board, player):
        """خوارزمية Minimax لاتخاذ أفضل قرار للروبوت"""
        available_spots = [i for i in range(9) if new_board[i] == ""]
        winner = check_winner()

        if winner == human:
            return -10
        elif winner == ai:
            return 10
        elif not available_spots:
            return 0

        moves = []
        for spot in available_spots:
            move = {}
            move["index"] = spot
            new_board[spot] = player

            if player == ai:
                result = minimax(new_board, human)
                move["score"] = result
            else:
                result = minimax(new_board, ai)
                move["score"] = result

            new_board[spot] = ""  
            moves.append(move)

        if player == ai:
            best_move = max(moves, key=lambda x: x["score"])
        else:
            best_move = min(moves, key=lambda x: x["score"])

        return best_move["index"] if isinstance(best_move["index"], int) else 0

    def ai_move():
        """حركة الذكاء الاصطناعي"""
        best_move = minimax(board, ai)
        board[best_move] = ai
        buttons[best_move].text = ai
        buttons[best_move].update()
        winner = check_winner()
        if winner:
            winner_text.value = f"🎉 الفائز: {winner}" if winner != "تعادل" else "😢 تعادل!"
            page.update()
            return

    def handle_click(index):
        """حدث النقر على الخلايا"""
        if board[index] == "" and winner_text.value == "":
            board[index] = human
            buttons[index].text = human
            buttons[index].update()
            
            winner = check_winner()
            if winner:
                winner_text.value = f"🎉 الفائز: {winner}" if winner != "تعادل" else "😢 تعادل!"
                page.update()
                return
            
            ai_move()

    def reset_game(e):
        """إعادة تشغيل اللعبة"""
        for i in range(9):
            board[i] = ""
            buttons[i].text = ""
            buttons[i].update()
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
