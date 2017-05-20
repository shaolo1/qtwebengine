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
from PyQt5.QtWidgets import QSizePolicy, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QUrl, QRect
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineProfile, QWebEngineView

from urllineedit import UrlLineEdit
from webpage import WebPage
from webview import WebView


class WebPopupWindow(QWidget):
    def __init__(self, profile: QWebEngineProfile):
        super().__init__()

        self.m_addressBar = UrlLineEdit(self)
        self.m_view = WebView(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        layout = QVBoxLayout()
        # layout.setMargin(0)
        self.setLayout(layout)
        layout.addWidget(self.m_addressBar)
        layout.addWidget(self.m_view)

        self.m_view.setPage(WebPage(profile, self.m_view))
        self.m_view.setFocus()
        self.m_addressBar.setReadOnly(True)
        self.m_addressBar.setFavIcon(QIcon(":defaulticon.png"))

        self.m_view.titleChanged.connect(self.setWindowTitle)
        self.m_view.urlChanged.connect(self.setUrl)
        self.m_view.page().iconChanged.connect(self.handleIconChanged)
        self.m_view.page().geometryChangeRequested.connect(self.handleGeometryChangeRequested)
        self.m_view.page().windowCloseRequested.connect(self.close)

    def view(self) -> QWebEngineView:
        return self.m_view

    def setUrl(self, url: QUrl):
        self.m_addressBar.setUrl(url)

    def handleGeometryChangeRequested(self, newGeometry: QRect):
        self.m_view.setMinimumSize(newGeometry.width(), newGeometry.height())
        self.move(newGeometry.topLeft() - self.m_view.pos())
        # let the layout do the magic
        self.resize(0, 0)
        self.show()

    def handleIconChanged(self, icon: QIcon):
        if icon.isNull():
            self.m_addressBar.setFavIcon(QIcon(":defaulticon.png"))
        else:
            self.m_addressBar.setFavIcon(icon)
