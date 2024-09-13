import functools
from typing import Dict, List, Tuple

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QStringListModel, QItemSelection, Qt, QObject, QAbstractItemModel, \
    QItemSelectionModel
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QWidget, QListView, QHBoxLayout, QVBoxLayout, QMenuBar, QMenu, QStatusBar, QMainWindow,
                             QMessageBox, QAbstractItemView, QPushButton, QFrame, QAbstractScrollArea, QSizePolicy,
                             QScrollArea, QGroupBox, QLineEdit)

import entity
import task
import util
from entity import Question, BaseTask
from entity.enum_task import EnumTask
from ui.qt_chat_cell import PromptCell, AnswerCell
from ui.qt_question_cell import QuestionCell
from ui.qt_translation_cell import TranslationCell

GLOBAL_FONT = QFont()
GLOBAL_FONT.setFamilies([u"Microsoft YaHei"])
GLOBAL_FONT.setPointSize(12)
GLOBAL_FONT.setBold(True)


class MainWindow(QMainWindow):
    # UI
    line_opinion: QLineEdit
    layout_opinion: QHBoxLayout
    group_opinion: QGroupBox
    button_next: QPushButton
    button_fail: QPushButton
    button_success: QPushButton
    button_prev: QPushButton
    layout_navigation: QVBoxLayout
    scroll_task_button_group: QScrollArea
    menu_language: QMenu
    status_bar: QStatusBar
    menu_open: QMenu
    menu_bar: QMenuBar
    layout_chat_slice: QHBoxLayout
    cell_answer_raw: QuestionCell
    cell_question: QuestionCell
    cell_question_raw: QuestionCell
    layout_raw: QHBoxLayout
    layout_task: QVBoxLayout
    list_row: QListView
    list_sheet: QListView
    layout_content_hbox: QHBoxLayout
    layout_content: QWidget
    # Task buttons
    button_group: List[QPushButton] = []
    # Chat slices
    cells: List[QuestionCell]
    cell_chat_slices: List[Tuple[QuestionCell, QuestionCell]] = []

    # Data in memory
    sheet_model: QStringListModel = QStringListModel()
    row_model: QStringListModel = QStringListModel()

    # Data in real world
    excel_file: str = ''
    excel_dict: Dict[str, int] = {}
    question: Question | None = None
    chosen_task: BaseTask = EnumTask.ANSWER_IN_ENGLISH.value

    def setup_ui(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(1026, 819)
        main_window.setMinimumSize(QtCore.QSize(640, 480))
        self.layout_content = QWidget(parent=main_window)
        self.config_layout_content()

        self.list_sheet = QListView(parent=self.layout_content)
        self.config_list_sheet()
        self.layout_content_hbox.addWidget(self.list_sheet)

        self.list_row = QListView(parent=self.layout_content)
        self.config_list_row()
        self.layout_content_hbox.addWidget(self.list_row)

        self.layout_task = QVBoxLayout()
        self.layout_task.setObjectName("layout_task")

        self.layout_raw = QHBoxLayout()
        self.layout_raw.setObjectName("layout_raw")

        self.setup_area_raw()
        self.layout_task.addLayout(self.layout_raw)

        self.setup_area_task_group()
        self.layout_task.addWidget(self.scroll_task_button_group)

        self.setup_area_chat()

        self.layout_task.addLayout(self.layout_chat_slice)
        self.layout_task.setStretch(0, 0)
        self.layout_task.setStretch(1, 0)
        self.layout_task.setStretch(2, 1)

        self.layout_content_hbox.addLayout(self.layout_task)
        self.layout_content_hbox.setStretch(0, 1)
        self.layout_content_hbox.setStretch(1, 1)
        self.layout_content_hbox.setStretch(2, 5)

        main_window.setCentralWidget(self.layout_content)
        self.menu_bar = QMenuBar(parent=main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 1026, 22))
        self.menu_bar.setObjectName("menu_bar")

        self.menu_open = QMenu(parent=self.menu_bar)
        self.menu_open.setObjectName("menu_open")
        self.menu_open.aboutToShow.connect(self.choose_file)

        self.menu_language = QMenu(parent=self.menu_bar)
        self.menu_language.setObjectName("menu_language")
        main_window.setMenuBar(self.menu_bar)

        self.status_bar = QStatusBar(parent=main_window)
        self.status_bar.setObjectName("status_bar")
        main_window.setStatusBar(self.status_bar)

        self.menu_bar.addAction(self.menu_open.menuAction())

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def setup_area_chat(self):
        self.layout_chat_slice = QHBoxLayout()
        self.layout_chat_slice.setObjectName("layout_chat")
        self.build_chat_slices()

    def setup_area_task_group(self):
        self.scroll_task_button_group = QtWidgets.QScrollArea(self)
        self.scroll_task_button_group.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_task_button_group.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.scroll_task_button_group.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_task_button_group.setWidgetResizable(True)
        self.scroll_task_button_group.setAlignment(Qt.AlignmentFlag.AlignCenter)
        widget_verbose = QWidget(self.scroll_task_button_group)
        layout_task_button_group = QHBoxLayout(widget_verbose)
        for index, enum_task in enumerate(list(EnumTask)):
            button = QPushButton(self.scroll_task_button_group)
            button.setText(enum_task.value.task_name)
            button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding))
            button.clicked.connect(functools.partial(self.handle_task_change, enum_task))

            self.button_group.append(button)
            layout_task_button_group.addWidget(button)
        self.scroll_task_button_group.setWidget(widget_verbose)

    def setup_area_raw(self):
        self.cell_question_raw = QuestionCell(title="question_raw", parent=self.layout_content)
        self.cell_question_raw.field = "question_raw"
        self.layout_raw.addWidget(self.cell_question_raw)
        self.cell_question = TranslationCell(title="question", function_text="Retranslate",
                                             function=util.translate_to, parent=self.layout_content,
                                             question_raw=self.cell_question_raw)
        self.cell_question.field = "question"
        self.layout_raw.addWidget(self.cell_question)
        self.cell_answer_raw = QuestionCell(title="answer_raw", parent=self.layout_content)
        self.cell_answer_raw.field = "answer_raw"
        self.layout_raw.addWidget(self.cell_answer_raw)

        self.layout_navigation = QVBoxLayout()

        self.group_opinion = QGroupBox()
        self.group_opinion.setTitle("Opinion")
        self.group_opinion.setFont(GLOBAL_FONT)
        self.group_opinion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.group_opinion.setMaximumWidth(150)
        self.group_opinion.setMaximumHeight(200)

        self.layout_opinion = QHBoxLayout()
        self.group_opinion.setLayout(self.layout_opinion)

        self.line_opinion = QLineEdit()
        self.line_opinion.setFont(GLOBAL_FONT)
        self.line_opinion.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_opinion.addWidget(self.line_opinion)
        self.layout_navigation.addWidget(self.group_opinion)

        self.button_prev = QPushButton()
        self.button_prev.setText("Prev")
        self.button_prev.clicked.connect(self.handle_prev)
        self.layout_navigation.addWidget(self.button_prev)

        self.button_success = QPushButton()
        self.button_success.setText("Success")
        self.button_success.clicked.connect(self.handle_success)
        self.button_success.setStyleSheet("QPushButton {color: #5cb85c;}")
        self.layout_navigation.addWidget(self.button_success)

        self.button_fail = QPushButton()
        self.button_fail.setText("Fail")
        self.button_fail.clicked.connect(self.handle_fail)
        self.button_fail.setStyleSheet("QPushButton {color: #d81e15;}")
        self.layout_navigation.addWidget(self.button_fail)

        self.button_next = QPushButton()
        self.button_next.setText("Next")
        self.button_next.clicked.connect(self.handle_next)
        self.layout_navigation.addWidget(self.button_next)

        self.layout_navigation.setStretch(0, 1)
        self.layout_navigation.setStretch(1, 0)
        self.layout_navigation.setStretch(2, 0)
        self.layout_navigation.setStretch(3, 0)
        self.layout_navigation.setStretch(4, 0)
        self.layout_raw.addLayout(self.layout_navigation)

        self.layout_raw.setStretch(0, 1)
        self.layout_raw.setStretch(1, 1)
        self.layout_raw.setStretch(2, 1)
        self.layout_raw.setStretch(3, 0)

    def config_list_row(self):
        self.list_row.setMaximumSize(QtCore.QSize(50, 16777215))
        self.list_row.setFont(GLOBAL_FONT)
        self.list_row.setObjectName("list_row")
        self.list_row.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.list_row.setModel(self.row_model)
        self.list_row.selectionModel().selectionChanged.connect(self.handle_row_change)

    def config_list_sheet(self):
        self.list_sheet.setMaximumSize(QtCore.QSize(150, 16777215))
        self.list_sheet.setFont(GLOBAL_FONT)
        self.list_sheet.setObjectName("list_sheet")
        self.list_sheet.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.list_sheet.setModel(self.sheet_model)
        self.list_sheet.selectionModel().selectionChanged.connect(self.handle_sheet_change)

    def config_layout_content(self):
        self.layout_content.setMinimumSize(QtCore.QSize(640, 480))
        self.layout_content.setObjectName("layout_content")
        self.layout_content_hbox = QHBoxLayout(self.layout_content)
        self.layout_content_hbox.setObjectName("horizontalLayout")

    def build_chat_slices(self):
        for i in range(self.chosen_task.chat_round_number):
            layout_chat_slice = QHBoxLayout()
            prompt = PromptCell(parent=self,
                                title=self.chosen_task.task_name + " Prompt Step " + str(i + 1))
            prompt.setStyleSheet("background: rgb(161, 204, 209); selection-background-color: rgb(233, 99, 0);")

            function_name = self.chosen_task.function_name + f"_step_{i + 1}"
            answer = AnswerCell(parent=self,
                                title=self.chosen_task.task_name + " Answer Step " + str(i + 1),
                                function_text="Regenerate",
                                function=getattr(task, function_name))
            if i < len(self.chosen_task.additional_fields):
                answer.field = self.chosen_task.additional_fields[i]
            else:
                answer.field = self.chosen_task.field_name
            answer.setStyleSheet("background: rgb(250, 240, 228); selection-background-color: rgb(233, 99, 0);")

            prompt.sibling = answer
            answer.sibling = prompt

            layout_chat_slice.addWidget(prompt)
            layout_chat_slice.addWidget(answer)
            layout_chat_slice.setStretch(0, 1)
            layout_chat_slice.setStretch(1, 1)
            self.cell_chat_slices.append((prompt, answer))
            self.layout_chat_slice.addLayout(layout_chat_slice)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Inspector"))
        self.menu_open.setTitle(_translate("main_window", "Open"))

    @QtCore.pyqtSlot()
    def choose_file(self):
        self.excel_file = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption='Choose File',
            directory='.',
            filter='*.xlsx', )[0]
        if self.excel_file:
            self.excel_dict = util.handle_excel_file(self.excel_file)
            self.sheet_model.setStringList(self.excel_dict.keys())
        else:
            message_box = QMessageBox(self)
            message_box.setIcon(QMessageBox.Icon.Information)
            message_box.setWindowTitle("No File Chosen")
            message_box.setText("Please choose a valid file to inspect!")
            message_box.exec()

    @QtCore.pyqtSlot(QItemSelection, QItemSelection)
    def handle_sheet_change(self, selected: QItemSelection, deselected: QItemSelection):
        max_index = list(self.excel_dict.values())[selected.indexes()[0].row()]
        self.row_model.setStringList([str(row_index) for row_index in range(2, max_index + 1)])

    @QtCore.pyqtSlot(QItemSelection, QItemSelection)
    def handle_row_change(self, selected: QItemSelection, deselected: QItemSelection):
        if self.excel_file:
            sheet_index = self.list_sheet.selectedIndexes()[0].row()
            sheet_name = list(self.excel_dict.keys())[sheet_index]

            self.question = util.handle_row_question(self.excel_file, sheet_name, selected.indexes()[0].row() + 2)

            self.cells = self.find_question_cells(self)
            for cell in self.cells:
                cell.update_text_content(self.question)

    @QtCore.pyqtSlot()
    def handle_task_change(self, enum_task: EnumTask):
        for chat_slice in self.cell_chat_slices:
            chat_slice[0].deleteLater()
            chat_slice[1].deleteLater()
        self.cell_chat_slices.clear()

        self.chosen_task = enum_task.value
        self.build_chat_slices()

        self.cells = self.find_question_cells(self)
        if self.question:
            for cell in self.cells:
                cell.update_text_content(self.question)
            opinion: str = getattr(self.question, self.chosen_task.opinion_field)
            self.line_opinion.setText(str(opinion))
            if opinion.lower() in ["success", "true", "right", u"对", u"√"]:
                self.line_opinion.setStyleSheet("color: #5cb85c;")
            elif opinion.lower() in ["fail", "false", "wrong", u"错", u"×"]:
                self.line_opinion.setStyleSheet("color: #d81e15;")

    @QtCore.pyqtSlot()
    def handle_prev(self):
        if self.question:
            selection_model = self.list_row.selectionModel()
            target = selection_model.currentIndex().row() - 1
            if target < 0:
                message_box = QMessageBox()
                message_box.setIcon(QMessageBox.Icon.Information)
                message_box.setWindowTitle("Information")
                message_box.setText("You have reached the top!")
                message_box.exec()
            else:
                selection_model.setCurrentIndex(QAbstractItemModel.createIndex(self.row_model, target, 0),
                                                QItemSelectionModel.SelectionFlag.SelectCurrent)

    @QtCore.pyqtSlot()
    def handle_next(self):
        if self.question:
            selection_model = self.list_row.selectionModel()
            target = selection_model.currentIndex().row() + 1
            if target >= self.row_model.rowCount():
                message_box = QMessageBox()
                message_box.setIcon(QMessageBox.Icon.Information)
                message_box.setWindowTitle("Information")
                message_box.setText("You have reached the bottom!")
                message_box.exec()
            else:
                selection_model.setCurrentIndex(QAbstractItemModel.createIndex(self.row_model, target, 0),
                                                QItemSelectionModel.SelectionFlag.SelectCurrent)

    @QtCore.pyqtSlot()
    def handle_success(self):
        if self.question:
            sheet_name = self.question.sheet_name
            row = self.question.row
            index = entity.get_real_index_by_field_name(field_name=self.chosen_task.opinion_field,
                                                        headers=self.question.headers)
            content = "Success"
            util.handle_save(sheet_name, row, index, content, self.excel_file)
            self.line_opinion.setText(str(content))
            self.line_opinion.setStyleSheet("color: #5cb85c;")
            self.notify_update()

    @QtCore.pyqtSlot()
    def handle_fail(self):
        if self.question:
            sheet_name = self.question.sheet_name
            row = self.question.row
            index = entity.get_real_index_by_field_name(field_name=self.chosen_task.opinion_field,
                                                        headers=self.question.headers)
            content = "Fail"
            util.handle_save(sheet_name, row, index, content, self.excel_file)
            self.line_opinion.setText(str(content))
            self.line_opinion.setStyleSheet("color: #d81e15;")
            self.notify_update()

    @staticmethod
    def find_question_cells(q_object: QObject) -> List[QuestionCell]:
        question_cell_list: List[QuestionCell] = []
        if isinstance(q_object, QuestionCell):
            question_cell_list.append(q_object)
        elif q_object.children():
            for o in q_object.children():
                cells = MainWindow.find_question_cells(o)
                if cells:
                    question_cell_list.extend(cells)
        return question_cell_list

    def notify_update(self):
        model = self.list_row.selectionModel()
        selection = model.selection()
        model.selectionChanged.emit(selection, selection)
