# -*- coding: utf-8 -*-
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
import datetime
import time


class Data_base_page(QWidget):
    def __init__(self, con):
        super().__init__()
        self.con = con
        self.path = os.getcwd()

        if self.con.isOpen():
            print('{}/prefer.db'.format(self.path), 'строка из if метода record setting table.py')
        else:
            self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            self.path = os.getcwd()
            print('{}/prefer.db'.format(self.path), 'строка из else метода record set')
            self.con.setDatabaseName('{}/prefer.db'.format(self.path))
            # con.setDatabaseName('//Users//user//PycharmProjects//razrabotka//prefer.db')
            self.con.open()

        self.vbox_main = QVBoxLayout()
        self.setLayout(self.vbox_main)
        self.hbox = QHBoxLayout()
        self.vbox_main.addLayout(self.hbox)
        self.vbox = QVBoxLayout()
        self.vbox_main.addLayout(self.vbox)

        self.but_sending_data_to_formwidget = QPushButton('Редактировать данные')
        self.hbox.addWidget(self.but_sending_data_to_formwidget)

        self.tab_model = QtSql.QSqlTableModel()
        self.tab_model.setTable('department')
        self.tab_model.setSort(1, QtCore.Qt.AscendingOrder)
        self.tab_model.select()

        self.how_many_days()

        self.list_header = ['Ф.И.О.', 'Дата рождения', 'Номер истории', 'Дата поступления', ]
        с = 1
        for i in self.list_header:
            self.tab_model.setHeaderData(с, QtCore.Qt.Horizontal, i)
            с+=1
        self.tab_model.setHeaderData(14, QtCore.Qt.Horizontal, 'Дата выписки')
        self.tab_model.setHeaderData(38, QtCore.Qt.Horizontal, 'К/День')

        self.tv = QTableView()
        self.tv.setModel(self.tab_model)
        self.tv.hideColumn(0)
        self.tv.hideColumn(3)
        for i in range(5, 41):
            self.tv.hideColumn(i)
        self.tv.showColumn(14)
        self.tv.showColumn(38)

        #self.tv.setColumnWidth(4, 120)
        #self.tv.setColumnWidth(1, 250)
        self.tv.resizeColumnsToContents()
        #self.tv.setColumnWidth(1, 250)


        #self.tv.setSortingEnabled(True)
        self.tv.sortByColumn(1, QtCore.Qt.AscendingOrder)
        self.tv.setAlternatingRowColors(True)
        self.vbox.addWidget(self.tv)

        self.tv_selector = QtCore.QItemSelectionModel(self.tab_model)
        self.tv.setSelectionModel(self.tv_selector)


        self.btn_del = QPushButton('Отправить выделенное в архив')
        self.vbox.addWidget(self.btn_del)

        self.show()

    def insert_record_to_db(self, values_for_table, dic):
        ''' добавляет запись  в конец таблицы когда нажимается кнопка добавить в отдел. Эта функция вызывается из другого модуля'''
        if self.con.isOpen():
            print('{}/prefer.db'.format(self.path), 'строка из if метода инсерт')
        else:
            self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            self.path = os.getcwd()
            print('{}/prefer.db'.format(self.path), 'строка из else метода инсерт')
            self.con.setDatabaseName('{}/prefer.db'.format(self.path))
            ## con.setDatabaseName('//Users//user//PycharmProjects//razrabotka//prefer.db')
            self.con.open()

        self.dict_values = values_for_table
        print(self.dict_values)
        # print(self.font_t, self.size, self.fio_zav, self.fio_doc, self.sex, 'это проверка данных на вход ')
        # if 'department' not in self.con.tables():
        #     query = QtSql.QSqlQuery()
        #     query.exec('create table department(id integer primary key autoincrement, fio text, date_birt text, date_enter text, hist_numb text, povtor text)')
        #     query.finish()
        #query2 = QtSql.QSqlQuery()
        #query2.prepare('CREATE TABLE department(id integer primary key autoincrement,  ? text, ? text, ? text, ? text, ? text, ? text, ? text, ? text, ? text, ? text, ? text, ? text, )')
        #for i in range(10):
        #    query2.addBindValue(i)
        # query.bindValue(':font', self.font_t)
        # query.bindValue(':size', self.size)
        # query.bindValue(':fio_doc', self.fio_doc)
        # query.bindValue(':fio_zav', self.fio_zav)
        # query.bindValue(':sex', self.sex)
        # query.exec_()
        # query.finish()

        self.osn_dic = dic

        stm = QtSql.QSqlTableModel()
        stm.setTable('department')
        stm.select()
        rec = self.con.record('department')  # получает сведения о  таблице в которую добавит запись рекорд
        for k, i in self.osn_dic.items():
            rec.setValue(k, self.dict_values[k])
        #rec.setValue('fio', self.dict_values['fio'])
        stm.insertRecord(-1, rec)

        '''
        rec = stm.record(0)  # получает сведения о записи в таблице в которой будет заменены данные   
        rec.setValue('font', self.font_t)
        stm.setRecord(0, rec)
        stm.removeRow(
            1)  # удаляет строку, а следующая строка, обновляет данные чтобы обновиться таблицу, удалив пустую строку
        stm.select()
        '''

    def how_many_days(self):
        count = self.con.record('department').count()
        print(count)
        for i in range(count):
            rec_date = self.tab_model.record(i)
            date_enter = rec_date.value('d_enter')
            date_vipiska = rec_date.value('vipiska')
            #print(date_enter, date_vipiska)
            try:
                date_enter = time.strptime(date_enter, '%d.%m.%Y')
            except ValueError:
                try:
                    date_enter = time.strptime(date_enter, '%d.%m.%y')
                except ValueError:
                    #print('формат введенной даты нестандартный')
                    date_enter = ''
            except TypeError:
                #print('запись в базе не заполнена имеет значение None')
                date_enter = ''
            try:
                date_vipiska = time.strptime(date_vipiska, '%d.%m.%Y')
            except ValueError:
                try:
                    date_vipiska = time.strptime(date_vipiska, '%d.%m.%y')
                except ValueError:
                    #print('формат введенной даты нестандартный')
                    date_vipiska = ''
            except TypeError:
                #print('запись в базе не заполнена имеет значение None')
                date_vipiska = ''

            if not date_enter == '':
                date_enter = datetime.date(year=date_enter.tm_year, month=date_enter.tm_mon, day=date_enter.tm_mday)
                if date_vipiska == '':
                    date_vipiska = datetime.date.today()
                else:
                    date_vipiska = datetime.date(year=date_vipiska.tm_year, month=date_vipiska.tm_mon,
                                                 day=date_vipiska.tm_mday)
            #print(type(date_enter), type(date_vipiska))
            if type(date_enter) is datetime.date and type(date_vipiska) is datetime.date:
                num_days = date_vipiska - date_enter
                num_days = num_days.days
                #print(f'высчитли койко дни {num_days}')
                rec_date.setValue('new_col', num_days)
                self.tab_model.setRecord(i, rec_date)

    def read_settings(self):
        query = QtSql.QSqlQuery()
        query.exec('SELECT * FROM settings')
        lst = []
        if query.isActive():
            query.first()
            while query.isValid():
                lst.append(query.value('font'))
                lst.append(query.value('fio_doc'))
                lst.append(query.value('fio_zav'))
                lst.append(query.value('size'))
                lst.append(query.value('sex'))
                query.next()
        query.finish()
        print(lst[:6])
        return lst[:6]

    def del_from_tab(self):
        if self.con.isOpen():
            self.tab_model.removeRow(self.tv.currentIndex().row())
            print('{}/prefer.db'.format(self.path), 'строка из if')
            self.tab_model.select()

        else:
            self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            self.path = os.getcwd()
            print('{}/prefer.db'.format(self.path), 'строка из else')
            self.con.setDatabaseName('{}/prefer.db'.format(self.path))
            ## con.setDatabaseName('//Users//user//PycharmProjects//razrabotka//prefer.db')
            self.con.open()
            self.tab_model.removeRow(self.tv.currentIndex().row())
            self.tab_model.select()

    def create_table(self):
        self.tab_model.select()
        print('create table Функция обновления таблицы select()')


if __name__ == '__main__':
    app = QApplication([])
    table_base = Data_base_page()
    sys.exit(app.exec_())
