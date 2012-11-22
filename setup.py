from distutils.core import setup
import py2exe
import sys
import matplotlib

sys.path.append("C:\\Users\\rehlers\\Documents\\GitHub\\Geiger-Counter\\dist\\Microsoft.VC90.CRT")

setup(data_files=matplotlib.get_py2exe_datafiles(),windows=["C:\\Users\\rehlers\\Documents\\GitHub\\Geiger-Counter\\GUI.py"])