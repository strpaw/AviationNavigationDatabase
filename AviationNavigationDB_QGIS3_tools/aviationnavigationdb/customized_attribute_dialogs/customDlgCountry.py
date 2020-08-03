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


def open_ais_www():
	""" Open AIS webpage in default web browser. """
	global ais_www
	if ais_www and ais_www != 'NULL':
		webbrowser.open(ais_www)


def check_country_attributes(dialog, layer, feature):
	global ais_www
	le_ais_www = dialog.findChild(QWidget, "ais_www")
	btn_open_www = dialog.findChild(QWidget, "pushButtonOpenWWW")
	btn_open_www.clicked.connect(open_ais_www)

	ais_www = le_ais_www.text()
	if ais_www and ais_www != 'NULL':
		btn_open_www.setEnabled(True)
	else:
		btn_open_www.setEnabled(False)
