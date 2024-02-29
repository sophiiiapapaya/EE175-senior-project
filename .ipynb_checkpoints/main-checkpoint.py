# main.py
import GUI
import server
import client

if __name__ == '__main__':
    #  execute the code in GUI.py as if it were written in the main.py file.
    with open("GUI.py") as gui:
        exec(gui.read())