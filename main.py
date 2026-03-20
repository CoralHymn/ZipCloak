#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ZipCloak 主入口"""
import os
import sys
import tkinter as tk
from gui import ZipCloakGUI


def main():
    root = tk.Tk()
    app = ZipCloakGUI(root)
    root.mainloop()


if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))
    main()