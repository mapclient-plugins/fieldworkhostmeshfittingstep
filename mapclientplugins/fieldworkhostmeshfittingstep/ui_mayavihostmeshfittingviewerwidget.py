# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mayavihostmeshfittingviewerwidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from mayaviscenewidget import MayaviSceneWidget


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(914, 679)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.widgetMain = QWidget(Dialog)
        self.widgetMain.setObjectName(u"widgetMain")
        self.widgetMain.setEnabled(True)
        sizePolicy.setHeightForWidth(self.widgetMain.sizePolicy().hasHeightForWidth())
        self.widgetMain.setSizePolicy(sizePolicy)
        self.widgetMain.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout = QGridLayout(self.widgetMain)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget = QWidget(self.widgetMain)
        self.widget.setObjectName(u"widget")
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(350, 0))
        self.widget.setMaximumSize(QSize(500, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.tableWidget = QTableWidget(self.widget)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy1)
        self.tableWidget.setMinimumSize(QSize(0, 0))
        self.tableWidget.setMaximumSize(QSize(16777215, 150))
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)

        self.verticalLayout.addWidget(self.tableWidget)

        self.groupBox = QGroupBox(self.widget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.fitParamsTableWidget = QTableWidget(self.groupBox)
        if (self.fitParamsTableWidget.columnCount() < 1):
            self.fitParamsTableWidget.setColumnCount(1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.fitParamsTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        if (self.fitParamsTableWidget.rowCount() < 13):
            self.fitParamsTableWidget.setRowCount(13)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.fitParamsTableWidget.setVerticalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.fitParamsTableWidget.setVerticalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.fitParamsTableWidget.setVerticalHeaderItem(2, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.fitParamsTableWidget.setVerticalHeaderItem(3, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.fitParamsTableWidget.setVerticalHeaderItem(4, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.fitParamsTableWidget.setVerticalHeaderItem(5, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.fitParamsTableWidget.setVerticalHeaderItem(6, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.fitParamsTableWidget.setVerticalHeaderItem(7, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.fitParamsTableWidget.setVerticalHeaderItem(8, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.fitParamsTableWidget.setVerticalHeaderItem(9, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.fitParamsTableWidget.setVerticalHeaderItem(10, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.fitParamsTableWidget.setVerticalHeaderItem(11, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.fitParamsTableWidget.setVerticalHeaderItem(12, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.fitParamsTableWidget.setItem(2, 0, __qtablewidgetitem16)
        self.fitParamsTableWidget.setObjectName(u"fitParamsTableWidget")

        self.verticalLayout_2.addWidget(self.fitParamsTableWidget)


        self.verticalLayout.addWidget(self.groupBox)

        self.fitButtonsGroup = QGridLayout()
        self.fitButtonsGroup.setObjectName(u"fitButtonsGroup")
        self.fitButton = QPushButton(self.widget)
        self.fitButton.setObjectName(u"fitButton")

        self.fitButtonsGroup.addWidget(self.fitButton, 0, 0, 1, 1)

        self.resetButton = QPushButton(self.widget)
        self.resetButton.setObjectName(u"resetButton")

        self.fitButtonsGroup.addWidget(self.resetButton, 0, 1, 1, 1)

        self.acceptButton = QPushButton(self.widget)
        self.acceptButton.setObjectName(u"acceptButton")

        self.fitButtonsGroup.addWidget(self.acceptButton, 1, 1, 1, 1)

        self.abortButton = QPushButton(self.widget)
        self.abortButton.setObjectName(u"abortButton")

        self.fitButtonsGroup.addWidget(self.abortButton, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.fitButtonsGroup)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.line = QFrame(self.widget)
        self.line.setObjectName(u"line")
        self.line.setLineWidth(3)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.errorGroup = QGroupBox(self.widget)
        self.errorGroup.setObjectName(u"errorGroup")
        self.formLayout_2 = QFormLayout(self.errorGroup)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.RMSELabel = QLabel(self.errorGroup)
        self.RMSELabel.setObjectName(u"RMSELabel")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.RMSELabel)

        self.meanErrorLabel = QLabel(self.errorGroup)
        self.meanErrorLabel.setObjectName(u"meanErrorLabel")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.meanErrorLabel)

        self.SDLabel = QLabel(self.errorGroup)
        self.SDLabel.setObjectName(u"SDLabel")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.SDLabel)

        self.RMSELineEdit = QLineEdit(self.errorGroup)
        self.RMSELineEdit.setObjectName(u"RMSELineEdit")
        self.RMSELineEdit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.RMSELineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.RMSELineEdit)

        self.meanErrorLineEdit = QLineEdit(self.errorGroup)
        self.meanErrorLineEdit.setObjectName(u"meanErrorLineEdit")
        self.meanErrorLineEdit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.meanErrorLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.meanErrorLineEdit)

        self.SDLineEdit = QLineEdit(self.errorGroup)
        self.SDLineEdit.setObjectName(u"SDLineEdit")
        self.SDLineEdit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.SDLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.SDLineEdit)


        self.verticalLayout.addWidget(self.errorGroup)

        self.screenshotgroup = QGroupBox(self.widget)
        self.screenshotgroup.setObjectName(u"screenshotgroup")
        self.screenshotgroup.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.formLayout = QFormLayout(self.screenshotgroup)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.pixelsXLabel = QLabel(self.screenshotgroup)
        self.pixelsXLabel.setObjectName(u"pixelsXLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pixelsXLabel.sizePolicy().hasHeightForWidth())
        self.pixelsXLabel.setSizePolicy(sizePolicy2)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.pixelsXLabel)

        self.screenshotPixelXLineEdit = QLineEdit(self.screenshotgroup)
        self.screenshotPixelXLineEdit.setObjectName(u"screenshotPixelXLineEdit")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.screenshotPixelXLineEdit.sizePolicy().hasHeightForWidth())
        self.screenshotPixelXLineEdit.setSizePolicy(sizePolicy3)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.screenshotPixelXLineEdit)

        self.pixelsYLabel = QLabel(self.screenshotgroup)
        self.pixelsYLabel.setObjectName(u"pixelsYLabel")
        sizePolicy2.setHeightForWidth(self.pixelsYLabel.sizePolicy().hasHeightForWidth())
        self.pixelsYLabel.setSizePolicy(sizePolicy2)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.pixelsYLabel)

        self.screenshotPixelYLineEdit = QLineEdit(self.screenshotgroup)
        self.screenshotPixelYLineEdit.setObjectName(u"screenshotPixelYLineEdit")
        sizePolicy3.setHeightForWidth(self.screenshotPixelYLineEdit.sizePolicy().hasHeightForWidth())
        self.screenshotPixelYLineEdit.setSizePolicy(sizePolicy3)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.screenshotPixelYLineEdit)

        self.screenshotFilenameLabel = QLabel(self.screenshotgroup)
        self.screenshotFilenameLabel.setObjectName(u"screenshotFilenameLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.screenshotFilenameLabel)

        self.screenshotFilenameLineEdit = QLineEdit(self.screenshotgroup)
        self.screenshotFilenameLineEdit.setObjectName(u"screenshotFilenameLineEdit")
        sizePolicy3.setHeightForWidth(self.screenshotFilenameLineEdit.sizePolicy().hasHeightForWidth())
        self.screenshotFilenameLineEdit.setSizePolicy(sizePolicy3)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.screenshotFilenameLineEdit)

        self.screenshotSaveButton = QPushButton(self.screenshotgroup)
        self.screenshotSaveButton.setObjectName(u"screenshotSaveButton")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.screenshotSaveButton.sizePolicy().hasHeightForWidth())
        self.screenshotSaveButton.setSizePolicy(sizePolicy4)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.screenshotSaveButton)


        self.verticalLayout.addWidget(self.screenshotgroup)


        self.verticalLayout_3.addLayout(self.verticalLayout)


        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        self.MayaviScene = MayaviSceneWidget(self.widgetMain)
        self.MayaviScene.setObjectName(u"MayaviScene")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(1)
        sizePolicy5.setVerticalStretch(1)
        sizePolicy5.setHeightForWidth(self.MayaviScene.sizePolicy().hasHeightForWidth())
        self.MayaviScene.setSizePolicy(sizePolicy5)

        self.gridLayout.addWidget(self.MayaviScene, 0, 1, 1, 1)


        self.horizontalLayout_2.addWidget(self.widgetMain)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Host Mesh Fitting", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Visible", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Type", None));
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Fitting Parameters", None))
        ___qtablewidgetitem2 = self.fitParamsTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Value", None));
        ___qtablewidgetitem3 = self.fitParamsTableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"fit mode", None));
        ___qtablewidgetitem4 = self.fitParamsTableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"host element type", None));
        ___qtablewidgetitem5 = self.fitParamsTableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"slave mesh discretisation", None));
        ___qtablewidgetitem6 = self.fitParamsTableWidget.verticalHeaderItem(3)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog", u"slave sobelov discretisation", None));
        ___qtablewidgetitem7 = self.fitParamsTableWidget.verticalHeaderItem(4)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Dialog", u"slave sobelov weight", None));
        ___qtablewidgetitem8 = self.fitParamsTableWidget.verticalHeaderItem(5)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Dialog", u"slave normal discretisation", None));
        ___qtablewidgetitem9 = self.fitParamsTableWidget.verticalHeaderItem(6)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Dialog", u"slave normal weight", None));
        ___qtablewidgetitem10 = self.fitParamsTableWidget.verticalHeaderItem(7)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Dialog", u"host sobelov discretisation", None));
        ___qtablewidgetitem11 = self.fitParamsTableWidget.verticalHeaderItem(8)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Dialog", u"host sobelov weight", None));
        ___qtablewidgetitem12 = self.fitParamsTableWidget.verticalHeaderItem(9)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Dialog", u"max iterations", None));
        ___qtablewidgetitem13 = self.fitParamsTableWidget.verticalHeaderItem(10)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Dialog", u"n closest points", None));
        ___qtablewidgetitem14 = self.fitParamsTableWidget.verticalHeaderItem(11)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("Dialog", u"kdtree args", None));
        ___qtablewidgetitem15 = self.fitParamsTableWidget.verticalHeaderItem(12)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("Dialog", u"verbose", None));

        __sortingEnabled = self.fitParamsTableWidget.isSortingEnabled()
        self.fitParamsTableWidget.setSortingEnabled(False)
        self.fitParamsTableWidget.setSortingEnabled(__sortingEnabled)

        self.fitButton.setText(QCoreApplication.translate("Dialog", u"Fit", None))
        self.resetButton.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.acceptButton.setText(QCoreApplication.translate("Dialog", u"Accept", None))
        self.abortButton.setText(QCoreApplication.translate("Dialog", u"Abort", None))
        self.errorGroup.setTitle(QCoreApplication.translate("Dialog", u"Fitting Errors", None))
        self.RMSELabel.setText(QCoreApplication.translate("Dialog", u"RMS:", None))
        self.meanErrorLabel.setText(QCoreApplication.translate("Dialog", u"Mean:", None))
        self.SDLabel.setText(QCoreApplication.translate("Dialog", u"S.D.:", None))
        self.screenshotgroup.setTitle(QCoreApplication.translate("Dialog", u"Screenshot", None))
        self.pixelsXLabel.setText(QCoreApplication.translate("Dialog", u"Pixels X:", None))
        self.screenshotPixelXLineEdit.setText(QCoreApplication.translate("Dialog", u"800", None))
        self.pixelsYLabel.setText(QCoreApplication.translate("Dialog", u"Pixels Y:", None))
        self.screenshotPixelYLineEdit.setText(QCoreApplication.translate("Dialog", u"600", None))
        self.screenshotFilenameLabel.setText(QCoreApplication.translate("Dialog", u"Filename:", None))
        self.screenshotFilenameLineEdit.setText(QCoreApplication.translate("Dialog", u"screenshot.png", None))
        self.screenshotSaveButton.setText(QCoreApplication.translate("Dialog", u"Save Screenshot", None))
    # retranslateUi

