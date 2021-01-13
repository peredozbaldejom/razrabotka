
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction,
                             QWidget, QPushButton, QToolTip, QMessageBox,
                             QTextEdit, QLabel, QHBoxLayout, QVBoxLayout,
                             QLineEdit, QTextEdit, QGridLayout, QLCDNumber,
                             QSlider, QInputDialog, QFileDialog, QFrame,
                             QFrame, QSplitter, QStyleFactory, QPlainTextEdit,
                             QComboBox, QCompleter, QDesktopWidget, qApp,
                             QSizePolicy, QTableView, QCheckBox)
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import QCoreApplication
from PyQt5 import Qt, QtCore, QtGui, QtSql
from random import randint,randrange
import sqlite3
import os
from docxtpl import DocxTemplate
import subprocess
import os.path



class Page_dairy(QWidget):
    def __init__(self, con = False):
        super().__init__()
        self.show()
        self.con = con
        self.gbox = QGridLayout()
        self.setLayout(self.gbox)

        if self.con == True and self.con.isOpen():
            print('{}/prefer.db'.format(self.path), 'строка из if метода dairy.py')
        else:
            self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            self.path = os.getcwd()
            self.con.setDatabaseName('{}/prefer.db'.format(self.path))
            self.con.open()

        if 'dairy_db' not in self.con.tables():
            query = QtSql.QSqlQuery()
            query.exec('create table dairy_db(id integer primary key autoincrement, soznanie text, orientir text, \
                       orientir2 text, bred text, bred2 text, gal text, gal2 text, thin text, thin2 text, intel text, intel2 text, \
                       behav1 text, behav2 text, behav3 text, act text, act2 text, aff1 text, aff2 text, emo1 text, emo2 text, emo3 text, \
                       somat text, somat2 text, somat3 text)')
            query.finish()
        self.count_col_dairy = self.con.record('dairy_db').count() # показывает количество столбцов в таблице
        print(self.count_col_dairy, 'количество столбцов в таблице dairy'  )

        self.list_with_prefer = self.get_prefer_from_db()

        self.dtm = QtSql.QSqlTableModel()
        self.dtm.setTable('dairy_db')
        self.list_check = [QCheckBox('использовать') for i in range(25)]
        self.list_text_edit = [MyQTextEdit2() for i in range(25)]
        #self.delete_tab()


        so = ['Сознание не помрачено. ', 'Сознание ясное. ', 'Сознание формально не помрачено. ',]
        oi = ['Ориентирована всесторонне правильно. ', 'Ориентирована верно. ', 'Всесторонне ориентирована верно. ',
              'В дате, месте, личности ориентирована верно. ', 'В месте, личности, времени ориентирована верно. ']
        aa = ['Ориентирована в личности, месте верно. ', 'Ориентирована в дате приблизительно. ',
              'Точную дату назвать затрудняется. ', 'Ориентирована в месте, личности верно. ']
        bb = ['Активно бредовых идей не высказывает. ', 'Бредовые идеи активно не звучат. ',
              ' Актуальных бредовых идей не звучит. ']
        cc = ['Активно высказывает бредовые идеи. ', ' Бредовые идеи прежние. ',
              ' Спонтанно звучат бредовые высказывания. ', 'В беседе активно звучат бредовые идеи. ']
        dd = ['Обманы восприятия отрицает. ', ' Без обманов восприятия. ', ' Галлюцинирующей не представляется. ',
              '"Голоса" отрицает. ']
        ee = ['Мышление паралогичное. ', 'Мышление малопродуктивное. ', 'Мышление нецеленаправленное. ',
              ' Мышление аутистичное. ', 'Мышление нецеленаправленное. ', ' ']
        ff = ['Мышление конкретное. ', 'Мышление тугоподвижное. ', 'Мышление обеднено, конкретное. ',
              ' Мышление малопродуктивное. ', ' Внимание застреваемое. ', ' ']
        gg = ['В поведении пассивна. ', ' К общению не стремится. ',
              ' Рисунок поведения определяется эндогенным заболеванием. ', ' В режим укладывается. ',
              ' Общение избирательное, время проводит пассивно. ']
        hh = ['Время проводит в одиночестве. ', ' Себя в отделении никак не проявляет. ',
              ' На вопросы отвечает формально. ']
        h1 = ['В беседе не заинтересована. ',
              ' Самостоятельно разговор не поддерживает, интереса к беседе не проявляет. ',
              'Остается отстраненной, отрешенной. ']
        jj = ['В высказываниях периодически нелепа. ', ' Близкого общения ни с кем не поддерживает. ',
              ' Рисунок поведения определяется эндогенным заболеванием. ']
        j1 = ['Свободное время проводит у телевизора. ', ' Общение избирательное, беседа малопродуктивная. ']
        kk = ['Фон настроения неустойчивый, тревожна. ', 'Периодически становится тревожной, напряженной. ',
              'Фон настроения неустойчивый, с колебаниями в течение дня. ',
              'Легко раздражается, становится беспокойной. ',
              'Переживаниями делится неохотно, несколько раздражительна. ']
        ll = ['Поговорки интерпретирует конкретно. ', ' Интеллектуально-мнестически снижена. ',
              ' Интеллектуально снижена, со счетом по Крепелину не справляется. ', ' Участвует в уборке отделения. ',
              ' Принимает участие в хозяйственных работах на отделении. ']
        mm = ['Фон настроения ровный. ', ' Фон настроения с невыраженными колебаниями. ',
              ' Фон настроения без колебаний в течение дня. ', ' Выраженных колебаний настроения не отмечается. ']
        nn = ['Эмоционально однообразна.', ' Эмоционально маловыразительна. ', ' Эмоционально монотонна. ',
              'Эмоционально холодна. ']
        n1 = ['Безразлична к окружающему, равнодушна. ', 'Аспонтанна, в беседе ничем не увлечь. ']
        oo = ['Стул, диурез не нарушены. ', ' Сон и аппетит в норме, стул и диурез в норме. ',
              ' Физиологические отправления в норме. ', ' Стул и диурез в норме. ']
        self.first_3 = ['Соматический статус: кожные покровы обычно окраски. Зев без признаков воспаления. Лимфоузлы не увеличены, б/б. Тоны сердца приглушены, звучные, шумов не выслушивается пульс 72 уд в минуту,  удовлетворительных свойств. В легких дыхание жесткое, одинаково проводится по всем легочным полям, хрипов нет. Живот мягкий, симметричный, при пальпации безболезненный. Печень, селезенка не пальпируются. Стул и диурез, со слов, не нарушены. ']
        self.ko_din = ['\nДинамика состояния: состояние постепенно стабилизируется.']
        self.ko_dia = ['\nДиагноз:  ']
        self.ko_r = ['\nРекомендации: нуждается в продолжение стационарного лечения для дообследования, подбора оптимальных доз поддерживающей терапии, достижения стабильной лекарственной ремиссии, формирования критического отношения к болезни, проведения реабилитационных мероприятий.  ']
        

        self.list_contents_text = [so, oi, aa, bb, cc, dd, ee, ff, gg, hh, h1, jj, j1, kk, ll, mm, nn, n1, oo]
        #self.list_contents_text = [aa, bb, cc, dd, ee, ff, gg, hh, h1, jj, j1, kk, ll, mm, nn, n1, oo]

        self.create_component()
        #self.record_data()
        #self.update_everything()


    def read_all(self):
        '''возвращает список прочитанных из базы списков (по идее должна быть только одна строка прочитана, так как в базе должна быть только одна строка)'''
        list_dairy = []
        #print(list_dairy, len(list_dairy), ' - длина. это список перед созданием в read all')
        dairy_query = QtSql.QSqlQuery()
        print(dairy_query.exec('SELECT * FROM dairy_db'), 'это считалась ли запис или нет в def init dairy')
        if dairy_query.isActive():
            dairy_query.first()
            i = 0
            while dairy_query.isValid():
                for i in range(self.count_col_dairy):
                    list_dairy.append(dairy_query.value(i))
                i+=1
                dairy_query.next()

        dairy_query.finish()
        return list_dairy


        # print(self.list_dairy)
        # print(self.con.close())
        # print(len(self.list_dairy), 'это список который считался в def init')
        # print(self.con.tables())

    def delete_tab(self):
        ''' удаляет таблицу если вызвать этот метод '''

        print(self.con.isOpen(), 'открыта ли база данных или нет в функции делит_таб')
        quer_del_tab = QtSql.QSqlQuery()
        print(quer_del_tab.exec('DROP TABLE dairy_db'), 'удалилась ли база или нет')
        quer_del_tab.finish()


    def record_data(self):
        ''' функция для добавления в таблицу записи в самом конце, через форму '''
        self.dtm.select()
        print(self.con.isOpen(), 'открыт ли con функция record_data')
        list1 = [i for i in range(25)]
        list2 = self.list_contents_text
        #list2 = [i*3 for i in range(25)]
        print(list1, list2)

        rec_add = self.con.record('dairy_db')
        for i in range(1, len(list2)):
            rec_add.setValue(list1[i], list2[i])
        self.dtm.insertRecord(-1, rec_add)

    def update_everything(self):
        '''   обновляют существующую строку с идексом 0, если нет строки выдаст ошибку   '''
        print(self.con.isOpen(), 'проверяет открыт ли con  в update_everything')
        self.list_values_from_listTextedit = [i.toPlainText() for i in self.list_text_edit]
        print(self.list_values_from_listTextedit)

        self.dtm.select()
        self.update_row = self.dtm.record(0)
        for i in range(2, len(self.list_values_from_listTextedit)):
            self.update_row.setValue(i, self.list_values_from_listTextedit[i])
        self.dtm.setRecord(0, self.update_row)
        self.dtm.removeRow(1)
        self.dtm.select()
        print(self.read_all())

    def check_combo(self):
        c = self.read_all()
        spisok_check = []
        for i in range(len(self.list_text_edit)):
            if self.list_check[i].isChecked() == True:
                if self.list_text_edit[i].toPlainText().split('. ') != ['']:
                    spisok_check.append(self.list_text_edit[i].toPlainText().split('. '))
            # if self.list_check[i].isChecked() == True:
            #     spisok_check.append(self.list_text_edit[i].toPlainText().split('. '))
        print(spisok_check)
        return spisok_check

    def create_component(self):
        ''' размещает компоненты формы по форме сами объекты созданы выше инит'''
        col = 0
        row = 5
        for i in range(2, len(self.list_check)):
            if i == 0 or i == 1:
                continue
            self.gbox.addWidget(self.list_check[i], row, col)
            row += 1

        col = 1
        row = 5
        for i in range(2, len(self.list_text_edit)):
            # if i == self.list_text_edit[0] or i == self.list_text_edit[1]:
            #     continue
            #print(i)
            self.gbox.addWidget(self.list_text_edit[i], row, col, 1, 1)
            row += 1
        # self.gbox.removeWidget(self.list_text_edit[0])
        # self.gbox.removeWidget(self.list_text_edit[1])

        self.box_part = QHBoxLayout()
        self.firs = QCheckBox('Первые 3 дня')
        self.box_part.addWidget(self.firs)
        self.firs2 = QCheckBox('К.О. с зав.отд.')
        self.box_part.addWidget(self.firs2)
        self.firs3 = QCheckBox('К.О. на отм.огр.')
        #self.box_part.addWidget(self.firs3)
        self.but_save_changes = QPushButton('Сохранить изменения')
        self.but_save_changes.clicked.connect(self.update_everything)
        self.box_part.addWidget(self.but_save_changes)
        self.gbox.addLayout(self.box_part, 1, 0, 2, 2)


        self.box_part2 = QHBoxLayout()
        self.but_generate = QPushButton('generation')
        self.but_generate.clicked.connect(self.generation_all)
        self.box_part2.addWidget(self.but_generate)
        self.gbox.addLayout(self.box_part2, 37, 0, 2, 2)

        self.box_part3 = QHBoxLayout()
        self.ch_20 = QCheckBox('F20')
        self.ch_20.clicked.connect(self.check_enab)
        self.box_part3.addWidget(self.ch_20)
        self.ch_06 = QCheckBox('F06')
        self.ch_06.clicked.connect(self.check_enab4)
        self.box_part3.addWidget(self.ch_06)
        self.ch_60 = QCheckBox('F60')
        self.ch_60.clicked.connect(self.check_enab3)
        #self.box_part3.addWidget(self.ch_60)
        self.ch_70 = QCheckBox('F70')
        self.ch_70.clicked.connect(self.check_enab4)
        #self.box_part3.addWidget(self.ch_70)
        self.gbox.addLayout(self.box_part3, 3, 0, 2, 2)

        self.doc_text = MyQTextEdit2()
        #self.doc_text.setFont(QFont('Times Font', 14)) 
        self.gbox.addWidget(self.doc_text, 40, 0, 1, 2)



        a = [1, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        b = []
        c = self.read_all()
        if c == a or c == b:
            self.autofill_text()
            print('заготовки изначальные - список из базы данных', c)
            if c == b:
                self.record_data()
                print('создана первая строка в  базе данных', c)

        else:
            for i in range(2, len(c)):
                self.list_text_edit[i].insertPlainText(''.join(c[i]))
            print('заготовки из базы')



    def autofill_text(self):
        ''' стандартные значения автозаполнения при первом запуске или обосрачке какой-никакой'''
        x = 0
        for i in range(2, len(self.list_contents_text)):
            self.list_text_edit[i].insertPlainText(''.join(self.list_contents_text[x]))
            x+=1

    def generation_all(self):
        one_list = []  # список по одному предложению из каждого списка
        all_lists = []  # список списков всех
        spisok_spiskov = self.check_combo()
        x = 9   # потом надо сделать ссылку на счетчик устанавливаемый
        y = 0
        while x > 0:
            x -= 1
            for i in spisok_spiskov:
                if y == len(spisok_spiskov):  # чтобы очищать список
                    one_list.clear()
                    y = 0
                for s in range(i.count('')):
                    i.remove('')

                for s in range(i.count(' ')):
                    i.remove(' ')

                y += 1
                r = randint(0, len(i)-1)
                try:
                    if i[r] != '' and i[r] != ' ':
                        one_list.append(i[r])
                        one_list.append('. ')
                        print(i[r])
                except IndexError:
                    print('это индекс еррор')
            print(one_list)
            if self.firs.isChecked():
                pres_m = randrange(115, 135, 3)
                pres_e = randrange(115, 135, 3)
                pres_m2 = randrange(75, 95, 3)
                pres_e2 = randrange(75, 95, 3)
                temp_m = randrange(3, 8, 1)
                temp_e = randrange(3, 8, 1)
                ad = [f'Утро АД {pres_m}/{pres_m2} Т 36.{temp_m} \t Вечер АД {pres_e}/{pres_e2}  Т 36.{temp_e}\n']
                if 6 <= x <= 9:
                    one_list.append(self.first_3[0])
                    one_list.insert(0, ''.join(ad))
            elif self.firs2.isChecked():
                print('если комиссионный отмечен')
                if not self.firs.isChecked():
                    if x == 8 or x == 5 or x == 2:
                        one_list.insert(0, '\t\t Комиссионный осмотр\n')
                        one_list.append(self.ko_din[0])
                        one_list.append(self.ko_dia[0])
                        one_list.append(self.ko_r[0])
                        #one_list.append(f'\nЗав.отд.\t{self.list_with_prefer[1]} Леч. врач\t{self.list_with_prefer[2]}')
                elif x == 5 or x == 2:
                    print('не отмечено ко с зав отд')
                    one_list.insert(0, '\t\t Комиссионный осмотр\n')
                    one_list.append(self.ko_din[0])
                    one_list.append(self.ko_dia[0])
                    one_list.append(self.ko_r[0])
                    #one_list.append(f'\nЗав.отд.\t{self.list_with_prefer[1]} Леч. врач\t{self.list_with_prefer[2]}')
                    
                    
                    
            all_lists.append(''.join(one_list))
            if self.firs2.isChecked() and x != 8 or x != 5 or x != 2:
                all_lists.append(f'\nЛеч. врач\t\t {self.list_with_prefer[1]}\n\n')  # надо доделать с форматированной строкой
        self.doc_text.clear()
        self.doc_text.insertPlainText(''.join(all_lists))
        all_lists.clear()
        one_list.clear()
        spisok_spiskov.clear()
        #  print(['list---->'] + all_lists + one_list + spisok_spiskov)

    def check_enab(self):
        print('нажата клавиша')
        print(self.ch_20.isTristate())
        if self.ch_20.isChecked():
            for i in [2, 3, 5,  7, 8, 9, 10]:
                self.list_check[i].toggle()

        else: #not self.ch_20.isChecked():
            for i in [2, 3, 5,  7, 8, 9, 10]:
                self.list_check[i].toggle()


    def check_enab2(self):
        print(self.ch_60.isTristate())
        if self.ch_60.isChecked():
            for i in [2, 4, 6, 9, 10, 11, 12]:
                self.list_check[i].toggle()

        else:# not self.ch_60.isChecked():
            for i in [5, 6, 8, 9, 10, 11, 12]:
                self.list_check[i].toggle()

    def check_enab3(self):
        if self.ch_70.isChecked():
            for i in [1, 2, 5, 4, 7, 12]:
                self.list_check[i].toggle()
                # self.ch_06.setChecked(False)
                # self.ch_20.setChecked(False)
                # self.ch_06.setChecked(False)
        elif not self.ch_70.isChecked():
            for i in [1, 2, 5, 4, 7, 12]:
                self.list_check[i].toggle()

    def check_enab4(self):
        if self.ch_06.isChecked():
            for i in [2, 4, 6, 7, 9, 15, 16]:
                self.list_check[i].toggle()
                # self.ch_60.setChecked(False)
                # self.ch_20.setChecked(False)
                # self.ch_70.setChecked(False)
        elif not self.ch_06.isChecked():
            for i in [2, 4, 6, 7, 9, 15, 16]:
                self.list_check[i].toggle()

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
        print(lst[:6], "<--- вывод  функции гет префер DAIRY она запустилась")
        return lst[:6]

class MyQTextEdit2(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document().contentsChanged.connect(self.sizeChange)
        self.setAcceptRichText(False)
        self.setMinimumHeight(50)
        self.heightMin = 50
        self.heightMax = 65000

    def sizeChange(self):
        docHeight = self.document().size().height()
        if self.heightMin <= docHeight <= self.heightMax:
            self.setMinimumHeight(docHeight)


if __name__ == '__main__':
    app = QApplication([])
    table_base = Page_dairy()
    sys.exit(app.exec_())
