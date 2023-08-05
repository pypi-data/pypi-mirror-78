from PyQt5 import QtCore, QtGui, QtWidgets, sip
from PyQt5.QtCore import Qt

from pandasgui import show
from pandasgui.widgets.dataframe_viewer import DataFrameViewer
from pandasgui.widgets.dataframe_explorer import DataFrameExplorer
from pandasgui.datasets import mpg, mi_manufacturing

app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

s_float = mpg['acceleration']
s_obj = mpg['acceleration']
s_int = mpg['acceleration']

test_data_list = [mpg, mi_manufacturing, s_float, s_obj, s_int]

for test_data in test_data_list:
    dfv = DataFrameViewer(test_data)
    dfv.pgdf.sort_column(0)

    dfe = DataFrameExplorer(test_data)
    dfe.pgdf.sort_column(0)
