import sys
import re
from PySide import QtGui, QtCore
from output import Ui_MainWindow


class Example(QtGui.QMainWindow):

    def __init__(self):
        super(Example, self).__init__()
        self.show()

        self.round_count = 1

        mygroupbox = QtGui.QWidget()
        self.myform = QtGui.QFormLayout()
        self.myform.setSpacing(0)
        self.myform.setContentsMargins(0,0,0,0)
        self.first_wid = self.entry_ui()
        self.myform.addRow(self.first_wid)
        mygroupbox.setLayout(self.myform)
        self.ui.scrollArea.setWidget(mygroupbox)
        self.ui.scrollArea.setWidgetResizable(True)

        openFile = QtGui.QAction( 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.show_load_dialog)

        menubar = self.ui.menubar
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        saveFile = QtGui.QAction("&Save File", self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.file_save)
        fileMenu.addAction(saveFile)


    def entry_ui(self):
        main_widget = QtGui.QWidget()
        main_widget.setObjectName('roundwid')
        layout = QtGui.QHBoxLayout()

        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(10)
        font.setItalic(False)

        selection_combo = QtGui.QComboBox()
        selection_combo.addItems(["Round", "Topic", "Material", "Row", "Note", "Info"])
        selection_combo.currentIndexChanged.connect(lambda :self.selection_change(main_widget))
        selection_combo.setMinimumWidth(75)
        selection_combo.setStyleSheet(
            'QComboBox {background-color: white; border: 2px solid #c6e3f9;border-radius:10px;}')
        selection_combo.setFont(font)
        layout.addWidget(selection_combo)

        round_num_box = QtGui.QLineEdit()
        round_num_box.setText(str(self.round_count))
        round_num_box.setMaximumWidth(40)
        round_num_box.setStyleSheet('QLineEdit {background-color: white; border: 2px solid #c6e3f9;border-radius:10px;}')
        round_num_box.setFont(font)
        layout.addWidget(round_num_box)

        description_box = QtGui.QLineEdit()
        description_box.placeholderText = 'Enter your round/note/material info here...'
        description_box.returnPressed.connect(lambda : self.add_new_box(selection_combo, round_num_box.text()))
        description_box.setStyleSheet(
            'QLineEdit {background-color: white; border: 2px solid #c6e3f9;border-radius:10px;}')
        description_box.setFont(font)
        layout.addWidget(description_box)

        url_label = QtGui.QLabel('URL:')
        url_label.hide()
        url_label.setFont(font)
        layout.addWidget(url_label)

        url_box = QtGui.QLineEdit()
        url_box.setMaximumWidth(200)
        url_box.hide()
        url_box.placeholderText= 'Enter URL here...'
        url_box.setStyleSheet(
            'QLineEdit {background-color: white; border: 2px solid #c6e3f9;border-radius:10px;}')
        url_box.setFont(font)
        layout.addWidget(url_box)

        delete_btn = QtGui.QPushButton('X')
        delete_btn.setMaximumWidth(25)
        delete_btn.setMinimumWidth(25)
        delete_btn.clicked.connect(lambda :self.delete_box(main_widget))
        delete_btn.setStyleSheet(
            'QPushButton {background-color: #c6e3f9; color: white; border: 2px solid #c6e3f9;border-radius:10px;}')
        delete_btn.setFont(font)
        delete_btn.hide()
        layout.addWidget(delete_btn)

        main_widget.setLayout(layout)
        return main_widget

    def selection_change(self, widget):
        children = widget.children()
        # print [x for x in children]
        if 'Round' in children[1].currentText() or 'Row' in children[1].currentText():
            children[2].show()
            children[-2].hide()
            children[-3].hide()
        else:
            children[2].hide()
            children[-2].show()
            children[-3].show()

        if 'Topic' in children[1].currentText():
            children[2].hide()
            children[-2].hide()
            children[-3].hide()

    def add_new_box(self, widget, round_num):
        if 'Topic' in widget.currentText():
            self.round_count = 1

        new_wid = self.entry_ui()
        my_children = new_wid.children()
        my_children[-1].show()

        if 'Round' in widget.currentText():
            if '-' in round_num:
                high_num = str(round_num).split('-')[-1]
                self.round_count = int(high_num)
            my_children[1].setCurrentIndex(0)
            self.round_count += 1
            my_children[2].setText(str(self.round_count))
        if 'Material' in widget.currentText():
            my_children[1].setCurrentIndex(2)
        if 'Row' in widget.currentText():
            my_children[1].setCurrentIndex(3)
            self.round_count += 1
        if 'Note' in widget.currentText():
            my_children[1].setCurrentIndex(4)
        if 'Info' in widget.currentText():
            my_children[1].setCurrentIndex(5)

        self.myform.addRow(new_wid)
        my_children[3].setFocus()

    def delete_box(self, widget):
        self.myform.removeWidget(widget)
        self.myform.update()

    def show_load_dialog(self):

        fname, _ = QtGui.QFileDialog.getOpenFileName(self, "Open Text File",
                                          dir=".", filter="Text Files (*.txt)")

        f = open(fname, 'r')

        with f:
            self.ui.lineEdit.setText(fname)
            self.myform.removeWidget(self.first_wid)
            for line in f.readlines():
                my_widget = self.entry_ui()
                children = my_widget.children()
                line_info = line.split(']')
                description = line_info[-1]
                regex = r"Round \d+"
                if 'continued' in line_info[0]:
                    topic, number, continued = line_info[0].split(' ')
                elif re.match(regex, line_info[0]):
                    topic, number = line_info[0].split(' ')
                else:
                    topic = line_info[0]

                if 'Round' in topic:
                    children[1].setCurrentIndex(0)
                    children[2].setText(number)
                    children[3].setText(description)
                if 'Topic' in topic:
                    children[1].setCurrentIndex(1)
                    children[3].setText(description)
                if 'Material' in topic:
                    desc, url = description.split('URL')
                    children[1].setCurrentIndex(2)
                    children[3].setText(desc)
                    children[5].setText(url)
                if 'Row' in topic:
                    children[1].setCurrentIndex(3)
                    children[2].setText(number)
                    children[3].setText(description)
                if 'Note' in topic:
                    if 'URL' in description:
                        desc, url = description.split('URL')
                        children[3].setText(desc)
                        children[5].setText(url)
                    else:
                        children[3].setText(description)

                    children[1].setCurrentIndex(4)
                if 'Info' in topic:
                    desc, url = description.split('URL')
                    children[1].setCurrentIndex(5)
                    children[3].setText(desc)
                    children[5].setText(url)

                self.myform.addRow(my_widget)



    def file_save(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File', self.ui.lineEdit.text(),'.txt')
        print name
        with open(name[0], "w") as f:

            widgets = self.findChildren(QtGui.QWidget, "roundwid")

            for wid in widgets:
                text = ''
                wid_children = wid.children()
                if 'Round' in wid_children[1].currentText():
                    text = '{0} {1}] {2}\n'.format(wid_children[1].currentText(), wid_children[2].text(), wid_children[3].text())
                elif 'Topic' in wid_children[1].currentText():
                    text = '{0}] {1}\n'.format(wid_children[1].currentText(), wid_children[3].text())
                else:
                    text = '{0}] {1} URL {2}\n'.format(wid_children[1].currentText(), wid_children[3].text(), wid_children[5].text())

                f.write(text)


def main():
    app = QtGui.QApplication(sys.argv)
    pixmap = QtGui.QPixmap(":/img/splash.png")
    splash = QtGui.QSplashScreen(pixmap)
    splash.show()
    import time
    time.sleep(2)  # delays for 5 seconds. You can Also Use Float Value.
    splash.hide()
    app.setWindowIcon(QtGui.QIcon(":/img/yarnie.png"))
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()