import cx_Freeze
from cx_Freeze import *
"""
cx_Freeze.setup(
    name = "SSBS",
    options ={"build_exe":{"packages":["pygame"]}},
    executables = [Executable("game.py")]
)"""

exe = [cx_Freeze.Executable("game.py", base = "Win32GUI" , icon = "resource/image/icon.ico",targetName="55135.exe")]

cx_Freeze.setup(
    name = "55135",
    version = "1.0",
    options = {"build_exe": {"packages": ["pygame"]}},
    executables = exe
)

