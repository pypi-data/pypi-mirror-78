from datetime import datetime
from functools import partial

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtWidgets import QHeaderView

from .component import TabMixin, FileSelectionWidget, PathInput, GuiProgress,\
    run_dialog, SelectionButton
from .model import TableModel
from .parallel import Worker
from ..core.metadata import Purpose
from ..workflows import encrypt


class EncryptTab(QtWidgets.QWidget, TabMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.app_data = self.parent().app_data

        files_panel = self.create_files_panel()
        user_panel = self.create_user_panel()
        output_panel = self.create_output_panel()
        self.create_run_panel("Package and Encrypt data", self.encrypt,
                              "Package && Encrypt")
        self.create_console()
        self.create_progress_bar()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(files_panel)

        layout_split = QtWidgets.QHBoxLayout()
        layout_split.addWidget(user_panel)
        layout_split.addWidget(output_panel)
        layout.addLayout(layout_split)

        layout.addWidget(self.run_panel)
        layout.addWidget(self.console)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def create_files_panel(self):
        box = FileSelectionWidget(
            "Select files and/or directories to encrypt", self)
        box.file_list_model.layoutChanged.connect(
            lambda: setattr(self.app_data, "encrypt_files", box.get_list()))
        return box

    def create_user_panel(self):
        box = QtWidgets.QGroupBox("Select data sender and recipients")
        sender_widget = QtWidgets.QComboBox()
        sender_widget.setModel(self.app_data.priv_keys_model)
        if self.app_data.default_key_index:
            sender_widget.setCurrentIndex(self.app_data.default_key_index)

        recipients_input_view = QtWidgets.QComboBox()
        recipients_input_view.setModel(self.app_data.pub_keys_model)

        recipients_output_view = QtWidgets.QTableView()
        recipients_output_model = TableModel(
            columns=("Name", "Email", "Fingerprint"))
        recipients_output_view.setModel(recipients_output_model)
        recipients_output_view.verticalHeader().hide()
        recipients_output_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        recipients_output_view.horizontalHeader().setStretchLastSection(True)
        recipients_output_view.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows)
        recipients_output_view.setSelectionMode(
            QtWidgets.QTableView.SelectionMode.SingleSelection)

        recipients_btn_add = QtWidgets.QPushButton("+")
        recipients_btn_remove = SelectionButton("Remove selected recipients",
                                                recipients_output_view.selectionModel())

        def update_sender(index):
            self.app_data.encrypt_sender = "" if index == -1 else \
                self.app_data.priv_keys_model.get_value(index).fingerprint

        def update_recipients(index):
            self.app_data.encrypt_recipients = [x[2] for x in
                                                index.model().get_data()]

        def add_recipient():
            key = recipients_input_view.model().get_value(
                recipients_input_view.currentIndex())
            row = (key.uids[0].full_name, key.uids[0].email, key.fingerprint)
            recipients_output_model.set_data(
                set(recipients_output_model.get_data()) | set([row]))

        def remove_recipient():
            recipients_output_view.model() \
                .removeRows(recipients_output_view.currentIndex().row(), 1)
            recipients_output_view.clearSelection()

        # Connect actions
        recipients_btn_add.clicked.connect(add_recipient)
        recipients_btn_remove.clicked.connect(remove_recipient)
        recipients_output_model.dataChanged.connect(update_recipients)
        sender_widget.currentIndexChanged.connect(update_sender)
        # Set the default value for the sender
        update_sender(sender_widget.currentIndex())

        layout = QtWidgets.QVBoxLayout()
        layout_form = QtWidgets.QFormLayout()
        layout_form.addRow("Sender", sender_widget)
        layout_recipients = QtWidgets.QHBoxLayout()
        layout_recipients.addWidget(recipients_input_view)
        layout_recipients.addWidget(recipients_btn_add)
        layout_form.addRow("Recipients", layout_recipients)
        layout.addLayout(layout_form)
        layout.addWidget(recipients_output_view)
        layout.addWidget(recipients_btn_remove)

        box.setLayout(layout)
        return box

    def create_output_panel(self):
        box = QtWidgets.QGroupBox("Select output name and location")
        # Create fields
        transfer_id = QtWidgets.QLineEdit()
        transfer_id.setStatusTip("(optional) Data Transfer Request ID")
        transfer_id.setValidator(QtGui.QIntValidator(1, 10**9))
        purpose = QtWidgets.QComboBox(box)
        purpose.setStatusTip("Purpose of the package")
        purpose.addItems(("",) + tuple(Purpose.__members__.keys()))
        purpose.setCurrentText("")

        offline = QtWidgets.QCheckBox("Offline")
        offline.setStatusTip("Offline mode: skip DTR ID validation and "
                             "key refreshing.")
        offline.setChecked(self.app_data.encrypt_offline)
        compress = QtWidgets.QCheckBox("Compress inner tarball")
        compress.setChecked(self.app_data.encrypt_compress)
        output_suffix = QtWidgets.QLineEdit(box)
        output_suffix.setStatusTip("(optional) File name suffix in the "
	                               "format datetime_suffix.tar")
        output_suffix.setValidator(
            QtGui.QRegExpValidator(QtCore.QRegExp(r"[\w-]*")))
        output_location = PathInput()
        # Add actions

        def on_transfer_id_changed(text):
            self.app_data.encrypt_transfer_id = int(text) if text else None
        transfer_id.textChanged.connect(on_transfer_id_changed)
        offline.stateChanged.connect(lambda state:
            setattr(self.app_data, "encrypt_offline",
                    state == QtCore.Qt.Checked))
        purpose.currentTextChanged.connect(lambda text:
            setattr(self.app_data, "encrypt_purpose",
                    None if text == "" else Purpose(text)))
        compress.stateChanged.connect(lambda state:
                                      setattr(self.app_data, "encrypt_compress",
                                              state == QtCore.Qt.Checked))
        output_suffix.editingFinished.connect(
            lambda: setattr(self.app_data, "encrypt_output_suffix",
                            output_suffix.text()))
        output_location.on_path_change(
            partial(setattr, self.app_data, "encrypt_output_location"))

        layout = QtWidgets.QFormLayout()
        layout.addRow("DTR ID", transfer_id)
        layout.addRow("Purpose", purpose)
        layout.addRow("", offline)
        layout.addRow("Output suffix", output_suffix)
        layout.addRow("Output location", output_location.text)
        layout.addRow("", output_location.btn)
        layout.addRow("Data package", compress)
        box.setLayout(layout)
        return box

    def encrypt(self, dry_run=False):
        warning_msg = []
        if not self.app_data.encrypt_files:
            warning_msg.append("Select files for encryption.")
        if not self.app_data.encrypt_recipients:
            warning_msg.append("Select at least one recipient.")
        if warning_msg:
            msg_warn = QtWidgets.QMessageBox()
            msg_warn.setWindowTitle("Warning")
            msg_warn.setText("\n".join(warning_msg))
            msg_warn.setIcon(QtWidgets.QMessageBox.Warning)
            msg_warn.exec_()
            return

        progress = GuiProgress()
        progress.updated.connect(self.progress_bar.setValue)
        output_path = str(
            self.app_data.encrypt_output_location /
            "_".join(filter(None,
                            [datetime.now().astimezone().strftime(
                                encrypt.DATE_FMT_FILENAME),
                                self.app_data.encrypt_output_suffix])))
        if not dry_run and self.app_data.config.sign_encrypted_data:
            pw = run_dialog(self, "Enter password for your GPG key")
            if pw is None:
                return
        else:
            pw = None
        worker = Worker(
            encrypt.encrypt,
            self.app_data.encrypt_files,
            logger=(encrypt.logger,),
            sender=self.app_data.encrypt_sender,
            recipient=self.app_data.encrypt_recipients,
            dtr_id=self.app_data.encrypt_transfer_id,
            config=self.app_data.config,
            passphrase=pw,
            output_name=output_path,
            dry_run=dry_run,
            offline=self.app_data.encrypt_offline,
            compress=self.app_data.encrypt_compress,
            purpose=self.app_data.encrypt_purpose,
            progress=progress,
            on_error=lambda _: None)
        self.add_worker_actions(worker)
        self.threadpool.start(worker)
