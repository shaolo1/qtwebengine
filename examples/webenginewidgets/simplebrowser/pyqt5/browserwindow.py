"""
Copyright (C) 2017 shao.lo <shao.lo@gmail.com>
This is a derived work, original license and copyright:
/****************************************************************************
**
** Copyright (C) 2016 The Qt Company Ltd.
** Contact: http://www.qt.io/licensing/
**
** This file is part of the examples of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:BSD$
** You may use this file under the terms of the BSD license as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of The Qt Company Ltd nor the names of its
**     contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/
"""
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QWidget, QVBoxLayout, QMenu, QToolBar, QFileDialog, QMessageBox, QProgressBar
from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtGui import QIcon, QKeySequence, QCloseEvent
from PyQt5.QtWebEngineWidgets import QWebEnginePage

from tabwidget import TabWidget
from urllineedit import UrlLineEdit
from webview import WebView

# import simplebrowser_rc


class BrowserWindow(QMainWindow):
    def __init__(self, parent: QWidget=None, flags: Qt.WindowFlags=Qt.Widget):
        super().__init__(parent, flags)
        self.m_tabWidget = TabWidget(self)
        self.m_progressBar = QProgressBar(self)
        self.m_historyBackAction = None
        self.m_historyForwardAction = None
        self.m_stopAction = None
        self.m_reloadAction = None
        self.m_stopReloadAction = None
        self.m_urlLineEdit = UrlLineEdit(self)
        self.setToolButtonStyle(Qt.ToolButtonFollowStyle)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        toolbar = self.createToolBar()
        self.addToolBar(toolbar)
        # self.menuBar().addMenu(self.createFileMenu(self.m_tabWidget))  # TODO: menu not created if done like this?
        self.createFileMenu(self.m_tabWidget)
        # self.menuBar().addMenu(self.createViewMenu(toolbar))
        self.createViewMenu(toolbar)
        # self.menuBar().addMenu(self.createWindowMenu(self.m_tabWidget))
        self.createWindowMenu(self.m_tabWidget)
        # self.menuBar().addMenu(self.createHelpMenu())
        self.createHelpMenu()

        centralWidget = QWidget(self)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        # layout.setMargin(0)
        self.addToolBarBreak()

        self.m_progressBar.setMaximumHeight(1)
        self.m_progressBar.setTextVisible(False)
        self.m_progressBar.setStyleSheet("QProgressBar {border: 0px } QProgressBar.chunk { background-color: red }")

        layout.addWidget(self.m_progressBar)
        layout.addWidget(self.m_tabWidget)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.m_tabWidget.titleChanged.connect(self.handleWebViewTitleChanged)
        self.m_tabWidget.linkHovered.connect(self._link_hovered)
        self.m_tabWidget.loadProgress.connect(self.handleWebViewLoadProgress)
        self.m_tabWidget.urlChanged.connect(self.handleWebViewUrlChanged)
        self.m_tabWidget.iconChanged.connect(self.handleWebViewIconChanged)
        self.m_tabWidget.webActionEnabledChanged.connect(self.handleWebActionEnabledChanged)
        self.m_urlLineEdit.returnPressed.connect(self._return_pressed)

        self.m_urlLineEdit.setFavIcon(QIcon(":defaulticon.png"))

        self.handleWebViewTitleChanged(self.tr("Qt Simple Browser"))
        self.m_tabWidget.createTab()

    def _link_hovered(self, url: str):
        self.statusBar().showMessage(url)

    def _return_pressed(self):
        self.m_urlLineEdit.setFavIcon(QIcon(":defaulticon.png"))
        self.loadPageUrl(self.m_urlLineEdit.url())

    def sizeHint(self) -> QSize:
        desktopRect = QApplication.desktop().screenGeometry()
        size = desktopRect.size()
        return QSize(int(size.width() * 0.9), int(size.height() * 0.9))

    def createFileMenu(self, tabWidget: TabWidget) -> QMenu:
        fileMenu = self.menuBar().addMenu(self.tr("&File"))
        # fileMenu = QMenu(self.tr("&File"))  # TODO: menu not created if done like this?...menu goes out of scope and is destroyed beore being added in caller?
        # self.file_menu = QMenu(self.tr("&File"))  # Saving as a member fixes the above issue
        # fileMenu = self.file_menu
        # fileMenu = QMenu(self.tr("&File"), self) # TODO: crashes if done like this?
        fileMenu.addAction(self.tr("&New Window"), self.handleNewWindowTriggered, QKeySequence.New)

        newTabAction = QAction(QIcon(":addtab.png"), self.tr("New &Tab"), self)
        newTabAction.setShortcuts(QKeySequence.AddTab)
        newTabAction.setIconVisibleInMenu(False)
        newTabAction.triggered.connect(tabWidget.createTab)
        fileMenu.addAction(newTabAction)

        fileMenu.addAction(self.tr("&Open File..."), self.handleFileOpenTriggered, QKeySequence.Open)
        fileMenu.addSeparator()

        closeTabAction = QAction(QIcon(":closetab.png"), self.tr("&Close Tab"), self)
        closeTabAction.setShortcuts(QKeySequence.Close)
        closeTabAction.setIconVisibleInMenu(False)
        closeTabAction.triggered.connect(lambda: tabWidget.closeTab(tabWidget.currentIndex()))
        fileMenu.addAction(closeTabAction)

        closeAction = QAction(self.tr("&Quit"),self)
        closeAction.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_Q))
        closeAction.triggered.connect(self.close)
        fileMenu.addAction(closeAction)

        fileMenu.aboutToShow.connect(lambda: self._about_to_show(closeAction))
        return fileMenu

    def _about_to_show(self, closeAction):
        from browser import Browser
        if len(Browser.instance().windows()) == 1:
            closeAction.setText(self.tr("&Quit"))
        else:
            closeAction.setText(self.tr("&Close Window"))

    def createViewMenu(self, toolbar: QToolBar) -> QMenu:
        # viewMenu = QMenu(self.tr("&View"))
        viewMenu = self.menuBar().addMenu(self.tr("&View"))
        self.m_stopAction = viewMenu.addAction(self.tr("&Stop"))
        shortcuts = [QKeySequence(Qt.CTRL | Qt.Key_Period), Qt.Key_Escape]
        self.m_stopAction.setShortcuts(shortcuts)
        self.m_stopAction.triggered.connect(lambda: self.m_tabWidget.triggerWebPageAction(QWebEnginePage.Stop))

        self.m_reloadAction = viewMenu.addAction(self.tr("Reload Page"))
        self.m_reloadAction.setShortcuts(QKeySequence.Refresh)
        self.m_reloadAction.triggered.connect(lambda: self.m_tabWidget.triggerWebPageAction(QWebEnginePage.Reload))

        zoomIn = viewMenu.addAction(self.tr("Zoom &In"))
        zoomIn.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_Plus))
        zoomIn.triggered.connect(self._zoom_in)

        zoomOut = viewMenu.addAction(self.tr("Zoom &Out"))
        zoomOut.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_Minus))
        zoomOut.triggered.connect(self._zoom_out)

        resetZoom = viewMenu.addAction(self.tr("Reset &Zoom"))
        resetZoom.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_0))
        resetZoom.triggered.connect(self._zoom_reset)

        viewMenu.addSeparator()
        viewToolbarAction = QAction(self.tr("Hide Toolbar"),self)
        viewToolbarAction.setShortcut(self.tr("Ctrl+|"))
        viewToolbarAction.triggered.connect(lambda: self._view_toolbar(toolbar, viewToolbarAction))
        viewMenu.addAction(viewToolbarAction)

        viewStatusbarAction = QAction(self.tr("Hide Status Bar"), self)
        viewStatusbarAction.setShortcut(self.tr("Ctrl+/"))
        viewStatusbarAction.triggered.connect(lambda: self._view_statusbar(viewStatusbarAction))
        viewMenu.addAction(viewStatusbarAction)
        return viewMenu

    def _zoom_in(self):
        if self.currentTab():
            self.currentTab().setZoomFactor(self.currentTab().zoomFactor() + 0.1)

    def _zoom_out(self):
        if self.currentTab():
            self.currentTab().setZoomFactor(self.currentTab().zoomFactor() - 0.1)

    def _zoom_reset(self):
        if self.currentTab():
            self.currentTab().setZoomFactor(1.0)

    def _view_toolbar(self, toolbar: QToolBar, viewToolbarAction: QAction):
        if toolbar.isVisible():
            viewToolbarAction.setText(self.tr("Show Toolbar"))
            toolbar.close()
        else:
            viewToolbarAction.setText(self.tr("Hide Toolbar"))
            toolbar.show()

    def _view_statusbar(self, viewStatusbarAction: QAction):
            if self.statusBar().isVisible():
                viewStatusbarAction.setText(self.tr("Show Status Bar"))
                self.statusBar().close()
            else:
                viewStatusbarAction.setText(self.tr("Hide Status Bar"))
                self.statusBar().show()

    def createWindowMenu(self, tabWidget: TabWidget) -> QMenu:
        # menu = QMenu(self.tr("&Window"))
        menu = self.menuBar().addMenu(self.tr("&Window"))

        nextTabAction = QAction(self.tr("Show Next Tab"), self)
        shortcuts = [QKeySequence(Qt.CTRL | Qt.Key_BraceRight),
                     QKeySequence(Qt.CTRL | Qt.Key_PageDown),
                     QKeySequence(Qt.CTRL | Qt.Key_BracketRight),
                     QKeySequence(Qt.CTRL | Qt.Key_Less)]
        nextTabAction.setShortcuts(shortcuts)
        nextTabAction.triggered.connect(tabWidget.nextTab)

        previousTabAction = QAction(self.tr("Show Previous Tab"), self)
        shortcuts.clear()
        shortcuts.append(QKeySequence(Qt.CTRL | Qt.Key_BraceLeft))
        shortcuts.append(QKeySequence(Qt.CTRL | Qt.Key_PageUp))
        shortcuts.append(QKeySequence(Qt.CTRL | Qt.Key_BracketLeft))
        shortcuts.append(QKeySequence(Qt.CTRL | Qt.Key_Greater))
        previousTabAction.setShortcuts(shortcuts)
        previousTabAction.triggered.connect(tabWidget.previousTab)

        menu.aboutToShow.connect(lambda: self._about_to_show_window_menu(menu, nextTabAction, previousTabAction))
        return menu

    def _about_to_show_window_menu(self, menu, nextTabAction, previousTabAction):
        menu.clear()
        menu.addAction(nextTabAction)
        menu.addAction(previousTabAction)
        menu.addSeparator()

        from browser import Browser
        windows = Browser.instance().windows()
        for index, window in enumerate(windows):
            action = menu.addAction(window.windowTitle(), self.handleShowWindowTriggered)
            action.setData(index)
            action.setCheckable(True)
            if window == self:
                action.setChecked(True)

    def createHelpMenu(self) -> QMenu:
        # helpMenu = QMenu(self.tr("&Help"))
        helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        helpMenu.addAction(self.tr("About &Qt"), QApplication.aboutQt)
        return helpMenu

    def createToolBar(self) -> QToolBar:
        navigationBar = QToolBar(self.tr("Navigation"))
        navigationBar.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)
        navigationBar.toggleViewAction().setEnabled(False)

        self.m_historyBackAction = QAction(self)
        backShortcuts = QKeySequence.keyBindings(QKeySequence.Back)
        for i, x in enumerate(reversed(backShortcuts)):
            if x[0] == Qt.Key_Backspace:
                # Chromium already handles navigate on backspace when appropriate.
                backShortcuts.pop(i)

        # For some reason Qt doesn't bind the dedicated Back key to Back.
        backShortcuts.append(QKeySequence(Qt.Key_Back))
        self.m_historyBackAction.setShortcuts(backShortcuts)
        self.m_historyBackAction.setIconVisibleInMenu(False)
        self.m_historyBackAction.setIcon(QIcon(":go-previous.png"))
        self.m_historyBackAction.triggered.connect(lambda: self.m_tabWidget.triggerWebPageAction(QWebEnginePage.Back))
        navigationBar.addAction(self.m_historyBackAction)

        self.m_historyForwardAction = QAction(self)
        fwdShortcuts = QKeySequence.keyBindings(QKeySequence.Forward)
        for i, x in enumerate(reversed(fwdShortcuts)):
            if x[0] & Qt.Key_unknown == Qt.Key_Backspace:
                fwdShortcuts.pop(i)
        fwdShortcuts.append(QKeySequence(Qt.Key_Forward))
        self.m_historyForwardAction.setShortcuts(fwdShortcuts)
        self.m_historyForwardAction.setIconVisibleInMenu(False)
        self.m_historyForwardAction.setIcon(QIcon(":go-next.png"))
        self.m_historyForwardAction.triggered.connect(lambda: self.m_tabWidget.triggerWebPageAction(QWebEnginePage.Forward))
        navigationBar.addAction(self.m_historyForwardAction)

        self.m_stopReloadAction = QAction(self)
        self.m_stopReloadAction.triggered.connect(lambda: self.m_tabWidget.triggerWebPageAction(
            QWebEnginePage.WebAction(self.m_stopReloadAction.data())))
        navigationBar.addAction(self.m_stopReloadAction)
        navigationBar.addWidget(self.m_urlLineEdit)
        size = self.m_urlLineEdit.sizeHint().height()
        navigationBar.setIconSize(QSize(size, size))
        return navigationBar

    def handleWebViewIconChanged(self, icon: QIcon):
        self.m_urlLineEdit.setFavIcon(icon)

    def handleWebViewUrlChanged(self, url: QUrl):
        self.m_urlLineEdit.setUrl(url)
        if url.isEmpty():
            self.m_urlLineEdit.setFocus()

    def handleWebActionEnabledChanged(self, action: QWebEnginePage.WebAction, enabled: bool):
        if action == QWebEnginePage.Back:
            self.m_historyBackAction.setEnabled(enabled)
            return
        if action == QWebEnginePage.Forward:
            self.m_historyForwardAction.setEnabled(enabled)
            return
        if action == QWebEnginePage.Reload:
            self.m_reloadAction.setEnabled(enabled)
            return
        if action == QWebEnginePage.Stop:
            self.m_stopAction.setEnabled(enabled)
            return
        # qWarning
        print("Unhandled webActionChanged signal", action, flush=True)

    def handleWebViewTitleChanged(self, title: str):
        if not title:
            self.setWindowTitle(self.tr("Qt Simple Browser"))
        else:
            self.setWindowTitle(self.tr("{} - Qt Simple Browser").format(title))

    def handleNewWindowTriggered(self):
        window = BrowserWindow()
        from browser import Browser
        Browser.instance().addWindow(window)
        window.loadHomePage()

    def handleFileOpenTriggered(self):
        file, success = QFileDialog.getOpenFileName(self, self.tr("Open Web Resource"), '',
                                           self.tr("Web Resources (*.html *.htm *.svg *.png *.gif *.svgz)All files (*.*)"))
        if not file:
            return
        self.loadPage(file)

    def closeEvent(self, event: QCloseEvent):
        if self.m_tabWidget.count() > 1:
            ret = QMessageBox.warning(self, self.tr("Confirm close"),
                                      self.tr("Are you sure you want to close the window ?\n"
                                              "There are {} tabs open.").format(self.m_tabWidget.count()),
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if ret == QMessageBox.No:
                event.ignore()
                return
        event.accept()
        # deleteLater()

    def loadHomePage(self):
        self.loadPage("http://www.qt.io")

    def loadPage(self, page: str):
        self.loadPageUrl(QUrl.fromUserInput(page))

    def loadPageUrl(self, url: QUrl):
        if url.isValid():
            self.m_urlLineEdit.setUrl(url)
            self.m_tabWidget.setUrl(url)

    def tabWidget(self) -> TabWidget:
        return self.m_tabWidget

    def currentTab(self) -> WebView:
        return self.m_tabWidget.currentWebView()

    def handleWebViewLoadProgress(self, progress: int):
        stopIcon = QIcon(":process-stop.png")
        reloadIcon = QIcon(":view-refresh.png")

        if progress < 100 and progress > 0:
            self.m_stopReloadAction.setData(QWebEnginePage.Stop)
            self.m_stopReloadAction.setIcon(stopIcon)
            self.m_stopReloadAction.setToolTip(self.tr("Stop loading the current page"))
        else:
            self.m_stopReloadAction.setData(QWebEnginePage.Reload)
            self.m_stopReloadAction.setIcon(reloadIcon)
            self.m_stopReloadAction.setToolTip(self.tr("Reload the current page"))
        self.m_progressBar.setValue(progress if progress < 100 else 0)

    def handleShowWindowTriggered(self):
        action = self.sender()
        if isinstance(action, QAction):
            offset = action.data()
            from browser import Browser
            windows = Browser.instance().windows()
            activate = windows[offset]
            activate.activateWindow()
            if isinstance(windows[offset], BrowserWindow):  # WebPopupWindow instances have no tabs
                windows[offset].currentTab().setFocus()
