# -*- coding: utf-8 -*-
"""
Python logic for taxiway forms - whe taxiway is created or modified.
"""
from qgis.PyQt.QtWidgets import QWidget, QMessageBox, QDialogButtonBox

err_msg = ''
is_wrong_input = False
taxiway_dialog = None
# le - QLineEdit
le_icao = None
le_name = None
le_width = None
btn_box = None
lyr_airports = None  # View airports
airport_id = None
le_airport_id = None
le_airport_short_name = None
cb_width_uom = None
cb_surface = None
my_dialog = None


def custom_taxiway_form_open(dialog, layer, feature):
	global my_dialog
	global le_icao
	global le_name
	global le_width
	global btn_box
	global taxiway_dialog
	global lyr_airports
	global le_airport_id
	global cb_width_uom
	global cb_surface
	global le_airport_short_name
	taxiway_dialog = dialog

	le_icao = dialog.findChild(QWidget, "icao")
	le_name = dialog.findChild(QWidget, "taxiway_name")
	le_width = dialog.findChild(QWidget, "width")
	cb_width_uom = dialog.findChild(QWidget, "width_uom")
	cb_surface = dialog.findChild(QWidget, "surface")
	le_airport_id = dialog.findChild(QWidget, "airport_id")
	le_airport_short_name = dialog.findChild(QWidget, "short_name")
	btn_box = dialog.findChild(QWidget, "buttonBox")
	btn_ok = btn_box.button(QDialogButtonBox.Ok)

	btn_box.blockSignals(True)
	btn_ok.clicked.connect(check_taxiway_input)
	cb_width_uom.setCurrentIndex(0)
	cb_surface.setCurrentIndex(0)
	# Get access to Airports PostGIS view
	lyr_airports = QgsProject.instance().mapLayersByName('airports')[0]
	if le_airport_id.text():
		lyr_airports.selectByExpression("\"wpt_id\" = {}".format(int(le_airport_id.text())))
		airport = lyr_airports.selectedFeatures()[0]
		icao = airport["wpt_ident"]
		short_name = airport["short_name"]
		le_icao.setText(icao)
		le_airport_short_name.setText(short_name)
	le_icao.textChanged.connect(get_waypoint_id_by_icao)


def get_waypoint_id_by_icao():
	""" Gets waypoint_id based on airport ICAO code
	:return:
	"""
	global airport_id
	icao = le_icao.text()
	if len(icao) == 4:
		lyr_airports.selectByExpression("\"wpt_ident\" = '{}'".format(icao))
		if len(lyr_airports.selectedFeatures()) == 1:
			airport = lyr_airports.selectedFeatures()[0]
			airport_id = airport["wpt_id"]
			short_name = airport["short_name"]
			le_airport_id.setText(str(airport_id))
			le_airport_short_name.setText(short_name)
		else:
			le_airport_id.clear()
			le_airport_short_name.clear()
			airport_id = None
			msg_box = QMessageBox()
			msg_box.setText("Airport {} not found".format(icao))
			msg_box.exec_()


def check_icao_code(icao):
	"""	Checks if ICAO code is not empty and exist in database.
	:param icao: str, value taken from icao QLineEdit """
	global err_msg
	global is_wrong_input
	if not icao:
		err_msg += 'Airport is required\n'
		is_wrong_input = True
	elif len(icao) < 4:
		err_msg += 'Enter airport ICAO code: 4 characters\n'
		is_wrong_input = True


def check_name(name):
	""" Checks if taxiway name is not empty and is unique for given airport.
	:param name: str, value taken from taxiway_name QLineEdit """
	global err_msg
	global is_wrong_input
	if not name:
		err_msg += 'Taxiway name is required.\n'
		is_wrong_input = True


def check_iaco_code_and_name(icao, name):
	""" Checks if taxiway name is unique for given airport.
	:param icao: str, value taken from icao QLineEdit
	:param name: str, taxiway_name QLineEdit """
	global err_msg
	global is_wrong_input
	lyr_airports.selectByExpression("\"wpt_ident\" = '{}'".format(icao))
	if len(lyr_airports.selectedFeatures()) == 1:
		airport = lyr_airports.selectedFeatures()[0]
		airport_id = airport["wpt_id"]
		lyr_taxiway = QgsProject.instance().mapLayersByName('Taxiway')[0]
		lyr_taxiway.selectByExpression("\"airport_id\" = {} AND \"taxiway_name\" = '{}'".format(airport_id,
																								 name))
		taxiway_count = len(lyr_taxiway.selectedFeatures())
		if taxiway_count > 0:
			err_msg += 'Exists taxiway {} fro airport {}.\n'.format(name, icao)
			is_wrong_input = True
			lyr_taxiway.removeSelection()


def check_width(width):
	""" Checks if taxiway width is a positive float number.
	:param width: str, value taken from width QLineEdit """
	global err_msg
	global is_wrong_input
	try:
		w = float(width)
		if w <= 0:
			err_msg += 'Width must be a positive number.\n'
			is_wrong_input = True
	except ValueError:
		err_msg += 'Width must be a positive number.\n'
		is_wrong_input = True


def check_taxiway_input():
	""" Checks input taxiway and saves into database if is ok or show message witch attributes are required/wrong
	inserted into attribute dialog.	"""
	global err_msg
	global is_wrong_input
	err_msg = ''
	is_wrong_input = False

	if len(le_icao.text()) == 4 and not airport_id:
		is_wrong_input = False
		err_msg += 'Enter valid ICAO airport code.\n'
	else:
		check_icao_code(le_icao.text())
	check_name(le_name.text())
	check_width(le_width.text())
	check_iaco_code_and_name(le_icao.text(), le_name.text())

	if is_wrong_input:
		msg_box = QMessageBox()
		msg_box.setText(err_msg)
		msg_box.exec_()
	else:
		taxiway_dialog.parent().accept()
