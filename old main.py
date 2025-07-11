from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
import os
# -*- coding: utf-8 -*-
SETTINGS_FILE = "path.txt"


class AppConfig:

    @staticmethod
    def get_config_path():
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                return f.read().strip()

        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Выберите файл конфигурации Rust (обычно .cfg файл)",
            filetypes=[("Config files", "*.cfg"), ("All files", "*.*")]
        )

        if not file_path:
            print("Путь не выбран. Приложение будет закрыто.")
            exit()

        with open(SETTINGS_FILE, 'w') as f:
            f.write(file_path)

        root.destroy()
        return file_path


class Screen:
    def __init__(self, size_x, size_y, config_path):
        self.size_x = size_x
        self.size_y = size_y
        self.config_path = config_path
        self.root = None
        self.combobox = None
        self.main_root = None

    def main_screen(self):
        self.main_root = Tk()
        self.main_root.geometry(f"{str(self.size_x)}x{str(self.size_y)}")
        self.main_root.title(f"Rust bind fast - {os.path.basename(self.config_path)}")

        binds = ["zoom", "heal", "auto sprints", "combat + pings + console"]
        languages_binds = StringVar(value=binds[0])

        label = ttk.Label(self.main_root, text="Select an option:")
        label.pack(anchor=NW, padx=6, pady=6)

        self.combobox = ttk.Combobox(self.main_root, textvariable=languages_binds, values=binds)
        self.combobox.pack(anchor=NW, padx=6, pady=6)
        self.combobox.bind("<<ComboboxSelected>>", self.selected)

        change_btn = ttk.Button(
            self.main_root,
            text="Change Config File",
            command=self.change_config
        )
        change_btn.pack(anchor=NW, padx=6, pady=6)

        self.main_root.mainloop()

    def change_config(self):
        if os.path.exists(SETTINGS_FILE):
            os.remove(SETTINGS_FILE)
        self.main_root.destroy()
        config_path = AppConfig.get_config_path()
        app = Screen(300, 250, config_path)
        app.main_screen()

    def selected(self, event):
        selection = self.combobox.get()
        self.main_root.withdraw()

        if selection == "zoom":
            zoom_root = Toplevel(self.main_root)
            zoom_root.geometry("300x250")
            zoom_root.title("Zoom Settings")
            zoom_app = Zoom(zoom_root, self.main_root, self.config_path)
            zoom_app.zoom()

        elif selection == "heal":
            heal_root = Toplevel(self.main_root)
            heal_root.geometry("300x250")
            heal_root.title("Heal Settings")
            heal_app = Heal(heal_root, self.main_root, self.config_path)
            heal_app.heal()

        elif selection == "auto sprints":
            sprint_root = Toplevel(self.main_root)
            sprint_root.geometry("300x250")
            sprint_root.title("Auto Sprints Settings")
            sprint_app = AutoSprints(sprint_root, self.main_root, self.config_path)
            sprint_app.auto_sprints()

        elif selection == "combat + pings + console":
            combat_root = Toplevel(self.main_root)
            combat_root.geometry("300x250")
            combat_root.title("Combat+Pings+Console Settings")
            combat_app = CombatPingsConsole(combat_root, self.main_root, self.config_path)
            combat_app.combat_pings_console()


class BaseSetting:

    def __init__(self, root, main_root, config_path):
        self.root = root
        self.main_root = main_root
        self.config_path = config_path
        self.label = ttk.Label(root, text="Enter key and press Apply:")
        self.entry = ttk.Entry(root)


        self.back_btn = ttk.Button(
            root,
            text="Back to Main",
            command=self.back_to_main
        )

    def back_to_main(self):
        self.root.destroy()
        self.main_root.deiconify()


class Zoom(BaseSetting):
    def __init__(self, root, main_root, config_path):
        super().__init__(root, main_root, config_path)
        self.label.config(text="Enter key for zoom:")

    def zoom(self):
        self.entry.pack(anchor=NW, padx=6, pady=6)
        btn = ttk.Button(self.root, text="Apply", command=self.show_message)
        btn.pack(anchor=NW, padx=6, pady=6)
        self.label.pack(anchor=NW, padx=6, pady=6)
        self.back_btn.pack(anchor=NW, padx=6, pady=6)

    def show_message(self):
        key = self.entry.get()
        self.label["text"] = f"Zoom binded to: {key}"
        replace_in_large_file(self.config_path, f'bind {key}', f'bind {key} +graphics.fov 90;graphics.fov 70\n')


class Heal(BaseSetting):
    def __init__(self, root, main_root, config_path):
        super().__init__(root, main_root, config_path)
        self.label.config(text="Enter key for heal:")

    def heal(self):
        self.entry.pack(anchor=NW, padx=6, pady=6)
        btn = ttk.Button(self.root, text="Apply", command=self.show_message)
        btn.pack(anchor=NW, padx=6, pady=6)
        self.label.pack(anchor=NW, padx=6, pady=6)
        self.back_btn.pack(anchor=NW, padx=6, pady=6)

    def show_message(self):
        key = self.entry.get()
        self.label["text"] = f"Heal binded to: {key}"
        replace_in_large_file(self.config_path, f'bind {key}', f'bind {key} Craft.add -2072273936\n')


class AutoSprints(BaseSetting):
    def __init__(self, root, main_root, config_path):
        super().__init__(root, main_root, config_path)
        self.label.config(text="Enter key for auto sprints:")

    def auto_sprints(self):
        self.entry.pack(anchor=NW, padx=6, pady=6)
        btn = ttk.Button(self.root, text="Apply", command=self.show_message)
        btn.pack(anchor=NW, padx=6, pady=6)
        self.label.pack(anchor=NW, padx=6, pady=6)
        self.back_btn.pack(anchor=NW, padx=6, pady=6)

    def show_message(self):
        key = self.entry.get()
        self.label["text"] = f"Auto sprints binded to: {key}"
        replace_in_large_file(self.config_path, f'bind {key}', f'bind {key} leftshift; +sprint\n')


class CombatPingsConsole(BaseSetting):
    def __init__(self, root, main_root, config_path):
        super().__init__(root, main_root, config_path)
        self.label.config(text="Enter key for combat+pings+console:")

    def combat_pings_console(self):
        self.entry.pack(anchor=NW, padx=6, pady=6)
        btn = ttk.Button(self.root, text="Apply", command=self.show_message)
        btn.pack(anchor=NW, padx=6, pady=6)
        self.label.pack(anchor=NW, padx=6, pady=6)
        self.back_btn.pack(anchor=NW, padx=6, pady=6)

    def show_message(self):
        key = self.entry.get()
        self.label["text"] = f"Combat+pings+console binded to: {key}"
        replace_in_large_file(self.config_path, f'bind {key}', f'bind {key} client.consoletoggle;combatlog;client.ping\n')

def open_file():
    with open('path.txt', 'r', encoding='utf-8') as file:
        replace_in_large_file(file.readline())


def replace_in_large_file(filename, search_str, replace_str):
    temp_file = filename + ".tmp"
    replaced = False

    with open(filename, 'r', encoding='utf-8') as fin, open(temp_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            if search_str in line:
                fout.write(replace_str + '\n')
                replaced = True
            else:
                fout.write(line)

    if replaced:
        os.replace(temp_file, filename)
        return True
    else:
        try:
            os.remove(temp_file)
        except:
            pass
        return False

if __name__ == "__main__":
    config_path = AppConfig.get_config_path()
    app = Screen(300, 250, config_path)
    app.main_screen()
