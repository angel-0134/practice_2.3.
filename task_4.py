import tkinter as tk
from tkinter import simpledialog, messagebox
import requests

def get_profile(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return (
            f"Имя: {data.get('name')}\n"
            f"Ссылка: {data.get('html_url')}\n"
            f"Репозитории: {data.get('public_repos')}\n"
            f"Подписчики: {data.get('followers')}\n"
            f"Подписки: {data.get('following')}\n"
        )
    else:
        return "Пользователь не найден."

def get_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        repos = response.json()
        if not repos:
            return "У пользователя нет репозиториев."
        text = ""
        for repo in repos:
            text += (
                f"Название: {repo.get('name')}\n"
                f"Ссылка: {repo.get('html_url')}\n"
                f"Язык: {repo.get('language')}\n"
                f"Видимость: {repo.get('visibility')}\n"
                f"Ветка по умолчанию: {repo.get('default_branch')}\n"
                + "-"*40 + "\n"
            )
        return text
    else:
        return "Ошибка получения репозиториев."

def search_repositories(query):
    url = f"https://api.github.com/search/repositories?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        items = response.json().get("items", [])
        if not items:
            return "Ничего не найдено."
        text = ""
        for repo in items[:5]:
            text += (
                f"Название: {repo.get('name')}\n"
                f"Ссылка: {repo.get('html_url')}\n"
                f"Язык: {repo.get('language')}\n"
                + "-"*40 + "\n"
            )
        return text
    else:
        return "Ошибка поиска."

# GUI
root = tk.Tk()
root.title("GitHub Monitor")

text_box = tk.Text(root, width=80, height=25)
text_box.pack(side=tk.RIGHT, padx=10, pady=10)

frame = tk.Frame(root)
frame.pack(side=tk.LEFT, padx=10, pady=10)

def show_profile():
    username = simpledialog.askstring("Профиль GitHub", "Введите имя пользователя:")
    if username:
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, get_profile(username))

def show_repositories():
    username = simpledialog.askstring("Репозитории GitHub", "Введите имя пользователя:")
    if username:
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, get_repositories(username))

def search_repo():
    query = simpledialog.askstring("Поиск репозитория", "Введите название репозитория:")
    if query:
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, search_repositories(query))

tk.Button(frame, text="Профиль пользователя", command=show_profile).pack(fill=tk.X)
tk.Button(frame, text="Все репозитории", command=show_repositories).pack(fill=tk.X)
tk.Button(frame, text="Поиск репозитория", command=search_repo).pack(fill=tk.X)

root.mainloop()
