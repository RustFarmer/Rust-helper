import json
import os


def find_setting(data, target_key, depth=0):
        indent = "  " * depth
        if isinstance(data, dict):
            if target_key in data:
                return data[target_key]

            for key, value in data.items():
                result = find_setting(value, target_key, depth + 1)
                if result is not None:
                    return result

        elif isinstance(data, list):
            for i, item in enumerate(data):
                result = find_setting(item, target_key, depth + 1)
                if result is not None:
                    return result
        return None


with open("system.json", 'r', encoding='utf-8') as x:
    data = json.load(x)
    KEYS_FILE = find_setting(data, "keys.cfg")
    SETTINGS_FILE = find_setting(data, "client.cfg")


def load_json_keys(filename):
    encodings = ['utf-8', 'cp1251', 'latin-1', 'iso-8859-1', 'windows-1252']

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                data = json.load(file)
            return list(data.keys())
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Ошибка загрузки JSON: {e}")
            return []
    messagebox.showerror("Ошибка", "Не удалось определить кодировку файла")
    return []


def replace_in_large_file(filename, search_str, replace_str):
    temp_file = filename + ".tmp"
    replaced = False
    with open(filename, 'r') as fin, open(temp_file, 'w') as fout:
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
        return False


class Save:
    @staticmethod
    def save_settings_user():
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as fiLe:
            __file = fiLe.read()
            print(__file)
            print("Good", __file)
        with open('save_clients_user_file.txt', 'w', encoding='utf-8') as file:
            file.write(__file)

    @staticmethod
    def save_keys_settings():
        with open(KEYS_FILE, 'r', encoding='utf-8') as file:
            _file = file.read()
            with open(_file, 'r', encoding='utf-8') as file:
                __file = file.read()
                print('Good', __file)
            print('very good', _file)
        with open('save_keys_settings.txt', 'a', encoding='utf-8') as file:
            file.write(__file)


def uses_save_file():
    with open(SETTINGS_FILE, 'w+', encoding='utf-8') as x:
        print(type(x), "jjff__---vjfufm103")
        print(x.read(), "\khgophej3u-t=30uvy0934=09utwejd9i")
        print(SETTINGS_FILE, "------====-=-4=5-083=4-67430")
        with open('save_clients_user_file.txt', 'r', encoding='utf-8') as file:
            data = file.read()
            x.write
            old_settings_file = x.read()
            print(type(old_settings_file))
            # old_settings_file.write(data)
            print(old_settings_file, "dkgh[oe9v043-9vrgk")

        # except FileNotFoundError:
        #   showerror('Файл не найден', 'файл не найден с путем к файлах: client.cfg или keys.cfg')


def change_key_in_json(
        file_path: str,
        old_key: str,
        new_key: str,
        replace_all: bool = True,
        backup: bool = False
) -> bool:
    import json
    from typing import Any, Union
    """
    Рекурсивно изменяет ключ в JSON файле на всех уровнях вложенности.

    :param file_path: Путь к JSON файлу
    :param old_key: Ключ, который нужно заменить
    :param new_key: Новый ключ
    :param replace_all: Если True, заменяет все вхождения, иначе только первое
    :param backup: Если True, создает резервную копию файла перед изменением
    :return: True если изменения были внесены, иначе False
    """

    def recursive_replace(obj: Any, found: bool = False) -> tuple[Any, bool]:
        """
        Рекурсивно обходит структуру данных и заменяет ключи.

        :param obj: Объект для обработки
        :param found: Флаг, указывающий, было ли уже найдено и заменено вхождение (для replace_all=False)
        :return: Кортеж (обработанный объект, флаг указывающий было ли сделано изменение)
        """
        changed = False

        if isinstance(obj, dict):
            new_dict = {}
            for key, value in obj.items():
                current_key = key
                key_changed = False

                # Заменяем ключ, если он совпадает с искомым
                if key == old_key and (replace_all or not found):
                    current_key = new_key
                    key_changed = True
                    changed = True

                # Рекурсивно обрабатываем значение
                processed_value, value_changed = recursive_replace(
                    value, found or (key_changed and not replace_all)
                )

                new_dict[current_key] = processed_value
                changed = changed or value_changed

            return new_dict, changed

        elif isinstance(obj, list):
            new_list = []
            list_changed = False
            for item in obj:
                processed_item, item_changed = recursive_replace(item, found)
                new_list.append(processed_item)
                list_changed = list_changed or item_changed
            return new_list, list_changed

        else:
            # Для простых типов возвращаем как есть
            return obj, False

    try:
        # Создание резервной копии при необходимости
        if backup:
            import shutil
            backup_path = f"{file_path}.backup"
            shutil.copy2(file_path, backup_path)
            print(f"Создана резервная копия: {backup_path}")

        # Чтение данных из файла
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Рекурсивная замена ключей
        updated_data, changes_made = recursive_replace(data)

        if changes_made:
            # Запись обновленных данных в файл
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(updated_data, file, ensure_ascii=False, indent=4)

            action = "все" if replace_all else "первое"
            print(f"Успешно заменено {action} вхождение ключа '{old_key}' на '{new_key}'.")
            return True
        else:
            print(f"Ключ '{old_key}' не найден в файле.")
            return False

    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
        return False
    except json.JSONDecodeError:
        print("Ошибка декодирования JSON. Проверьте формат файла.")
        return False
    except PermissionError:
        print(f"Нет прав для записи в файл '{file_path}'.")
        return False
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {str(e)}")
        return False


import json
from typing import Any, Union, Dict, List


def modify_all_key_values(file_path: str, key_name: str, new_value: Any):
    """
    Изменяет значения всех ключей с указанным названием в JSON файле.

    :param file_path: путь к JSON файлу
    :param key_name: название ключа, значения которого нужно изменить
    :param new_value: новое значение для всех найденных ключей
    """
    # Чтение данных из файла
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Рекурсивная функция для поиска и изменения значений
    def modify_key_values_recursive(obj: Union[Dict, List], target_key: str, value: Any):
        if isinstance(obj, dict):
            for key in obj:
                if key == target_key:
                    obj[key] = value
                else:
                    modify_key_values_recursive(obj[key], target_key, value)
        elif isinstance(obj, list):
            for item in obj:
                modify_key_values_recursive(item, target_key, value)

    # Применяем изменения
    modify_key_values_recursive(data, key_name, new_value)

    # Запись обратно в файл
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


