

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction,
                             QWidget, QPushButton, QToolTip, QMessageBox,
                             QTextEdit, QLabel, QHBoxLayout, QVBoxLayout,
                             QLineEdit, QTextEdit, QGridLayout, QLCDNumber,
                             QSlider, QInputDialog, QFileDialog, QFrame,
                             QFrame, QSplitter, QStyleFactory, QPlainTextEdit,
                             QComboBox, QCompleter, QDesktopWidget, qApp,
                             QSizePolicy, QTableView)
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import QCoreApplication
from PyQt5 import Qt, QtCore, QtGui, QtSql
import sqlite3
import os
from docxtpl import DocxTemplate
import subprocess
import os.path

class Table_Data(QWidget):

    def __init__(self, con):
        super().__init__()
        self.con = con
        self.path = os.getcwd()

        if self.con.isOpen():
            print('{}/prefer.db'.format(self.path), 'строка из if метода read setting')
        else:
            self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            print('{}/prefer.db'.format(self.path), 'строка из else метода read settings')
            self.con.setDatabaseName('{}/prefer.db'.format(self.path))
            ## con.setDatabaseName('//Users//user//PycharmProjects//razrabotka//prefer.db')
            self.con.open()
            print('open')

        self.vbox_main = QVBoxLayout()
        self.setLayout(self.vbox_main)
        self.hbox = QHBoxLayout()
        self.vbox_main.addLayout(self.hbox)
        self.vbox = QVBoxLayout()
        self.vbox_main.addLayout(self.vbox)

        self.btn_send_data_from_archive_to_form = QPushButton('Редактировать данные')
        self.hbox.addWidget(self.btn_send_data_from_archive_to_form)

        self.tab_model2 = QtSql.QSqlTableModel()
        self.tab_model2.setTable('department2')
        self.tab_model2.setSort(1, QtCore.Qt.AscendingOrder)
        self.tab_model2.select()

        self.list_header = ['Ф.И.О.', 'Дата рождения', 'Номер истории', 'Дата поступления', ]
        с = 1
        for i in self.list_header:
            self.tab_model2.setHeaderData(с, QtCore.Qt.Horizontal, i)
            с+=1
        self.tab_model2.setHeaderData(14, QtCore.Qt.Horizontal, 'Дата выписки')

        # self.rec = self.tab_model2.record()
        # self.rec.setValue('fio', 'следующий')
        # self.tab_model2.insertRecord(-1, self.rec)

        self.tv2 = QTableView()
        self.tv2.setModel(self.tab_model2)
        self.tv2.hideColumn(0)
        self.tv2.hideColumn(3)
        for i in range(5, 41):
            self.tv2.hideColumn(i)
        self.tv2.showColumn(14)
        self.tv2.resizeColumnsToContents()
        # self.tv2.setColumnWidth(4, 120)
        # self.tv2.setColumnWidth(1, 250)
        self.tv2.setSortingEnabled(False)
        self.tv2.sortByColumn(1, QtCore.Qt.AscendingOrder)
        self.tv2.setAlternatingRowColors(True)

        self.tv2_selector = QtCore.QItemSelectionModel(self.tab_model2)
        self.tv2.setSelectionModel(self.tv2_selector)


        self.vbox.addWidget(self.tv2)

        self.btn_delete_from_arcive = QPushButton('Удалить из архива')
        self.vbox.addWidget(self.btn_delete_from_arcive)

        self.show()






    def del_from_tab2(self):
        if self.tv2_selector.hasSelection():
            if self.con.isOpen():
                self.tab_model2.removeRow(self.tv2.currentIndex().row())
                print('{}/prefer.db'.format(self.path), 'строка из if')
                self.tab_model2.select()

            else:
                self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
                self.path = os.getcwd()
                print('{}/prefer.db'.format(self.path), 'строка из else')
                self.con.setDatabaseName('{}/prefer.db'.format(self.path))
                ## con.setDatabaseName('//Users//user//PycharmProjects//razrabotka//prefer.db')
                self.con.open()
                self.tab_model2.removeRow(self.tv2.currentIndex().row())
                self.tab_model2.select()


    def new_aproach(self):
        pass




if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ex = Table_Data()
    sys.exit(app.exec_())