from tkinter import *
import motor


class MainWindow:
    def __init__(self, is_debug, motor_ctrl):
        self.window = Tk()

        self.motor_ctrl = motor_ctrl

        if not is_debug:
            self.window.title("machine control")
        else:
            self.window.title("machine control-test/debug mode")

        self.window.mainloop()
