"""
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland

This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
"""
import os
import copy

from PySide2.QtWidgets import QDialog, QAbstractItemView, QTableWidgetItem
from PySide2.QtCore import Qt
from PySide2.QtCore import QThread, Signal

from mapclientplugins.fieldworkhostmeshfittingstep.ui_mayavihostmeshfittingviewerwidget import Ui_Dialog
from traits.api import on_trait_change

from gias2.mappluginutils.mayaviviewer import MayaviViewerObjectsContainer, MayaviViewerDataPoints, \
    MayaviViewerFieldworkModel, colours

os.environ['ETS_TOOLKIT'] = 'qt'


class _ExecThread(QThread):
    update = Signal(tuple)

    def __init__(self, func):
        QThread.__init__(self)
        self.func = func

    def run(self):
        output = self.func()
        self.update.emit(output)


class MayaviHostMeshFittingViewerWidget(QDialog):
    """
    Configure dialog to present the user with the options to configure this step.
    """
    defaultColor = colours['bone']
    objectTableHeaderColumns = {'visible': 0, 'type': 1}
    backgroundColour = (0.0, 0.0, 0.0)
    _dataRenderArgs = {'mode': 'point', 'scale_factor': 0.1, 'color': (0, 1, 0)}
    _slaveGFUnfittedRenderArgs = {'color': (1, 0, 0)}
    _slaveGFFittedRenderArgs = {'color': (1, 1, 0)}
    _hostGFUnfittedRenderArgs = {'color': (1, 0, 0)}
    _hostGFFittedRenderArgs = {'color': (1, 1, 0)}
    _GFD = [15, 15]

    _fitParamTableRows = ('fit mode', 'host element type', 'slave mesh discretisation',
                          'slave sobelov discretisation', 'slave sobelov weight',
                          'slave normal discretisation', 'slave normal weight',
                          'host sobelov discretisation', 'host sobelov weight', 'max iterations',
                          'n closest points', 'kdtree args', 'verbose')

    _renderHost = False

    def __init__(self, data, slaveGFUnfitted, hostGFUnfitted, config, fitFunc, resetCallback, parent=None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self._ui = Ui_Dialog()
        self._ui.setupUi(self)

        self._scene = self._ui.MayaviScene.visualisation.scene
        self._scene.background = self.backgroundColour

        self.selectedObjectName = None
        self._data = data
        self._slaveGFUnfitted = slaveGFUnfitted
        self._slaveGFFitted = copy.deepcopy(self._slaveGFUnfitted)
        self._hostGFUnfitted = hostGFUnfitted
        self._hostGFFitted = copy.deepcopy(self._hostGFUnfitted)
        self._fitFunc = fitFunc
        self._config = config
        self._resetCallback = resetCallback

        self._worker = _ExecThread(self._fitFunc)
        self._worker.update.connect(self._fitUpdate)

        # create self._objects
        self._objects = MayaviViewerObjectsContainer()
        self._objects.addObject('data', MayaviViewerDataPoints('data', self._data,
                                                               renderArgs=self._dataRenderArgs))
        self._objects.addObject('slave GF Unfitted',
                                MayaviViewerFieldworkModel('slave GF Unfitted', self._slaveGFUnfitted, self._GFD,
                                                           renderArgs=self._slaveGFUnfittedRenderArgs))
        self._objects.addObject('slave GF Fitted',
                                MayaviViewerFieldworkModel('slave GF Fitted', self._slaveGFFitted, self._GFD,
                                                           renderArgs=self._slaveGFFittedRenderArgs))

        if self._renderHost:
            self._objects.addObject('host GF Unfitted',
                                    MayaviViewerFieldworkModel('host GF Unfitted', self._hostGFUnfitted, self._GFD,
                                                               renderArgs=self._hostGFUnfittedRenderArgs))
            self._objects.addObject('host GF Fitted',
                                    MayaviViewerFieldworkModel('host GF Fitted', self._hostGFFitted, self._GFD,
                                                               renderArgs=self._hostGFFittedRenderArgs))

        self._makeConnections()
        self._initialiseObjectTable()
        self._initialiseSettings()
        self._refresh()

        # self.testPlot()
        # self.drawObjects()

    def _makeConnections(self):
        self._ui.tableWidget.itemClicked.connect(self._tableItemClicked)
        self._ui.tableWidget.itemChanged.connect(self._visibleBoxChanged)
        self._ui.screenshotSaveButton.clicked.connect(self._saveScreenShot)

        # self._ui.fitButton.clicked.connect(self._fit)
        self._ui.fitButton.clicked.connect(self._worker.start)
        self._ui.fitButton.clicked.connect(self._fitLockUI)

        self._ui.resetButton.clicked.connect(self._reset)
        self._ui.abortButton.clicked.connect(self._abort)
        self._ui.acceptButton.clicked.connect(self._accept)

        # connect up changes to params table
        self._ui.fitParamsTableWidget.itemChanged.connect(self._fitParamsTableChanged)

    def _initialiseSettings(self):
        # set values for the params table
        for row, param in enumerate(self._fitParamTableRows):
            self._ui.fitParamsTableWidget.setItem(row, 0, QTableWidgetItem(self._config[param]))

    def _fitParamsTableChanged(self, item):
        param = self._fitParamTableRows[item.row()]
        self._config[param] = item.text()

    def _initialiseObjectTable(self):

        self._ui.tableWidget.setRowCount(self._objects.getNumberOfObjects())
        self._ui.tableWidget.verticalHeader().setVisible(False)
        self._ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        self._addObjectToTable(0, 'data', self._objects.getObject('data'))
        self._addObjectToTable(1, 'slave GF Unfitted',
                               self._objects.getObject('slave GF Unfitted'))
        self._addObjectToTable(2, 'slave GF Fitted',
                               self._objects.getObject('slave GF Fitted'), checked=False)

        if self._renderHost:
            self._addObjectToTable(3, 'host GF Unfitted',
                                   self._objects.getObject('host GF Unfitted'))
            self._addObjectToTable(4, 'host GF Fitted',
                                   self._objects.getObject('host GF Fitted'), checked=False)

        self._ui.tableWidget.resizeColumnToContents(self.objectTableHeaderColumns['visible'])
        self._ui.tableWidget.resizeColumnToContents(self.objectTableHeaderColumns['type'])

    def _addObjectToTable(self, row, name, obj, checked=True):
        typeName = obj.typeName
        print(typeName)
        print(name)
        tableItem = QTableWidgetItem(name)
        if checked:
            tableItem.setCheckState(Qt.Checked)
        else:
            tableItem.setCheckState(Qt.Unchecked)

        self._ui.tableWidget.setItem(row, self.objectTableHeaderColumns['visible'],
                                     tableItem)
        self._ui.tableWidget.setItem(row, self.objectTableHeaderColumns['type'],
                                     QTableWidgetItem(typeName))

    def _tableItemClicked(self):
        selectedRow = self._ui.tableWidget.currentRow()
        self.selectedObjectName = self._ui.tableWidget.item(selectedRow,
                                                            self.objectTableHeaderColumns['visible']).text()
        self._populateScalarsDropDown(self.selectedObjectName)
        print(selectedRow)
        print(self.selectedObjectName)

    def _visibleBoxChanged(self, tableItem):

        # checked changed item is actually the checkbox
        if tableItem.column() == self.objectTableHeaderColumns['visible']:
            # get visible status
            name = tableItem.text()
            visible = tableItem.checkState() == Qt.CheckState.Checked

            print('visibleboxchanged name', name)
            print('visibleboxchanged visible', visible)

            # toggle visibility
            obj = self._objects.getObject(name)
            print(obj.name)
            if obj.sceneObject:
                print('changing existing visibility')
                obj.setVisibility(visible)
            else:
                print('drawing new')
                obj.draw(self._scene)

    def _getSelectedObjectName(self):
        return self.selectedObjectName

    def _getSelectedScalarName(self):
        return 'none'

    def drawObjects(self):
        for name in self._objects.getObjectNames():
            self._objects.getObject(name).draw(self._scene)

    def _fitUpdate(self, fitOutput):
        slaveGFFitted, slaveGFParamsFitted, \
        RMSEFitted, errorsFitted, hostGFFitted = fitOutput

        # update error fields
        self._ui.RMSELineEdit.setText(str(RMSEFitted))
        self._ui.meanErrorLineEdit.setText(str(errorsFitted.mean()))
        self._ui.SDLineEdit.setText(str(errorsFitted.std()))

        # update fitted GF
        slaveFittedObj = self._objects.getObject('slave GF Fitted')
        slaveFittedObj.updateGeometry(slaveGFParamsFitted, self._scene)
        slaveFittedTableItem = self._ui.tableWidget.item(2, self.objectTableHeaderColumns['visible'])
        slaveFittedTableItem.setCheckState(Qt.Checked)

        if self._renderHost:
            hostFittedObj = self._objects.getObject('host GF Fitted')
            hostFittedObj.updateGeometry(hostGFParamsFitted, self._scene)
            hostFittedTableItem = self._ui.tableWidget.item(4, self.objectTableHeaderColumns['visible'])
            hostFittedTableItem.setCheckState(Qt.Checked)

        # unlock reg ui
        self._fitUnlockUI()

    def _fitLockUI(self):
        self._ui.fitParamsTableWidget.setEnabled(False)
        self._ui.fitButton.setEnabled(False)
        self._ui.resetButton.setEnabled(False)
        self._ui.acceptButton.setEnabled(False)
        self._ui.abortButton.setEnabled(False)

    def _fitUnlockUI(self):
        self._ui.fitParamsTableWidget.setEnabled(True)
        self._ui.fitButton.setEnabled(True)
        self._ui.resetButton.setEnabled(True)
        self._ui.acceptButton.setEnabled(True)
        self._ui.abortButton.setEnabled(True)

    def _fitCallback(self, output):
        """
        not fully implemented
        """
        slaveGFParamsFitted = output[1]
        slaveFittedObj = self._objects.getObject('slave GF Fitted')
        slaveFittedObj.updateGeometry(slaveGFParamsFitted, self._scene)
        slaveFittedTableItem = self._ui.tableWidget.item(2, self.objectTableHeaderColumns['visible'])
        slaveFittedTableItem.setCheckState(Qt.Checked)

        if self._renderHost:
            hostGFParamsFitted = output[2]
            hostFittedObj = self._objects.getObject('host GF Fitted')
            hostFittedObj.updateGeometry(hostGFParamsFitted, self._scene)
            hostFittedTableItem = self._ui.tableWidget.item(4, self.objectTableHeaderColumns['visible'])
            hostFittedTableItem.setCheckState(Qt.Checked)

    def _reset(self):
        self._resetCallback()
        slaveFittedObj = self._objects.getObject('slave GF Fitted')
        slaveFittedObj.updateGeometry(self._slaveGFUnfitted.field_parameters.copy(), self._scene)
        slaveFittedTableItem = self._ui.tableWidget.item(2, self.objectTableHeaderColumns['visible'])
        slaveFittedTableItem.setCheckState(Qt.Unchecked)

        if self._renderHost:
            hostFittedObj = self._objects.getObject('host GF Fitted')
            hostFittedObj.updateGeometry(self._hostGFUnfitted.field_parameters.copy(), self._scene)
            hostFittedTableItem = self._ui.tableWidget.item(4, self.objectTableHeaderColumns['visible'])
            hostFittedTableItem.setCheckState(Qt.Unchecked)

        # clear error fields
        self._ui.RMSELineEdit.clear()
        self._ui.meanErrorLineEdit.clear()
        self._ui.SDLineEdit.clear()

    def _accept(self):
        self._close()

    def _abort(self):
        self._reset()
        self._close()

    def _close(self):
        for name in self._objects.getObjectNames():
            self._objects.getObject(name).remove()

        self._objects._objects = {}
        self._objects == None

        # for r in xrange(self._ui.tableWidget.rowCount()):
        #     self._ui.tableWidget.removeRow(r)

    def _refresh(self):
        for r in range(self._ui.tableWidget.rowCount()):
            tableItem = self._ui.tableWidget.item(r, self.objectTableHeaderColumns['visible'])
            name = tableItem.text()
            visible = tableItem.checkState() == Qt.CheckState.Checked
            obj = self._objects.getObject(name)
            print(obj.name)
            if obj.sceneObject:
                print('changing existing visibility')
                obj.setVisibility(visible)
            else:
                print('drawing new')
                obj.draw(self._scene)

    def _saveScreenShot(self):
        filename = self._ui.screenshotFilenameLineEdit.text()
        width = int(self._ui.screenshotPixelXLineEdit.text())
        height = int(self._ui.screenshotPixelYLineEdit.text())
        self._scene.mlab.savefig(filename, size=(width, height))

    # ================================================================#
    @on_trait_change('scene.activated')
    def testPlot(self):
        # This function is called when the view is opened. We don't
        # populate the scene when the view is not yet open, as some
        # VTK features require a GLContext.
        print('trait_changed')

        # We can do normal mlab calls on the embedded scene.
        self._scene.mlab.test_points3d()

    # def _saveImage_fired( self ):
    #     self.scene.mlab.savefig( str(self.saveImageFilename), size=( int(self.saveImageWidth), int(self.saveImageLength) ) )
