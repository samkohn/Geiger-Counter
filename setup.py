from distutils.core import setup
import py2exe
import matplotlib

setup(data_files=matplotlib.get_py2exe_datafiles(),windows=["C:\\Users\\rehlers\\Documents\\GitHub\\Geiger-Counter\\GUI.py"])