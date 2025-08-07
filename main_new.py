# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.messagebox import showerror
from PIL import ImageTk, Image
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
        except FileNotFoundError:
            AppConfig.get_config_path()
            print('37 line')
        return False


class ChoiceFile:

    @staticmethod
    def apply_youtuber_settings(config_path, youtuber):
        settings_file = YOUTUBERS_FILE.get(youtuber)
        if not settings_file or not os.path.exists(settings_file):
            return False

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
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                youtuber_settings = [line.strip() for line in f if line.strip()]

            for i, command in enumerate(commands):
                if i < len(youtuber_settings):
                    replace_in_large_file(config_path, command, youtuber_settings[i])

            return True
        except FileNotFoundError:
            os.remove(SETTINGS_FILE)
            AppConfig.get_config_path()


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

    @staticmethod
    def graphics_file():
        flag = 0
        for dirpath, dirnames, filenames in os.walk('.'):
            try:
                for filename in filenames:
                    if filename == 'client.cfg':
                        flag = 1
                        print(filename)
                try:
                    if flag == 0:
                        showerror(title='Ошибка', message='Файл keys.cfg был перемещён. Выберите его снова')
                        os.remove(SETTINGS_FILE)
                        AppConfig.get_config_path()
                except print('Файл найден'):
                    pass
            except:
                print(os.path.join(dirpath, filename))
        with open('rust_bind_settings.txt', 'r', encoding='utf-8') as file:
            graphics_file = file.read()[:-8] + 'client.cfg'

        return graphics_file


class HelperWindow:

    def __init__(self, parent):
        self.window = Toplevel(parent)
        self.window.title("Помощь")
        self.window.geometry("400x300")
        self.window.resizable(True, True)
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.window)

        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="Общая информация")

        general_text = Text(general_frame, wrap=WORD, padx=10, pady=10)
        general_text.insert(END,
                            "Rust Bind Fast - программа для быстрой настройки биндов в Rust\n\n"
                            "Функции:\n"
                            "one. Zoom - динамическое изменение FOV\n"
                            "two. Auto crafting -  быстрый крафт бинтов\n"
                            "3. Auto sprints - автоматический спринт\n"
                            "4. Combat + pings + console - комбо-бинды для боя\n\n"
                            "Инструкция:\n"
                            "one. Выберите действие из главного меню\n"
                            "two. Введите клавишу для бинда\n"
                            "3. Нажмите Apply для применения\n"
                            "4. Изменения сохраняются в ваш конфиг-файл"
                            )
        general_text.config(state=DISABLED)
        general_text.pack(fill=BOTH, expand=True)

        about_frame = ttk.Frame(notebook)
        notebook.add(about_frame, text="О программе")

        about_text = Text(about_frame, wrap=WORD, padx=10, pady=10)
        about_text.insert(END,
                          "Rust Bind Fast v3.0\n\n"
                          "Разработано для упрощения настройки биндов в Rust\n\n"
                          "Особенности:\n"
                          "- Простой и интуитивно понятный интерфейс\n"
                          "- Автоматическое сохранение пути к конфигурации\n"
                          "- Безопасное изменение файлов\n"
                          "- Возможность смены конфигурационного файла\n\n"
                          "Автор: -\n"
                          "Дата релиза: 2025"
                          )
        about_text.config(state=DISABLED)
        about_text.pack(fill=BOTH, expand=True)

        notebook.pack(fill=BOTH, expand=True, padx=5, pady=5)
        close_btn = ttk.Button(self.window, text="Закрыть", command=self.window.destroy)
        close_btn.pack(pady=10)


class GraphicsWindow:

    def __init__(self, parent):
        self.window = Toplevel(parent)
        self.window.title("Графика от ютуберов")
        self.window.geometry("300x200")
        self.window.resizable(True, True)
        self.config_path = AppConfig.graphics_file()

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
        if ChoiceFile.apply_youtuber_settings(AppConfig.graphics_file(), youtuber):
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
        self.main_root.resizable(True, True)

        binds = ["zoom", "Auto crafting", "auto sprints", "combat + pings + console", "changing the color of the holographic sight"]
        languages_var = StringVar(value=binds[0])

        main_frame = ttk.Frame(self.main_root)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        label = ttk.Label(main_frame, text="После использования перезагрузите Rust.\nВыберите действие:")
        label.pack(anchor=NW, padx=1, pady=1)

        self.combobox = ttk.Combobox(main_frame, textvariable=languages_var, values=binds)
        self.combobox.pack(anchor=NW, fill=X, padx=6, pady=6)
        self.combobox.bind("<<ComboboxSelected>>", self.selected)

        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=X, pady=5)

        graphics_btn = ttk.Button(
            bottom_frame,
            text="Графика популярных ютуберов",
            command=self.open_graphics_window
        )
        graphics_btn.pack(side=LEFT, padx=6, pady=6)
        change_btn = ttk.Button(
            bottom_frame,
            text="Сменить конфиг",
            command=self.change_config
        )
        change_btn.pack(side=RIGHT, padx=6, pady=6)
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=X, pady=5)

        helper_btn = ttk.Button(
            top_frame,
            text="Помощь",
            command=lambda: HelperWindow(self.main_root)
        )
        helper_btn.pack(side=LEFT, padx=6, pady=0, anchor=SW)

        # color_holo_btn = ttk.Button(
        #     top_frame,
            # text='Смена цвета прицела',
            # command=lambda: ColorHolo(self.main_root)
        # )

        # farm_btn = ttk.Button(
            # top_frame,
            # text="Ферммерство",
            # command=lambda: Farmer(self.main_root)
        # )
        # farm_btn.pack(side=RIGHT, padx=6, pady=0, anchor=N)

        self.main_root.mainloop()

    def open_graphics_window(self):
        GraphicsWindow(self.main_root)

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
            zoom_root.resizable(True, True)
            zoom_root.title("Настройки зума")
            zoom_app = Zoom(zoom_root, self.main_root, self.config_path)
            zoom_app.zoom()

        elif selection == "Auto crafting":
            heal_root = Toplevel(self.main_root)
            heal_root.geometry("300x250")
            heal_root.resizable(True, True)
            heal_root.title("Настройки лечения")
            heal_app = Heal(heal_root, self.main_root, self.config_path)
            heal_app.heal()

        elif selection == "auto sprints":
            sprint_root = Toplevel(self.main_root)
            sprint_root.geometry("300x250")
            sprint_root.resizable(True, True)
            sprint_root.title("Настройки автоспринта")
            sprint_app = AutoSprints(sprint_root, self.main_root, self.config_path)
            sprint_app.auto_sprints()

        elif selection == "combat + pings + console":
            combat_root = Toplevel(self.main_root)
            combat_root.geometry("300x250")
            combat_root.resizable(True, True)
            combat_root.title("Настройки боя")
            combat_app = CombatPingsConsole(combat_root, self.main_root, self.config_path)
            combat_app.combat_pings_console()

        elif selection == "changing the color of the holographic sight":
            changing_root = Toplevel(self.main_root)
            changing_root.geometry("300x300")
            changing_root.resizable(True, True)
            changing_root.title("Настройка смены цвета голаграфического прицела")
            changing_app = ColorHolo(changing_root, self.main_root, self.config_path)
            changing_app.color_holo()


class BaseSetting:
    def __init__(self, root, main_root, config_path):
        self.root = root
        self.main_root = main_root
        self.config_path = config_path
        self.label = ttk.Label(root, text="Введите клавишу и нажмите Применить:")
        self.entry = ttk.Entry(root)

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
        self.label.config(text="Введите клавишу для приближения:")

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
            with open(config_path, 'r+', encoding='utf-8') as file:
                file.write(f'{replace_str}\n')


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
            self.label["text"] = f"Крафт назначен на: {key}"
        else:
            self.label["text"] = f"Клавиша '{key}' не найдена! Добавлена новая привязка."
            with open(config_path, 'r+', encoding='utf-8') as file:
                file.write(f'{replace_str}\n')


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
            with open(config_path, 'r+', encoding='utf-8') as file:
                file.write(f'{replace_str}\n')


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
            with open(config_path, 'r+', encoding='utf-8') as file:
                file.write(f'{replace_str}\n')


class ColorHolo(BaseSetting):
    def __init__(self, root, main_root, config_path):
        super().__init__(root, main_root, config_path)
        self.label.config(text="Введите клвашишу для смены цвета прицела")

    def color_holo(self):
        self.entry.pack(anchor=NW, padx=6, pady=6)
        btn = ttk.Button(self.root, text="Приминить", command=self.show_message)
        btn.pack(anchor=NW, padx=6, pady=6)
        self.label.pack(anchor=NW, padx=6, pady=6)
        self.back_btn.pack(anchor=NW, padx=6, pady=6)

    def show_message(self):
        key = self.entry.get()
        search_str = f'bind {key}'
        if (key == 'mouse0') or (key == 'mouse1'):
            replace_str = f'bind {key} +attack;+accessibility.holosightcolour 2;accessibility.holosightcolour 0'
        else:
            replace_str = f'bind {key} key +accessibility.holosightcolour 2;accessibility.holosightcolour 0'

        if replace_in_large_file(self.config_path, search_str, replace_str):
            self.label["text"] = f"Смена цвета голографического прицела назначена на {key}"
        else:
            self.label["text"] = f'Клавиша {key} не найдена! Добавлена новая привязка.'
            with open(config_path, 'r+', encoding='utf-8') as file:
                file.write(f'{replace_str}\n')


class HealSyringe(BaseSetting):
    def __init__(self, root, main_root, config_path):
        super().__init__(root, main_root, config_path)
        self.label.config(text="Введите клавишу для авто кравта цприцов")

    def syringe(self):
        self.entry.pack(anchor=NW, padx=6, pady=6)
        btn = ttk.Button(self.root, text="Приминить", command=self.show_message)
        btn.pack(anchor=NW, padx=6, pady=6)
        self.label.pack(anchor=NW, padx=6, pady=6)
        self.back_btn.pack(anchor=NW, padx=6, pady=6)

    def show_message(self):
        key = self.entry.get()
        search_str = f'bind {key}'
        replace_str = f'bind {key} craft.add 1079279582'
        if replace_in_large_file(self.config_path, search_str, replace_str):
            self.label["text"] = f"Авто крафт шприцов назначено: {key}"
        else:
            self.label["text"] = f"Клавиша '{key}' не найдена! Добавлена новая привязка."
            with open(config_path, 'r+', encoding='utf-8') as file:
                file.write(f'{replace_str}\n')


class Farmer:
    def __init__(self, parent):
        self.Parent = parent
        self.window = Toplevel(parent)
        self.window.title("Фермерство")
        self.window.geometry("1280x720")
        self.window.resizable(True, True)
        self.manual_farmer()

    def manual_farmer(self):
        img_1 = "image/2421719461_preview_Conditions.png"
        img_2 = "image/2421719461_preview_1.png"
        img_3 = "image/2421719461_preview_розприскувачі 4-ох.png"
        img_4 = "image/2421719461_preview_Схема.png"
        img_5 = "image/2421719461_preview_Генотип клону.png"
        img_6 = "image/2421719461_preview_гени.png"
        img_7 = "image/2421719461_preview_перший росток.png"
        img_8 = "image/2421719461_preview_другий росток.png"
        img_9 = "image/2421719461_preview_як садити.png"

        notebook = ttk.Notebook(self.window)
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="Общая информация о фермерстве")

        general_text = Text(general_frame, wrap=WORD, padx=10, pady=10)

        # for path in [img_1, img_2, img_3, img_4, img_5, img_6, img_7, img_8, img_9]:
            # img = ImageTk.PhotoImage(Image.open(path))
            # general_text.image_create(tk.END, image=img)
            # images.append(img)

        general_text.insert(tk.END,
                        f'''Основы фермерства.
На данный момент в игре можно выращивать:
    one.картофель
    two.конопля
    3.кукуруза
    4.тыква
6 видов кустов с ягодами
В процессе выращивания, каждое растение проходит 8 стадий роста. Скорость прохождения стадий зависит от условий содержания, а также и от генетики.
Какие же нужны условия: свет, вода, почва и температура. Все они указаны в таблице растения в разделе Conditions.
''')
        # general_text.image_create(tk.END, image=images[0])

        general_text.insert(END,
                            f'''\nТакже здесь есть еще одна шкала Overall.
Ее количество равно самом худшем показателю во всех шкалах.
Также выше есть шкалы на которых указаны показатели здоровья,
возраст и стадия на которой находится растение.''')

        # general_text.image_create(tk.END, image=images[one])
        general_text.insert(END,
                            f'''\nСтадии роста:
seed (очень короткая стадыя)
seedling (+- 10 мин)
sapling (+- 10 мин, на этой стадии аже можно клонировать растение)
crossbreed (сама важная стадия для клонирования, которая длится очень короткое время)
mature (можно собирать плод)
fruiting (можно собирать плод)
ripe (можно собирать плод)
dying (растение начинает умирать)
Также нужно знать, что на температуру выращивания растения мы повлиять не можем, поэтому нужно строить ферму в лесном биоме.
В игре есть одобрение, но их следует использовать только в маленьких фермах (они не подходят для скрещения, поэтому мы их не рассматриваем).
Каждому растению нужна вода. В игре есть водозборникы, но в промышленых масштабах они не эффективны, поэтому лучше всего будет использование помпы. Ее мы ставим реку (потому что там пресная вода (соленая вода нам категорически не подходит)).Мы ее подключаем к сете и отводим шланг дальше. Если вы уже поставили помпу в соленую воду, то шлангом подключаем к электрическому опреснителю (есть небольшая потеря воды и он также принимает электричество).Далее у нас есть тройники и так далее, но оно не очень необходимо, мы просто ставим помпу, а именно циркуляционный насос.Он позволяет перекрывать воду или впускать ее дальше, также он позволяет поднимать воду вверх, но для этого нужно подключить его к электричеству и дальше мы ведем в разбрызгиватель. Разбрызгиватели мы ставим на перекрестке 4-х грядок, так мы будем экономить на разбрызгивателях и воде.                            
От помпы можно подсоединить до 6-ти разбрызгивателей. В них до сих пор есть проблема с поливом, их нужно то включать, то выключать. Чтобы обойти эту историю была придумана система авто полива, которая является достаточно легкой. Как ее составить представлено на фото.
После того, как подключили схему, то нужно one раз самостоятельно полить грядки из канистры, а дальше авто полив справится сам (если почва начнет сохнуть, то поднимите немного время работы таймера).
Дальше нужно подумать о освещении. С ним все гораздо проще, мы ставим светильник над каждой грядкой, но раз в два этажа (это баг игры, который поможет нам сэкономить (на момент написания, он до сих пор существует)       
                            ''')

        general_text.config(state=DISABLED)
        general_text.pack(fill=BOTH, expand=True)

        # general_text.photo = images[0]
        # general_text.photo = images[one]

        about_frame = ttk.Frame(notebook)
        notebook.add(about_frame, text="Ягоды")

        about_text = Text(about_frame, wrap=WORD, padx=10, pady=10)
        about_text.insert(END,
                          f'''Ягоды
С ягодами все будет проще, их можно найти в лесу, их есть 6 видов:
    Желтые
    Белые
    Красные
    Зеленые
    Синие
    Черные
На данный момент черные ягоды не используются для изготовления чая, поэтому держать их нет смысла.
На смешивающих столе с ягод можно варить чаи, которые дает бафы при выпивании их. Какой самый баф и сколько времени осталось можно проверить в инвентаре.
Будьте осторожны, при смерти все бафы пропадают.
Теперь давайте обо всех бафах понемногу поговорим.
Каждый чай бывает 3-х разрядов, простой, продвинутый, чистый. Чем выше разряд, тем сильнее эффект.
Самый простой баф, это баф на хилл, он по сути такой же, как и большая аптечка. Но есть проблема, перед использованием его нужно сбить с себя радиацию, или остановить кровотечение.
Баф на увеличение количества здоровья, нужно прокачивать на максимум, время и затраты оправдываются увеличением здоровья на 20 единиц.
Баф на увеличение количества скрапа по моему мнению самый бесполезный, потому что увеличивает только количество скрапа, падающие с бочек.
А вот бафы на руды или дерево, самые классные, но прокачивать их к чистым, не лучшая идея, так как 4 чая на 60% не намного хуже чем one чай на 100%.
Баф на радиацию странный, и бесполезный, потому он подходит только для лутання сферы в сов костюме (он нужен, чтобы не видхилюватись на горе).
После этого понятно, что нужно собирать только синие, красные и желтые ягоды, а с их разведенным есть несколько проблем.Связано это с клонированием, потому что оно возможно только после 100 минут после посадки. Но оно все же возможно и в следствие этого будут портить гены друг другу.Чтобы решить проблему, нужно не клонировать ростки, а съедать ягоды, чтобы получити больше семечек. Но сажать их нужно тоже по особому, как это делать показано на фото (одинаковый цвет, это одинаковый тип семян).
А центральный слот можно засадить любимой другим растением.Затем покупаем, изучаем стол для чаеварення и варим чай.
'''
                          )
        about_text.config(state=DISABLED)
        about_text.pack(fill=BOTH, expand=True)

        over_frame = ttk.Frame(notebook)
        notebook.add(over_frame, text='Ткань')
        over_text = Text(over_frame, wrap=WORD, padx=10, pady=10)
        over_text.insert(END,
                         f'''
Основы генетики.
Теперь наши растения будут жить, теперь нужно из него делать потомство. У каждого растения есть 6-ть генов, они могут быть хорошими и плохими.
К хорошим генов относятся:
G - каждый такой ген увеличивает скорость роста.
Y - позволяет собирать больший урожай.
H - позволяет лучше выживать растению в неподходящих условиях(прекрасно подойдет для ферм в зиме или пустыни).
Плохие гены:
W - увеличивает количество воды, которая нужна растению.
X - пустой ген.
Ген попадается каждый раз разный. Вам может попасться полностью плохой ген (W-W-W-W-W-W), атк и полностью хороший (G-Y-G-H-H-Y).Если вам попался хороший ген, то его можно клонировать, для дальнейшего размножения или скрещивания. Ждем стадию, когда растение можно подобрать, эта стадия у каждого растения разная. Самая ранняя стадия, чтобы подобрать у конопли - sapling. Зажимаем кнопку E и наводимось на '' Клонировать ''. Клонов можно собрать от two-х до 5-ти (зависит это от гена Y). Генотип клона отображается в инвентаре при наведении на него курсором.
Самый лучший генотип для конопли, это генотип G-G-G-Y-Y-Y (3-G, 3-Y), порядок генов не влияет нианчто.
О'кей, как нам получити генотип 3-G, 3-Y?
Для начала висажаем все ростки которые у нас есть и смотрим, что у вас получилось. Шанс того, что вам выпадет росток, который нужен очень мал, но и такое бывает :).
Если он вам не выпал, то посмотрим, что получилось.За 50 семян у меня выпал G-G-Y-Y-Y-X, это практически идеально, от идеала нас отделяет только ген X, который нужно заменить. Для этого нам нужно дождаться, пока он перейдет в фазу sapling и сделать клон.
Давайте разберёмся, как нужно скрещивать растения.
Принцип у всех растений здесь один. Как только сажанець доходит до стадии crossbreed, он принимает самые сильные гены у соседей.
Дальше нам нужно разобраться, как гены влияют друг на друга.
Первое, что нам нужно знать, это то, что первый ген, влияет только на первый.Гены из разных слотов, не влияют друг на друга.Таким образом, чтобы поменять последний ген, нужно найти росток из желаемым последним геном. В нашем случае нам нужно заменить ген X на G. Так что давайте найдем парочку ростков с G на конце. У меня есть много ростков в сундуке, так что я уже подобрал неплохие варианти.
Тепер я выпишу все гены в столбик, но перед началом договоримся, что в красного гена является 100 силы, а в зеленой лишь 60.
Это так только в фотошопе, давайте сделаем это в игре и посмотрим, что получится.Сначала посередине сажаем наш основной росток. Ждем, пока он дойдет до стадии sapling (на это уйдет не более 10 минут). Когда стадия sapling уже идет, сажаем по соседству наши другие клоны и ждем еще минут 5 пока не начнется скрещивание.
До:
После:
Ждем пока закинчеться стадия скрещивание, после того можем собирать ростки и рассаживать снова, чтобы собрать достаточное количество чтобы рассадить ее повсюду.Но это даже не десятая часть того, что необходимо знать о схрещння.
        '''
                         )

        over_text.config(state=DISABLED)
        over_text.pack(fill=BOTH, expand=True)

        notebook.pack(fill=BOTH, expand=True, padx=5, pady=5)
        close_btn = ttk.Button(self.window, text="Закрыть", command=self.window.destroy)
        close_btn.pack(pady=10)


if __name__ == "__main__":
    config_path = AppConfig.get_config_path()
    app = Screen(400, 200, config_path)
    app.main_screen()
