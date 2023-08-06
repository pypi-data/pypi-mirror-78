import time
import datetime

from PySide2.QtCore import QThread, QMutexLocker, QItemSelectionModel, \
                            Qt, QObject, QMutex, Signal

from PySide2.QtGui import QStandardItemModel, QStandardItem, QIcon, QBrush, \
                            QPen, QPalette, QPixmap, QCursor, QGuiApplication

from PySide2.QtWidgets import QMainWindow, QTreeView, QDialog, QFormLayout, \
                                QSpinBox, QDialogButtonBox, QSpacerItem, \
                                QSizePolicy, QStyledItemDelegate, \
                                QStyleOptionViewItem, QStyle, QWidget, QLabel, \
                                QHBoxLayout, QMenu, QLineEdit, QPushButton, \
                                QFileDialog

from . import resources

from rssht_controller_lib import factories
from rssht_controller_lib import config as cconfig

from . import util
from . import config
from . import data_access


class RSSHTControllerProxy(QObject):
    updating = Signal(QObject)
    updated = Signal(QObject)
    
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self._controller = controller
        self._mutex = QMutex()
    
    def get_controller(self):
        return self._controller
    
    def get_mutex(self):
        return self._mutex
    
    def update(self):
        self.updating.emit(self)
        
        locker = QMutexLocker(self._mutex)
        self._controller.update()
        locker.unlock()
        
        self.updated.emit(self)
    
    def __getattr__(self, name):
        return getattr(self._controller, name)


class _RSSHTControllerUpdater(QThread):
    def __init__(self, sleep_interval, parent=None):
        super().__init__(parent)
        self._sleep_interval = sleep_interval
        sshc = factories.SSHClientFactory.new_connected()
        rda = data_access.RetryDataAccess(sshc)
        controller = factories.RSSHTControllerFactory.new(da=rda)
        self._controllerp = RSSHTControllerProxy(controller)
        self._controllerp.moveToThread(self)
    
    def get_sleep_interval(self):
        return self._sleep_interval
    
    def get_controllerp(self):
        return self._controllerp
    
    def run(self):
        while not self.isInterruptionRequested():
            self._controllerp.update()
            timestamp = time.time()
            
            while (not self.isInterruptionRequested() and
                    time.time() - timestamp < self._sleep_interval):
                time.sleep(min(0.5, self._sleep_interval))


class RSSHTControllerConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.resize(400, 150)
        self.setWindowTitle('Settings')
        
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        self.setLayout(form)
        
        self._server_addr_edit = QLineEdit()
        form.addRow('Server address:', self._server_addr_edit)
        
        self._server_port_spin = QSpinBox()
        self._server_port_spin.setRange(1, 65535)
        form.addRow('Server port:', self._server_port_spin)
        
        self._server_username_edit = QLineEdit()
        form.addRow('Server username:', self._server_username_edit)
        
        key_filename_container = QWidget()
        key_filename_layout = QHBoxLayout()
        key_filename_layout.setContentsMargins(0, 0, 0, 0)
        key_filename_container.setLayout(key_filename_layout)
        
        self._key_filename_edit = QLineEdit()
        self._key_filename_edit.setReadOnly(True)
        key_filename_layout.addWidget(self._key_filename_edit)
        
        key_filename_button = QPushButton(QIcon(':folder.svg'), None)
        key_filename_button.clicked.connect(self.select_key_filename)
        key_filename_layout.addWidget(key_filename_button)
        
        form.addRow('Key filename:', key_filename_container)
        
        self._server_swap_dir_edit = QLineEdit()
        form.addRow('Server swap directory:', self._server_swap_dir_edit)
        
        self._sleep_interval_spin = QSpinBox()
        self._sleep_interval_spin.setRange(0, 60 * 60 * 24)
        form.addRow('Sleep interval (secs):', self._sleep_interval_spin)
        
        self._last_seen_alarm_spin = QSpinBox()
        self._last_seen_alarm_spin.setRange(0, 60 * 60 * 24)
        form.addRow('"Last Seen" alarm (secs):', self._last_seen_alarm_spin)
        
        form.addItem(QSpacerItem(0, 5000, 
                                QSizePolicy.Expanding, QSizePolicy.Expanding))
        
        button_box = QDialogButtonBox(QDialogButtonBox.Save | 
                                    QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.save)
        button_box.rejected.connect(self.reject)
        form.addRow(button_box)
        
        self.load()
    
    def select_key_filename(self):
        cur_key_filename = self._key_filename_edit.text()
        selected_key_filename, filter_ = QFileDialog.getOpenFileName(self, 
                                                        'Select Key Filename', 
                                                        cur_key_filename)
        if selected_key_filename:
            self._key_filename_edit.setText(selected_key_filename)
    
    def load(self):
        self._server_addr_edit.setText(cconfig.RSSHT_SERVER_ADDR)
        self._server_port_spin.setValue(cconfig.RSSHT_SERVER_PORT)
        self._server_username_edit.setText(cconfig.RSSHT_SERVER_USERNAME)
        self._key_filename_edit.setText(cconfig.KEY_FILENAME)
        self._server_swap_dir_edit.setText(cconfig.RSSHT_SERVER_SWAP_DIR)
        self._sleep_interval_spin.setValue(config.UPDATE_SLEEP_INTERVAL)
        self._last_seen_alarm_spin.setValue(config.AGENT_LAST_SEEN_ALARM_THRESHOLD)
    
    def save(self):
        cconfig.RSSHT_SERVER_ADDR = self._server_addr_edit.text()
        cconfig.RSSHT_SERVER_PORT = self._server_port_spin.value()
        cconfig.RSSHT_SERVER_USERNAME = self._server_username_edit.text()
        cconfig.KEY_FILENAME = self._key_filename_edit.text()
        cconfig.RSSHT_SERVER_SWAP_DIR = self._server_swap_dir_edit.text()
        config.UPDATE_SLEEP_INTERVAL = self._sleep_interval_spin.value()
        config.AGENT_LAST_SEEN_ALARM_THRESHOLD = self._last_seen_alarm_spin.value()
        
        try:
            util.persist_config()
        finally:
            self.accept()


class OpenRSSHTDialog(QDialog):
    def __init__(self, agent_id, bind_port=None, dest_port=None, parent=None):
        super().__init__(parent)
        self._agent_id = agent_id
        self._bind_port = bind_port
        self._dest_port = dest_port
        
        self.resize(400, 150)
        self.setWindowTitle(f'Open Tunnel For: {self._agent_id}')
        
        form = QFormLayout()
        self.setLayout(form)
        
        self._bind_port_spin = QSpinBox()
        self._bind_port_spin.setRange(1024, 65535)
        if self._bind_port is not None:
            self._bind_port_spin.setValue(self._bind_port)
        form.addRow('Bind port:', self._bind_port_spin)
        
        self._dest_port_spin = QSpinBox()
        self._dest_port_spin.setRange(1, 65535)
        if self._dest_port is not None:
            self._dest_port_spin.setValue(self._dest_port)
        form.addRow('Dest port:', self._dest_port_spin)
        
        form.addItem(QSpacerItem(0, 5000, 
                                QSizePolicy.Expanding, QSizePolicy.Expanding))
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | 
                                    QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        form.addRow(button_box)
    
    def get_agent_id(self):
        return self._agent_id
    
    def get_bind_port(self):
        return self._bind_port
    
    def get_dest_port(self):
        return self._dest_port
    
    def accept(self):
        self._bind_port = self._bind_port_spin.value()
        self._dest_port = self._dest_port_spin.value()
        super().accept()


class CustomStyledItemDelegate(QStyledItemDelegate):
    def paint(self, painter, options, index):
        is_selected = options.state & QStyle.State_Selected
        
        options.state &= ~QStyle.State_Selected
        options.state &= ~QStyle.State_HasFocus
        super().paint(painter, options, index)
        
        if is_selected:
            painter.save()
            pen = QPen(options.palette.color(QPalette.Highlight))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawLine(options.rect.topLeft(), options.rect.topRight())
            painter.drawLine(options.rect.bottomLeft(), options.rect.bottomRight())
            painter.restore()


class RSSHTControllerWindow(QMainWindow):
    (
    AGENT_ID_COL,
    STATUS_TIMEDELTA_COL,
    RSSHT_SERVER_ADDR_COL,
    BINDED_PORT_COL,
    DEST_PORT_COL,
    CONTROLLER_ID_COL,
    CMDLINE_TIMEDELTA_COL,
    ) = range(7)
    
    FIRST_APP_SPEC_ROLE = Qt.UserRole + 1
    
    (
    SORT_ROLE,
    ) = range(FIRST_APP_SPEC_ROLE, FIRST_APP_SPEC_ROLE + 1)
    
    ICON_FILENAME = {
        cconfig.RSSHT_CMD: ':/open-tunnel.svg',
        cconfig.TERM_RSSHT_CMD: ':/close-tunnel.svg',
        'copy': ':/copy.svg',
        'edit-settings': ':/edit-settings.svg',
    }
    
    def __init__(self):
        super().__init__()
        
        self._update_sleep_interval = None
        self._alarm_threshold = None
        self._updater = None
        self._controllerp = None
        
        self.resize(800, 600)
        self.setWindowTitle('Remote SSH Tunnel Controller')
        self.setWindowIcon(QIcon(self.ICON_FILENAME[cconfig.RSSHT_CMD]))
        
        cmd_toolbar = self.addToolBar('Command')
        self._open_rssht_action = cmd_toolbar.addAction(
            QIcon(self.ICON_FILENAME[cconfig.RSSHT_CMD]), 'Open Tunnel')
        self._open_rssht_action.triggered.connect(self.open_rssht)
        self._close_rssht_action = cmd_toolbar.addAction(
            QIcon(self.ICON_FILENAME[cconfig.TERM_RSSHT_CMD]), 'Close Tunnel')
        self._close_rssht_action.triggered.connect(self.close_rssht)
        self._copy_binded_action = cmd_toolbar.addAction(
            QIcon(self.ICON_FILENAME['copy']), 'Copy Binded addr:port')
        self._copy_binded_action.triggered.connect(self.copy_binded)
        
        edit_toolbar = self.addToolBar('Edit')
        self._edit_settings_action = edit_toolbar.addAction(
            QIcon(self.ICON_FILENAME['edit-settings']), 'Settings')
        self._edit_settings_action.triggered.connect(self.edit_settings)
        
        self._menu = QMenu(self)
        self._menu.addAction(self._open_rssht_action)
        self._menu.addAction(self._close_rssht_action)
        self._menu.addAction(self._copy_binded_action)
        
        self._treeview = QTreeView()
        
        self._treeview_model = QStandardItemModel(self._treeview)
        self._treeview_model.setHorizontalHeaderLabels([
            'Agent ID', 
            'Last Seen', 
            'SSH Server', 
            'Binded Port', 
            'Dest Port', 
            'Cmd Author', 
            'Cmd Time'])
        self._treeview_model.setSortRole(self.SORT_ROLE)
        self._treeview.setModel(self._treeview_model)
        
        self._treeview.setItemDelegate(CustomStyledItemDelegate(self._treeview))
        self._treeview.setSortingEnabled(True)
        self._treeview.header().setSortIndicator(self.AGENT_ID_COL, Qt.AscendingOrder)
        self._treeview.header().setSectionsMovable(False)
        
        width = self.size().width()
        agent_id_col_width = int(0.2 * width)
        other_col_width = int((width - agent_id_col_width) / 6)
        
        self._treeview.setColumnWidth(self.AGENT_ID_COL, agent_id_col_width - 2)
        self._treeview.setColumnWidth(self.STATUS_TIMEDELTA_COL, other_col_width)
        self._treeview.setColumnWidth(self.RSSHT_SERVER_ADDR_COL, other_col_width)
        self._treeview.setColumnWidth(self.BINDED_PORT_COL, other_col_width)
        self._treeview.setColumnWidth(self.DEST_PORT_COL, other_col_width)
        self._treeview.setColumnWidth(self.CONTROLLER_ID_COL, other_col_width)
        self._treeview.setColumnWidth(self.CMDLINE_TIMEDELTA_COL, other_col_width)
        
        self._treeview.setContextMenuPolicy(Qt.CustomContextMenu)
        
        self._treeview.activated.connect(self.on_activated)
        self._treeview.customContextMenuRequested.connect(self.on_menu_requested)
        self._treeview.selectionModel().selectionChanged.connect(
                                                    self.on_selection_changed)
        
        self.setCentralWidget(self._treeview)
        
        self.statusBar()
        self._agent_counter = QLabel()
        self._agent_counter.is_permanent = True
        self.statusBar().addPermanentWidget(self._agent_counter)
        
        self.update_actions()
    
    def startUpdater(self, update_sleep_interval=None, alarm_threshold=None):
        assert not self._updater
        
        if update_sleep_interval is not None:
            self._update_sleep_interval = update_sleep_interval
        else:
            self._update_sleep_interval = config.UPDATE_SLEEP_INTERVAL
        
        if alarm_threshold is not None:
            self._alarm_threshold = alarm_threshold
        else:
            self._alarm_threshold = config.AGENT_LAST_SEEN_ALARM_THRESHOLD
        
        self._updater = _RSSHTControllerUpdater(self._update_sleep_interval, 
                                                parent=self)
        self._controllerp = self._updater.get_controllerp()
        self._controllerp.updating.connect(self.on_fetch)
        self._controllerp.updated.connect(self.on_fetched)
        self._controllerp.updated.connect(self.update)
        self._updater.start()
        
        self.update_actions()
    
    def stopUpdater(self):
        if not self._updater:
            return
        self._updater.requestInterruption()
        self._updater.wait()
        self._controllerp.dispose()
        
        self._updater = None
        self._controllerp = None
        self.clear_status_bar()
        self.update_actions()
    
    def restartUpdater(self, update_sleep_interval=None, alarm_threshold=None):
        self.stopUpdater()
        self.startUpdater(update_sleep_interval, alarm_threshold)
    
    def closeEvent(self, event):
        self.stopUpdater()
        event.accept()
    
    def on_activated(self, index):
        self.open_rssht()
    
    def on_menu_requested(self, pos):
        self._menu.popup(QCursor.pos())
    
    def on_selection_changed(self, selected, deselected):
        self.update_actions()
    
    def update_actions(self):
        if self._treeview.selectionModel().hasSelection():
            self._open_rssht_action.setEnabled(True)
            self._close_rssht_action.setEnabled(True)
            self._copy_binded_action.setEnabled(True)
        else:
            self._open_rssht_action.setEnabled(False)
            self._close_rssht_action.setEnabled(False)
            self._copy_binded_action.setEnabled(False)
        
        if not self._updater:
            self._open_rssht_action.setEnabled(False)
            self._close_rssht_action.setEnabled(False)
    
    def clear_status_bar(self, exclude_permanent=True):
        status_bar = self.statusBar()
        
        status_bar.clearMessage()
        
        for child in status_bar.children():
            if isinstance(child, QWidget):
                if not exclude_permanent \
                    or not hasattr(child, 'is_permanent') \
                    or not child.is_permanent:
                    
                    status_bar.removeWidget(child)
    
    def on_fetch(self, controllerp):
        if controllerp.is_disposed():
            return
        self.clear_status_bar()
        self.statusBar().showMessage('Fetching info...')
    
    def on_fetched(self, controllerp):
        if controllerp.is_disposed():
            return
        self.clear_status_bar()
    
    def update(self, controllerp, lock_mutex=True):
        if controllerp.is_disposed():
            return
        if lock_mutex:
            locker = QMutexLocker(controllerp.get_mutex())
        
        header = self._treeview.header()
        sel_model = self._treeview.selectionModel()
        model = self._treeview_model
        status_bar = self.statusBar()
        
        # Save state
        
        if sel_model.hasSelection():
            selected_agent_id = self._selected_data(self.AGENT_ID_COL)
        else:
            selected_agent_id = None
        
        cur_index = sel_model.currentIndex()
        
        if cur_index.isValid():
            cur_agent_id = model.data(model.index(cur_index.row(), 0))
            cur_col = cur_index.column()
        else:
            cur_agent_id = None
            cur_col = None
        
        # Clear
        
        model.removeRows(0, model.rowCount())
        alarm_count = 0
        self.clear_status_bar()
        
        # Update
        
        for agent in controllerp.get_agents():
            rssht_server_addr = agent.get_da().get_sshc().get_transport()\
                                                            .getpeername()[0]
            agent_id = agent.get_id()
            agent_status = agent.get_status()
            status_timestamp = agent_status.get_timestamp()
            status_timedelta = datetime.datetime.now(
                                datetime.timezone.utc) - status_timestamp
            trigger_alarm = \
                        status_timedelta.total_seconds() > self._alarm_threshold
            cmdline = agent_status.get_cmdline()
            
            if cmdline:
                cmdline_timestamp = cmdline.get_timestamp()
                cmdline_timedelta = datetime.datetime.now(
                                    datetime.timezone.utc) - cmdline_timestamp
                controller_id = cmdline.get_controller_id()
                uuid_ = cmdline.get_uuid()
                args = cmdline.get_args()
                
                if cmdline.get_cmd() == cconfig.RSSHT_CMD:
                    binded_port, dest_port = args
                else:  # cmdline.get_cmd() == cconfig.TERM_RSSHT_CMD
                    binded_port = None
                    dest_port = None
                
                cmdline_status = cmdline.get_status()
            else:
                cmdline_timedelta = None
                controller_id = None
                binded_port = None
                dest_port = None
                cmdline_status = None
            
            history = agent.get_cmdline_history()
            
            if not history or history[-1] == cmdline or \
                (cmdline and cmdline_timestamp >= history[-1].get_timestamp()):
                in_progress = False
                in_progress_icon_filename = None
                in_progress_icon = None
                in_progress_bind_port = None
                in_progress_dest_port = None
                in_progress_desc = None
            else:
                in_progress = True
                
                if history[-1].get_cmd() == cconfig.RSSHT_CMD:
                    in_progress_icon_filename = self.ICON_FILENAME[cconfig.RSSHT_CMD]
                    in_progress_icon = QIcon(in_progress_icon_filename)
                    in_progress_bind_port = history[-1].get_args()[0]
                    in_progress_dest_port = history[-1].get_args()[1]
                    in_progress_desc = f'Opening tunnel '\
                                f'{rssht_server_addr}:{in_progress_bind_port}'\
                                f':{agent_id}:{in_progress_dest_port}...'
                else:
                    in_progress_icon_filename = self.ICON_FILENAME[cconfig.TERM_RSSHT_CMD]
                    in_progress_icon = QIcon(in_progress_icon_filename)
                    in_progress_desc = f'Closing tunnel to {agent_id}...'
            
            cmdline_failed = cmdline_status not in (None, 0)
            
            agent_id_repr = agent_id
            status_timedelta_repr = \
                f'{util.timedelta_repr(status_timedelta)} ago'
            rssht_server_addr_repr = f'{rssht_server_addr}'
            
            if not cmdline:
                binded_port_repr = ''
                dest_port_repr = ''
            elif cmdline.get_cmd() == cconfig.TERM_RSSHT_CMD:
                binded_port_repr = '-'
                dest_port_repr = '-'
            else:  # cmdline.get_cmd() == cconfig.RSSHT_CMD
                binded_port_repr = f'{binded_port}'
                dest_port_repr = f'{dest_port}'
            
            controller_id_repr = '' if controller_id is None else controller_id
            cmdline_timedelta_repr = '' if cmdline_timedelta is None else \
                f'{util.timedelta_repr(cmdline_timedelta)} ago'
            
            flags = (
                Qt.ItemIsEnabled
                #|Qt.ItemIsEditable
                |Qt.ItemIsSelectable
                |Qt.ItemIsUserCheckable
                |Qt.ItemIsDragEnabled
                #|Qt.ItemIsDropEnabled
            )
            
            agent_id_item = QStandardItem(agent_id_repr)
            agent_id_item.setFlags(flags)
            agent_id_item.setData(agent_id_repr, self.SORT_ROLE)
            
            if in_progress:
                agent_id_item.setData(in_progress_icon, Qt.DecorationRole)
                
                height = status_bar.contentsRect().height() - 5
                
                widget = QWidget()
                widget.setMaximumHeight(height)
                
                layout = QHBoxLayout()
                layout.setContentsMargins(0, 0, 0, 0)
                widget.setLayout(layout)
                
                pixmap_label = QLabel()
                pixmap_label.setPixmap(QPixmap(in_progress_icon_filename)
                                            .scaledToHeight(height))
                layout.addWidget(pixmap_label)
                
                text_label = QLabel()
                text_label.setText(in_progress_desc)
                layout.addWidget(text_label)
                
                status_bar.addWidget(widget)
            
            status_timedelta_item = QStandardItem(status_timedelta_repr)
            status_timedelta_item.setFlags(flags)
            status_timedelta_item.setData(status_timedelta.total_seconds(), self.SORT_ROLE)
            
            if trigger_alarm:
                alarm_count += 1
                status_timedelta_item.setData(QBrush(Qt.red), Qt.BackgroundRole)
            
            rssht_server_addr_item = QStandardItem(rssht_server_addr_repr)
            rssht_server_addr_item.setFlags(flags)
            rssht_server_addr_item.setData(rssht_server_addr_repr, self.SORT_ROLE)
            
            binded_port_item = QStandardItem(binded_port_repr)
            binded_port_item.setFlags(flags)
            binded_port_item.setData(binded_port_repr, self.SORT_ROLE)
            
            if cmdline_failed:
                binded_port_item.setData(QBrush(Qt.red), Qt.BackgroundRole)
            
            dest_port_item = QStandardItem(dest_port_repr)
            dest_port_item.setFlags(flags)
            dest_port_item.setData(dest_port_repr, self.SORT_ROLE)
            
            if cmdline_failed:
                dest_port_item.setData(QBrush(Qt.red), Qt.BackgroundRole)
            
            controller_id_item = QStandardItem(controller_id_repr)
            controller_id_item.setFlags(flags)
            controller_id_item.setData(controller_id_repr, self.SORT_ROLE)
            
            cmdline_timedelta_item = QStandardItem(cmdline_timedelta_repr)
            cmdline_timedelta_item.setFlags(flags)
            cmdline_timedelta_item.setData(0 if cmdline_timedelta is None 
                                        else cmdline_timedelta.total_seconds(), 
                                        self.SORT_ROLE)
            
            model.appendRow([
                agent_id_item, 
                status_timedelta_item, 
                rssht_server_addr_item, 
                binded_port_item, 
                dest_port_item, 
                controller_id_item, 
                cmdline_timedelta_item])
        
        row_count = model.rowCount()
        active_agents = row_count - alarm_count
        self._agent_counter.setText(f'{active_agents} / {row_count} agents')
        
        # Restore state
        
        if selected_agent_id is not None:
            items = model.findItems(selected_agent_id)
            
            if items:
                agent_id_index = items[0].index()
                sel_model.select(agent_id_index, 
                        QItemSelectionModel.Select | QItemSelectionModel.Rows)
        
        if cur_agent_id is not None:
            items = model.findItems(cur_agent_id)
            
            if items:
                agent_id_index = items[0].index()
                cur_index = model.index(agent_id_index.row(), cur_col)
                sel_model.setCurrentIndex(cur_index, 
                        QItemSelectionModel.Current)
        
        if header.isSortIndicatorShown():
            sort_section = header.sortIndicatorSection()
            sort_order = header.sortIndicatorOrder()
            model.sort(sort_section, sort_order)
        
    def _selected_data(self, col):
        sel_model = self._treeview.selectionModel()
        index = sel_model.selectedRows(col)[0]
        return self._treeview_model.data(index)
    
    def _selected_agent(self):
        agent_id = self._selected_data(self.AGENT_ID_COL)
        return self._agent(agent_id)
    
    def _agent(self, agent_id):
        return next(filter(lambda a: a.get_id() == agent_id, 
                            self._controllerp.get_agents()))
    
    def open_rssht(self):
        if not self._treeview.selectionModel().hasSelection():
            return
        
        agent_id = self._selected_data(self.AGENT_ID_COL)
        
        binded_port = self._selected_data(self.BINDED_PORT_COL)
        binded_port = None if binded_port in ('', '-') else int(binded_port)
        
        dest_port = self._selected_data(self.DEST_PORT_COL)
        dest_port = None if dest_port in ('', '-') else int(dest_port)
        
        dialog = OpenRSSHTDialog(agent_id, binded_port, dest_port, self)
        
        if dialog.exec_() == QDialog.Rejected:
            return
        
        new_bind_port = dialog.get_bind_port()
        new_dest_port = dialog.get_dest_port()
        
        locker = QMutexLocker(self._controllerp.get_mutex())
        
        agent = self._agent(agent_id)
        agent.push_rssht_cmdline(new_bind_port, new_dest_port)
        
        self.update(self._controllerp, False)
    
    def close_rssht(self):
        locker = QMutexLocker(self._controllerp.get_mutex())
        
        if not self._treeview.selectionModel().hasSelection():
            return
        
        agent = self._selected_agent()
        agent.push_term_rssht_cmdline()
        
        self.update(self._controllerp, False)
    
    def copy_binded(self):
        if not self._treeview.selectionModel().hasSelection():
            return
        
        binded_addr = self._selected_data(self.RSSHT_SERVER_ADDR_COL)
        binded_port = self._selected_data(self.BINDED_PORT_COL)
        
        QGuiApplication.clipboard().setText(f'{binded_addr}:{binded_port}')
    
    def edit_settings(self):
        dialog = RSSHTControllerConfigDialog(self)
        if dialog.exec_() == QDialog.Rejected:
            return
        self.restartUpdater()
