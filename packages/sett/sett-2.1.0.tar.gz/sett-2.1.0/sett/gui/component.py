from functools import partial
from pathlib import Path
from typing import Callable, Iterable, List, Optional

from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QItemSelectionModel
from PySide2.QtWidgets import QPushButton

from .parallel import Worker
from ..utils.progress import ProgressInterface


class SelectionButton(QPushButton):
    """A push button extension which connects this button to given selection model.

    The button is disabled by default. And gets enabled when the selection has, at least,
    one selected row.
    """

    def __init__(self, label: str, selection_model: QItemSelectionModel):
        super().__init__(label)
        self.setEnabled(False)
        self._selection_model = selection_model
        selection_model.selectionChanged.connect(self.selection_changed)

    def selection_changed(self):
        # Following works better than using 'QItemSelection', especially in cases
        # where multiple selection is possible
        self.setEnabled(bool(len(self._selection_model.selectedRows())))
        # Repaint the button on each selection changed. Should happen automatically,
        # but does NOT seem to be always the case on Mac OS X.
        self.repaint()


class GuiProgress(QtCore.QObject, ProgressInterface):
    updated = QtCore.Signal(int)
    new_label = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.label = ""
        self.n = 0

    def set_label(self, label):
        self.label = label
        self.new_label.emit(label)

    def update(self, completed_fraction):
        self.n = completed_fraction
        self.updated.emit(round(completed_fraction * 100, 0))

    def get_completed_fraction(self):
        return self.n


class ConsoleWidget(QtWidgets.QGroupBox):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.textbox = QtWidgets.QPlainTextEdit()
        self.textbox.setReadOnly(True)
        btn_clear_console = QtWidgets.QPushButton("Clear console")
        btn_clear_console.clicked.connect(self.clear)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.textbox)
        layout.addWidget(btn_clear_console)
        self.setLayout(layout)

    def clear(self) -> None:
        self.textbox.clear()
        self.textbox.repaint()

    def append(self, text: str) -> None:
        self.textbox.appendPlainText(text)

    def write(self, text: str) -> None:
        self.textbox.appendPlainText(text)


class FileSelectionWidget(QtWidgets.QGroupBox):
    def __init__(self, title, parent, directory=True, archives_only=False):
        super().__init__(title, parent)
        self.path = str(Path.home())
        self.archives_only = archives_only

        self.file_list_model = QtCore.QStringListModel()
        self.file_list_view = QtWidgets.QListView(self)
        self.file_list_view.setModel(self.file_list_model)
        self.file_list_view.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.file_list_view.setLayout(QtWidgets.QVBoxLayout())

        btn_select_files = QtWidgets.QPushButton('Add files', self)
        btn_select_files.clicked.connect(self.add_files)

        self.btn_clear_selected = SelectionButton('Remove selected',
                                                  self.file_list_view.selectionModel())
        self.btn_clear_selected.clicked.connect(self.clear_selected)

        btn_clear_list = QtWidgets.QPushButton('Clear list', self)
        btn_clear_list.clicked.connect(self.clear_list)

        buttons = [btn_select_files, self.btn_clear_selected, btn_clear_list]

        if directory:
            btn_select_dir = QtWidgets.QPushButton('Add directory', self)
            btn_select_dir.clicked.connect(self.add_directory)
            buttons.insert(1, btn_select_dir)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.file_list_view, 0, 0, len(buttons), 1)
        for i, btn in enumerate(buttons):
            layout.addWidget(btn, i, 1)
        self.setLayout(layout)

    def _update_paths(self, paths: Iterable[str]) -> None:
        paths = set(filter(None, paths))
        if paths:
            self.path = Path(next(iter(paths))).parent
        self.file_list_model.setStringList(
            sorted(set(self.file_list_model.stringList()) | paths))
        # TODO this shouldn't be necessary, but it's currently used to notify
        # other (than listview) components about the changes to the files list
        self.file_list_model.layoutChanged.emit()

    def add_files(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        dialog.setDirectory(str(self.path))
        if self.archives_only:
            dialog.setNameFilters(["Archives *.tar (*.tar)"])
            dialog.selectNameFilter("Archives *.tar (*.tar)")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self._update_paths(dialog.selectedFiles())

    def add_directory(self):
        directory = (QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Select directory', str(self.path)))
        self._update_paths((directory, ))

    def clear_selected(self) -> None:
        indices = self.file_list_view.selectedIndexes()
        for index in indices:
            self.file_list_model.removeRows(index.row(), 1)
        self.file_list_model.layoutChanged.emit()

    def clear_list(self) -> None:
        # Clear the selection BEFORE resetting the model
        self.file_list_view.selectionModel().clearSelection()
        self.file_list_model.setStringList([])
        self.file_list_model.layoutChanged.emit()

    def get_list(self) -> List[str]:
        return self.file_list_model.stringList()


class PathInput:
    """Path selection widget with a select button and a show path field."""

    def __init__(self, directory=True, path: Optional[Path] = Path.home(),
                 parent=None):
        self.parent = parent
        self.text = QtWidgets.QLineEdit(parent)
        self.text.setReadOnly(True)
        self.btn = QtWidgets.QPushButton("Change location")
        self.btn.clicked.connect(partial(self._update_location, directory))
        # Additional button to clear the selected path
        self.btn_clear = QtWidgets.QPushButton("Clear")
        self.btn_clear.clicked.connect(self._clear_location)
        self.update_path(path)

    def update_path(self, path: Optional[Path]):
        self.path = path
        self.text.setText("" if path is None else str(path))
        self.text.editingFinished.emit()

    def _update_location(self, directory: bool):
        if self.path and self.path.exists():
            location = self.path if self.path.is_dir() else self.path.parent
        else:
            location = Path.home()
        if directory:
            new_path = QtWidgets.QFileDialog.getExistingDirectory(
                self.parent, "Select Directory", str(location))
        else:
            new_path, _ = QtWidgets.QFileDialog.getOpenFileName(
                self.parent, "Select File", str(location))
        if new_path:
            self.update_path(Path(new_path))

    def _clear_location(self):
        self.update_path(None)

    @property
    def btn_label(self) -> str:
        """Button label"""
        return self.btn.text()

    @btn_label.setter
    def btn_label(self, label: str):
        self.btn.setText(label)

    def on_path_change(self, fn: Callable[[Optional[Path]], None]) -> None:
        """Run callback when path changes."""
        self.text.editingFinished.connect(lambda: fn(self.path))


class TabMixin:
    def create_console(self):
        self.console = ConsoleWidget("Console", self)

    def create_progress_bar(self):
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.hide()

    def create_run_panel(self, panel_name: str, action: Callable,
                         action_name: str):
        self.run_panel = QtWidgets.QGroupBox(panel_name)
        layout = QtWidgets.QHBoxLayout()
        self.btn_test = QtWidgets.QPushButton("Test")
        self.btn_test.clicked.connect(partial(action, dry_run=True))
        self.btn_run = QtWidgets.QPushButton(action_name)
        self.btn_run.clicked.connect(action)
        layout.addWidget(self.btn_test)
        layout.addWidget(self.btn_run)
        self.run_panel.setLayout(layout)

    def add_worker_actions(self, worker: Worker):
        """Attach GUI-updating signals to worker"""
        worker.signals.started.connect(self.progress_bar.show)
        worker.signals.started.connect(
            lambda: self.run_panel.setEnabled(False))
        worker.signals.logging.connect(self.console.write)
        worker.signals.error.connect(lambda e: self.console.append(str(e[1])))
        worker.signals.finished.connect(lambda: self.progress_bar.setValue(0))
        worker.signals.finished.connect(self.progress_bar.hide)
        worker.signals.finished.connect(
            lambda: self.run_panel.setEnabled(True))


def run_dialog(parent, msg: str, password: bool = True):
    dialog_pwd = QtWidgets.QInputDialog(parent)
    dialog_pwd.setLabelText(msg)
    dialog_pwd.setWindowTitle("SETT")
    if password:
        dialog_pwd.setTextEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    if dialog_pwd.exec_() != QtWidgets.QDialog.Accepted or not dialog_pwd.textValue():
        return None
    return dialog_pwd.textValue()
