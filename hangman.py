import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# -------------------- WORD CATEGORIES --------------------

CATEGORIES = {
    "Programming": ["python", "java", "coding", "debug"],
    "Education": ["student", "teacher", "school", "college"],
    "Technology": ["computer", "console", "project", "system"]
}

# -------------------- COLORS --------------------

BG_COLOR = "#fef3c7"
TITLE_COLOR = "#f5c542"
TEXT_COLOR = "black"
ACCENT_COLOR = "#4caf50"

# -------------------- GAME STATE --------------------

secret_word = ""
display_word = []
guessed_letters = []
wrong_attempts = 0
MAX_ATTEMPTS = 6
game_over = False

current_category = ""
score = 0

# -------------------- GAME FUNCTIONS --------------------

def start_new_game():
    global secret_word, display_word, guessed_letters, wrong_attempts, game_over

    words = CATEGORIES[current_category]
    secret_word = random.choice(words)

    display_word = ["_"] * len(secret_word)
    guessed_letters = []
    wrong_attempts = 0
    game_over = False

    update_display()
    entry.focus()

def update_display():
    word_label.config(text=" ".join(display_word))
    attempts_label.config(text=f"❤️ Remaining Attempts: {MAX_ATTEMPTS - wrong_attempts}")
    guessed_label.config(
        text="Guessed Letters: " + (", ".join(guessed_letters) if guessed_letters else "None")
    )
    score_label.config(text=f"Score: {score}")
    category_label.config(text=f"Category: {current_category}")

def process_guess(event=None):
    global wrong_attempts, game_over

    if game_over:
        return

    letter = entry.get().lower()
    entry.delete(0, tk.END)

    if len(letter) != 1 or not letter.isalpha():
        messagebox.showwarning("Invalid Input", "Enter a single alphabet letter")
        return

    if letter in guessed_letters:
        messagebox.showinfo("Info", "Letter already guessed")
        return

    guessed_letters.append(letter)

    if letter in secret_word:
        for i in range(len(secret_word)):
            if secret_word[i] == letter:
                display_word[i] = letter
    else:
        wrong_attempts += 1

    update_display()
    check_game_status()

def check_game_status():
    global game_over, score

    if "_" not in display_word:
        game_over = True
        score += 10
        update_display()
        messagebox.showinfo("🎉 Result", f"You WON!\nWord: {secret_word}")

    elif wrong_attempts >= MAX_ATTEMPTS:
        game_over = True
        score -= 5
        update_display()
        messagebox.showerror("💀 Result", f"You LOST!\nWord was: {secret_word}")

# -------------------- PAGE SWITCHING --------------------

def go_to_difficulty():
    welcome_frame.pack_forget()
    difficulty_frame.pack(fill="both", expand=True)

def start_game(level, category):
    global MAX_ATTEMPTS, current_category

    current_category = category

    if level == "easy":
        MAX_ATTEMPTS = 8
    elif level == "medium":
        MAX_ATTEMPTS = 6
    elif level == "hard":
        MAX_ATTEMPTS = 4

    difficulty_frame.pack_forget()
    game_frame.pack(fill="both", expand=True)
    start_new_game()

# -------------------- GUI SETUP --------------------

window = tk.Tk()
window.title("Hangman Game")
window.geometry("420x440")
window.resizable(False, False)

# ================== WELCOME PAGE ==================

welcome_frame = tk.Frame(window)
welcome_frame.pack(fill="both", expand=True)

bg_image = Image.open("images/welcome_bg.png")
bg_image = bg_image.resize((420, 440))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(welcome_frame, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(
    welcome_frame,
    text="🎯 Welcome to Hangman",
    font=("Segoe UI", 22, "bold"),
    fg="white",
    bg="#000000"
).pack(pady=40)

tk.Button(
    welcome_frame,
    text="Start Game",
    command=go_to_difficulty,
    bg="#2563eb",
    fg="white",
    font=("Segoe UI", 14, "bold"),
    width=15,
    relief="flat"
).pack(pady=30)

# ================== DIFFICULTY PAGE ==================

difficulty_frame = tk.Frame(window, bg=BG_COLOR)

tk.Label(
    difficulty_frame,
    text="Select Difficulty & Category",
    font=("Segoe UI", 16, "bold"),
    bg=BG_COLOR
).pack(pady=10)

for category in CATEGORIES:
    tk.Label(
        difficulty_frame,
        text=category,
        font=("Segoe UI", 13, "bold"),
        bg=BG_COLOR
    ).pack(pady=5)

    tk.Button(
        difficulty_frame,
        text="Easy",
        command=lambda c=category: start_game("easy", c),
        bg="#d1fae5",
        fg="black",
        width=10
    ).pack(pady=2)

    tk.Button(
        difficulty_frame,
        text="Medium",
        command=lambda c=category: start_game("medium", c),
        bg="#fde68a",
        fg="black",
        width=10
    ).pack(pady=2)

    tk.Button(
        difficulty_frame,
        text="Hard",
        command=lambda c=category: start_game("hard", c),
        bg="#fecaca",
        fg="black",
        width=10
    ).pack(pady=2)

# ================== GAME PAGE ==================

game_frame = tk.Frame(window, bg=BG_COLOR)

category_label = tk.Label(game_frame, font=("Segoe UI", 12, "bold"), bg=BG_COLOR)
category_label.pack(pady=3)

score_label = tk.Label(game_frame, font=("Segoe UI", 12, "bold"), bg=BG_COLOR)
score_label.pack(pady=3)

word_label = tk.Label(game_frame, font=("Courier", 20), bg=BG_COLOR)
word_label.pack(pady=10)

attempts_label = tk.Label(game_frame, font=("Segoe UI", 14), bg=BG_COLOR)
attempts_label.pack()

guessed_label = tk.Label(game_frame, font=("Segoe UI", 13), bg=BG_COLOR)
guessed_label.pack(pady=5)

entry = tk.Entry(game_frame, font=("Segoe UI", 20), width=5, justify="center")
entry.pack(pady=10)

window.bind("<Return>", process_guess)

tk.Button(
    game_frame,
    text="Guess",
    command=process_guess,
    bg=ACCENT_COLOR,
    fg="white",
    font=("Segoe UI", 12, "bold")
).pack(pady=5)

tk.Button(
    game_frame,
    text="Restart Game",
    command=start_new_game,
    bg="#2563eb",
    fg="white"
).pack(pady=8)

window.mainloop()
