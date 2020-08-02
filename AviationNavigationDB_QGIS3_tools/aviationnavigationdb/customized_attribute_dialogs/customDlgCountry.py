# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget
import webbrowser
ais_www = None
leAISWWW = None
btnOpenWWW = None


def open_ais_www():
	""" Open AIS webpage in default browser """
	if ais_www and ais_www != 'NULL':
		webbrowser.open(ais_www)


def my_form_open(dialog, layer, feature):
	global ais_www
	global leAISWWW
	global btnOpenWWW
	leAISWWW = dialog.findChild(QWidget, "ais_www")
	btnOpenWWW = dialog.findChild(QWidget, "pushButtonOpenWWW")
	btnOpenWWW.clicked.connect(open_ais_www)

	ais_www = leAISWWW.text()
	if ais_www and ais_www != 'NULL':
		btnOpenWWW.setEnabled(True)
	else:
		btnOpenWWW.setEnabled(False)
