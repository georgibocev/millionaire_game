import tkinter as tk
from module.modules.millionaire_gui import MillionaireGUI


def main():
    root = tk.Tk()
    MillionaireGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()