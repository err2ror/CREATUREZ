import random
import tkinter as tk
from tkinter import ttk, messagebox

# --- DATA LOAD ---

try:
    from monsterdb import al_frm
except ImportError:
    print("monsterdb.py with al_frm not found. Run your breeder first.")
    raise SystemExit

# --- LOGIC ---

def nice_text(x):
    return (
        f"Name: {x['name']}\n"
        f"Color: {x['color']}\n"
        f"Ability: {x['ability']}\n"
        f"Weakness: {x['weakness']}\n"
        f"Power: {x['power_level']}"
    )

def battle(a, b):
    base_a = a["power_level"]
    base_b = b["power_level"]

    chaos_a = random.randint(-base_a // 5, base_a // 5)
    chaos_b = random.randint(-base_b // 5, base_b // 5)

    final_a = max(1, base_a + chaos_a)
    final_b = max(1, base_b + chaos_b)

    if final_a > final_b:
        winner = a
        result = f"{a['name']} wins!\n\n{a['name']} final power: {final_a}\n{b['name']} final power: {final_b}"
    elif final_b > final_a:
        winner = b
        result = f"{b['name']} wins!\n\n{a['name']} final power: {final_a}\n{b['name']} final power: {final_b}"
    else:
        winner = None
        result = f"It's a tie!\n\n{a['name']} final power: {final_a}\n{b['name']} final power: {final_b}"

    return winner, result

# --- GUI ---

root = tk.Tk()
root.title("Creature Battle GUI")

# Dropdown options: "index - name (power)"
options = [f"{i} - {c['name']} ({c['power_level']})" for i, c in enumerate(al_frm)]

frame_top = ttk.Frame(root, padding=10)
frame_top.pack(fill="x")

ttk.Label(frame_top, text="Fighter A:").grid(row=0, column=0, sticky="w")
ttk.Label(frame_top, text="Fighter B:").grid(row=1, column=0, sticky="w")

var_a = tk.StringVar(value=options[0] if options else "")
var_b = tk.StringVar(value=options[1] if len(options) > 1 else (options[0] if options else ""))

combo_a = ttk.Combobox(frame_top, textvariable=var_a, values=options, state="readonly", width=40)
combo_b = ttk.Combobox(frame_top, textvariable=var_b, values=options, state="readonly", width=40)
combo_a.grid(row=0, column=1, padx=5, pady=2)
combo_b.grid(row=1, column=1, padx=5, pady=2)

btn_frame = ttk.Frame(root, padding=10)
btn_frame.pack(fill="x")

def on_show_stats():
    try:
        idx_a = int(var_a.get().split(" - ")[0])
        idx_b = int(var_b.get().split(" - ")[0])
    except Exception:
        messagebox.showerror("Error", "Invalid selection.")
        return

    crea_a = al_frm[idx_a]
    crea_b = al_frm[idx_b]

    text_a.config(state="normal")
    text_b.config(state="normal")
    text_a.delete("1.0", "end")
    text_b.delete("1.0", "end")
    text_a.insert("1.0", nice_text(crea_a))
    text_b.insert("1.0", nice_text(crea_b))
    text_a.config(state="disabled")
    text_b.config(state="disabled")

def on_battle():
    try:
        idx_a = int(var_a.get().split(" - ")[0])
        idx_b = int(var_b.get().split(" - ")[0])
    except Exception:
        messagebox.showerror("Error", "Invalid selection.")
        return

    if idx_a == idx_b:
        messagebox.showwarning("Warning", "Pick two different fighters.")
        return

    crea_a = al_frm[idx_a]
    crea_b = al_frm[idx_b]

    _, result = battle(crea_a, crea_b)
    result_text.config(state="normal")
    result_text.delete("1.0", "end")
    result_text.insert("1.0", result)
    result_text.config(state="disabled")

btn_stats = ttk.Button(btn_frame, text="Show Stats", command=on_show_stats)
btn_battle = ttk.Button(btn_frame, text="Battle!", command=on_battle)
btn_stats.pack(side="left", padx=5)
btn_battle.pack(side="left", padx=5)

frame_mid = ttk.Frame(root, padding=10)
frame_mid.pack(fill="both", expand=True)

ttk.Label(frame_mid, text="Fighter A Stats").grid(row=0, column=0)
ttk.Label(frame_mid, text="Fighter B Stats").grid(row=0, column=1)

text_a = tk.Text(frame_mid, width=40, height=10, state="disabled")
text_b = tk.Text(frame_mid, width=40, height=10, state="disabled")
text_a.grid(row=1, column=0, padx=5, pady=5)
text_b.grid(row=1, column=1, padx=5, pady=5)

frame_bottom = ttk.Frame(root, padding=10)
frame_bottom.pack(fill="both", expand=True)

ttk.Label(frame_bottom, text="Battle Result").pack(anchor="w")
result_text = tk.Text(frame_bottom, width=85, height=6, state="disabled")
result_text.pack(fill="both", expand=True)

root.mainloop()

