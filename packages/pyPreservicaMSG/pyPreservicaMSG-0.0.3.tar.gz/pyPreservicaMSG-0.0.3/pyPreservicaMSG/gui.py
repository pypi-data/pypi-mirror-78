import configparser
import os
import shutil
import uuid
import email.utils
import datetime
import mimetypes
import xml
from email.policy import default
from os import listdir
from os.path import isfile, join
from pathlib import Path
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement

import PySide2
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import Qt, QRunnable, Slot, QThreadPool, QObject
from PySide2.QtGui import QIcon, QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QAction, QMainWindow, QFileDialog, QTreeView, \
    QAbstractItemView, QProgressDialog
from pyPreservica import EntityAPI

from pyPreservicaMSG import parsemsg, submission
from pyPreservicaMSG.submission import prettify


class CollectionNameDialog(QDialog):

    def __init__(self, entity):
        super().__init__()
        self.collection = None
        self.entity = entity
        self.setFixedSize(450, 180)
        self.folder_name = ""
        self.setWindowTitle("Email Collection")

        self.help_label = QtWidgets.QLabel("Paste the reference of the folder the emails\nshould be ingested into")

        self.folder_label = QtWidgets.QLabel("Folder Reference: ")
        self.folder_ref = QtWidgets.QLineEdit("")

        self.folder_name_label = QtWidgets.QLabel("Folder Name: ")
        self.folder_name_ref = QtWidgets.QLineEdit("")
        self.folder_name_ref.setEnabled(False)

        self.folder_description_label = QtWidgets.QLabel("Folder Description: ")
        self.folder_description_ref = QtWidgets.QLineEdit("")
        self.folder_description_ref.setEnabled(False)

        self.gridlayout = QtWidgets.QGridLayout()
        self.setLayout(self.gridlayout)

        self.gridlayout.addWidget(self.help_label, 1, 1)
        self.gridlayout.addWidget(self.folder_label, 2, 1)
        self.gridlayout.addWidget(self.folder_ref, 2, 2)
        self.gridlayout.addWidget(self.folder_name_label, 3, 1)
        self.gridlayout.addWidget(self.folder_name_ref, 3, 2)
        self.gridlayout.addWidget(self.folder_description_label, 4, 1)
        self.gridlayout.addWidget(self.folder_description_ref, 4, 2)

        self.folder_ref.textChanged.connect(self.find_folder)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        btn = self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)
        self.gridlayout.addWidget(self.buttonBox, 6, 2)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def find_folder(self):
        btn = self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)
        self.folder_name_ref.setText("")
        self.folder_description_ref.setText("")
        self.collection = None
        try:
            f = self.entity.folder(self.folder_ref.text())
            self.folder_name_ref.setText(f.title)
            self.folder_description_ref.setText(f.description)
            self.collection = f.reference
            btn = self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(False)
        except RuntimeError:
            pass

    def collection_ref(self):
        return self.collection

    def accept(self):
        super().accept()

    def reject(self):
        super().reject()


def human_size(bytes, units=[' bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']):
    return str(bytes) + units[0] if bytes < 1024 else human_size(bytes >> 10, units[1:])


class Worker(QRunnable):
    def __init__(self, msg_path, collection_ref, username, password, tenant, server, callback):
        super().__init__()
        self.msg_path = msg_path
        self.collection_ref = collection_ref
        self.server = server
        self.username = username
        self.password = password
        self.tenant = tenant
        self.callback = callback

    @Slot()  # QtCore.Slot
    def run(self):
        ingest_msg(self.msg_path, self.collection_ref, self.username, self.password, self.server, self.tenant,
                   self.callback)


def ingest_msg(path, collection_ref, username, password, server, tenant, callback):
    msg_email = os.path.abspath(path)
    print(msg_email)
    msg_name_ext = os.path.basename(msg_email)
    path = Path(msg_email)
    msg_name = path.stem
    msg_folder = path.parent

    msg = parsemsg.load(msg_email)

    package_dir = str(uuid.uuid4())
    wd = os.path.join(msg_folder, package_dir)
    wd_access = os.path.join(wd, "access")
    wd_preservation = os.path.join(wd, "preservation")
    os.mkdir(wd)
    os.mkdir(wd_access)
    os.mkdir(wd_preservation)

    shutil.copy(msg_email, wd_preservation)

    xml.etree.ElementTree.register_namespace('email', 'http://www.tessella.com/mailbox/v1')
    xip = Element(xml.etree.ElementTree.QName('http://www.tessella.com/mailbox/v1', "email"))
    xip.set('xmlns', 'http://www.tessella.com/mailbox/v1')

    email_md = SubElement(xip, "to")
    email_md.text = msg.get("To", "")
    email_md = SubElement(xip, "from")
    email_md.text = msg.get("From", "")
    email_md = SubElement(xip, "cc")
    email_md.text = msg.get("CC", "")
    email_md = SubElement(xip, "bcc")
    email_md.text = msg.get("BCC", "")
    email_md = SubElement(xip, "date")
    date_str = msg.get("Date", "")

    date = None
    if date_str:
        date_tuple = email.utils.parsedate_tz(date_str)
        if date_tuple:
            date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
    if date:
        email_md.text = date.isoformat()

    email_subject = SubElement(xip, "subject")
    email_subject.text = msg.get("Subject", "")

    numberOfAttachments = SubElement(xip, "numberOfAttachments")

    eml_path = os.path.join(wd_access, msg_name + ".eml")
    with open(eml_path, "wb") as f:
        f.write(msg.as_bytes())

    with open(eml_path, 'rb') as fp:
        msg = email.message_from_binary_file(fp, policy=default)
        print(msg.get("Date"))

        counter = 1
        for part in msg.walk():
            # multipart/* are just containers
            if part.get_content_maintype() == 'multipart':
                continue
            # Applications should really sanitize the given filename so that an
            # email message can't be used to overwrite important files
            filename = part.get_filename()
            if not filename:
                ext = mimetypes.guess_extension(part.get_content_type())
                if not ext:
                    # Use a generic bag-of-bits extension
                    ext = '.bin'
                filename = f'part-{counter:03d}{ext}'
            counter += 1
            access_file = os.path.join(wd_access, filename)
            with open(access_file, 'wb') as part_fp:
                part_fp.write(part.get_payload(decode=True))
                attachmentFileNames = SubElement(xip, "attachmentFileNames")
                attachmentFileNames.text = filename
            shutil.copy(access_file, wd_preservation)

    numberOfAttachments.text = str(counter - 1)

    email_md = SubElement(xip, "sizeInBytes")
    email_md.text = str(path.stat().st_size)

    metadata_path = os.path.join(wd, "metadata.xml")
    metadata = open(metadata_path, "wt", encoding='utf-8')
    metadata.write(prettify(xip))
    metadata.close()

    submission.createSIP(email_subject.text, email_subject.text, "open", collection_ref,
                         wd_preservation, wd_access, metadata_path, server, username,
                         password, tenant, msg_name + ".eml")

    callback()

    shutil.rmtree(wd)


class CallBack(QObject):
    change_value = QtCore.Signal(int)
    change_state = QtCore.Signal(PySide2.QtCore.Qt.CheckState)

    def __init__(self, value):
        QObject.__init__(self)
        self.value = value

    def __call__(self):
        self.change_value.emit(self.value)
        self.change_state.emit(PySide2.QtCore.Qt.CheckState.Unchecked)


class MyWidget(QMainWindow):

    def prettify(elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = xml.etree.ElementTree.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def ingest(self, collection_ref):
        item_model = self.model
        self.progress = QProgressDialog("Uploading packages...", None, 0, item_model.rowCount() - 1)
        self.progress.setMinimum(0)
        self.progress.setMaximum(item_model.rowCount() - 1)
        self.progress.setModal(True)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setWindowTitle("Uploads")
        self.progress.setAutoClose(True)
        self.progress.setAutoReset(True)
        self.progress.show()
        for i in range(item_model.rowCount()):
            callback = CallBack(i)
            standard_item = item_model.item(i, 0)
            if standard_item.checkState() == PySide2.QtCore.Qt.CheckState.Checked:
                email_path = standard_item.text()
                callback.change_value.connect(self.progress.setValue)
                callback.change_state.connect(standard_item.setCheckState)
                worker = Worker(email_path, collection_ref, self.username, self.password, self.tenant, self.server,
                                callback)
                self.threadpool.start(worker)

    def __init__(self):
        super().__init__()
        self.progress = None
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)
        self.setWindowTitle("Preservica Outlook MSG Importer")
        self.windowModality()
        if not os.path.isfile("../credentials.properties"):
            dialog = PasswordDialog()
            if dialog.exec_():
                self.username = dialog.username()
                self.password = dialog.password()
                self.tenant = dialog.tenant()
                self.server = dialog.server()
                self.client = EntityAPI(dialog.username(), dialog.password(), dialog.tenant(), dialog.server())
            else:
                raise SystemExit
        else:
            self.client = EntityAPI()
            config = configparser.ConfigParser()
            config.read('credentials.properties')
            self.username = config['credentials']['username']
            self.password = config['credentials']['password']
            self.tenant = config['credentials']['tenant']
            self.server = config['credentials']['server']

        self.create_menu()

        self.list = QTreeView(self)

        self.setCentralWidget(self.list)

        self.list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['File Name', 'Message Size', 'Subject'])
        self.list.setModel(self.model)
        self.list.setUniformRowHeights(True)
        self.list.setAlternatingRowColors(True)
        self.list.setColumnWidth(0, 350)
        self.list.setColumnWidth(1, 150)
        self.list.setColumnWidth(1, 250)

    def create_menu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        ingestMenu = mainMenu.addMenu("Ingest")

        openActionAll = QAction(QIcon('open.png'), "Open Directory of Outlook Messages", self)
        openActionAll.setShortcut("Ctrl+O")

        openActionSingle = QAction(QIcon('open.png'), "Open Individual Outlook Message", self)
        openActionSingle.setShortcut("Ctrl+m")

        exitAction = QAction(QIcon('exit.png'), "Exit", self)
        exitAction.setShortcut("Ctrl+X")

        ingestAction = QAction(QIcon('open.png'), "Ingest Selected Emails", self)
        ingestAction.setShortcut("Ctrl+I")

        exitAction.triggered.connect(self.exit_app)
        openActionSingle.triggered.connect(self.open_single_msg)
        openActionAll.triggered.connect(self.open_folder_msg)

        ingestAction.triggered.connect(self.ingest_selected)

        fileMenu.addAction(openActionAll)
        fileMenu.addAction(openActionSingle)
        fileMenu.addAction(exitAction)

        ingestMenu.addAction(ingestAction)

    def ingest_selected(self):
        dialog = CollectionNameDialog(self.client)
        if dialog.exec_():
            collection_ref = dialog.collection_ref()
            self.ingest(collection_ref)

    def exit_app(self):
        self.close()

    def open_single_msg(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setViewMode(QFileDialog.Detail)
        dialog.setNameFilter("Outlook Messages (*.msg)")
        if dialog.exec_():
            msgPath = dialog.selectedFiles()
            msg = parsemsg.load(msgPath[0])
            subject = QStandardItem(msg.get("Subject", ""))
            subject.setEditable(False)
            path = os.path.abspath(msgPath[0])
            name = QStandardItem(path)
            size = QStandardItem(human_size(Path(path).stat().st_size))
            size.setEditable(False)
            name.setCheckable(True)
            name.setCheckState(PySide2.QtCore.Qt.CheckState.Checked)
            name.setEditable(False)
            self.model.appendRow([name, size, subject])

    def open_folder_msg(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec_():
            msgPath = dialog.selectedFiles()
            print(msgPath)
            onlyfiles = [f for f in listdir(msgPath[0]) if isfile(join(msgPath[0], f))]
            for msg in onlyfiles:
                if msg.endswith(".msg") or msg.endswith(".MSG"):
                    filename = join(msgPath[0], msg)
                    msg = parsemsg.load(filename)
                    subject = QStandardItem(msg.get("Subject", ""))
                    subject.setEditable(False)
                    name = QStandardItem(os.path.abspath(filename))
                    size = QStandardItem(human_size(Path(os.path.abspath(filename)).stat().st_size))
                    size.setEditable(False)
                    name.setCheckable(True)
                    name.setCheckState(PySide2.QtCore.Qt.CheckState.Checked)
                    name.setEditable(False)
                    self.model.appendRow([name, size, subject])


class PasswordDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enter Preservica Credentials")
        self.resize(300, 200)
        self.setFixedSize(300, 200)

        self.username_label = QtWidgets.QLabel("Username: ")
        self.password_label = QtWidgets.QLabel("Password: ")
        self.tenant_label = QtWidgets.QLabel("Tenant: ")
        self.server_label = QtWidgets.QLabel("Server: ")

        self.username_text = QtWidgets.QLineEdit("")
        self.username_text.setToolTip("This is your username (email) for Preservica")
        self.password_text = QtWidgets.QLineEdit("")
        self.password_text.setEchoMode(QLineEdit.Password)
        self.password_text.setToolTip("This is your password for Preservica")
        self.tenant_text = QtWidgets.QLineEdit("")
        self.tenant_text.setToolTip("This is short code for your tenancy name")
        self.server_text = QtWidgets.QLineEdit("")
        self.server_text.setToolTip("e.g eu.preservica.com or us.preservica.com etc")

        self.save_creds = QtWidgets.QCheckBox("Save Credentials")
        self.save_creds.setToolTip("Save your login details to a local file to auto-login on next run")

        self.gridlayout = QtWidgets.QGridLayout()
        self.setLayout(self.gridlayout)

        self.gridlayout.addWidget(self.username_label, 1, 1)
        self.gridlayout.addWidget(self.password_label, 2, 1)
        self.gridlayout.addWidget(self.tenant_label, 3, 1)
        self.gridlayout.addWidget(self.server_label, 4, 1)

        self.gridlayout.addWidget(self.username_text, 1, 2)
        self.gridlayout.addWidget(self.password_text, 2, 2)
        self.gridlayout.addWidget(self.tenant_text, 3, 2)
        self.gridlayout.addWidget(self.server_text, 4, 2)

        self.gridlayout.addWidget(self.save_creds, 5, 2)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.gridlayout.addWidget(self.buttonBox, 6, 2)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def username(self):
        return self.username_text.text()

    def password(self):
        return self.password_text.text()

    def tenant(self):
        return self.tenant_text.text()

    def server(self):
        return self.server_text.text()

    def accept(self):
        if self.save_creds.isChecked():
            e = EntityAPI(self.username(), self.password(), self.tenant(), self.server())
            e.save_config()

        super().accept()
