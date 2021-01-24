import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtWidgets, Qt

import sql_manip as Turtal

class WidgetMimeData(QtCore.QMimeData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.itemObject = None

    def hasFormat(self, mime):
        if (self.itemObject and (mime == 'widgetitem')):
            return True
        return super().hasFormat(mime)

    def setItem(self, obj):
        self.itemObject = obj

    def item(self):
        return self.itemObject


class DraggableWidget(QGroupBox):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setAcceptDrops(True)

    def addWidget(self, widget):
        return self.layout().addWidget(widget)

    def mouseMoveEvent(self, ev):
        pixmap = QPixmap(self.size())
        pixmap.fill(QtCore.Qt.transparent)
        painter = QPainter()
        painter.begin(pixmap)
        painter.setOpacity(0.8)
        painter.drawPixmap(0, 0, self.grab())
        painter.end()
        drag = QDrag(self)
        mimedata = WidgetMimeData()
        mimedata.setItem(self)
        drag.setMimeData(mimedata)
        drag.setPixmap(pixmap)
        drag.setHotSpot(ev.pos())
        drag.exec_(QtCore.Qt.MoveAction)
    
    def destroy(self):
        self.close()

class DroppableWidget(QGroupBox):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setAcceptDrops(True)

    def addWidget(self, widget):
        return self.layout().addWidget(widget)
    
    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        item = event.source()
        self.addWidget(item)
        event.acceptProposedAction()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # setting some basic formatting properties
        self.setWindowTitle("Turtle House")
        # setting layout
        self.initUI()
        
    def initUI(self):
        self.general_layout = QGridLayout()

        self._all_buttons_groupbox = DroppableWidget("Possible Classes")
        all_buttons_layout = QVBoxLayout()
        self.all_buttons = {}

        self._central_widget = QWidget(self)
        self.setCentralWidget(self._central_widget)
        self._central_widget.setLayout(self.general_layout)
        self._create_class_buttons()
        self.create_grid_layout()
        self.setGeometry(450, 200, 700, 600)
        self.show()
        
    def _create_class_buttons(self):
        for i in Turtal.SqlManip().get_classes():
            self.all_buttons[f"{i[0]} {i[1]}"] = self._make_class_widget(i[0], i[1])
            self._all_buttons_groupbox.addWidget(self.all_buttons[f"{i[0]} {i[1]}"])
    
        # self._all_buttons_groupbox.setLayout(all_buttons_layout)
        scroll = QScrollArea()
        scroll.setWidget(self._all_buttons_groupbox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(600)
        self.general_layout.addWidget(scroll, 1, 2)
        
    def create_grid_layout(self):
        self.quarter_groupbox = QGroupBox("4-Year Schedule")
        self.quarter_groupbox.setStyleSheet("QGroupBox { border: 1px solid black;}")
        self.quarter_layout = QGridLayout()
        for i in range (0, 3):
            self.quarter_layout.setColumnStretch(i+1, 4)
            self.quarter_layout.setRowStretch(i+1, 4)
        self.quarter_layout.setRowStretch(4, 4)
        
        # making the droppable areas for the quarters
        self.quarter_droppables = []
        for i in range(0, 4):
            temp = []
            for j in range(0, 3):
                temp.append(DroppableWidget())
                self.quarter_layout.addWidget(temp[j], i+1, j+1)
            self.quarter_droppables.append(temp)

        self.quarter_layout.addWidget(QLabel("Sem 1"), 0, 1)
        self.quarter_layout.addWidget(QLabel("Sem 2"), 0, 2)
        self.quarter_layout.addWidget(QLabel("Sem 3"), 0, 3)
        self.quarter_layout.addWidget(QLabel("Year 1"), 1, 0)
        self.quarter_layout.addWidget(QLabel("Year 2"), 2, 0)
        self.quarter_layout.addWidget(QLabel("Year 3"), 3, 0)
        self.quarter_layout.addWidget(QLabel("Year 4"), 4, 0)

        self.quarter_groupbox.setLayout(self.quarter_layout)
        self.general_layout.addWidget(self.quarter_groupbox, 1, 1)
        
    def _make_class_widget(self, dept, class_id):
        grades = {"pnp": r"P/NP",
                  "letter": "Letter",
                  "both": r"Letter or P/NP"}
        
        current_class = DraggableWidget(f"{dept} {class_id}")
        grade_type, units, hours = Turtal.SqlManip().get_grade_type_units_hours(class_id, dept)
        
        units_hrs = QGroupBox()
        units_hrs_layout = QHBoxLayout()
        
        units_hrs_layout.addWidget(QLabel(f"{units} units"))
        units_hrs_layout.addWidget(QLabel(f"{hours} hrs per week"))
        
        units_hrs.setLayout(units_hrs_layout)
        
        current_class.addWidget(QLabel(f"{grades[grade_type]} Grading"))
        current_class.addWidget(units_hrs)
        desc_button = QPushButton("See Description", current_class)
        current_class.addWidget(desc_button)
        desc_button.clicked.connect((lambda: self._clicked(dept, class_id)))
        
        return current_class
        
    def _clicked(self, dept, class_id):
        self.window = PopupWindow(class_id, dept)
        
class PopupWindow(QWidget):
    def __init__(self, class_id, dept):
        QWidget.__init__(self)
        self.class_id = class_id
        self.dept = dept
        self.initUI()

    def initUI(self):
        self.popup_layout = QVBoxLayout()
        self.setWindowTitle(f"{self.dept} {self.class_id}")
        self.setGeometry(50, 50, 250, 300)
        self.show()
        
        self.set_info()

    def set_info(self):
        desc, req, coreq = Turtal.SqlManip().get_desc(self.class_id, self.dept)
        
        req = str(req).replace(r"[", "").replace(r"]", "").replace(r"'", "")
        coreq = str(coreq).replace(r"[", "").replace(r"]", "").replace(r"'", "")
        req_label = QLabel(f"Requisites: {req}")
        req_label.setWordWrap(True)
        
        coreq_label = QLabel(f"Corequisites: {coreq}")
        coreq_label.setWordWrap(True)
        
        desc_label = QLabel(f"Desc: {desc}")
        desc_label.setWordWrap(True)
        
        self.popup_layout.addWidget(req_label)
        self.popup_layout.addWidget(coreq_label)
        self.popup_layout.addWidget(desc_label)
        self.setLayout(self.popup_layout)
            
def main():
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()