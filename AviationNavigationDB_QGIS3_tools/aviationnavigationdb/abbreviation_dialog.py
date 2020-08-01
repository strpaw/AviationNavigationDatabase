# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AviationNavigationDBDialog
                                 A QGIS plugin
 Tools for dealing with aviation data in PostGIS
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-06-11
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
from PyQt5.QtWidgets import QWidget, QMessageBox, QDialog, QFileDialog, QTableWidgetItem
from qgis.core import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'abbreviation_dialog.ui'))


class AbbreviationDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(AbbreviationDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.table_name = 'abbreviation'
        self.pushButtonInsert.clicked.connect(self.insert_abbreviation)
        self.pushButtonUpdate.clicked.connect(self.update_abbreviation)
        self.lineEditAbbrev.textChanged.connect(self.set_background_abbrev_white)
        self.plainTextEditTerm.textChanged.connect(self.set_background_term_white)
        self.pushButtonFindByAbbrev.clicked.connect(self.get_abbreviations_by_abbrev)
        self.pushButtonFinByTerm.clicked.connect(self.get_abbreviations_by_term)
        self.tableWidgetFetchedAbbreviations.itemClicked.connect(self.get_abbreviation_details)

    def set_background_abbrev_white(self):
        """ Sets background for abbreviation input field white. """
        self.lineEditAbbrev.setStyleSheet("QLineEdit {background-color: white}")

    def set_background_term_white(self):
        """ Sets background for term input field white. """
        self.plainTextEditTerm.setStyleSheet("QPlainTextEdit {background-color: white}")

    def validate_input(self):
        """ Checks if abbreviation and term meets required values. """
        err_msg = ''
        if self.lineEditAbbrev.text().strip() == '':
            self.lineEditAbbrev.setStyleSheet("QLineEdit {background-color: red}")
            err_msg += 'Abbreviation is required.\n'
        elif len(self.lineEditAbbrev.text()) > 20:
            self.lineEditAbbrev.setStyleSheet("QLineEdit {background-color: red}")
            err_msg += 'Abbreviation is too long. Max 20 characters.\n'

        if self.plainTextEditTerm.toPlainText().strip() == '':
            self.plainTextEditTerm.setStyleSheet("QPlainTextEdit {background-color: red}")
            err_msg += 'Term is required.\n'
        elif len(self.plainTextEditTerm.toPlainText()) > 300:
            self.plainTextEditTerm.setStyleSheet("QPlainTextEdit {background-color: red}")
            err_msg += 'Term is to long. Max 300 characters.\n'

        if err_msg:
            QMessageBox.critical(QWidget(), "Message", err_msg)
            return False
        return True

    def insert_abbreviation(self):
        """ Insert abbreviation data into database. """
        if self.validate_input():
            layer = QgsProject.instance().mapLayersByName(self.table_name)[0]
            feat = QgsFeature(layer.fields())
            feat.setAttribute('abbrev', self.lineEditAbbrev.text())
            feat.setAttribute('term', self.plainTextEditTerm.toPlainText())
            layer.dataProvider().addFeatures([feat])
            layer.commitChanges()
            self.pushButtonUpdate.setEnabled(True)

    def update_abbreviation(self):
        """ Updates selected abbreviation. """
        if self.validate_input():
            any_changes = False
            layer = QgsProject.instance().mapLayersByName(self.table_name)[0]
            query = "abbr_id = {}".format(int(self.lineEditAbbrevId.text()))
            layer.selectByExpression(query)
            feat_id = layer.selectedFeatures()[0][0]
            feat = layer.selectedFeatures()[0]
            attrs = feat.attributes()
            feat.setAttribute('term', self.plainTextEditTerm.toPlainText())

            current_values = {
                1: attrs[1],
                2: attrs[2]
            }

            new_values = {
                1: self.lineEditAbbrev.text(),
                2: self.plainTextEditTerm.toPlainText()
            }

            for attr in new_values:
                if current_values[attr] != new_values[attr]:
                    any_changes = True
                    break

            if any_changes:
                layer.dataProvider().changeAttributeValues({feat_id: new_values})
                layer.commitChanges()
            else:
                QMessageBox.information(QWidget(), "Message", 'No changes!')

    def get_abbreviations(self, feats):
        self.tableWidgetFetchedAbbreviations.clearContents()
        self.tableWidgetFetchedAbbreviations.setRowCount(0)
        if len(feats) == 0:
            self.pushButtonUpdate.setEnabled(False)
            self.lineEditAbbrevId.setText("")
            QMessageBox.information(QWidget(), "Message", 'Nothing found!')
        elif len(feats) == 1:  # Fill in lineEditAbbrev and plainTextEditTerm
            attr = feats[0].attributes()
            self.lineEditAbbrev.setText(attr[1])
            self.plainTextEditTerm.clear()
            self.plainTextEditTerm.appendPlainText(attr[2])
            self.pushButtonUpdate.setEnabled(True)
        else:
            for feat in feats:
                attr = feat.attributes()
                row_pos = self.tableWidgetFetchedAbbreviations.rowCount()
                self.tableWidgetFetchedAbbreviations.insertRow(row_pos)
                self.tableWidgetFetchedAbbreviations.setItem(row_pos, 0, QTableWidgetItem(str(attr[0])))
                self.tableWidgetFetchedAbbreviations.setItem(row_pos, 1, QTableWidgetItem(attr[1]))
                self.tableWidgetFetchedAbbreviations.setItem(row_pos, 2, QTableWidgetItem(attr[2]))

    def get_abbreviation_details(self):
        """ Fills in selected abbreviation data from list. """
        index = self.tableWidgetFetchedAbbreviations.currentIndex().row()
        self.lineEditAbbrevId.setText(self.tableWidgetFetchedAbbreviations.item(index, 0).text())
        self.lineEditAbbrev.setText(self.tableWidgetFetchedAbbreviations.item(index, 1).text())
        self.plainTextEditTerm.clear()
        self.plainTextEditTerm.appendPlainText(self.tableWidgetFetchedAbbreviations.item(index, 2).text())
        self.pushButtonUpdate.setEnabled(True)

    def get_abbreviations_by_abbrev(self):
        """ Finds abbreviations from database based on abbreviation. """
        self.plainTextEditTerm.clear()
        pattern = self.lineEditAbbrev.text().strip()
        if pattern:
            if '%' or '_' in pattern:
                query = "abbrev LIKE '{}'".format(pattern)
            else:
                query = "abbrev = '{}'".format(pattern)

            layer = QgsProject.instance().mapLayersByName(self.table_name)[0]
            layer.selectByExpression(query)
            feats = layer.selectedFeatures()
            self.get_abbreviations(feats)
        else:
            self.lineEditAbbrev.setStyleSheet("QLineEdit {background-color: red}")
            QMessageBox.critical(QWidget(), "Message", 'Enter abbreviation or acronym!')

    def get_abbreviations_by_term(self):
        """ Finds abbreviations from database based on term. """
        self.lineEditAbbrev.setText("")
        pattern = self.plainTextEditTerm.toPlainText().strip()
        if pattern:
            if '%' or '_' in pattern:
                query = "term LIKE '{}'".format(pattern)
            else:
                query = "term = '{}'".format(pattern)

            layer = QgsProject.instance().mapLayersByName(self.table_name)[0]
            layer.selectByExpression(query)
            feats = layer.selectedFeatures()
            self.get_abbreviations(feats)
        else:
            self.plainTextEditTerm.setStyleSheet("QPlainTextEdit {background-color: red}")
            QMessageBox.critical(QWidget(), "Message", 'Enter part or full term!')
