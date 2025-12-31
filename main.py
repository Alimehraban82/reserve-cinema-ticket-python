import tkinter as tk
from tkinter import messagebox
import json, os, sys
from PIL import Image, ImageTk
from tkcalendar import Calendar

def get_data_path():
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(os.path.dirname(sys.executable), "data.json")
    return "data.json"

DATA_FILE = get_data_path()



def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

reservations = load_data()


movies = {
    "Avatar": {"seats": 30, "poster": "avatar.jpg"},
    "Inception": {"seats": 30, "poster": "inception.jpg"},
    "Interstellar": {"seats": 30, "poster": "interstellar.jpg"}
}

sessions = ["12:00", "15:00", "18:00", "21:00"]


root = tk.Tk()
root.title("🎬 سیستم رزرو بلیط سینما")
root.geometry("900x600")
root.configure(bg="#0f0f0f")

tk.Label(
    root, text="سیستم رزرو بلیط سینما",
    font=("Arial", 26, "bold"),
    fg="white", bg="#0f0f0f"
).pack(pady=20)

frame_movies = tk.Frame(root, bg="#0f0f0f")
frame_movies.pack()


def open_session_window(movie):
    win = tk.Toplevel(root)
    win.title("انتخاب سانس")
    win.geometry("300x350")
    win.configure(bg="#1c1c1c")

    tk.Label(
        win, text=f"سانس‌های {movie}",
        font=("Arial", 16),
        fg="white", bg="#1c1c1c"
    ).pack(pady=15)

    for s in sessions:
        tk.Button(
            win, text=s,
            font=("Arial", 14),
            bg="#e50914", fg="white",
            width=10,
            command=lambda session=s: open_date_window(movie, session)
        ).pack(pady=6)


def open_date_window(movie, session):
    win = tk.Toplevel(root)
    win.title("انتخاب تاریخ")
    win.geometry("350x350")
    win.configure(bg="#1c1c1c")

    cal = Calendar(
        win, selectmode="day",
        date_pattern="yyyy-mm-dd"
    )
    cal.pack(pady=20)

    tk.Button(
        win, text="تأیید",
        font=("Arial", 14),
        bg="#e50914", fg="white",
        command=lambda: open_seat_window(
            movie, session, cal.get_date()
        )
    ).pack(pady=10)


def open_seat_window(movie, session, date):
    win = tk.Toplevel(root)
    win.title("انتخاب صندلی")
    win.geometry("600x500")
    win.configure(bg="#1c1c1c")

    tk.Label(
        win,
        text=f"{movie} | {date} | {session}",
        font=("Arial", 16),
        fg="white", bg="#1c1c1c"
    ).pack(pady=10)

    seat_frame = tk.Frame(win, bg="#1c1c1c")
    seat_frame.pack()

    movie_data = reservations.setdefault(movie, {})
    date_data = movie_data.setdefault(date, {})
    reserved = date_data.setdefault(session, [])

    buttons = []

    def reserve(seat):
        if seat in reserved:
            messagebox.showerror("خطا", "این صندلی رزرو شده")
            return

        reserved.append(seat)
        save_data(reservations)
        buttons[seat-1].config(bg="#e74c3c")
        messagebox.showinfo(
            "موفق",
            f"رزرو انجام شد\nفیلم: {movie}\nتاریخ: {date}\nسانس: {session}\nصندلی: {seat}"
        )

    seat = 1
    for r in range(5):
        for c in range(6):
            color = "#2ecc71" if seat not in reserved else "#e74c3c"
            btn = tk.Button(
                seat_frame, text=str(seat),
                width=5, height=2,
                bg=color, fg="white",
                command=lambda s=seat: reserve(s)
            )
            btn.grid(row=r, column=c, padx=5, pady=5)
            buttons.append(btn)
            seat += 1


def create_movie_card(name, info):
    frame = tk.Frame(
        frame_movies,
        bg="#1c1c1c",
        highlightbackground="#333",
        highlightthickness=2
    )
    frame.pack(side="left", padx=20)

    try:
        img = Image.open(resource_path(info["poster"]))
        img = img.resize((150, 220))
        photo = ImageTk.PhotoImage(img)
    except:
        photo = None

    lbl = tk.Label(frame, image=photo, bg="#1c1c1c")
    lbl.image = photo
    lbl.pack(pady=10)

    tk.Label(
        frame, text=name,
        font=("Arial", 16),
        fg="white", bg="#1c1c1c"
    ).pack()

    tk.Button(
        frame, text="رزرو بلیط",
        font=("Arial", 14),
        bg="#e50914", fg="white",
        width=12,
        command=lambda: open_session_window(name)
    ).pack(pady=15)


for m, info in movies.items():
    create_movie_card(m, info)

root.mainloop()
