import tkinter as tk
from tkinter import messagebox
import requests

# Список сайтов
urls = [
    "https://github.com/",
    "https://www.binance.com/en",
    "https://tomtit.tomsk.ru/",
    "https://jsonplaceholder.typicode.com/",
    "https://moodle.tomtit-tomsk.ru/"
]

def check_sites():
    result_text.delete(1.0, tk.END)

    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            status_code = response.status_code

            if status_code == 200:
                status = "доступен"
            elif status_code == 404:
                status = "не найден"
            elif status_code == 403:
                status = "вход запрещен"
            else:
                status = "не доступен"

            result_text.insert(tk.END, f"{url} – {status} – {status_code}\n")

        except requests.exceptions.RequestException:
            result_text.insert(tk.END, f"{url} – не доступен – ошибка соединения\n")

    messagebox.showinfo("Готово", "Проверка сайтов завершена!")

# Создание окна
window = tk.Tk()
window.title("Проверка доступности сайтов")
window.geometry("750x400")

label = tk.Label(window, text="Нажмите кнопку для проверки сайтов")
label.pack(pady=5)

button = tk.Button(window, text="Проверить сайты", command=check_sites)
button.pack(pady=5)

result_text = tk.Text(window, width=90, height=15)
result_text.pack(pady=10)

window.mainloop()
