from functools import partial

from PySide2 import QtWidgets, QtCore

from .component import TabMixin, FileSelectionWidget, PathInput, GuiProgress, run_dialog
from .parallel import Worker
from ..workflows import decrypt


class DecryptTab(QtWidgets.QWidget, TabMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.app_data = self.parent().app_data

        files_panel = self.create_files_panel()
        decrypt_options_panel = self.create_decrypt_options_panel()
        self.create_run_panel("Decrypt data", self.decrypt,
                              "Decrypt selected files")
        self.create_console()
        self.create_progress_bar()

        layout = QtWidgets.QGridLayout()
        layout.addWidget(files_panel, 0, 0, 1, 2)
        layout.addWidget(decrypt_options_panel, 1, 0, 1, 2)
        layout.addWidget(self.run_panel, 2, 0, 1, 2)
        layout.addWidget(self.console, 3, 0, 1, 2)
        layout.addWidget(self.progress_bar, 4, 0, 1, 2)
        self.setLayout(layout)

    def create_files_panel(self):
        box = FileSelectionWidget("Select files to decrypt",
                                  self, directory=False, archives_only=True)
        box.file_list_model.layoutChanged.connect(
            lambda: setattr(self.app_data, "decrypt_files", box.get_list()))
        return box

    def create_decrypt_options_panel(self):
        box = QtWidgets.QGroupBox("Select data decryption options")

        group_extract = QtWidgets.QButtonGroup(box)
        btn_decrypt_and_extract = QtWidgets.QRadioButton(
            "Decrypt and unpack files")
        btn_decrypt_and_extract.setChecked(
            not self.app_data.decrypt_decrypt_only)
        btn_decrypt_only = QtWidgets.QRadioButton("Decrypt only")
        btn_decrypt_only.toggled.connect(
            lambda: setattr(self.app_data, "decrypt_decrypt_only",
                            btn_decrypt_only.isChecked()))
        group_extract.addButton(btn_decrypt_and_extract)
        group_extract.addButton(btn_decrypt_only)
        output_location = PathInput()
        output_location.on_path_change(
            partial(setattr, self.app_data, "decrypt_output_location"))

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(btn_decrypt_and_extract, 0, 0)
        layout.addWidget(btn_decrypt_only, 1, 0)
        layout.addWidget(QtWidgets.QLabel("Output location"), 2, 0)
        layout.addWidget(output_location.text, 2, 1)
        layout.addWidget(output_location.btn, 2, 2)
        box.setLayout(layout)
        return box

    def decrypt(self, dry_run=False):
        if not self.app_data.decrypt_files:
            msg_warn = QtWidgets.QMessageBox()
            msg_warn.setWindowTitle("Warning")
            msg_warn.setText("Select files for decryption.")
            msg_warn.setIcon(QtWidgets.QMessageBox.Warning)
            msg_warn.exec_()
            return
        progress = GuiProgress()
        progress.updated.connect(self.progress_bar.setValue)
        if not dry_run:
            pw = run_dialog(self, "Enter password for your GPG key")
            if pw is None:
                return
        else:
            pw = None
        worker = Worker(
            decrypt.decrypt,
            files=self.app_data.decrypt_files,
            logger=(decrypt.logger,),
            output_dir=str(self.app_data.decrypt_output_location),
            config=self.app_data.config,
            decrypt_only=self.app_data.decrypt_decrypt_only,
            passphrase=pw,
            dry_run=dry_run,
            progress=progress,
            on_error=lambda _: None)
        self.add_worker_actions(worker)
        self.threadpool.start(worker)
