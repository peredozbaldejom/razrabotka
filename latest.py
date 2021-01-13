# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction,
                             QWidget, QPushButton, QToolTip, QMessageBox,
                             QTextEdit, QLabel, QHBoxLayout, QVBoxLayout,
                             QLineEdit, QTextEdit, QGridLayout, QLCDNumber,
                             QSlider, QInputDialog, QFileDialog, QFrame,
                             QFrame, QSplitter, QStyleFactory, QPlainTextEdit,
                             QComboBox, QCompleter, QDesktopWidget, qApp,
                             QSizePolicy, QTableView, QDialog)
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import QCoreApplication
from PyQt5 import Qt, QtCore, QtGui, QtSql
import sqlite3
import os
from docxtpl import DocxTemplate
import subprocess
import datetime
import os.path
from table import *
from page_form_widget import *
from table_archive import *
from dairy import *


class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        desktop_h = app.desktop().availableGeometry().height() - 40
        desktop_w = app.desktop().availableGeometry().width() // 2 + 80


        self.desc = QApplication.desktop().availableGeometry().height()

        self.setGeometry(0, 0, desktop_w, desktop_h)
        self.setWindowTitle('Абсолютно новейшая разработка из 3020 года')

        self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.path = os.getcwd()
        self.con.setDatabaseName('{}/prefer.db'.format(self.path))
        #con.setDatabaseName('//Users//user//PycharmProjects//razrabotka//prefer.db')
        self.con.open()

        if 'department' not in self.con.tables():
            query = QtSql.QSqlQuery()
            print(query.exec('create table department(id integer primary key autoincrement, fio text, dbirth text, numbhist text, d_enter text, t_enter text, povtorno text, dps text, dobrovol text, d_view text, t_view text, doctor text, zavotd text, zaloba text, vipiska text, area text, adress text, an_live text, an_bol text, an_nark text, iz_napr text, priemn text, votdele text, somat  text, ginek text, nevrol text, zabolevan text, allerg text, epid text, strah text, zakl text, diag_osn text, diag_sop text, dinamika text, kvipiske text, treatment text, recommendations text, department text, new_col text, add_col text, just_col text)'))
            query.finish()

        if 'department2' not in self.con.tables():
            query2 = QtSql.QSqlQuery()
            print(query2.exec('create table department2(id integer primary key autoincrement, fio text, dbirth text, numbhist text, d_enter text, t_enter text, povtorno text, dps text, dobrovol text, d_view text, t_view text, doctor text, zavotd text, zaloba text, vipiska text, area text, adress text, an_live text, an_bol text, an_nark text, iz_napr text, priemn text, votdele text, somat  text, ginek text, nevrol text, zabolevan text, allerg text, epid text, strah text, zakl text, diag_osn text, diag_sop text, dinamika text, kvipiske text, treatment text, recommendations text, department text, new_col text, add_col text, just_col text)'))
            query2.finish()


        self.main_dict = {'fio': '', 'dbirth': '', 'numbhist': '', 'd_enter': '', 't_enter': '', 'povtorno': '', 'dps': '',
         'dobrovol': '', 'd_view': '', 't_view': '', 'doctor': '', 'zavotd': '', 'zaloba': '', 'vipiska': '',
         'area': '', 'adress': '', 'an_live': '', 'an_bol': '', 'an_nark': '', 'iz_napr': '', 'priemn': '',
         'votdele': '', 'somat': '', 'ginek': '', 'nevrol': '', 'zabolevan': '', 'allerg': '', 'epid': '',
         'strah': '', 'zakl': '', 'diag_osn': '', 'diag_sop': '', 'treatment': '', 'dinamika': '', 'kvipiske': '',
         'recommendations': '', 'department': '',  'new_col': '', 'add_col': '', 'just_col': ''}

        self.preferences = Preferences_page(self.con)  # формвиджет для
        self.form_widget = FormWidget(self.con, self.main_dict)  # формвиджет для размещения на этом виджете всех кнопок
        self.arcive_table = Table_Data(self.con)  # формвиджет для размещения
        self.data_base_page = Data_base_page(self.con)  # формвиджет для
        self.dairy = Page_dairy(self.con)

        self.main_widget = QWidget()  # сделаем виджет для установки его на главное окно
        self.main_layout = QVBoxLayout()  # делаем лайаут куда все будем размещать
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)  # на главное окно ставим скроллареа

        self.stac_widg = Qt.QStackedWidget()  # стэквиджет в котором меняются другие виджеты через кнопку

        self.mw = Qt.QScrollArea()  # скроллареа для размещения на стэкет виджете чтобы прокручивать содержимое устновленного виджета
        self.mw.setWidgetResizable(True)
        self.mw.setWidget(self.form_widget)

        self.scroll_dairy = Qt.QScrollArea()
        self.scroll_dairy.setWidget(self.dairy)
        self.scroll_dairy.setWidgetResizable(True)

        self.stac_widg.addWidget(self.mw)
        self.stac_widg.addWidget(self.data_base_page)
        self.stac_widg.addWidget(self.arcive_table)
        self.stac_widg.addWidget(self.preferences)
        self.stac_widg.addWidget(self.scroll_dairy)
        print('finish')

        self.button_box = QHBoxLayout(self)
        self.main_layout.addLayout(self.button_box)
        self.men_but = QPushButton('Редактор')
        self.men_but.clicked.connect(self.page1)
        self.men_but2 = QPushButton('Архив')
        self.men_but2.clicked.connect(self.page2)
        self.men_but3 = QPushButton('Пациенты в отделении')
        self.men_but3.clicked.connect(self.page3)
        self.men_but4 = QPushButton('Настройки')
        self.men_but4.clicked.connect(self.page4)
        self.men_but5 = QPushButton('Новый пациент')
        self.men_but5.clicked.connect(self.dialog_new_patience)
        self.men_but6 = QPushButton('Дневники')
        self.men_but6.clicked.connect(self.page6)
        self.button_box.addWidget(self.men_but)
        self.button_box.addWidget(self.men_but3)
        self.button_box.addWidget(self.men_but2)
        self.button_box.addWidget(self.men_but4)
        self.button_box.addWidget(self.men_but5)
        self.button_box.addWidget(self.men_but6)
        self.main_layout.addWidget(self.stac_widg)
        self.show()

        self.data_base_page.but_sending_data_to_formwidget.clicked.connect(lambda: self.edit_tabel_row(1))
        self.data_base_page.btn_del.clicked.connect(self.delete_button_from_tab1)
        self.form_widget.btn_change.clicked.connect(self.changed_font2)
        self.form_widget.btn_update.clicked.connect(self.update_data_department)
        self.arcive_table.btn_send_data_from_archive_to_form.clicked.connect(lambda: self.edit_tabel_row(2))
        self.arcive_table.btn_delete_from_arcive.clicked.connect(self.arcive_table.del_from_tab2)
        

        self.main_list_obj = [self.form_widget.fio_t, self.form_widget.datebirt_t, self.form_widget.numbhis_t,
                    self.form_widget.dateenter_t, self.form_widget.timeenter_t, self.form_widget.povtorno_t,
                    self.form_widget.dps_t, self.form_widget.dobrov_t, self.form_widget.dateosm_t,
                    self.form_widget.timeosm_t, self.form_widget.doc_t, self.form_widget.zav_t,
                    self.form_widget.coplain_t, self.form_widget.leave_t, self.form_widget.combo, self.form_widget.adres_t,
                    self.form_widget.anam_live_t, self.form_widget.anam_dese_t, self.form_widget.anam_nark_t,
                    self.form_widget.napravlee_t, self.form_widget.psy_st_pr_t, self.form_widget.psy_st_ot_t,
                    self.form_widget.somatikas_t, self.form_widget.ginekolog_t, self.form_widget.nevrologi_t,
                    self.form_widget.concomita_t, self.form_widget.allergiaa_t, self.form_widget.epidemiol_t,
                    self.form_widget.strahovoi_t, self.form_widget.zakluchen_t, self.form_widget.diagnozos_t,
                    self.form_widget.diagnozso_t, self.form_widget.treatment_t, self.form_widget.dinamika_t,
                    self.form_widget.k_vipisk_t, self.form_widget.prescribe_t]

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Выход', 'Закрыть приложение', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def get_data_from_tab_model(self, dic, var):
        ''' функция которая получает и возвращает выделенные данные из таблицы отделения в словарь (потом надо будет переделать, чтобы можно использовать для обеих таблиц)'''

        if self.con.isOpen():
            print('{}/prefer.db'.format(self.path), 'строка из if метода get data')
        else:
            self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            self.path = os.getcwd()
            print('{}/prefer.db'.format(self.path), 'строка из else метода get data')
            self.con.setDatabaseName('{}/prefer.db'.format(self.path))
            # con.setDatabaseName('//Users//user//PycharmProjects//razrabotka//prefer.db')
            self.con.open()
        #self.men_but3.setDisabled(True)
        if var == 1:
            self.cur_index = self.data_base_page.tv.currentIndex().row()
            self.cur_index2 = self.data_base_page.tv.currentIndex()
            #self.cur_index3 = self.data_base_page.tab_model.index()

            print(self.cur_index)
            # print(self.cur_index2)
            # print(self.cur_index3)

            self.form_widget.btn_update.setDisabled(False)
            self.form_widget.btn_change.setDisabled(True)
            self.form_widget.change_background(0)
        else:
            self.cur_index = self.arcive_table.tv2.currentIndex().row()
            self.form_widget.btn_update.setDisabled(True)
            print(self.cur_index)
            print(self.arcive_table.tv2_selector.currentIndex().row())
            print(self.arcive_table.tv2_selector.hasSelection())

        self.cols = dic

        self.quer_edit = QtSql.QSqlQueryModel()
        if var == 1:
            self.quer_edit.setQuery('SELECT * FROM department ORDER BY fio')
        else:
            self.quer_edit.setQuery('SELECT * FROM department2 ORDER BY fio')
        for k, i in self.cols.items():
            self.cols[k] = self.quer_edit.record(self.cur_index).value(k)
        #print(self.cols)  # работает
        print( 'это объект индекс выделенной строки в таблице отделения гет дата фром табле') # работает
        return self.cols

    def changed_font2(self):
        self.form_widget.changed_font()
        self.men_but3.setDisabled(False)
        self.men_but2.setDisabled(False)

        
        
    def insert_from_table_to_form(self, dic, obj):
        '''вставляет данные из таблицы в формвиджет'''
        self.dic = dic
        self.list_obj = self.main_list_obj
        x = 0
        while x < len(self.list_obj):
            for k, i in self.dic.items():
                try:
                    self.list_obj[x].setText(self.dic[k])
                    x+=1
                    #print(x)
                except AttributeError:
                    self.list_obj[x].setCurrentText(self.dic[k])
                    x += 1
                    continue
                except IndexError:
                    break

        #self.form_widget.fio_t.setText(self.dic['fio']) #  переносит данные из словаря в виджет

    def edit_tabel_row(self, var):
        ''' функция на которую установлена кнопка редактировать данные (можно ее использовать для обоих таблиц)'''
        if self.con.isOpen():
            print('{}/prefer.db'.format(self.path), 'строка из if метода get data')
        else:
            self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            self.path = os.getcwd()
            print('{}/prefer.db'.format(self.path), 'строка из else метода get data')
            self.con.setDatabaseName('{}/prefer.db'.format(self.path))
            # con.setDatabaseName('//Users//user//PycharmProjects//razrabotka//prefer.db')
            self.con.open()
        #if (self.data_base_page.tv.currentIndex().isValid() == True and self.arcive_table.tv2.currentIndex().isValid() == False) or (self.data_base_page.tv.currentIndex().isValid() == False and self.arcive_table.tv2.currentIndex().isValid() == True):
        if (self.data_base_page.tv_selector.hasSelection() == True and self.arcive_table.tv2_selector.hasSelection() == False) or (self.data_base_page.tv_selector.hasSelection() == False and self.arcive_table.tv2_selector.hasSelection() == True):
            print('я тут после сравнения выделенных срок')
            print(self.data_base_page.tv.currentIndex().row(), self.arcive_table.tv2.currentIndex().row())
            print(self.data_base_page.tv_selector.currentIndex().row(), self.arcive_table.tv2_selector.currentIndex().row())
            self.var = var
            dic = self.get_data_from_tab_model(self.main_dict, self.var) # создает словарь из выделенной строки в таблице отделения
            self.insert_from_table_to_form(dic, self.main_list_obj) # отправлет все данные в поля редактирования в формвиджет
            self.men_but3.setDisabled(True)
            self.men_but2.setDisabled(True)
            self.stac_widg.setCurrentWidget(self.mw)

        else:
            print(' ничего не выделено ')
            print(self.data_base_page.tv.currentIndex().row(), self.arcive_table.tv2.currentIndex().row())

    def update_data_department(self):
        '''функция для внесения изменений в редактируемые данные, переносит из формвиджета в выделенную строку таблицы '''
        self.update_row = self.data_base_page.tab_model.record(self.cur_index)
        self.dic = self.main_dict
        self.lis = self.main_list_obj
        x = 0
        while x < len(self.main_list_obj):
            for k, i in self.dic.items():
                try:
                    self.update_row.setValue(k, self.lis[x].text())
                    #print(self.lis[x].text())
                except AttributeError:
                    try:
                        self.update_row.setValue(k, self.lis[x].toPlainText())
                    except AttributeError:
                        self.update_row.setValue(k, self.lis[x].currentText())
                except IndexError:
                    break
                    
                x+=1
                #print(x)
        self.data_base_page.tab_model.setRecord(self.cur_index, self.update_row)
        self.men_but3.setDisabled(False)
        self.men_but2.setDisabled(False)
        self.form_widget.btn_update.setDisabled(True)
        self.form_widget.btn_change.setDisabled(False)
        self.form_widget.change_background(1)

        

    def transfer_data_to_arhive(self):
        ''' получает словарь с измененными данными, и перезаписывает их в таблицу'''
        if self.data_base_page.tv_selector.hasSelection():
            self.dic = self.get_data_from_tab_model(self.main_dict, 1)
            #print(self.dic)
            self.rec = self.arcive_table.tab_model2.record()
            for k, i in self.dic.items():
                self.rec.setValue(k, self.dic[k])
            self.arcive_table.tab_model2.insertRecord(-1, self.rec)
            self.form_widget.btn_update.setDisabled(True)
            self.form_widget.btn_change.setDisabled(False)
            self.form_widget.change_background(1)
        else:
            print('отправлять нечего')


    def delete_button_from_tab1(self):
        ''' функция которая выполняется когда нажимается кнопка ПЕРЕНЕСТИ В АРХИВ'''
        if self.data_base_page.tv_selector.hasSelection():
            self.transfer_data_to_arhive()
            self.data_base_page.del_from_tab()
            self.arcive_table.tab_model2.select()



    def page1(self):
        self.stac_widg.setCurrentWidget(self.mw)

    def page3(self):
        self.stac_widg.setCurrentWidget(self.data_base_page)
        self.data_base_page.create_table()
        self.data_base_page.tv_selector.clearSelection()
        self.arcive_table.tv2_selector.clearSelection()


    def page2(self):
        self.stac_widg.setCurrentWidget(self.arcive_table)
        self.arcive_table.tv2_selector.clearSelection()
        self.data_base_page.tv_selector.clearSelection()


    def page4(self):
        self.stac_widg.setCurrentWidget(self.preferences)

    def page6(self):
        self.stac_widg.setCurrentWidget(self.scroll_dairy)


    def dialog_new_patience(self):
        reply = QMessageBox.question(self, 'Удалить все из редактора', 'Удалить все из редактора', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.page5()
        else:
            print('произошла отмена создания нового пациента')

        '''dialog = QDialog()
        result = dialog.exec()
        if result == QDialog.Accepted:
            self.page5()
        else:
            print('произошла отмена создания нового пациента')
        '''

    def page5(self):
        dic = {'fio': '', 'dbirth': '', 'numbhist': '', 'd_enter': '', 't_enter': '', 'povtorno': 'повторно', 'dps': 'ДПС', 'dobrovol': 'добровольно', 'd_view': '', 't_view': '', 'doctor': 'Меньшиков Г.А.', 'zavotd': 'Меньшиков Г.А.', 'zaloba': 'нет', 'vipiska': '', 'area': 'Приморский', 'adress': '', 'an_live': '(со слов, по данным медсведений) ', 'an_bol': '(со слов, по данным медсведений) ', 'an_nark': 'Не курит. Алкоголем не злоупотребляет. ', 'iz_napr': '', 'priemn': '', 'votdele': '', 'somat': 'температура тела 36,6; ЧСС 80 в мин.; ЧД 16 в мин. АД 120\\80 мм.рт.ст. Кожные покровы и слизистые:   Опорно-двигательный аппарат: без видимых повреждений. Дыхательная система: дыхание жесткое, хрипов нет.  Сердечно-сосудистая система: сердечные тоны приглушены, шумов нет.  Пищеварительная система: живот мягкий, безболезненный. Мочевыделительная система: без жалоб, диурез не нарушен. Эндокринная система: без жалоб. Дополнения:   Гинекологический анамнез:', 'ginek': 'mensis с 13 лет, регулярные, безболезненные. Б-. Р-. А-.', 'nevrol': 'симптомы поражения ЧМН: отсутствуют. Зрачки:  одинакового размера; Реакция на свет: сохранена; Парезы, параличи: нет/есть; Координация движений: грубо не нарушена; Сухожильные и периостальные рефлексы: живые; Патологические рефлексы: нет; Менингеальные симптомы:  нет;', 'zabolevan': 'отр.', 'allerg': 'отр.', 'epid': 'туберкулезом, гепатитом А, В, С; брюшным тифом, малярией, дизентерией: не болела. Жидкий стул  и повышение температуры тела в последние 2 недели: отрицает. Венерические заболевания: отрицает; В 23:  отрицает. За последние 14 дней пределов РФ не покидала, аэропорт не посещала, с приезжими из-за рубежа не встречалась, с инфицированными COVID-19 не контактировала.', 'strah': 'инвалид  группы, по психическому заболеванию. Не работает, в ЦЗН не состоит. ЛН не нужен.', 'zakl': 'психические нарушения много лет. В анамнезе бредовая, галлюцинаторная симптоматика. С годами нарастает эмоционально-волевое снижение. В настоящее время в клинической картине бредовые идеи, обманы восприятия, эмоционально-волевые нарушения. Таким образом на первый выходит параноидный синдром.', 'diag_osn': '', 'diag_sop': '', 'treatment': '', 'dinamika': 'за время нахождения в отделении первое время состояние было неустойчивым, отмечались нарушения сна, поведение оставалось неупорядоченным, фон настроения был с колебаниями, в поведении обнаруживалась галлюцинаторная симптоматика, спонтанно звучали бредовые идеи, сохранялась выраженные напряженность и раздражительность. В дальнейшем наблюдалась положительная динамика, состояние стабилизировалось, выровнялся фон настроения, нормализовался сон, поведение стало упорядоченным, появилась критика к состоянию, психопродуктивная симптоматика нивелировалась. ', 'kvipiske': 'в настоящее время состояние длительно стабильное. Активно бредовых идей не высказывает. Обманы восприятия отрицает, косвенно в поведении не обнаруживает.  Фон настроения ровный. Эмоционально огрублена. Поведение упорядоченное. Без агрессивных, аутоагрессивных, депрессивных, суицидных и других опасных тенденций на момент осмотра. Признаков 29 ст. п. "а, б, в," нет. Данных для НГ нет.',  'recommendations': '1.Наблюдение ПНД по месту жительства. 2.Таб. рисполепт   0,002 - 0 - 0,002 в 10-00,  21-00, 2р/д, per os. ', 'department': '777', 'new_col': '', 'add_col': '', 'just_col': ''}
        try:
            dic['doctor'] = self.preferences.list_values[1]
            dic['zavotd'] = self.preferences.list_values[2]
        except:
            print('ok')

        self.list_obj = self.main_list_obj
        x = 0
        while x < len(self.list_obj):
            for k, i in dic.items():
                try:
                    self.list_obj[x].setText(dic[k])
                    x += 1
                    # print(x)
                except AttributeError:
                    self.list_obj[x].setCurrentText(dic[k])
                    x += 1
                    continue
                except IndexError:
                    break
        self.men_but3.setDisabled(False)
        self.men_but2.setDisabled(False)
        self.form_widget.btn_update.setDisabled(True)
        self.form_widget.btn_change.setDisabled(False)
        self.form_widget.change_background(1)



class Another_page(QWidget):
    def __init__(self):
        super().__init__()
        self.main_lay = QVBoxLayout()
        self.setLayout(self.main_lay)
        self.but_thesame = QPushButton('another page2')
        self.but_thesame.clicked.connect(self.another_page2)
        self.main_lay.addWidget(self.but_thesame, alignment=QtCore.Qt.AlignTop)
        self.show()

    def another_page2(self):
        MMW.stac_widg.setCurrentWidget(MMW.mw)


class Preferences_page(QWidget):
    def __init__(self, con):
        super().__init__()
        self.con = con
        self.path = os.getcwd()
        self.list_values = self.read_settings()
        self.show()
        self.visual_obj()

    def visual_obj(self):

        def save_but_fu():
            getfont = self.com_font.currentText()
            getsize = int(self.com_size.currentText())
            getsex = self.com_sex.currentText()
            get_fio_d = self.fio_doc_text.text()
            get_fio_z = self.fio_zav_text.text()
            get_otdel = self.otdel_t.text()
            print(getfont, getsize, getsex, get_fio_d, get_fio_z, get_otdel)
            self.record_settings(getfont, getsize, getsex, get_fio_d, get_fio_z, get_otdel)
            list_values = self.read_settings()
            self.font = QFont(list_values[0], list_values[3])
            list_f = [MMW.form_widget.fio_l, MMW.form_widget.fio_t, MMW.form_widget.datebirt_t,
                      MMW.form_widget.datebirt_l, MMW.form_widget.numbhis_t, MMW.form_widget.numbhis_l,
                      MMW.form_widget.dateenter_l, MMW.form_widget.dateenter_t, MMW.form_widget.timeenter,
                      MMW.form_widget.timeenter_t, MMW.form_widget.povtorno_t, MMW.form_widget.povtorno_l,
                      MMW.form_widget.dps_t, MMW.form_widget.dps_l, MMW.form_widget.dobrov_l,
                      MMW.form_widget.dobrov_t, MMW.form_widget.dateosm_t, MMW.form_widget.dateosm_l,
                      MMW.form_widget.timeosm_l, MMW.form_widget.timeosm_t, MMW.form_widget.area_l,
                      MMW.form_widget.doc_t, MMW.form_widget.doc_l, MMW.form_widget.zav_l,
                      MMW.form_widget.zav_t, MMW.form_widget.adres_t, MMW.form_widget.adres_l,
                      MMW.form_widget.coplain_l, MMW.form_widget.coplain_t, MMW.form_widget.anam_live_l,
                      MMW.form_widget.anam_live_t, MMW.form_widget.combo, MMW.form_widget.anam_dese_l,
                      MMW.form_widget.anam_dese_t, MMW.form_widget.anam_nark_l, MMW.form_widget.anam_nark_t,
                      MMW.form_widget.napravlee_l, MMW.form_widget.napravlee_t, MMW.form_widget.psyh_status,
                      MMW.form_widget.psy_st_pr_l, MMW.form_widget.psy_st_pr_t, MMW.form_widget.psy_st_ot_l,
                      MMW.form_widget.psy_st_ot_t, MMW.form_widget.somatikas_l, MMW.form_widget.somatikas_t,
                      MMW.form_widget.ginekolog_l, MMW.form_widget.ginekolog_t, MMW.form_widget.nevrologi_l,
                      MMW.form_widget.nevrologi_t, MMW.form_widget.concomita_l, MMW.form_widget.concomita_t,
                      MMW.form_widget.allergiaa_l, MMW.form_widget.allergiaa_t, MMW.form_widget.epidemiol_l,
                      MMW.form_widget.epidemiol_t, MMW.form_widget.strahovoi_l, MMW.form_widget.strahovoi_t,
                      MMW.form_widget.zakluchen_l, MMW.form_widget.zakluchen_t, MMW.form_widget.diagnozos_l,
                      MMW.form_widget.diagnozos_t, MMW.form_widget.diagnozso_l, MMW.form_widget.diagnozso_t,
                      MMW.data_base_page.tv, MMW.form_widget.treatment_t, MMW.form_widget.treatment_l,
                      MMW.form_widget.dinamika_t, MMW.form_widget.dinamika_l, MMW.form_widget.k_vipisk_t,
                      MMW.form_widget.k_vipisk_l, MMW.arcive_table.tv2, MMW.form_widget.prescribe_l,
                      MMW.form_widget.prescribe_t, MMW.form_widget.leave_t, MMW.form_widget.leave_l, self.clabel, self.slabel,
                      self.com_size, self.sex_label, self.com_sex, self.fio_doclabel, self.fio_doc_text, self.fio_zavlabel,
                      self.fio_zav_text, self.com_font, self.otdel_l, self.otdel_t, MMW.form_widget.firs_os, MMW.form_widget.btn_pre,
                      MMW.form_widget.btn_vkk, MMW.form_widget.btn_prt, MMW.form_widget.btn_lnd, MMW.form_widget.btn_hiv,
                      MMW.form_widget.btn_gam, MMW.form_widget.btn_ian, MMW.form_widget.btn_est, MMW.form_widget.btn_car,
                      MMW.form_widget.btn_sta, MMW.form_widget.btn_msv, MMW.form_widget.btn_change, MMW.form_widget.btn_update,
                      MMW.form_widget.com_diag_osn, MMW.form_widget.com_diag_sin, MMW.form_widget.com_diag_sop, ]
            for i in list_f:
                i.setFont(self.font)
            MMW.form_widget.doc_t.setText(get_fio_d)
            MMW.form_widget.zav_t.setText(get_fio_z)
            print(str(self.font))

        self.vv_lay = QVBoxLayout()
        perf_grid = QGridLayout()
        self.setLayout(self.vv_lay)
        self.vv_lay.addLayout(perf_grid, stretch=0)


        self.clabel = QLabel('Шрифт')
        try:
            self.clabel.setFont(QFont(self.list_values[0], self.list_values[3]))
        except IndexError:
            self.clabel.setFont(QFont('Times Font', 12))
        self.com_font = QComboBox()
        self.com_font.addItems(['Times Font', 'Arial', 'Courier New', 'Times', 'Helvetica'])
        try:
            self.com_font.setCurrentText(self.list_values[0])
        except IndexError:
            self.com_font.setCurrentText('Times Font')
        try:
            self.com_font.setFont(QFont(self.list_values[0], self.list_values[3]))
        except IndexError:
            self.com_font.setFont(QFont('Times Font', 12))
        # self.com_font.activated[str].connect(self.onActivated)
        self.slabel = QLabel('Размер шрифта')
        try:
            self.slabel.setFont(QFont(self.list_values[0], self.list_values[3]))
        except IndexError:
            self.slabel.setFont(QFont('Times Font', 12))
        self.com_size = QComboBox()
        self.com_size.addItems(['10', '11', '12', '13', '14', '16'])
        self.com_size.setEditable(True)
        try:
            self.com_size.setCurrentText(str(self.list_values[3]))
        except IndexError:
             self.com_size.setCurrentText('12')
        try:
            self.com_size.setFont(QFont(self.list_values[0], self.list_values[3]))
        except IndexError:
            self.com_size.setFont(QFont('Times Font', 12))
        # self.com_size.activated[str].connect(self.onActivated)
        self.sex_label = QLabel('Пол')
        try:
            self.sex_label.setFont(QFont(self.list_values[0], self.list_values[3]))
        except IndexError:
            self.sex_label.setFont(QFont('Times Font', 12))
        self.com_sex = QComboBox()
        self.com_sex.addItems(['мужчины', 'женщины'])
        try:
            self.com_sex.setCurrentText(self.list_values[4])
        except IndexError:
            self.com_sex.setCurrentText('женщины')
        try:
            self.com_sex.setFont(QFont(self.list_values[0], self.list_values[3]))
        except IndexError:
            self.com_sex.setFont(QFont('Times Font', 12))
        # self.com_sex.activated[str].connect(self.onActivated)

        self.fio_doclabel = QLabel('"Фамилия И.О." врача:')
        try:
            self.fio_doclabel.setFont(QFont(self.list_values[0], self.list_values[3]))
        except IndexError:
            self.fio_doclabel.setFont(QFont('Times Font', 12))
        self.fio_doc_text = QLineEdit()
        try:
            self.fio_doc_text.setText(self.list_values[1])
        except IndexError:
            self.fio_doc_text.setText('Меньшиков Г.А.')
        try:
            self.fio_doc_text.setFont(QFont(self.list_values[0], self.list_values[3]))
        except IndexError:
            self.fio_doc_text.setFont(QFont('Times Font', 12))

        self.fio_zavlabel = QLabel('"Фамилия И.О." зав.отд.:')
        try:
            self.fio_zavlabel.setFont(QFont(self.list_values[0], self.list_values[3]))
        except IndexError:
            self.fio_zavlabel.setFont(QFont('Times Font', 12))
        self.fio_zav_text = QLineEdit()
        try:
            self.fio_zav_text.setText(self.list_values[2])
        except IndexError:
            self.fio_zav_text.setText('Меньшиков Г.А.')
        try:
            self.fio_zav_text.setFont(QFont(self.list_values[0], self.list_values[3]))
        except IndexError:
            self.fio_zav_text.setFont(QFont('Times Font', 12))
        self.otdel_l = QLabel('Номер отделения:')
        try:
            self.otdel_l.setFont(QFont(self.list_values[0], self.list_values[3]))
        except IndexError:
            self.otdel_l.setFont(QFont('Times Font', 12))
        self.otdel_t = QLineEdit()
        try:
            self.otdel_t.setText(self.list_values[5])
        except IndexError:
            self.otdel_t.setText(' ')
        try:
            self.otdel_t.setFont(QFont(self.list_values[0], self.list_values[3]))
        except IndexError:
            self.otdel_t.setFont(QFont('Times Font', 12))
        perf_grid.addWidget(self.clabel, 0, 0)
        perf_grid.addWidget(self.com_font, 0, 1)
        perf_grid.addWidget(self.slabel, 1, 0)
        perf_grid.addWidget(self.com_size, 1, 1)
        perf_grid.addWidget(self.sex_label, 2, 0)
        perf_grid.addWidget(self.com_sex, 2, 1)
        perf_grid.addWidget(self.fio_doclabel, 3, 0)
        perf_grid.addWidget(self.fio_doc_text, 3, 1)
        perf_grid.addWidget(self.fio_zavlabel, 4, 0)
        perf_grid.addWidget(self.fio_zav_text, 4, 1)
        perf_grid.addWidget(self.otdel_l, 5, 0)
        perf_grid.addWidget(self.otdel_t, 5, 1)
        self.save_but = QPushButton('Сохранить изменения')
        self.vv_lay.addWidget(self.save_but, alignment=QtCore.Qt.AlignTop)
        self.save_but.clicked.connect(save_but_fu)

        # return [getfont, getsize, getsex, get_fio_d, get_fio_z]

    def onActivated(self, text):
        self.text = text
        self.combotext = self.com_font.currentText()
        print(self.text, self.combotext)
        return self.text

    def record_settings(self, fontt, size, sex, fio_doc, fio_zav, otdel):

        self.font_t = fontt
        self.size = size
        self.fio_doc = fio_doc
        self.fio_zav = fio_zav
        self.sex = sex
        self.otdel = otdel

        print(self.font_t, self.size, self.fio_zav, self.fio_doc, self.sex, self.otdel, 'это проверка данных на вход ')

        if self.con.isOpen():
            print('{}/prefer.db'.format(self.path), 'строка из if метода record setting')
        else:
            self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            self.path = os.getcwd()
            print('{}/prefer.db'.format(self.path), 'строка из else метода record set')
            self.con.setDatabaseName('{}/prefer.db'.format(self.path))
            ## con.setDatabaseName('//Users//user//PycharmProjects//razrabotka//prefer.db')
            self.con.open()


        if 'settings' not in self.con.tables():
            query = QtSql.QSqlQuery()
            query.exec('create table settings(id integer primary key autoincrement, font text, size integer, fio_doc text, fio_zav text, sex text, otdel text)')
            query.finish()

        # query = QtSql.QSqlQuery()
        # query.prepare('INSERT INTO settings (id, font, size, fio_doc, fio_zav, sex) '
        #                 'VALUES (null, :font, :size, :fio_doc, :fio_zav, :sex)')
        # query.bindValue(':font', self.font_t)
        # query.bindValue(':size', self.size)
        # query.bindValue(':fio_doc', self.fio_doc)
        # query.bindValue(':fio_zav', self.fio_zav)
        # query.bindValue(':sex', self.sex)
        # query.exec_()
        # query.finish()

        stm = QtSql.QSqlTableModel()
        stm.setTable('settings')
        stm.select()

        rec = self.con.record('settings')  # получает сведения о  таблице в которую добавит запись рекорд
        rec.setValue('font', self.font_t)
        rec.setValue('size', self.size)
        rec.setValue('fio_doc', self.fio_doc)
        rec.setValue('fio_zav', self.fio_zav)
        rec.setValue('sex', self.sex)
        rec.setValue('otdel', self.otdel)
        stm.insertRecord(-1, rec)



        rec = stm.record(0)  # получает сведения о записи в таблице в которой будет заменены данные
        rec.setValue('font', self.font_t)
        rec.setValue('size', self.size)
        rec.setValue('fio_doc', self.fio_doc)
        rec.setValue('fio_zav', self.fio_zav)
        rec.setValue('sex', self.sex)
        rec.setValue('otdel', self.otdel)
        stm.setRecord(0, rec)


        stm.removeRow(1)  # удаляет строку, а следующая строка, обновляет данные чтобы обновиться таблицу, удалив пустую строку
        stm.select()



    def read_settings(self):

        if self.con.isOpen():
            print('{}/prefer.db'.format(self.path), 'строка из if метода read setting')
        else:
            self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            self.path = os.getcwd()
            print('{}/prefer.db'.format(self.path), 'строка из else метода read settings')
            self.con.setDatabaseName('{}/prefer.db'.format(self.path))
            ## con.setDatabaseName('//Users//user//PycharmProjects//razrabotka//prefer.db')
            self.con.open()

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
                lst.append(query.value('otdel'))
                query.next()
        query.finish()

        print(lst[:7])
        return lst[:7]


app = QApplication([])

a = datetime.date.today()
b = datetime.date(2021, 7, 15)
print(a, b)
razn = b - a

if 10 >= razn.days > 1:
    print('код запускаем но с ошибкой')
    MMW = MyMainWindow()
    er_wid = QWidget()
    er_wid.show()
    er_lay = QVBoxLayout()
    rax = b - a
    print(rax)

    print(type(rax))
    l = QLabel(f'ошибка! Осталось {rax.days} дней')

    er_lay.addWidget(l, alignment=QtCore.Qt.AlignCenter)
    er_wid.setLayout(er_lay)

elif a >= b:
    print('код запускаем')
    er_wid = QWidget()
    er_wid.show()
    er_lay = QVBoxLayout()
    rax = b - a
    print(rax)

    print(type(rax))
    l = QLabel(f'ошибка необходимо переустановить программу')

    er_lay.addWidget(l, alignment=QtCore.Qt.AlignCenter)
    er_wid.setLayout(er_lay)



elif a <= b:
    MMW = MyMainWindow()

sys.exit(app.exec_())
