#importing necessary libraries
import tkinter as tk
import json

with open("quiz.json", "r") as file:
    data = json.load(file)


class Quiz:
    def __init__(self, quiz_data):
        self.quiz_data = quiz_data
        self.score = 0
        self.current_question = 0
        self.total_questions = len(quiz_data)

    def get_current_question(self):
        return self.quiz_data[self.current_question]

    def check_answer(self, selected_answer):
        correct_answer = self.quiz_data[self.current_question]["answer"]
        if selected_answer == correct_answer:
            self.score += 1
        self.current_question += 1

    def final_score(self):
        return self.score

    def is_finished(self):
        return self.current_question >= self.total_questions


# Create Quiz instance
quiz = Quiz(data)

# Get first question
first_question = quiz.get_current_question()

# Create window
root = tk.Tk()
root.title("Programming Quiz")
root.geometry("500x300")
root = tk.Tk()
root.title("Programming Quiz")
root.geometry("500x400")
root.configure(bg="#f5f5f5")

# Variable to store selected option
selected_option = tk.StringVar()

#  Widgets 
progress_label = tk.Label(
    root,
    text="",
    font=("Arial", 10),
    bg="#f5f5f5",
    fg="#888888"
)
progress_label.pack(pady=(15, 0))

question_label = tk.Label(
    root,
    text="",
    font=("Arial", 14, "bold"),
    bg="#f5f5f5",
    fg="#222222",
    wraplength=450,
    justify="left"
)
question_label.pack(padx=30, pady=(10, 15), anchor="w")

options_frame = tk.Frame(root, bg="#f5f5f5")
options_frame.pack(padx=30, fill="x")

feedback_label = tk.Label(
    root,
    text="",
    font=("Arial", 11, "italic"),
    bg="#f5f5f5"
)
feedback_label.pack(pady=8)

next_button = tk.Button(
    root,
    text="Next →",
    font=("Arial", 12),
    bg="#1D9E75",
    fg="white",
    relief="flat",
    padx=20,
    pady=6,
    state="disabled",
    command=lambda: next_question()
)
next_button.pack()


# --- Step 5: Display functions ---

def display_question():
    """Retrieves the current question from quiz data and updates the GUI."""

    # Clear previous options
    for widget in options_frame.winfo_children():
        widget.destroy()

    # Reset state
    selected_option.set(None)
    feedback_label.config(text="")
    next_button.config(state="disabled")

    # Retrieve current question data
    q = quiz.get_current_question()

    # Update progress label
    progress_label.config(
        text=f"Question {quiz.current_question + 1} of {quiz.total_questions}  |  Score: {quiz.score}"
    )

    # Update question text
    question_label.config(text=q["question"])

    # Display each option as a radio button
    display_options(q["options"])


def display_options(options):
    """Retrieves the options list and renders each one as a radio button."""
    for option in options:
        radio = tk.Radiobutton(
            options_frame,
            text=option,
            variable=selected_option,
            value=option,
            font=("Arial", 12),
            bg="#f5f5f5",
            fg="#333333",
            activebackground="#f5f5f5",
            selectcolor="#d0f0e0",
            anchor="w",
            command=lambda: check_selected()   # fires when user clicks
        )
        radio.pack(fill="x", pady=3)


def check_selected():
    """Checks the selected answer and shows feedback."""
    selected = selected_option.get()
    if not selected or selected == "None":
        return

    quiz.check_answer(selected)

    # Show feedback
    correct_answer = data[quiz.current_question - 1]["answer"]
    if selected == correct_answer:
        feedback_label.config(text=" Correct!", fg="#1D9E75")
    else:
        feedback_label.config(text=f"Wrong. Answer: {correct_answer}", fg="#993C1D")

    # Disable all radio buttons after answering
    for widget in options_frame.winfo_children():
        widget.config(state="disabled")

    next_button.config(state="normal")


def next_question():
    """Moves to the next question or shows final score."""
    if quiz.is_finished():
        show_results()
    else:
        display_question()


def show_results():
    """Clears the window and displays the final score."""
    for widget in root.winfo_children():
        widget.destroy()

    pct = round((quiz.final_score() / quiz.total_questions) * 100)

    tk.Label(root, text="Quiz Complete!", font=("Arial", 18, "bold"),
             bg="#f5f5f5").pack(pady=30)
    tk.Label(root, text=f"{quiz.final_score()} / {quiz.total_questions}",
             font=("Arial", 36), bg="#f5f5f5", fg="#1D9E75").pack()
    tk.Label(root, text=f"{pct}%", font=("Arial", 16),
             bg="#f5f5f5", fg="#888888").pack(pady=5)

    if pct >= 80:
        msg = "Excellent work!"
    elif pct >= 50:
        msg = "Good effort, keep practicing!"
    else:
        msg = "Keep studying, you'll get there!"

    tk.Label(root, text=msg, font=("Arial", 12, "italic"),
             bg="#f5f5f5", fg="#555555").pack(pady=10)


# Step 4: Show the first question when app starts
display_question()

root.mainloop()
