# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
import os

SETTINGS_FILE = "rust_bind_settings.txt"

YOUTUBERS_FILE = {
    "CheZee": "chezee_graphics.txt",
    "Fleeca": "fleeca_graphics.txt",
    "Shroud": "shroud_graphics.txt"
}


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


class ChoiceFile:

    @staticmethod
    def apply_youtuber_settings(config_path, youtuber):
        settings_file = YOUTUBERS_FILE.get(youtuber)
        if not settings_file or not os.path.exists(settings_file):
            return False

        # Список команд для замены
        commands = [
            "grass.distance", "graphics.renderscale", "graphics.dlaa", "graphics.dlss",
            "render.instancing_render_distance", "graphics.shaderlod", "graphics.drawdistance",
            "graphics.parallax", "water.quality", "water.reflections", "grass.displacement",
            "graphics.grassshadows", "graphicssettings.softparticles", "graphicssettings.pixellightcount",
            "graphicssettings.particleraycastbudget", "graphics.lodbias", "particle.quality",
            "tree.quality", "mesh.quality", "tree.meshes", "terrain.quality", "grass.quality",
            "decor.quality", "effects.antialiasing", "effects.motionblur", "effects.shafts",
            "effects.sharpen", "effects.hurtoverleyapplylighting", "effects.hurtoverlay", "gc.buffer"
        ]

        with open(settings_file, 'r', encoding='utf-8') as f:
            youtuber_settings = [line.strip() for line in f if line.strip()]

        for i, command in enumerate(commands):
            if i < len(youtuber_settings):
                replace_in_large_file(config_path, command, youtuber_settings[i])

        return True


class AppConfig:

    @staticmethod
    def get_config_path():
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
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

        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            f.write(file_path)

        root.destroy()
        return file_path


class HelperWindow:

    def __init__(self, parent):
        self.window = Toplevel(parent)
        self.window.title("Помощь")
        self.window.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.window)

        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="Общая информация")

        general_text = Text(general_frame, wrap=WORD, padx=10, pady=10)
        general_text.insert(END,
                            "Rust Bind Fast - программа для быстрой настройки биндов в Rust\n\n"
                            "Функции:\n"
                            "1. Zoom - динамическое изменение FOV\n"
                            "2. Heal -  быстрый крафт бинтов\n"
                            "3. Auto sprints - автоматический спринт\n"
                            "4. Combat + pings + console - комбо-бинды для боя\n\n"
                            "Инструкция:\n"
                            "1. Выберите действие из главного меню\n"
                            "2. Введите клавишу для бинда\n"
                            "3. Нажмите Apply для применения\n"
                            "4. Изменения сохраняются в ваш конфиг-файл"
                            )
        general_text.config(state=DISABLED)
        general_text.pack(fill=BOTH, expand=True)

        about_frame = ttk.Frame(notebook)
        notebook.add(about_frame, text="О программе")

        about_text = Text(about_frame, wrap=WORD, padx=10, pady=10)
        about_text.insert(END,
                          "Rust Bind Fast v2.0\n\n"
                          "Разработано для упрощения настройки биндов в Rust\n\n"
                          "Особенности:\n"
                          "- Простой и интуитивно понятный интерфейс\n"
                          "- Автоматическое сохранение пути к конфигурации\n"
                          "- Безопасное изменение файлов\n"
                          "- Возможность смены конфигурационного файла\n\n"
                          "Автор: я даун\n"
                          "Дата релиза: 2025"
                          )
        about_text.config(state=DISABLED)
        about_text.pack(fill=BOTH, expand=True)

        notebook.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Кнопка закрытия
        close_btn = ttk.Button(self.window, text="Закрыть", command=self.window.destroy)
        close_btn.pack(pady=10)


class GraphicsWindow:

    def __init__(self, parent, config_path):
        self.window = Toplevel(parent)
        self.window.title("Графика от ютуберов")
        self.window.geometry("300x200")
        self.config_path = config_path

        label = ttk.Label(self.window, text="Выберите ютубера:")
        label.pack(pady=10)

        youtubers = list(YOUTUBERS_FILE.keys())
        self.combobox = ttk.Combobox(self.window, values=youtubers)
        self.combobox.pack(pady=5)
        self.combobox.current(0)

        apply_btn = ttk.Button(
            self.window,
            text="Применить настройки",
            command=self.apply_settings
        )
        apply_btn.pack(pady=10)

        self.result_label = ttk.Label(self.window, text="")
        self.result_label.pack(pady=5)

        close_btn = ttk.Button(self.window, text="Закрыть", command=self.window.destroy)
        close_btn.pack(pady=5)

    def apply_settings(self):
        youtuber = self.combobox.get()
        if ChoiceFile.apply_youtuber_settings(self.config_path, youtuber):
            self.result_label["text"] = f"Настройки {youtuber} успешно применены!"
        else:
            self.result_label["text"] = f"Ошибка: не удалось применить настройки {youtuber}"


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
        languages_var = StringVar(value=binds[0])

        main_frame = ttk.Frame(self.main_root)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        label = ttk.Label(main_frame, text="Выберите действие:")
        label.pack(anchor=NW, padx=6, pady=6)

        self.combobox = ttk.Combobox(main_frame, textvariable=languages_var, values=binds)
        self.combobox.pack(anchor=NW, fill=X, padx=6, pady=6)
        self.combobox.bind("<<ComboboxSelected>>", self.selected)

        helper_btn = ttk.Button(
            main_frame,
            text="Помощь",
            command=lambda: HelperWindow(self.main_root)
        )
        helper_btn.pack(anchor=NW, padx=6, pady=6)

        graphics_btn = ttk.Button(
            main_frame,
            text="Графика популярных ютуберов",
            command=self.open_graphics_window
        )
        graphics_btn.pack(anchor=NW, padx=6, pady=6)

        change_btn = ttk.Button(
            main_frame,
            text="Сменить конфиг",
            command=self.change_config
        )
        change_btn.pack(anchor=NW, padx=6, pady=6)

        self.main_root.mainloop()

    def open_graphics_window(self):
        GraphicsWindow(self.main_root, self.config_path)

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
            zoom_root.title("Настройки зума")
            zoom_app = Zoom(zoom_root, self.main_root, self.config_path)
            zoom_app.zoom()

        elif selection == "heal":
            heal_root = Toplevel(self.main_root)
            heal_root.geometry("300x250")
            heal_root.title("Настройки лечения")
            heal_app = Heal(heal_root, self.main_root, self.config_path)
            heal_app.heal()

        elif selection == "auto sprints":
            sprint_root = Toplevel(self.main_root)
            sprint_root.geometry("300x250")
            sprint_root.title("Настройки автоспринта")
            sprint_app = AutoSprints(sprint_root, self.main_root, self.config_path)
            sprint_app.auto_sprints()

        elif selection == "combat + pings + console":
            combat_root = Toplevel(self.main_root)
            combat_root.geometry("300x250")
            combat_root.title("Настройки боя")
            combat_app = CombatPingsConsole(combat_root, self.main_root, self.config_path)
            combat_app.combat_pings_console()


class BaseSetting:
    def __init__(self, root, main_root, config_path):
        self.root = root
        self.main_root = main_root
        self.config_path = config_path
        self.label = ttk.Label(root, text="Введите клавишу и нажмите Применить:")
        self.entry = ttk.Entry(root)

        # Кнопка возврата в главное меню
        self.back_btn = ttk.Button(
            root,
            text="Назад в меню",
            command=self.back_to_main
        )

    def back_to_main(self):
        self.root.destroy()
        self.main_root.deiconify()


class Zoom(BaseSetting):
    def __init__(self, root, main_root, config_path):
        super().__init__(root, main_root, config_path)
        self.label.config(text="Введите клавишу для зума:")

    def zoom(self):
        self.entry.pack(anchor=NW, padx=6, pady=6)
        btn = ttk.Button(self.root, text="Применить", command=self.show_message)
        btn.pack(anchor=NW, padx=6, pady=6)
        self.label.pack(anchor=NW, padx=6, pady=6)
        self.back_btn.pack(anchor=NW, padx=6, pady=6)

    def show_message(self):
        key = self.entry.get()
        search_str = f'bind {key}'
        replace_str = f'bind {key} +graphics.fov 90;graphics.fov 70'
        if replace_in_large_file(self.config_path, search_str, replace_str):
            self.label["text"] = f"Зум назначен на: {key}"
        else:
            self.label["text"] = f"Клавиша '{key}' не найдена! Добавлена новая привязка."


class Heal(BaseSetting):
    def __init__(self, root, main_root, config_path):
        super().__init__(root, main_root, config_path)
        self.label.config(text="Введите клавишу для лечения:")

    def heal(self):
        self.entry.pack(anchor=NW, padx=6, pady=6)
        btn = ttk.Button(self.root, text="Применить", command=self.show_message)
        btn.pack(anchor=NW, padx=6, pady=6)
        self.label.pack(anchor=NW, padx=6, pady=6)
        self.back_btn.pack(anchor=NW, padx=6, pady=6)

    def show_message(self):
        key = self.entry.get()
        search_str = f'bind {key}'
        replace_str = f'bind {key} Craft.add -2072273936'
        if replace_in_large_file(self.config_path, search_str, replace_str):
            self.label["text"] = f"Лечение назначено на: {key}"
        else:
            self.label["text"] = f"Клавиша '{key}' не найдена! Добавлена новая привязка."


class AutoSprints(BaseSetting):
    def __init__(self, root, main_root, config_path):
        super().__init__(root, main_root, config_path)
        self.label.config(text="Введите клавишу для автоспринта:")

    def auto_sprints(self):
        self.entry.pack(anchor=NW, padx=6, pady=6)
        btn = ttk.Button(self.root, text="Применить", command=self.show_message)
        btn.pack(anchor=NW, padx=6, pady=6)
        self.label.pack(anchor=NW, padx=6, pady=6)
        self.back_btn.pack(anchor=NW, padx=6, pady=6)

    def show_message(self):
        key = self.entry.get()
        search_str = f'bind {key}'
        replace_str = f'bind {key} forward;sprint'
        if replace_in_large_file(self.config_path, search_str, replace_str):
            self.label["text"] = f"Автоспринт назначен на: {key}"
        else:
            self.label["text"] = f"Клавиша '{key}' не найдена! Добавлена новая привязка."


class CombatPingsConsole(BaseSetting):
    def __init__(self, root, main_root, config_path):
        super().__init__(root, main_root, config_path)
        self.label.config(text="Введите клавишу для боевых действий:")

    def combat_pings_console(self):
        self.entry.pack(anchor=NW, padx=6, pady=6)
        btn = ttk.Button(self.root, text="Применить", command=self.show_message)
        btn.pack(anchor=NW, padx=6, pady=6)
        self.label.pack(anchor=NW, padx=6, pady=6)
        self.back_btn.pack(anchor=NW, padx=6, pady=6)

    def show_message(self):
        key = self.entry.get()
        search_str = f'bind {key}'
        replace_str = f'bind {key} client.consoletoggle;combatlog;client.ping'
        if replace_in_large_file(self.config_path, search_str, replace_str):
            self.label["text"] = f"Боевые действия назначены на: {key}"
        else:
            self.label["text"] = f"Клавиша '{key}' не найдена! Добавлена новая привязка."


if __name__ == "__main__":
    config_path = AppConfig.get_config_path()
    app = Screen(300, 250, config_path)
    app.main_screen()