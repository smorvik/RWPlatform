import pyodbc
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk


def get_db_connection():
    conn = pyodbc.connect("Driver={SQL Server};"
                          "Server=DESKTOP-6M85KI2\\SQLEXPRESS;"
                          "Database=firstDB;"
                          "Trusted_Connection=yes;")
    return conn


conn = get_db_connection()
cursor = conn.cursor()

root = tk.Tk()
root.title("Платформа для оценки сотрудников")
root.geometry("760x100")
root.configure(bg="#D3DEFD")


def create_questionnaire():
    title = simpledialog.askstring("Создать анкету", "Введите название анкеты:")
    description = simpledialog.askstring("Создать анкету", "Введите описание анкеты:")
    if title and description:
        cursor.execute("INSERT INTO Questionnaires (title, description) VALUES (?, ?)", title, description)
        conn.commit()
        messagebox.showinfo("Успех", "Анкета успешно создана.")


def add_question():
    questionnaire_id = simpledialog.askinteger("Добавить вопрос", "Введите ID анкеты:")
    question_text = simpledialog.askstring("Добавить вопрос", "Введите текст вопроса:")
    if questionnaire_id and question_text:
        cursor.execute("INSERT INTO Questions (questionnaire_id, text) VALUES (?, ?)", questionnaire_id, question_text)
        conn.commit()
        messagebox.showinfo("Успех", "Вопрос успешно добавлен.")


def add_answer():
    question_window = tk.Toplevel(root)
    question_window.title("Выберите вопрос для добавления ответа")
    question_window.geometry("600x300")
    question_window.configure(bg="#ffffff")

    cursor.execute("SELECT * FROM Questions")
    questions = cursor.fetchall()

    question_label = tk.Label(question_window, text="Выберите вопрос:", font=("Arial", 12), bg="#ffffff")
    question_label.pack(pady=10)

    question_listbox = tk.Listbox(question_window, font=("Arial", 10), width=80, height=10)
    question_listbox.pack(pady=10)

    question_dict = {}
    for question in questions:
        question_text = f"ID: {question.id} - Вопрос: {question.text}"
        question_listbox.insert(tk.END, question_text)
        question_dict[question_text] = question.id

    def submit_answer():
        selected_question = question_listbox.get(tk.ACTIVE)
        question_id = question_dict.get(selected_question)
        response_text = simpledialog.askstring("Добавить ответ", "Введите текст ответа:")
        rating = simpledialog.askinteger("Добавить ответ", "Введите оценку (от 1 до 5):")
        if question_id and response_text and rating:
            cursor.execute("INSERT INTO Answers (question_id, response_text, rating) VALUES (?, ?, ?)", question_id,
                           response_text, rating)
            conn.commit()
            messagebox.showinfo("Успех", "Ответ успешно добавлен.")
            question_window.destroy()

    submit_button = tk.Button(question_window, text="Выбрать и добавить ответ", command=submit_answer, bg="#8A91D0",
                              fg="white", font=("Arial", 12), padx=10, pady=5)
    submit_button.pack(pady=10)


def view_questionnaires():
    cursor.execute("SELECT * FROM Questionnaires")
    questionnaires = cursor.fetchall()
    result_window = tk.Toplevel(root)
    result_window.title("Просмотр анкет")
    result_window.geometry("1000x400")
    result_window.configure(bg="#ffffff")

    for q in questionnaires:
        tk.Label(result_window, text=f"Анкета ID: {q.id}, Название: {q.title}, Описание: {q.description}",
                 font=("Arial", 10, "bold"), fg="#333").pack(anchor="w", padx=10, pady=5)
        cursor.execute("SELECT * FROM Questions WHERE questionnaire_id = ?", q.id)
        questions = cursor.fetchall()
        for question in questions:
            tk.Label(result_window, text=f"  Вопрос ID: {question.id}, Текст: {question.text}", font=("Arial", 10),
                     fg="#555").pack(anchor="w", padx=20)
            cursor.execute("SELECT * FROM Answers WHERE question_id = ?", question.id)
            answers = cursor.fetchall()
            for answer in answers:
                tk.Label(result_window, text=f"    Ответ: {answer.response_text}, Оценка: {answer.rating}",
                         font=("Arial", 10), fg="#777").pack(anchor="w", padx=30)


control_frame = tk.Frame(root, bg="#D3DEFD")
control_frame.pack(pady=20)

button_color = "#8A91D0"

tk.Button(control_frame, text="Создать анкету", command=create_questionnaire, bg=button_color, fg="white",
          font=("Arial", 12), padx=10, pady=5).grid(row=0, column=0, padx=10, pady=5)
tk.Button(control_frame, text="Добавить вопрос", command=add_question, bg=button_color, fg="white", font=("Arial", 12),
          padx=10, pady=5).grid(row=0, column=1, padx=10, pady=5)
tk.Button(control_frame, text="Добавить ответ", command=add_answer, bg=button_color, fg="white", font=("Arial", 12),
          padx=10, pady=5).grid(row=0, column=2, padx=10, pady=5)
tk.Button(control_frame, text="Просмотреть анкеты", command=view_questionnaires, bg=button_color, fg="white",
          font=("Arial", 12), padx=10, pady=5).grid(row=0, column=3, padx=10, pady=5)

root.mainloop()
conn.close()
