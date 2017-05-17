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
from PyQt5.QtWidgets import QLineEdit, QWidget, QToolButton
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QResizeEvent


class UrlLineEdit(QLineEdit):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.m_favButton = QToolButton(self)
        self.m_clearButton = QToolButton(self)
        self.m_clearButton.setIcon(QIcon(":closetab.png"))
        self.m_clearButton.setVisible(False)
        self.m_clearButton.setCursor(Qt.ArrowCursor)
        style = "QToolButton { border: none; padding: 1px; }"
        self.m_clearButton.setStyleSheet(style)
        self.m_favButton.setStyleSheet(style)
        self.setStyleSheet("QLineEdit {{ padding-left: {}px; padding-right: {}px; }} ".format(
            self.m_clearButton.sizeHint().width(), self.m_favButton.sizeHint().width()))
        minIconHeight = max(self.m_favButton.sizeHint().height(), self.m_clearButton.sizeHint().height())
        self.setMinimumSize(self.minimumSizeHint().width() + self.m_favButton.sizeHint().width() +
                            self.m_clearButton.sizeHint().width(), max(self.minimumSizeHint().height(), minIconHeight))

        self.m_clearButton.clicked.connect(self.clear)
        self.textChanged.connect(self._text_changed)

    def _text_changed(self, text: str):
        self.m_clearButton.setVisible(not not text and not self.isReadOnly())

    def url(self) -> QUrl:
        return QUrl.fromUserInput(self.text())

    def setUrl(self, url: QUrl):
        self.setText(url.toString())
        self.setCursorPosition(0)

    def setFavIcon(self, icon: QIcon):
        pixmap = icon.pixmap(16, 16)
        self.m_favButton.setIcon(QIcon(pixmap))

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        clearButtonSize = self.m_clearButton.sizeHint()
        self.m_clearButton.move(self.rect().right() - clearButtonSize.width(),
                            (self.rect().bottom() - clearButtonSize.height()) // 2)
        self.m_favButton.move(self.rect().left(), (self.rect().bottom() - self.m_favButton.sizeHint().height()) // 2)
