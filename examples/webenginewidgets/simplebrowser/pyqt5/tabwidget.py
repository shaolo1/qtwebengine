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
from PyQt5.QtWidgets import QWidget, QTabWidget, QTabBar, QMenu
from PyQt5.QtCore import Qt, QUrl, QPoint, pyqtSignal
from PyQt5.QtGui import QCursor, QIcon, QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineProfile

from webpage import WebPage
from webview import WebView


class TabWidget(QTabWidget):
    linkHovered = pyqtSignal(str)
    loadProgress = pyqtSignal(int)
    titleChanged = pyqtSignal(str)
    urlChanged = pyqtSignal(QUrl)
    iconChanged = pyqtSignal(QIcon)
    webActionEnabledChanged = pyqtSignal(QWebEnginePage.WebAction, bool)

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        tabBar = self.tabBar()
        tabBar.setTabsClosable(True)
        tabBar.setSelectionBehaviorOnRemove(QTabBar.SelectPreviousTab)
        tabBar.setMovable(True)
        tabBar.setContextMenuPolicy(Qt.CustomContextMenu)
        tabBar.customContextMenuRequested.connect(self.handleContextMenuRequested)
        tabBar.tabCloseRequested.connect(self.closeTab)
        tabBar.tabBarDoubleClicked.connect(self._tab_double_clicked)

        self.setDocumentMode(True)
        self.setElideMode(Qt.ElideRight)

        self.currentChanged.connect(self.handleCurrentChanged)

    def _tab_double_clicked(self, index):
        if index != -1:
            return
        self.createTab()

    def handleCurrentChanged(self, index: int):
        if index != -1:
            view = self.webView(index)
            if not view.url().isEmpty():
                view.setFocus()
            self.titleChanged.emit(view.title())
            self.loadProgress.emit(view.get_loadProgress())
            self.urlChanged.emit(view.url())
            pageIcon = view.page().icon()
            if not pageIcon.isNull():
                self.iconChanged.emit(pageIcon)
            else:
                self.iconChanged.emit(QIcon(":defaulticon.png"))
            self.webActionEnabledChanged.emit(QWebEnginePage.Back, view.isWebActionEnabled(QWebEnginePage.Back))
            self.webActionEnabledChanged.emit(QWebEnginePage.Forward, view.isWebActionEnabled(QWebEnginePage.Forward))
            self.webActionEnabledChanged.emit(QWebEnginePage.Stop, view.isWebActionEnabled(QWebEnginePage.Stop))
            self.webActionEnabledChanged.emit(QWebEnginePage.Reload, view.isWebActionEnabled(QWebEnginePage.Reload))
        else:
            self.titleChanged.emit('')
            self.loadProgress.emit(0)
            self.urlChanged.emit(QUrl())
            self.iconChanged.emit(QIcon(":defaulticon.png"))
            self.webActionEnabledChanged.emit(QWebEnginePage.Back, False)
            self.webActionEnabledChanged.emit(QWebEnginePage.Forward, False)
            self.webActionEnabledChanged.emit(QWebEnginePage.Stop, False)
            self.webActionEnabledChanged.emit(QWebEnginePage.Reload, True)

    def handleContextMenuRequested(self, pos: QPoint):
        menu = QMenu()
        menu.addAction(self.tr("New &Tab"), self.createTab, QKeySequence.AddTab)
        index = self.tabBar().tabAt(pos)
        if index != -1:
            action = menu.addAction(self.tr("Clone Tab"))
            action.triggered.connect(lambda: self.cloneTab(index))

            menu.addSeparator()
            action = menu.addAction(self.tr("&Close Tab"))
            action.setShortcut(QKeySequence.Close)
            action.triggered.connect(lambda: self.closeTab(index))
            action = menu.addAction(self.tr("Close &Other Tabs"))
            action.triggered.connect(lambda: self.closeOtherTabs(index))
            menu.addSeparator()
            action = menu.addAction(self.tr("Reload Tab"))
            action.setShortcut(QKeySequence.Refresh)
            action.triggered.connect(lambda: self.reloadTab(index))
        else:
            menu.addSeparator()
        menu.addAction(self.tr("Reload All Tabs"), self.reloadAllTabs)
        menu.exec(QCursor.pos())

    def currentWebView(self) -> WebView:
        return self.webView(self.currentIndex())

    def webView(self, index: int) -> WebView:
        return self.widget(index)

    def setupView(self, webView: WebView):
        webPage = webView.page()

        webView.titleChanged.connect(self._title_changed)
        webView.urlChanged.connect(self._url_changed)
        webView.loadProgress.connect(self._load_progress)
        webPage.linkHovered.connect(self._link_hovered)
        webPage.iconChanged.connect(self._icon_changed)
        webView.webActionEnabledChanged.connect(self._web_action_enabled_changed)
        webView.loadStarted.connect(self._load_started)
        webPage.windowCloseRequested.connect(self._window_close_requested)

    def _title_changed(self, title: str):
        webView = self.sender()
        index = self.indexOf(webView)
        if index != -1:
            self.setTabText(index, title)
        if self.currentIndex() == index:
            self.titleChanged.emit(title)

    def _url_changed(self, url: QUrl):
        webView = self.sender()
        index = self.indexOf(webView)
        if index != -1:
            self.tabBar().setTabData(index, url)
        if self.currentIndex() == index:
            self.urlChanged.emit(url)

    def _load_progress(self, progress: int):
        webView = self.sender()
        if not isinstance(webView, QWidget):
            print('_load_progress...wrong sender?', webView.type, progress)
            return
        if self.currentIndex() == self.indexOf(webView):
            self.loadProgress.emit(progress)

    def _link_hovered(self, url: str):
        webView = self.sender().view()
        if self.currentIndex() == self.indexOf(webView):
            self.linkHovered.emit(url)

    def _icon_changed(self, icon: QIcon):
        webView = self.sender().view()
        index = self.indexOf(webView)
        ico = QIcon(":defaulticon.png") if icon.isNull() else icon
        if index != -1:
            self.setTabIcon(index, ico)
        if self.currentIndex() == index:
            self.iconChanged.emit(ico)

    def _web_action_enabled_changed(self, action: QWebEnginePage.WebAction, enabled: bool):
        webView = self.sender()
        if self.currentIndex() ==  self.indexOf(webView):
            self.webActionEnabledChanged.emit(action, enabled)

    def _load_started(self):
        webView = self.sender()
        index = self.indexOf(webView)
        if index != -1:
            self.setTabIcon(index, QIcon(":view-refresh.png"))

    def _window_close_requested(self):
        webView = self.sender()
        index = self.indexOf(webView)
        if index >= 0:
            self.closeTab(index)

    def createTab(self, makeCurrent: bool=True) -> WebView:
        webView = WebView()
        webPage = WebPage(QWebEngineProfile.defaultProfile(), webView)
        webView.setPage(webPage)
        self.setupView(webView)
        self.addTab(webView, self.tr("(Untitled)"))
        if makeCurrent:
            self.setCurrentWidget(webView)
        return webView

    def reloadAllTabs(self):
        for i in range(self.count()):
            self.webView(i).reload()

    def closeOtherTabs(self, index: int):
        for i in range(self.count() - 1, index, -1):
            self.closeTab(i)
        for i in range(index - 1, -1, -1):
            self.closeTab(i)

    def closeTab(self, index: int):
        view = self.webView(index)
        if view:
            hasFocus = view.hasFocus()
            self.removeTab(index)
            if hasFocus and self.count() > 0:
                self.currentWebView().setFocus()
            if self.count() == 0:
                self.createTab()
            view.deleteLater()

    def cloneTab(self, index: int):
        view = self.webView(index)
        if view:
            tab = self.createTab(False)
            tab.setUrl(view.url())

    def setUrl(self, url: QUrl):
        view = self.currentWebView()
        if view:
            view.setUrl(url)
            view.setFocus()

    def triggerWebPageAction(self, action: QWebEnginePage.WebAction):
        view = self.currentWebView()
        if view:
            view.triggerPageAction(action)
            view.setFocus()

    def nextTab(self):
        next_ = self.currentIndex() + 1
        if next_ == self.count():
            next_ = 0
        self.setCurrentIndex(next_)

    def previousTab(self):
        next_ = self.currentIndex() - 1
        if next_ < 0:
            next_ = self.count() - 1
        self.setCurrentIndex(next_)

    def reloadTab(self, index: int):
        view = self.webView(index)
        if view:
            view.reload()
