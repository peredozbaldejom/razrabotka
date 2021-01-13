# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction,
                             QWidget, QPushButton, QToolTip, QMessageBox,
                             QTextEdit, QLabel, QHBoxLayout, QVBoxLayout,
                             QLineEdit, QTextEdit, QGridLayout, QLCDNumber,
                             QSlider, QInputDialog, QFileDialog, QFrame,
                             QFrame, QSplitter, QStyleFactory, QPlainTextEdit,
                             QComboBox, QCompleter, QDesktopWidget, qApp,
                             QSizePolicy, QTableView, )
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




class FormWidget(QWidget):

    def __init__(self, con, dic):
        super().__init__()
        self.con = con
        self.emp_dic = dic
        #self.list_obj = list_obj



        self.path = os.getcwd()

        self.list_with_prefer = self.get_prefer_from_db()
        self.list_contents_qtext = self.change_sex()
        print(self.list_contents_qtext, 'список содержимого который пойдет в форму', self.list_with_prefer[4])

        self.all_layout = QVBoxLayout(self)

        self.grid_info = QGridLayout(self)
        self.other = QVBoxLayout(self)

        self.fio_l = self.create_obj('l', 0, 0, 'Фамилия И.О.')
        self.fio_t = self.create_obj('t', 0, 1, row1=3, )
        self.datebirt_l = self.create_obj('l', 0, 4, 'Дата рождения:')
        self.datebirt_t = self.create_obj('t', 0, 5)
        self.numbhis_l = self.create_obj('l', 1, 0, '№ истории:')
        self.numbhis_t = self.create_obj('t', 1, 1)
        self.dateenter_l = self.create_obj('l', 1, 2, 'Дата поступ.:')
        self.dateenter_t = self.create_obj('t', 1, 3)
        self.timeenter = self.create_obj('l', 1, 4, 'Время поступ.:')
        self.timeenter_t = self.create_obj('t', 1, 5)
        self.povtorno_l = self.create_obj('l', 2, 0, 'В ГПБ№3:')
        self.povtorno_t = self.create_obj('t', 2, 1, 'повторно')
        self.dps_l = self.create_obj('l', 2, 2, 'Направлен:')
        self.dps_t = self.create_obj('t', 2, 3, 'ДПС')
        self.dobrov_l = self.create_obj('l', 2, 4, 'Госпитализация:')
        self.dobrov_t = self.create_obj('t', 2, 5, 'добровольно')
        self.dateosm_l = self.create_obj('l', 3, 0, 'Дата осмотра:')
        self.dateosm_t = self.create_obj('t', 3, 1)
        self.timeosm_l = self.create_obj('l', 3, 2, 'Время осмотра:')
        self.timeosm_t = self.create_obj('t', 3, 3)
        self.area_l = self.create_obj('l', 3, 4, 'Район:')
        self.combo = MyQComboBox(self)
        self.combo.addItems(['Красногвардейский', 'Приморский', 'Калининский', 'Невский', 'Кронштадский', 'Выборгский', 'Курортный'])
        self.combo.activated[str].connect(self.onActivated)
        self.combo.setEditable(True)
        self.combo.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.combo.setCurrentText('Приморский')
        try:
            self.combo.setFont(QFont(self.list_with_prefer[0], self.list_with_prefer[3]))
        except IndexError:
            self.combo.setFont(QFont('Times Font', 12))
        self.grid_info.addWidget(self.combo, 3, 5)
        # self.area_t = self.create_obj('t', 3, 5)
        self.doc_l = self.create_obj('l', 4, 0, 'Ф.И.О. врача:')
        try:
            self.doc_t = self.create_obj('t', 4, 1, text=self.list_with_prefer[1])
        except IndexError:
            self.doc_t = self.create_obj('t', 4, 1)
        self.zav_l = self.create_obj('l', 4, 2, 'Зав.отд.:')
        try:
            self.zav_t = self.create_obj('t', 4, 3, text=self.list_with_prefer[2])
        except IndexError:
            self.zav_t = self.create_obj('t', 4, 3)
        self.adres_l = self.create_obj('l', 4, 4, 'Адрес проживания:')
        self.adres_t = self.create_obj('t', 4, 5)
        self.coplain_l = self.create_obj('l', 5, 0, 'Жалобы:')
        self.coplain_t = self.create_obj('t', 5, 1, 'нет', row1=3)
        self.leave_l = self.create_obj('l', 5, 4, 'Дата выписки:')
        self.leave_t = self.create_obj('t', 5, 5, '')

        self.all_layout.addLayout(self.grid_info)  # разместили сетку  на главном лэйауте

        #self.anam_live_l = self.create_lab_qtext('l', 'Анамнез жизни:')
        self.anam_live_l = QPushButton('Анамнез жизни:')
        self.other.addWidget(self.anam_live_l, alignment=QtCore.Qt.AlignLeft)
        self.anam_live_l.clicked.connect(lambda: self.text_to_textedit('live'))
        self.anam_live_l.setMinimumWidth(5)
                                         
        self.anam_live_t = self.create_lab_qtext('t', '(со слов, по данным медсведений) ', he=70)

        #self.anam_dese_l = self.create_lab_qtext('l', 'Анамнез болезни:')
        self.anam_dese_l = QPushButton('Анамнез болезни:')
        self.other.addWidget(self.anam_dese_l, alignment=QtCore.Qt.AlignLeft)
        self.anam_dese_l.clicked.connect(lambda: self.text_to_textedit('dese'))
        self.anam_dese_l.setMinimumWidth(5)

        self.anam_dese_t = self.create_lab_qtext('t', '(со слов, по данным медсведений) ', he=70)
        self.anam_nark_l = self.create_lab_qtext('l', 'Наркологический анамнез:')
        self.anam_nark_t = self.create_lab_qtext('t', 'не курит. Алкоголем не злоупотребляет. ')
        self.napravlee_l = self.create_lab_qtext('l', 'Из направления:', he=70)
        self.napravlee_t = self.create_lab_qtext('t', )
        self.psyh_status = self.create_lab_qtext('l', 'Психический статус:')
        self.psy_st_pr_l = self.create_lab_qtext('l', 'В приемном покое:')
        self.psy_st_pr_t = self.create_lab_qtext('t', he=70)
        #self.psy_st_ot_l = self.create_lab_qtext('l', 'В отделении:')

        self.psy_st_ot_l = QPushButton('В отделении:')
        self.other.addWidget(self.psy_st_ot_l, alignment=QtCore.Qt.AlignLeft)
        self.psy_st_ot_l.clicked.connect(lambda: self.text_to_textedit('psyh'))
        self.psy_st_ot_l.setMinimumWidth(5)


        self.psy_st_ot_t = self.create_lab_qtext('t', he=70)
        self.somatikas_l = self.create_lab_qtext('l', 'Соматический статус:')
        self.somatikas_t = self.create_lab_qtext('t', self.list_contents_qtext[1], he=110)
        self.ginekolog_l = self.create_lab_qtext('l', 'Гинекологический анамнез:')
        self.ginekolog_t = self.create_lab_qtext('t', self.list_contents_qtext[2], he=30)
        self.nevrologi_l = self.create_lab_qtext('l', 'Неврологический статус:')
        self.nevrologi_t = self.create_lab_qtext('t', 'симптомы поражения ЧМН: отсутствуют. Зрачки:  одинакового размера; Реакция на свет: сохранена; Парезы, параличи: нет/есть; Координация движений: грубо не нарушена; Сухожильные и периостальные рефлексы: живые; Патологические рефлексы: нет; Менингеальные симптомы:  нет;', he=70)
        self.concomita_l = self.create_lab_qtext('l', 'Хронические соматические заболения по поводу которых пациента постоянно принимает медикаменты:', he=110)
        self.concomita_t = self.create_lab_qtext('t', 'отр.', he=50)
        self.allergiaa_l = self.create_lab_qtext('l', 'Аллергологический анамнез:')
        self.allergiaa_t = self.create_lab_qtext('t', 'отр.', he=50)
        self.epidemiol_l = self.create_lab_qtext('l', 'Эпидемиологически анамнез: ')
        self.epidemiol_t = self.create_lab_qtext('t', self.list_contents_qtext[3], he=70)
        self.strahovoi_l = self.create_lab_qtext('l', 'Страховой анамнез:')
        self.strahovoi_t = self.create_lab_qtext('t', 'инвалид  группы, по психическому заболеванию. Не работает, в ЦЗН не состоит. ЛН не нужен.', he=50)
        self.zakluchen_l = self.create_lab_qtext('l', 'Заключение:')
        self.zakluchen_t = self.create_lab_qtext('t', 'психические нарушения много лет. В анамнезе бредовая, галлюцинаторная симптоматика. С годами нарастает эмоционально-волевое снижение. В настоящее время в клинической картине бредовые идеи, обманы восприятия, эмоционально-волевые нарушения. Таким образом на первый выходит параноидный синдром.', he=70)

        self.diagnozos_l = self.create_lab_qtext('l', 'Диагноз основной:')

        self.com_diag_osn = MyQComboBox()
        self.com_diag_osn.addItems([' ', 'шизофрения, параноидная форма. Непрерывный тип течения. Эмоционально-волевой дефект. F20.0 ', 'умственная отсталость легкой степени со значительными нарушениями поведения требующими лечения. F70.1 ', 'другие психотические расстройства, в связи со смешанными заболеваниями. F06.818 ', 'другие непсихотические расстройства, в связи со смешанными заболеваниями. F06.828 ', 'абстинентное состояние с делирием, вызванное употреблением алкоголя.  F10.4 '])
        self.com_diag_osn.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.com_diag_osn.activated[str].connect(lambda: self.from_combo_to_edit(self.diagnozos_t, self.com_diag_osn))
        #self.com_diag_osn.setEditable(True)
        self.com_diag_osn.setFocusPolicy(QtCore.Qt.NoFocus)
        try:
            self.com_diag_osn.setFont(QFont(self.list_with_prefer[0], self.list_with_prefer[3]))
        except IndexError:
            self.com_diag_osn.setFont(QFont('Times Font', 12))

        #self.com_diag_osn.setCurrentText('Шизофрения, параноидная форма. Непрерывный тип течения. Эмоционально-волевой дефект. F20.0')
        self.other.addWidget(self.com_diag_osn)

        self.com_diag_sin = MyQComboBox()
        self.com_diag_sin.addItems([' ', 'Параноидный синдром. ', 'Галлюцинаторно-бредовой синдром. ', 'Аффективно-бредовой синдром. ', 'Психопатоподобный синдром. ', 'Депрессивный синдром. ', 'Судорожный синдром в анамнезе. ', 'Психоорганический синдром. ', 'Тревожно-диссомнический синдром. '])
        self.com_diag_sin.activated[str].connect(lambda: self.from_combo_to_edit(self.diagnozos_t, self.com_diag_sin))
        #self.com_diag_sin.setEditable(True)
        #self.com_diag_sin.setCurrentText('Параноидный синдром. ')

        try:
            self.com_diag_sin.setFont(QFont(self.list_with_prefer[0], self.list_with_prefer[3]))
        except IndexError:
            self.com_diag_sin.setFont(QFont('Times Font', 12))
        self.other.addWidget(self.com_diag_sin)

        self.diagnozos_t = self.create_lab_qtext('t', he=70)

        self.com_diag_sop = MyQComboBox()
        self.com_diag_sop.addItems(['   _', 'Гипертоническая болезнь 2 ст. ', 'Сахарный диабет, 2 тип. ', 'Аутоиммунный тиреоидит. ', 'Цереброваскулярная болезнь. ', 'Дисцирукуляторная энцефалопатия. ', 'Эпилепсия. ', 'U07.1 – Коронавирусная инфекция COVID‑19, вирус идентифицирован. ', 'U07.2 – Коронавирусная инфекция COVID‑19, вирус не идентифицирован. ', 'Z03.8 – Наблюдение при подозрении на коронавирусную инфекцию', 'Z22.8 – Носительство возбудителя коронавирусной инфекции', 'Z20.8 – Контакт с больным коронавирусной инфекцией', 'Z11.5 – Скрининговое обследование по коронавирусной инфекции', 'В34.2 – Коронавирусная инфекция неуточненная (кроме COVID‑19)', 'В33.8 – Коронавирусная инфекция уточненная (кроме COVID‑19)','Z29.0 – Изоляция' ])
        self.com_diag_sop.activated.connect(lambda: self.from_combo_to_edit(self.diagnozso_t, self.com_diag_sop))
        #self.com_diag_sop.setEditable(True)
        self.com_diag_sop.setCurrentText('')
        try:
            self.com_diag_sop.setFont(QFont(self.list_with_prefer[0], self.list_with_prefer[3]))
        except IndexError:
            self.com_diag_sop.setFont(QFont('Times Font', 12))

        self.other.addWidget(self.com_diag_sop)

        self.diagnozso_l = self.create_lab_qtext('l', 'Диагноз сопутствующий:')
        self.diagnozso_t = self.create_lab_qtext('t', he=50)

        self.treatment_l = self.create_lab_qtext('l', 'Лечение:')

        self.com_treatment = MyQComboBox()
        self.com_treatment.addItems([' ', 'Ограничительный режим (агр.)  ', 'Ограничительный режим (депр.)  ', 'Режим эпид. изоляции  ', 'Cтол ОВД   ', 'Стол ОВД9',  'Sol. Phenazepami 0,1% - 2,0  в/м; в 10-00, 21-00; 1 р/д; №3   ', 'Sol. Haloperidoli 0,5% - 1,0  в/м; 2 р/д; в 10-00, 21-00; №3  ', 'Sol. Clopixoli-acuphasi 5% - 1,0 в/м; 1 раз в 2 дня; в 10-00; №3  ', 'Tab. Quetiapini 0.025  per os; 2 р/д; в 10-00, 20-00  ', 'Tab. Rispolept 0.002 per os; 1 р/д; в 20-00  ', 'Tab. Olanzapini 0.01 per os; 1 р/д; в 20-00  ', 'Tab. Alimemazini 0.01 per os; 1 р/д; в 20-00', 'Tab. Trazodoni 0.05 per os; 1 р/д; в 20-00', 'Tab. Chlorprothixeni 0.015 per os; 1 р/д; в 20-00', 'Tab. Escitaloprami 0.01 per os; 1 р/д; в 20-00'])
        self.com_treatment.activated.connect(lambda: self.from_combo_to_edit(self.treatment_t, self.com_treatment))
        #self.com_diag_sop.setEditable(True)
        self.com_treatment.setCurrentText('')
        try:
            self.com_treatment.setFont(QFont(self.list_with_prefer[0], self.list_with_prefer[3]))
        except IndexError:
            self.com_treatment.setFont(QFont('Times Font', 12))
        self.other.addWidget(self.com_treatment)

        self.treatment_t = self.create_lab_qtext('t', )

        # self.create_fir_and_epic = QPushButton('создание первичного осмотра и медсведений')
        # self.other.addWidget(self.create_fir_and_epic)
        # self.create_fir_and_epic.clicked.connect(self.save_as_name)
        vbox_but = QVBoxLayout()
        self.other.addLayout(vbox_but)
        self.btn_change = QPushButton('сохранить как нового пациента')
        vbox_but.addWidget(self.btn_change)

        gbox_but = QGridLayout()
        gbox_but.setSpacing(1)
        self.other.addLayout(gbox_but)
        self.firs_os = QPushButton('первичный')
        self.btn_pre = QPushButton('лист назн')
        self.btn_vkk = QPushButton('вк рв повт')
        self.btn_prt = MyQComboBox()
        self.btn_prt.addItems(['   протокол', 'F00.0-F00.3', 'F06.4 - F06.3', 'F06.8 06.2 06.0', 'F10.2 - F19.2', 'F10.3 - F19.3', 'F10.5 - F19.5', 'F20', 'F21 22 23 25', 'F30 - F39', 'F31.3 - F33.2', 'F40 41 43 44 45', 'F60',  'F70-F79', 'G20', 'G40.0'])
        self.btn_prt.setEditable(False)
        self.btn_lnd = QPushButton('лист нетруд')
        self.btn_hiv = QPushButton('ВИЧ')
        self.btn_gam = QPushButton('Гамильтон')
        self.btn_ian = QPushButton('Янг')
        self.btn_est = QPushButton('карта оценки')
        self.btn_car = QPushButton('учетная карта')
        self.btn_sta = QPushButton('перевод') #потом стат карту
        self.btn_msv = QPushButton('медсведния')

        gbox_but.addWidget(self.firs_os, 0, 0)
        gbox_but.addWidget(self.btn_pre, 0, 1)
        gbox_but.addWidget(self.btn_vkk, 0, 2)
        gbox_but.addWidget(self.btn_prt, 0, 3)
        gbox_but.addWidget(self.btn_lnd, 0, 4)
        gbox_but.addWidget(self.btn_hiv, 0, 5)
        gbox_but.addWidget(self.btn_gam, 1, 0)
        gbox_but.addWidget(self.btn_ian, 1, 1)
        gbox_but.addWidget(self.btn_est, 1, 2)
        gbox_but.addWidget(self.btn_sta, 1, 3)
        gbox_but.addWidget(self.btn_car, 1, 4)
        gbox_but.addWidget(self.btn_msv, 1, 5)
        #self.btn_change.clicked.connect(self.changed_font)
        btn_lis = [self.btn_change, self.firs_os, self.btn_pre,  self.btn_vkk,  self.btn_prt,  self.btn_lnd,  self.btn_hiv,  self.btn_gam,
                   self.btn_ian,  self.btn_est,  self.btn_car,  self.btn_sta,  self.btn_msv]
        for i in btn_lis:
            try:
                i.setFont(QFont(self.list_with_prefer[0], self.list_with_prefer[3]))
            except IndexError:
                i.setFont(QFont('Times Font', 12))


        self.dinamika_l = self.create_lab_qtext('l', 'Динамика в отделении:')
        self.dinamika_t = self.create_lab_qtext('t', 'за время нахождения в отделении первое время состояние было неустойчивым, отмечались нарушения сна, поведение оставалось неупорядоченным, фон настроения был с колебаниями, в поведении обнаруживалась галлюцинаторная симптоматика, спонтанно звучали бредовые идеи, сохранялась выраженные напряженность и раздражительность. В дальнейшем наблюдалась положительная динамика, состояние стабилизировалось, выровнялся фон настроения, нормализовался сон, поведение стало упорядоченным, появилась критика к состоянию, психопродуктивная симптоматика нивелировалась. ', he=100)
        self.k_vipisk_l = self.create_lab_qtext('l', 'К выписке:')
        self.k_vipisk_t = self.create_lab_qtext('t', 'в настоящее время состояние длительно стабильное. Активно бредовых идей не высказывает. Обманы восприятия отрицает, косвенно в поведении не обнаруживает.  Фон настроения ровный. Эмоционально огрублена. Поведение упорядоченное. Без агрессивных, аутоагрессивных, депрессивных, суицидных и других опасных тенденций на момент осмотра. Признаков 29 ст. п. "а, б, в," нет. Данных для НГ нет.', he=100)

        self.prescribe_l = self.create_lab_qtext('l', 'Рекомендовано:')
        self.prescribe_t = self.create_lab_qtext('t', '1.Наблюдение ПНД по месту жительства. 2. ')

        self.btn_update = QPushButton('Сохранить изменения')
        self.btn_update.setDisabled(True)
        
        self.other.addWidget(self.btn_update)

        self.all_layout.addLayout(self.other)
        self.setLayout(self.all_layout)




        #self.anam_live_t.document().contentsChanged.connect(lambda: self.sizeChange(self.anam_live_t))
        #self.anam_dese_t.document().contentsChanged.connect(lambda: self.sizeChange(self.anam_dese_t))
        #self.napravlee_t.document().contentsChanged.connect(lambda: self.sizeChange(self.napravlee_t))

        # self.firs_os.clicked.connect(self.first)
        # self.btn_msv.clicked.connect(self.medsv)
        self.firs_os.clicked.connect(lambda: self.all_filles_btn('первичка'))
        self.btn_pre.clicked.connect(lambda: self.all_filles_btn('листыназ'))
        self.btn_vkk.clicked.connect(lambda: self.all_filles_btn('вк рв'))
        self.btn_prt.activated.connect(lambda: self.all_filles_btn(self.btn_prt.currentText()))
        self.btn_lnd.clicked.connect(lambda: self.all_filles_btn('вк лн'))
        self.btn_hiv.clicked.connect(lambda: self.all_filles_btn('ВИЧ'))
        self.btn_gam.clicked.connect(lambda: self.all_filles_btn('гамильтон'))
        self.btn_ian.clicked.connect(lambda: self.all_filles_btn('янг'))
        self.btn_est.clicked.connect(lambda: self.all_filles_btn('карта оценки'))
        self.btn_car.clicked.connect(lambda: self.all_filles_btn('учетная карта'))
        self.btn_sta.clicked.connect(lambda: self.all_filles_btn('перевод'))
        self.btn_msv.clicked.connect(lambda: self.all_filles_btn('медсведения'))


    def change_sex(self):
        try:
            sex = self.list_with_prefer[4]
        except IndexError:
            sex = 'женщины'
        if sex == 'мужчины':
            list_contents_textedit = ['уроженец города . Наследственность по психической линии не отягощена. Раннее развитие без особенностей. В школу пошел с 7 лет. Успевал средне. Окончил  классов. Далее учебу продолжил в . Получил  образование по специальности  . Работал  . Женат не был. Детей  . Проживает с  в квартире. Отношения в семье  . ', 'температура тела 36,6; ЧСС 80 в мин.; ЧД 16 в мин. АД 120\80 мм.рт.ст. Кожные покровы и слизистые:   Опорно-двигательный аппарат: без видимых повреждений. Дыхательная система: дыхание жесткое, хрипов нет.  Сердечно-сосудистая система: сердечные тоны приглушены, шумов нет. Пищеварительная система: живот мягкий, безболезненный. Мочевыделительная система: без жалоб, диурез не нарушен. Эндокринная система: без жалоб. Дополнения:   ', ' ', 'туберкулезом, гепатитом А, В, С; брюшным тифом, малярией, дизентерией: не болел. Жидкий стул  и повышение температуры тела в последние 2 недели: отрицает. Венерические заболевания: отрицает; В 23:  отрицает. За последние 14 дней пределов РФ не покидал, аэропорт не посещал, с приезжими из-за рубежа не встречался, с инфицированными COVID-19 не контактировал.', ]
            #self.ginekolog_t.setDisabled(True)
        elif sex == 'женщины':
            list_contents_textedit = ['уроженка города . Наследственность по психической линии не отягощена. Раннее развитие без особенностей. В школу пошла с 7 лет. Успевала средне. Окончила  классов. Далее учебу продолжила в . Получила  образование по специальности  . Работала  . Замужем не была. Детей  . Проживает с  в квартире. Отношения в семье  . ', 'температура тела 36,6; ЧСС 80 в мин.; ЧД 16 в мин. АД 120\80 мм.рт.ст. Кожные покровы и слизистые:   Опорно-двигательный аппарат: без видимых повреждений. Дыхательная система: дыхание жесткое, хрипов нет.  Сердечно-сосудистая система: сердечные тоны приглушены, шумов нет. Пищеварительная система: живот мягкий, безболезненный. Мочевыделительная система: без жалоб, диурез не нарушен. Эндокринная система: без жалоб. Дополнения:   Гинекологический анамнез: ', 'mensis с 13 лет, регулярные, безболезненные. Б-. Р-. А-.', 'туберкулезом, гепатитом А, В, С; брюшным тифом, малярией, дизентерией: не болела. Жидкий стул  и повышение температуры тела в последние 2 недели: отрицает. Венерические заболевания: отрицает; В 23:  отрицает. За последние 14 дней пределов РФ не покидала, аэропорт не посещала, с приезжими из-за рубежа не встречалась, с инфицированными COVID-19 не контактировала.', ]
        else:
            list_contents_textedit = ['уроженка города . Наследственность по психической линии не отягощена. Раннее развитие без особенностей. В школу пошла с 7 лет. Успевала средне. Окончила  классов. Далее учебу продолжила в . Получила  образование по специальности  . Работала  . Замужем не была. Детей  . Проживает с  в квартире. Отношения в семье  . ', 'температура тела 36,6; ЧСС 80 в мин.; ЧД 16 в мин. АД 120\80 мм.рт.ст. Кожные покровы и слизистые:   Опорно-двигательный аппарат: без видимых повреждений. Дыхательная система: дыхание жесткое, хрипов нет.  Сердечно-сосудистая система: сердечные тоны приглушены, шумов нет. Пищеварительная система: живот мягкий, безболезненный. Мочевыделительная система: без жалоб, диурез не нарушен. Эндокринная система: без жалоб. Дополнения:   Гинекологический анамнез: ', 'mensis с 13 лет, регулярные, безболезненные. Б-. Р-. А-.', 'туберкулезом, гепатитом А, В, С; брюшным тифом, малярией, дизентерией: не болела. Жидкий стул  и повышение температуры тела в последние 2 недели: отрицает. Венерические заболевания: отрицает; В 23:  отрицает. За последние 14 дней пределов РФ не покидала, аэропорт не посещала, с приезжими из-за рубежа не встречалась, с инфицированными COVID-19 не контактировала.', ]

        return list_contents_textedit




    def sizeChange(self, i):
        print('я тут', i)
        self.heightMin = 150
        self.heightMax = 65000
        docHeight = i.document().size().height()
        if self.heightMin <= docHeight <= self.heightMax:
            i.setMinimumHeight(docHeight)

    def change_background(self, var=0):
        if var == 1:
            appearance = self.palette()
            appearance.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window, QtGui.QColor(242, 242, 242))
            self.setPalette(appearance)

            
        else:
            appearance = self.palette()
            appearance.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window, QtGui.QColor(221, 195, 95))
            self.setPalette(appearance)

    def text_to_textedit(self, str):
        if str == 'live':
            self.anam_live_t.insertPlainText(self.list_contents_qtext[0])
        elif str == 'dese':
            self.anam_dese_t.insertPlainText('психическое заболевание с  года. Когда стали отмечаться  . В дальнейшем присоединились  . Накануне госпитализации  .')
        elif str == 'psyh':
            self.psy_st_ot_t.insertPlainText('сознание не помрачено. Ориентирована . Внешне . Голос . Речь . В беседу вступает охотно. На вопросы отвечает по существу. Сообщает: "". Данные направления не отрицает. Обманы восприятия отрицает. Мышление . Внимание . Интеллектуально-мнестически . Фон настроения . Эмоционально . Личностно . В поведении . Критика к состоянию . ')

    def get_prefer_from_db(self):
        if self.con.isOpen():
            print('{}/prefer.db'.format(self.path), 'строка из if метода record setting')
        else:
            self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            self.path = os.getcwd()
            print('{}/prefer.db'.format(self.path), 'строка из else метода record set')
            self.con.setDatabaseName('{}/prefer.db'.format(self.path))
            ## con.setDatabaseName('//Users//user//PycharmProjects//razrabotka//prefer.db')
            self.con.open()

        self.query = QtSql.QSqlQuery()
        self.query.exec('SELECT * FROM settings')
        lst = []
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                lst.append(self.query.value('font'))
                lst.append(self.query.value('fio_doc'))
                lst.append(self.query.value('fio_zav'))
                lst.append(self.query.value('size'))
                lst.append(self.query.value('sex'))
                lst.append(self.query.value('otdel'))
                self.query.next()

        self.query.finish()
        print(lst[:6], "<--- вывод  функции гет префер она запустилась")
        return lst[:6]

    def insert_record_to_db(self, values_for_table):
        if self.con.isOpen():
            print('{}/prefer.db'.format(self.path), 'строка из if def инсерт record')
        else:
            self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            self.path = os.getcwd()
            print('{}/prefer.db'.format(self.path), 'строка из else метода инсерт record')
            self.con.setDatabaseName('{}/prefer.db'.format(self.path))
            ## con.setDatabaseName('//Users//user//PycharmProjects//razrabotka//prefer.db')
            self.con.open()

        self.dict_values = values_for_table
        self.osn_dic = self.emp_dic

        print(self.dict_values)
        if 'department' not in self.con.tables():
            query = QtSql.QSqlQuery()
            print(query.exec('create table department(id integer primary key autoincrement, fio text, dbirth text, numbhist text, d_enter text, t_enter text, povtorno text, dps text, dobrovol text, d_view text, t_view text, doctor text, zavotd text, zaloba text, vipiska text, area text, adress text, an_live text, an_bol text, an_nark text, iz_napr text, priemn text, votdele text, somat  text, ginek text, nevrol text, zabolevan text, allerg text, epid text, strah text, zakl text, diag_osn text, diag_sop text, dinamika text, kvipiske text)'))
            query.finish()

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
        #self.con.close()



    def changed_font(self):
        print('button clicked')
        #print(self.save_as_name)
        self.dict_for_send = self.save_as_name()
        self.insert_record_to_db(self.dict_for_send)
        self.create_name_path()

        '''
        self.font = QFont(self.list_with_prefer[0], self.list_with_prefer[3])
        list_f = [MMW.form_widget.fio_l, MMW.form_widget.datebirt_l, MMW.form_widget.dps_l, MMW.form_widget.anam_live_l, \
                  MMW.form_widget.anam_live_t]
        for i in list_f:
            i.setFont(self.font)
        # MMW.form_widget.fio_t.setFont(self.font)   #   работает
        '''

    def onActivated(self, text):
        self.text = text
        self.combotext = self.combo.currentText()
        print(self.text)

    def from_combo_to_edit(self, editt, where):
        editt.insertPlainText(where.currentText())
        # self.napravlee_t.insertPlainText(self.combotext)

    def create_obj(self, i, col, row, text='', col1=1, row1=1):
        #obj_font = MMW.preferences.fio_doc_text.text()
        #print(self.obj_font)

        self.i = i
        self.col = col
        self.row = row
        self.text = text
        self.col1 = col1
        self.row1 = row1
        if self.i == 'l':
            self.lab = QLabel()
            self.lab.setText(self.text)
            # self.lab.setFont(QFont(self.obj_font[0], self.obj_font[3]))  # это потом надо доделать, ссылка на переменную, в которой метод шрифта, надо доделать
            try:
                self.lab.setFont(QFont(self.list_with_prefer[0], self.list_with_prefer[3]))
            except IndexError:
                self.lab.setFont(QFont('Times Font', 12))
            self.grid_info.addWidget(self.lab, self.col, self.row)
            return self.lab
        elif i == 't':
            self.qtext = QLineEdit()
            self.qtext.setText(self.text)
            try:
                self.qtext.setFont(QFont(self.list_with_prefer[0], self.list_with_prefer[3]))
            except IndexError:
                self.qtext.setFont(QFont('Times Font', 12))
            #self.qtext.setFont(QFont(self.list_with_prefer[0], self.list_with_prefer[3]))
            self.grid_info.addWidget(self.qtext, self.col, self.row, self.col1, self.row1)
            return self.qtext

    def create_lab_qtext(self, i, text='', he=30):

        self.i = i
        self.he = he
        self.text = text
        if self.i == 'l':
            self.an_label = QLabel()
            self.an_label.setText(self.text)
            try:
                self.an_label.setFont(QFont(self.list_with_prefer[0], self.list_with_prefer[3]))
            except IndexError:
                self.an_label.setFont(QFont('Times Font', 12))
            self.other.addWidget(self.an_label)
            return self.an_label
        elif self.i == 't':
            self.an_qtext = MyQTextEdit(self.he)
            self.an_qtext.insertPlainText(self.text)
            self.an_qtext.setAcceptRichText(False)
            #self.an_qtext.setMinimumHeight(50)
            try:
                self.an_qtext.setFont(QFont(self.list_with_prefer[0], self.list_with_prefer[3]))
            except IndexError:
                self.an_qtext.setFont(QFont('Times Font', 12))

            # dc_he2 = int(self.an_qtext.document().size().height())
            # print(dc_he2)
            # self.an_qtext.setMinimumHeight(150)
            # if self.he:
            #      self.an_qtext.setMinimumHeight(self.he)

            self.other.addWidget(self.an_qtext)
            return self.an_qtext



    def save_as_name(self):
        # doc = DocxTemplate('Первичка.docx')
        self.dict = {}
        self.dict['fio'] =      self.fio_t.text().title()
        self.dict['dbirth'] =   self.datebirt_t.text()
        self.dict['numbhist'] = self.numbhis_t.text()
        self.dict['d_enter'] =  self.dateenter_t.text()
        self.dict['t_enter'] =  self.timeenter_t.text()
        self.dict['povtorno'] = self.povtorno_t.text()
        self.dict['dps'] =      self.dps_t.text()
        self.dict['dobrovol'] = self.dobrov_t.text()
        self.dict['d_view'] =   self.dateosm_t.text()
        self.dict['t_view'] = self.timeosm_t.text()
        self.dict['doctor'] = self.doc_t.text()
        self.dict['zavotd'] = self.zav_t.text()
        self.dict['zaloba'] = self.coplain_t.text()
        self.dict['vipiska'] = self.leave_t.text()
        self.dict['area'] =   self.combo.currentText()
        self.dict['adress'] = self.adres_t.text()
        self.dict['an_live'] =self.anam_live_t.toPlainText()
        self.dict['an_bol'] = self.anam_dese_t.toPlainText()
        self.dict['an_nark'] =self.anam_nark_t.toPlainText()
        self.dict['iz_napr'] =self.napravlee_t.toPlainText()
        self.dict['priemn'] = self.psy_st_pr_t.toPlainText()
        self.dict['votdele'] =self.psy_st_ot_t.toPlainText()
        self.dict['somat'] = self.somatikas_t.toPlainText()
        self.dict['ginek'] = self.ginekolog_t.toPlainText()
        self.dict['nevrol'] =    self.nevrologi_t.toPlainText()
        self.dict['zabolevan'] = self.concomita_t.toPlainText()
        self.dict['allerg'] =       self.allergiaa_t.toPlainText()
        self.dict['epid'] =         self.epidemiol_t.toPlainText()
        self.dict['strah'] =        self.strahovoi_t.toPlainText()
        self.dict['zakl'] =         self.zakluchen_t.toPlainText()
        self.dict['diag_osn'] =     self.diagnozos_t.toPlainText()
        self.dict['diag_sop'] =     self.diagnozso_t.toPlainText()
        self.dict['dinamika'] =     self.dinamika_t.toPlainText()
        self.dict['kvipiske'] =     self.k_vipisk_t.toPlainText()
        self.dict['treatment'] = self.treatment_t.toPlainText()
        self.dict['recommendations'] = self.prescribe_t.toPlainText()
        try:
            self.dict['department'] =  self.list_with_prefer[5]
        except IndexError:
            self.dict['department'] = ''

        try:
            date_enter = time.strptime(self.dateenter_t.text(), '%d.%m.%Y')
        except ValueError:
            try:
                date_enter = time.strptime(self.dateenter_t.text(), '%d.%m.%y')
            except ValueError:
                print('формат введенной даты нестандартный')
                date_enter = ''
        except TypeError:
            print('запись в базе не заполнена имеет значение None')
            date_enter = ''

        try:
            date_vipiska = time.strptime(self.leave_t.text(), '%d.%m.%Y')
        except ValueError:
            try:
                date_vipiska = time.strptime(self.leave_t.text(), '%d.%m.%y')
            except ValueError:
                print('формат введенной даты нестандартный')
                date_vipiska = ''
        except TypeError:
            print('запись в базе не заполнена имеет значение None')
            date_vipiska = ''
        if not date_enter == '':
            date_enter = datetime.date(year=date_enter.tm_year, month=date_enter.tm_mon, day=date_enter.tm_mday)
            if date_vipiska == '':
                date_vipiska = datetime.date.today()
            else:
                date_vipiska = datetime.date(year=date_vipiska.tm_year, month=date_vipiska.tm_mon, day=date_vipiska.tm_mday)
        print(type(date_enter), type(date_vipiska))
        if type(date_enter) is datetime.date and type(date_vipiska) is datetime.date:
            num_days = date_vipiska - date_enter
            num_days = num_days.days
            print(f'высчитали койко дни в page form widget {num_days}')

        try:
            self.dict['new_col'] = num_days
        except:
            self.dict['new_col'] = ''


        self.dict['add_col'] = ''
        self.dict['just_col'] = ''

        print(self.dict)
        return self.dict

    def create_name_path(self):
        n = self.fio_t.text().title().split()
        print(n)
        try:
            name_n = n[0] + ' ' + n[1][0] + n[2][0]
        except IndexError:
            try:
                name_n = n[0] + ' ' + n[1][0]
            except IndexError:
                try:
                    name_n = n[0]
                except IndexError:
                    name_n = 'без фамилии'

        date = self.dateosm_t.text().replace('.', '-')
        date_exit = self.leave_t.text().replace('.', '-')
        print(name_n, date)
        #global file_name
        #file_name = f'{name_n} первичный {date}.docx'
        #doc.save(f'{name_n} перв {date}.docx')

        #print(os.getcwd())
        diri = os.getcwd()
        print(diri)
        path_diri = '{}/{}'.format(diri, name_n)
        print(path_diri)
        #print("{}\{}".format(r, file_name))
        if not os.path.exists(path_diri):
            os.mkdir(path_diri)

        return path_diri, name_n, date, date_exit


    def all_filles_btn(self, str):
        if str == '   протокол':
            return print('протокольчик')
        cons_diri = os.getcwd()
        adr = f'{cons_diri}/files'
        os.chdir(adr)
        doc = DocxTemplate(f'{str}.docx')
        os.chdir(cons_diri)
        dic = self.save_as_name()
        doc.render(dic)
        path_diri, name_n, date, date_exit = self.create_name_path()
        
        os.chdir(path_diri)
        if str == 'медсведения':
            if not os.path.exists(f'{path_diri}/{name_n} {str} {date_exit}.docx'):
                doc.save(f'{path_diri}/{name_n} {str} {date_exit}.docx')
                file_name = f'{name_n} {str} {date_exit}.docx'
            else:
                doc.save(f'{path_diri}/{name_n} {str} {date_exit} (2).docx')
                file_name = f'{name_n} {str} {date_exit} (2).docx'
        else:
            if not os.path.exists(f'{path_diri}/{name_n} {str} {date}.docx'):
                doc.save(f'{path_diri}/{name_n} {str} {date}.docx')
                file_name = f'{name_n} {str} {date}.docx'
            else:
                doc.save(f'{path_diri}/{name_n} {str} {date} (2).docx')
                file_name = f'{name_n} {str} {date} (2).docx'

        os.chdir(cons_diri)
        full_file_name = f'{path_diri}/{file_name}'
        print(file_name)
        print(full_file_name)
        def open_file():
            os.chdir(path_diri)
            try:
                subprocess.Popen(f'explorer "{file_name}"')
            except FileNotFoundError:
                os.popen(f"open {cons_diri}")
            except:
                print('ничего не открывается... ')

            os.chdir(cons_diri)
        open_file()

class MyQTextEdit(QTextEdit):

    def __init__(self, he=0, *args, **kwargs):
        super(MyQTextEdit, self).__init__(*args, **kwargs)
        self.document().contentsChanged.connect(self.sizeChange)

        # dc_he = self.document().size().height()
        self.setMinimumHeight(he)
        self.heightMin = he
        self.heightMax = 65000


    def sizeChange(self):
        docHeight = self.document().size().height()

        if self.heightMin <= docHeight <= self.heightMax:
            self.setMinimumHeight(docHeight)



class MyQComboBox(QComboBox):
    def __init__(self, scrollWidget=None, *args, **kwargs):
        super(MyQComboBox, self).__init__(*args, **kwargs)  
        self.scrollWidget=scrollWidget
        self.setFocusPolicy(QtCore.Qt.StrongFocus)


    def wheelEvent(self, *args, **kwargs):
        if self.hasFocus():
            return print(' here here')#QComboBox.wheelEvent(self, *args, **kwargs)
        else:
            return print(' here here')#self.scrollWidget.wheelEvent(*args, **kwargs)


"""

if __name__ == '__main__':
    app = QApplication([])
    form = FormWidget()
    sys.exit(app.exec_())


"""
