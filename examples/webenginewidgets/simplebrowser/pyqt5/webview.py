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
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QContextMenuEvent
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtWidgets import QWidget, QMessageBox, QAction

from webpage import WebPage


class WebView(QWebEngineView):
    webActionEnabledChanged = pyqtSignal(QWebEnginePage.WebAction, bool)

    def __init__(self, parent: QWidget=None):
        super().__init__(parent)
        self.m_loadProgress = 0
        self.loadProgress.connect(self._load_progress)
        self.loadFinished.connect(self._load_finished)
        self.renderProcessTerminated.connect(self._render_process_terminated)

    def _load_progress(self, progress: int):
        self.m_loadProgress = progress

    def _load_finished(self, success: bool):
        if not success:
            self.m_loadProgress = 0

    def _render_process_terminated(self, termStatus: QWebEnginePage.RenderProcessTerminationStatus, statusCode: int):
        if termStatus == QWebEnginePage.NormalTerminationStatus:
            status = self.tr("Render process normal exit")
        elif termStatus == QWebEnginePage.AbnormalTerminationStatus:
            status = self.tr("Render process abnormal exit")
        elif termStatus == QWebEnginePage.CrashedTerminationStatus:
            status = self.tr("Render process crashed")
        elif termStatus == QWebEnginePage.KilledTerminationStatus:
            status = self.tr("Render process killed")
        else:
            status = ''
        btn = QMessageBox.question(self.window(), status,
                                   self.tr("Render process exited with code: %1\n"
                                           "Do you want to reload the page ?").format(statusCode))
        if btn == QMessageBox.Yes:
            QTimer.singleShot(0, self.reload)

    def setPage(self, page: WebPage):
        if page is not None:
            self.createWebActionTrigger(page, QWebEnginePage.Forward)
            self.createWebActionTrigger(page, QWebEnginePage.Back)
            self.createWebActionTrigger(page, QWebEnginePage.Reload)
            self.createWebActionTrigger(page, QWebEnginePage.Stop)
        super().setPage(page)

    def get_loadProgress(self) -> int:
        return self.m_loadProgress

    def createWebActionTrigger(self, page: QWebEnginePage, webAction: QWebEnginePage.WebAction):
        action = page.action(webAction)
        action.changed.connect(self._emit_action)

    def _emit_action(self):
        action = self.sender()
        webAction = action.data()
        self.webActionEnabledChanged.emit(webAction, action.isEnabled())

    def isWebActionEnabled(self, webAction: QWebEnginePage.WebAction) -> bool:
        return self.page().action(webAction).isEnabled()

    def createWindow(self, type: QWebEnginePage.WebWindowType) -> QWebEngineView:
        if type == QWebEnginePage.WebBrowserTab:
            mainWindow = self.window()
            return mainWindow.tabWidget().createTab()
        if type == QWebEnginePage.WebBrowserBackgroundTab:
            mainWindow = self.window()
            return mainWindow.tabWidget().createTab(False)
        if type == QWebEnginePage.WebBrowserWindow:
            from browserwindow import BrowserWindow
            from browser import Browser
            mainWindow = BrowserWindow()
            Browser.instance().addWindow(mainWindow)
            return mainWindow.currentTab()
        if type == QWebEnginePage.WebDialog:
            from webpopupwindow import WebPopupWindow
            popup = WebPopupWindow(self.page().profile())
            return popup.view()
        print('createWindow: unhandled type', type)
        return None

    def contextMenuEvent(self, event: QContextMenuEvent):
        menu = self.page().createStandardContextMenu()
        actions = menu.actions()
        open_action = self.page().action(QWebEnginePage.OpenLinkInThisWindow)
        index = next((i for i, x in enumerate(actions) if x == open_action), -1)
        if index != -1:
            actions[index].setText(self.tr("Open Link in self Tab"))
            before = QAction() if index==len(actions) else actions[index+1]
            menu.insertAction(before, self.page().action(QWebEnginePage.OpenLinkInNewWindow))
            menu.insertAction(before, self.page().action(QWebEnginePage.OpenLinkInNewTab))
        self.popup_menu = menu  # keep from going out of scope too soon and not being displayed
        menu.popup(event.globalPos())
