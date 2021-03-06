# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AviationNavigationDBDialog
                                 A QGIS plugin
 Tools for dealing with aviation data in PostGIS
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-05-19
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Paweł Strzelewicz
        email                : @
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox, QDialog, QFileDialog
from qgis.core import *
from qgis.gui import *
import psycopg2
from aviationnavigationdb.aviation_navdb_libs.eaip_data_extraction.etod_parser import *
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'obstacle_dialog_base.ui'))


class ObstacleDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(ObstacleDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.iface = iface

        try:
            self.lyr_obstacle = QgsProject.instance().mapLayersByName('obstacle')[0]
            self.iface.setActiveLayer(self.lyr_obstacle)
        except IndexError:
            pass

        self.comboBoxObstInsertMethod.currentIndexChanged.connect(self.change_obstacle_insert_method)
        self.pushButtonSelecteTODFile.clicked.connect(self.select_etod_file)
        self.pushButtonImporteTOD.clicked.connect(self.import_etod)

    def change_obstacle_insert_method(self):
        self.stackedWidgetObstInsertMethod.setCurrentIndex(self.comboBoxObstInsertMethod.currentIndex())

    def select_etod_file(self):
        etod_file = QFileDialog.getOpenFileName(self, "Select eTOD file", "", '(*.csv *.dat)')[0]
        if etod_file:
            self.lineEditeTODFile.setText(etod_file)

    def get_ctry_id(self, country):
        lyr_countries = QgsProject.instance().mapLayersByName('Countries')[0]
        countries_provider = lyr_countries.dataProvider()
        if countries_provider.name() == 'postgres':
            uri = QgsDataSourceUri(countries_provider.dataSourceUri())

            query = """SELECT
                        ctry_id
                       FROM
                        country
                       WHERE short_name = '{}';""".format(country)
            conn = psycopg2.connect(host=uri.host(),
                                    database=uri.database(),
                                    user=uri.username(),
                                    password=uri.password())
            cur = conn.cursor()
            cur.execute(query)
            records = cur.fetchall()
            cur.close()
            conn.commit()
            return int(records[0][0])

    def get_obst_type_map(self):
        """ Gets map between obst_type and obst_type_id from obstacle_type table.
        :return:
        """
        obst_type_map = {}
        provider = self.lyr_obstacle.dataProvider()
        if provider.name() == 'postgres':
            uri = QgsDataSourceUri(provider.dataSourceUri())

            query = """SELECT
                        obst_type,
                        obst_type_id
                       FROM
                        obstacle_type;"""
            conn = psycopg2.connect(host=uri.host(),
                                    database=uri.database(),
                                    user=uri.username(),
                                    password=uri.password())
            cur = conn.cursor()
            cur.execute(query)
            records = cur.fetchall()
            cur.close()
            conn.commit()

            for record in records:
                obst_type_map[record[0]] = record[1]
            return obst_type_map

    def import_etod(self):
        self.iface.setActiveLayer(self.lyr_obstacle)
        etod_file = self.lineEditeTODFile.text().strip()
        if etod_file:
            if os.path.isfile(etod_file):
                country = self.comboBoxeTODCountry.currentText()
                provider = self.lyr_obstacle.dataProvider()
                feat = QgsFeature()
                feat.setFields(self.lyr_obstacle.fields())
                
                etod = EtodParser(country, etod_file)
                etod.init_parser(self.get_ctry_id(country))
                etod.obst_type_map = self.get_obst_type_map()
                if etod.file_format == 'CSV':
                    delimiter = etod_map[etod.ctry_short_name]['csv_delimiter']

                    with open(etod.etod_file, 'r', errors='ignore') as data_file:
                        reader = csv.DictReader(data_file, delimiter=delimiter)
                        for row in reader:
                            etod.parse_csv_row(row)
                            is_valid = etod.validate_obstacle_data()
                            if is_valid:
                                feat.setAttribute('obst_id', provider.defaultValue(0))
                                feat.setAttribute('ctry_id', etod.obstacle_data['ctry_id'])
                                feat.setAttribute('obst_identifier', etod.obstacle_data['obst_identifier'])
                                feat.setAttribute('obst_name', etod.obstacle_data['obst_name'])
                                feat.setAttribute('lon_src', etod.obstacle_data['lon_src'])
                                feat.setAttribute('lat_src', etod.obstacle_data['lat_src'])
                                feat.setAttribute('agl', float(etod.obstacle_data['agl']))
                                feat.setAttribute('amsl', float(etod.obstacle_data['amsl']))
                                feat.setAttribute('vert_uom', etod.obstacle_data['vert_uom'])
                                feat.setAttribute('hor_acc', etod.obstacle_data['hor_acc'])
                                feat.setAttribute('hor_acc_uom', etod.obstacle_data['hor_acc_uom'])
                                feat.setAttribute('vert_acc', etod.obstacle_data['vert_acc'])
                                feat.setAttribute('vert_acc_uom', etod.obstacle_data['vert_acc_uom'])
                                feat.setAttribute('obst_type_id', etod.obstacle_data['obst_type_id'])
                                feat.setAttribute('lighting', etod.obstacle_data['lighting'])
                                feat.setAttribute('marking', etod.obstacle_data['marking'])
                                feat.setAttribute('is_group', etod.obstacle_data['is_group'])
                                feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(etod.obstacle_data['lon_dd'],
                                                                                    etod.obstacle_data['lat_dd'])))
                                provider.addFeature(feat)
                                self.lyr_obstacle.commitChanges()
                        QMessageBox.information(QWidget(), "Message", 'Import completed')

                elif etod.file_format == 'DAT':
                    line_nr = 0
                    with open(etod.etod_file, 'r', errors='ignore') as data_file:
                        for row in data_file:
                            line_nr += 1
                            if line_nr < 5:
                                continue
                            else:
                                etod.parse_dat_row(row)
                                is_valid = etod.validate_obstacle_data()
                                if is_valid:
                                    feat.setAttribute('obst_id', provider.defaultValue(0))
                                    feat.setAttribute('ctry_id', etod.obstacle_data['ctry_id'])
                                    feat.setAttribute('obst_identifier', etod.obstacle_data['obst_identifier'])
                                    feat.setAttribute('obst_name', etod.obstacle_data['obst_name'])
                                    feat.setAttribute('lon_src', etod.obstacle_data['lon_src'])
                                    feat.setAttribute('lat_src', etod.obstacle_data['lat_src'])
                                    feat.setAttribute('agl', float(etod.obstacle_data['agl']))
                                    feat.setAttribute('amsl', float(etod.obstacle_data['amsl']))
                                    feat.setAttribute('vert_uom', etod.obstacle_data['vert_uom'])
                                    feat.setAttribute('hor_acc', etod.obstacle_data['hor_acc'])
                                    feat.setAttribute('hor_acc_uom', etod.obstacle_data['hor_acc_uom'])
                                    feat.setAttribute('vert_acc', etod.obstacle_data['vert_acc'])
                                    feat.setAttribute('vert_acc_uom', etod.obstacle_data['vert_acc_uom'])
                                    feat.setAttribute('obst_type_id', etod.obstacle_data['obst_type_id'])
                                    feat.setAttribute('lighting', etod.obstacle_data['lighting'])
                                    feat.setAttribute('marking', etod.obstacle_data['marking'])
                                    feat.setAttribute('is_group', etod.obstacle_data['is_group'])
                                    feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(etod.obstacle_data['lon_dd'],
                                                                                        etod.obstacle_data['lat_dd'])))
                                    provider.addFeature(feat)
                                    self.lyr_obstacle.commitChanges()
                        QMessageBox.information(QWidget(), "Message", 'Import completed')


            else:
                QMessageBox.critical(QWidget(), "Message", '{} is not a file!'.format(etod_file))
        else:
            QMessageBox.critical(QWidget(), "Message", 'Select eTOD data file!')