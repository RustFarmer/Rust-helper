
def buffer(text: str):
    # -*- coding: utf-8 -*-
    import subprocess
    import sys
    if sys.platform == 'darwin':  # macOS
        subprocess.run('pbcopy', universal_newlines=True, input=text)
    elif sys.platform == 'win32':  # Windows
        subprocess.run('clip', universal_newlines=True, input=text)
    else:
        try:
            subprocess.run(['xclip', '-selection', 'c'], input=text.encode('utf-8'))
        except FileNotFoundError:
            print("Установите xclip для работы с буфером обмена (sudo apt install xclip)")
