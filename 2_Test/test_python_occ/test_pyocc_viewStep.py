# -*- coding: utf-8 -*-

import os

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"


# ============================================================
# 1. Patch PyQt5 QMainWindow.move()
#    解决 pythonocc 7.5.1 SimpleGui.py 中传入 float 的问题
# ============================================================

from PyQt5.QtWidgets import QMainWindow


_original_move = QMainWindow.move


def move_fixed(self, *args):
    """
    pythonocc 7.5.1 的 SimpleGui.centerOnScreen()
    会调用：

        self.move(x, y)

    其中 x/y 是 float。

    Qt 5.12.9 要求 int，因此这里统一转换。
    """

    if len(args) == 2:
        x, y = args
        return _original_move(self, int(x), int(y))

    elif len(args) == 1:
        # 如果传入 QPoint，则保持原行为
        return _original_move(self, args[0])

    return _original_move(self, *args)


QMainWindow.move = move_fixed


# ============================================================
# 2. STEP 文件解析
# ============================================================

from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.TopologyUtils import TopologyExplorer


step_path = r"Data\01124_index_2.step"

shape = read_step_file(
    step_path,
    as_compound=True
)

topo = TopologyExplorer(shape)

solids = list(topo.solids())
shells = list(topo.shells())
faces = list(topo.faces())


print("======================")
print("OCC STEP")
print("======================")
print("Solid 数量:", len(solids))
print("Shell 数量:", len(shells))
print("Face 数量:", len(faces))
print("======================")

# ============================================================
# 4. 启动 pythonOCC Viewer
# ============================================================

from OCC.Display.SimpleGui import init_display


display, start_display, add_menu, add_function_to_menu = (
    init_display()
)


display.DisplayShape(
    shape,
    update=True
)


display.FitAll()

start_display()