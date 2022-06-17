from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

from design import Ui_MainWindow
from add_ui import Ui_AddWindow
import sys
import db


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.next_window = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # подключение клик-сигнал к слотам
        self.ui.pushButton_add.clicked.connect(self.press_add)
        self.ui.pushButton_show.clicked.connect(self.press_show)
        self.ui.pushButton_show_2.clicked.connect(self.press_show_log)
        self.ui.pushButton_locations.clicked.connect(self.press_locations)

        self.ui.comboBox_devices.textActivated.connect(self.update_dev_help)
        self.ui.comboBox_log.textActivated.connect(self.update_log_help)

        # показывает таблицу при изменении параметров
        self.ui.comboBox_devices.textActivated.connect(self.press_show)
        self.ui.comboBox_dev_help.textActivated.connect(self.press_show)

        self.ui.comboBox_log.textActivated.connect(self.press_show_log)
        self.ui.comboBox_log_help.textActivated.connect(self.press_show_log)

        self.ui.comboBox_City.textActivated.connect(self.update_object)
        self.ui.comboBox_Object.textActivated.connect(self.update_building)
        self.ui.comboBox_Building.textActivated.connect(self.update_room)
        #self.ui.comboBox_Room.textActivated.connect(self.update_location)
        # ну типа базу данных сделал типа

        self.db = db.Database()
        try:
            self.db.create_table_equipment()
        except Exception as err:
            print(err)
        try:
            self.db.create_table_work_log()
        except Exception as err:
            print(err)
        try:
            self.db.create_table_locations()
        except Exception as err:
            print(err)

        self.loc = self.db.select_help_location()
        self.update_location()

    def update_city(self):
        # loc = filter(lambda x: x[0] == self.ui.comboBox_City.currentText(), self.loc)
        cities = set([i[0] for i in self.loc])
        self.ui.comboBox_City.clear()
        for city in cities:
            self.ui.comboBox_City.addItem(str(city))

    def update_object(self):
        loc = filter(lambda x: x[0] == self.ui.comboBox_City.currentText(), self.loc)
        objects = set([i[1] for i in loc])
        self.ui.comboBox_Object.clear()
        for obj in objects:
            self.ui.comboBox_Object.addItem(str(obj))

    def update_building(self):
        loc = filter(lambda x: x[1] == self.ui.comboBox_Object.currentText(), self.loc)
        buildings = set([i[2] for i in loc])
        self.ui.comboBox_Building.clear()
        for obj in buildings:
            self.ui.comboBox_Building.addItem(str(obj))

    def update_room(self):
        loc = filter(lambda x: str(x[2]) ==  str(self.ui.comboBox_Building.currentText()), self.loc)
        rooms = set([i[3] for i in loc])
        self.ui.comboBox_Room.clear()
        for obj in rooms:
            self.ui.comboBox_Room.addItem(str(obj))

    def update_location(self):
        self.loc = self.db.select_help_location()
        self.update_city()

    def update_dev_help(self):
        text = self.ui.comboBox_devices.currentText()
        if text == "Все":
            return
        else:
            self.ui.comboBox_dev_help.clear()
            try:
                types = set(self.db.select_help_dev(text))
                for i in types:
                    self.ui.comboBox_dev_help.addItem(str(i[0]))
            except Exception as e:
                print(e)

    def press_add(self):
        location = " ".join([self.ui.comboBox_City.currentText(),
                            self.ui.comboBox_Object.currentText(),
                            self.ui.comboBox_Building.currentText(),
                            self.ui.comboBox_Room.currentText()])

        params = [self.ui.lineEdit_name.text(),
                  self.ui.lineEdit_serial_num.text(),
                  self.ui.comboBox.currentText(),
                  str(self.ui.dateEdit.date().toPyDate()).replace("-", "."),
                  location,
                  self.ui.comboBox_2.currentText(),
                  self.ui.lineEdit_description.text()]

        if all(params):
            for i in params:
                print(i)
            self.db.add_equipment(params[0], params[1], params[2], params[3],
                params[4], params[5], params[6])
            self.ui.label_add.setText("Добавлено")
        else:
            self.ui.label_add.setText("Ошибка! Не все поля заполнены")

    def press_show(self):
        if self.ui.comboBox_devices.currentText() == "Все":
            self.press_show_devices()
        else:
            self.press_show_devices_param()

    def press_show_devices(self):
        # Получим результат запроса,
        # который ввели в текстовое поле
        query = self.db.select_all_equipment()
        # Заполним размеры таблицы
        width = len(query[0])
        height = len(query)
        self.ui.tableWidget.setColumnCount(width)
        self.ui.tableWidget.setRowCount(height)
        names = ["Наименование", "серийный номер", "Тип", "Дата ТО", "Место установки", "Статус", "Примечание"]
        self.ui.tableWidget.setHorizontalHeaderLabels(names)

        # Заполняем таблицу элементами
        for i, row in enumerate(query):
            self.ui.tableWidget.setRowCount(
                self.ui.tableWidget.rowCount())
            for j, elem in enumerate(row):
                self.ui.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        print("Вы нажали на кнопку показать")

    def press_show_devices_param(self):
        params_dict = {"Тип": "type",
                       "Место": "location",
                       "Статус": "condition"}  # вместо подл. обсл. должно быть другое действие
        param_name = params_dict[self.ui.comboBox_devices.currentText()]
        param = self.ui.comboBox_dev_help.currentText()

        if param_name == "type":
            query = self.db.select_equipment(type=param)
        elif param_name == "location":
            query = self.db.select_equipment(location=param)
        elif param_name == "condition":
            query = self.db.select_equipment(condition=param)
            #Вот это тоже нужно сделать по нормальному
        # Получим результат запроса,
        # который ввели в текстовое поле
        # Заполним размеры таблицы
        if query:
            width = len(query)
            height = 1
            if isinstance(query[0], tuple):
                width = len(query[0])
                height = len(query)
        else:
            width, height = 0, 0

        self.ui.tableWidget.setColumnCount(width)
        self.ui.tableWidget.setRowCount(height)
        names = ["Наименование", "серийный номер", "Тип", "Дата ТО", "Место установки", "Статус", "Примечание"]
        self.ui.tableWidget.setHorizontalHeaderLabels(names)

        # Заполняем таблицу элементами
        for i, row in enumerate(query):
            self.ui.tableWidget.setRowCount(
                self.ui.tableWidget.rowCount())
            for j, elem in enumerate(row):
                self.ui.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        print("Вы нажали на кнопку показать")

    def press_show_log(self):

        if self.ui.comboBox_log.currentText() == "Все":
            self.press_show_log_all()
        else:
            self.press_show_log_param()

    def press_show_log_param(self):
        param = self.ui.comboBox_log_help.currentText()
        query = self.db.select_work_log(date=param)
        print(query)
        # Заполним размеры таблицы
        if query:
            width = len(query)
            height = 1
            if isinstance(query[0], tuple):
                width = len(query[0])
                height = len(query)
        else:
            width, height = 0, 0
        print(width, height)
        self.ui.tableWidget.setColumnCount(width)
        self.ui.tableWidget.setRowCount(height)
        names = ["Номер", "Дата", "Тип", "Описание"]
        self.ui.tableWidget.setHorizontalHeaderLabels(names)
        if query:
            if isinstance(query[0], tuple):
                for i, row in enumerate(query):
                    self.ui.tableWidget.setRowCount(
                        self.ui.tableWidget.rowCount())

                    for j, elem in enumerate(row):
                        self.ui.tableWidget.setItem(
                            i, j, QTableWidgetItem(str(elem)))
            else:
                for col, i in enumerate(query):
                    self.ui.tableWidget.setItem(0, col, QTableWidgetItem(str(i)))
        print("Вы нажали на кнопку показать")

    def press_show_log_all(self):
        # Получим результат запроса,
        # который ввели в текстовое поле
        query = self.db.select_all_work_log()
        # Заполним размеры таблицы
        if query:
            width = len(query[0])
            height = len(query)
        else:
            width, height = 0, 0
        self.ui.tableWidget.setColumnCount(width)
        self.ui.tableWidget.setRowCount(height)
        names = ["Номер", "Дата", "Тип", "Описание"]
        self.ui.tableWidget.setHorizontalHeaderLabels(names)
        # Заполняем таблицу элементами
        for i, row in enumerate(query):
            self.ui.tableWidget.setRowCount(
                self.ui.tableWidget.rowCount())
            for j, elem in enumerate(row):
                self.ui.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        print("Вы нажали на кнопку показать")

    def update_log_help(self):
        text = self.ui.comboBox_log.currentText()
        self.ui.comboBox_log_help.clear()
        try:
            types = set(self.db.select_help_log(text))
            for i in types:
                self.ui.comboBox_log_help.addItem(str(i[0]))
        except Exception as e:
            print(e)

    def press_locations(self):
        try:
            if self.next_window is None:
                self.next_window = AddLocation(self)
                self.next_window.show()
                self.next_window.focusWidget()
        except Exception as e:
            print(e)


class AddLocation(QtWidgets.QMainWindow, Ui_AddWindow):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setupUi(self)
        self.next_window = None
        self.show_locations()
        self.pushButton_ad.clicked.connect(self.add_location)

        self.tableWidget.itemClicked.connect(self.chose)
        self.pushButton_delete.clicked.connect(self.delete_location)

        self.selected = 0
        self.selected_row = ""

    def closeEvent(self, a0):
        self.parent_window.next_window = None
        self.parent_window.show()
        a0.accept()

    def show_locations(self):
        query = self.parent_window.db.select_locations()
        if query:
            # Заполним размеры таблицы
            width = len(query[0])
            height = len(query)
            self.tableWidget.setColumnCount(width)
            self.tableWidget.setRowCount(height)
            names = ["Город", "Объект", "Здание", "Помещение"]
            self.tableWidget.setHorizontalHeaderLabels(names)
            # Заполняем таблицу элементами
            for i, row in enumerate(query):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount())
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(elem)))

    def add_location(self):
        try:
            city = str(self.lineEdit_city.text())
            object = str(self.lineEdit_obj.text())
            building = str(self.lineEdit_building.text())
            room = str(self.lineEdit_room.text())
            self.parent_window.db.add_location(city, object, building, room)
            self.parent_window.update_location()
        except Exception as e:
            pass
        self.show_locations()

    def chose(self):
        self.selected_row = self.tableWidget.currentItem().row()
        selected = self.selected_row
        self.selected = ""
        for i in range(3):
            self.selected += (self.tableWidget.item(selected, i).text() + " ")
        self.lineEdit_2.setText(self.selected)

    def delete_location(self):
        try:
            print(*[self.tableWidget.item(self.selected_row, i).text() for i in range(4)])
            self.parent_window.db.delete_location(*[self.tableWidget.item(self.selected_row, i).text() for i in range(4)])
            self.show_locations()
        except Exception as e:
            print(e)


app = QtWidgets.QApplication([])
application = MyWindow()
application.show()
sys.exit(app.exec())
