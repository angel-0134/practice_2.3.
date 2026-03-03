import tkinter as tk
from tkinter import simpledialog, messagebox
import requests
import json

# Получаем курсы
url = "https://www.cbr-xml-daily.ru/daily_json.js"
response = requests.get(url)
data = response.json()
valutes = data["Valute"]

# Загружаем группы
try:
    with open("save.json", "r", encoding="utf-8") as f:
        groups = json.load(f)
except FileNotFoundError:
    groups = {}

# Функции для кнопок
def show_all_valutes():
    text_box.delete("1.0", tk.END)
    for code, currency in valutes.items():
        text_box.insert(tk.END, f"{code} - {currency['Name']} - {currency['Value']}\n")

def find_valute():
    code = simpledialog.askstring("Поиск валюты", "Введите код валюты:").upper()
    if code in valutes:
        currency = valutes[code]
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, f"{currency['Name']} - {currency['Value']}")
    else:
        messagebox.showerror("Ошибка", "Валюта не найдена")

def create_group():
    group_name = simpledialog.askstring("Создать группу", "Введите название группы:")
    if not group_name:
        return
    groups[group_name] = []
    while True:
        code = simpledialog.askstring("Добавить валюту", "Код валюты (Enter для окончания):")
        if not code:
            break
        code = code.upper()
        if code in valutes:
            groups[group_name].append(code)
        else:
            messagebox.showerror("Ошибка", f"Валюта {code} не найдена")
    # Сохраняем в файл
    with open("save.json", "w", encoding="utf-8") as f:
        json.dump(groups, f, ensure_ascii=False, indent=4)
    messagebox.showinfo("Группа", "Группа сохранена!")

def show_groups():
    text_box.delete("1.0", tk.END)
    if not groups:
        text_box.insert(tk.END, "Нет созданных групп")
        return
    for group, codes in groups.items():
        text_box.insert(tk.END, f"{group}: {', '.join(codes)}\n")

# Создаем главное окно
root = tk.Tk()
root.title("Монитор курсов валют")

# Кнопки
frame = tk.Frame(root)
frame.pack(side=tk.LEFT, padx=10, pady=10)

tk.Button(frame, text="Все валюты", command=show_all_valutes).pack(fill=tk.X)
tk.Button(frame, text="Поиск валюты", command=find_valute).pack(fill=tk.X)
tk.Button(frame, text="Создать группу", command=create_group).pack(fill=tk.X)
tk.Button(frame, text="Показать группы", command=show_groups).pack(fill=tk.X)

# Текстовое поле для вывода
text_box = tk.Text(root, width=50, height=20)
text_box.pack(side=tk.RIGHT, padx=10, pady=10)

root.mainloop()
