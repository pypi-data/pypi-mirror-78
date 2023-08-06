#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'xiaobaiauto2Help.py'
__create_time__ = '2020/7/22 20:10'

from tkinter import *
from tkinter.ttk import Notebook
from xiaobaiauto2.config.config import TIMERCONFIG
from xiaobaiauto2.utils.help_ui import HELP_UI

_timer = TIMERCONFIG()
_help_ui = HELP_UI()

root = Tk()
root.geometry('800x600')
root.title('小白自动化工具箱 v0.1')
root.iconbitmap(_timer.timerpath)

tab = Notebook(root)
case_frame = Frame(master=tab)
timer_frame = Frame(master=tab)
option_frame = Frame(master=tab)
tab.add(case_frame, text='用例编辑')
tab.add(timer_frame, text='环境监测')
tab.add(option_frame, text='数据配置')
tab.pack(expand=True, fill=BOTH)

# HELP_UI(master=case_frame)
_help_ui.edit_case_ui(case_frame)

root.mainloop()