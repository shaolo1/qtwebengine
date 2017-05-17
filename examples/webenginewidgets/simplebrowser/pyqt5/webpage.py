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
from PyQt5.QtWidgets import QStyle, QDialog, QMessageBox
from PyQt5.QtCore import Qt, QUrl, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineProfile, QWebEngineCertificateError
from PyQt5.QtNetwork import QAuthenticator

from ui_certificateerrordialog import Ui_CertificateErrorDialog
from ui_passworddialog import Ui_PasswordDialog


class WebPage(QWebEnginePage):
    def __init__(self, profile: QWebEngineProfile, parent: QObject):
        super().__init__(profile, parent)
        self.authenticationRequired.connect(self.handleAuthenticationRequired)
        self.proxyAuthenticationRequired.connect(self.handleProxyAuthenticationRequired)

    def certificateError(self, error: QWebEngineCertificateError) -> bool:
        mainWindow = self.view().window()
        if (error.isOverridable()):
            dialog = QDialog(mainWindow)
            dialog.setModal(True)
            dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
            certificateDialog = Ui_CertificateErrorDialog()
            certificateDialog.setupUi(dialog)
            certificateDialog.m_iconLabel.setText('')
            icon = QIcon(mainWindow.style().standardIcon(QStyle.SP_MessageBoxWarning, 0, mainWindow))
            certificateDialog.m_iconLabel.setPixmap(icon.pixmap(32, 32))
            certificateDialog.m_errorLabel.setText(error.errorDescription())
            dialog.setWindowTitle(self.tr("Certificate Error"))
            return dialog.exec() == QDialog.Accepted

        QMessageBox.critical(mainWindow, self.tr("Certificate Error"), error.errorDescription())
        return False

    def handleAuthenticationRequired(self, requestUrl: QUrl, auth: QAuthenticator):
        mainWindow = self.view().window()
        dialog = QDialog(mainWindow)
        dialog.setModal(True)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        passwordDialog = Ui_PasswordDialog()
        passwordDialog.setupUi(dialog)

        passwordDialog.m_iconLabel.setText('')
        icon = QIcon(mainWindow.style().standardIcon(QStyle.SP_MessageBoxQuestion, mainWindow))
        passwordDialog.m_iconLabel.setPixmap(icon.pixmap(32, 32))

        # introMessage = self.tr("Enter username and password for \"{}\" at {}").format(
        #     auth.realm(), requestUrl.toString().toHtmlEscaped())
        # passwordDialog.m_infoLabel.setText(introMessage)
        # passwordDialog.m_infoLabel.setWordWrap(True)
        #
        # if (dialog.exec() == QDialog.Accepted):
        #     auth.setUser(passwordDialog.m_userNameLineEdit.text())
        #     auth.setPassword(passwordDialog.m_passwordLineEdit.text())
        # else:
        #     # Set authenticator null if dialog is cancelled
        #     *auth = QAuthenticator()

    def handleProxyAuthenticationRequired(self, QUrl , auth: QAuthenticator, proxyHost: str):
        mainWindow = self.view().window()
        dialog = QDialog(mainWindow)
        dialog.setModal(True)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        passwordDialog = Ui_PasswordDialog()
        passwordDialog.setupUi(dialog)

        passwordDialog.m_iconLabel.setText('')
        icon = QIcon(mainWindow.style().standardIcon(QStyle.SP_MessageBoxQuestion, 0, mainWindow))
        passwordDialog.m_iconLabel.setPixmap(icon.pixmap(32, 32))

        # introMessage = self.tr("Connect to proxy \"%1\" using:").fromat(proxyHost.toHtmlEscaped())
        # passwordDialog.m_infoLabel.setText(introMessage)
        # passwordDialog.m_infoLabel.setWordWrap(True)
        #
        # if (dialog.exec() == QDialog.Accepted):
        #     auth.setUser(passwordDialog.m_userNameLineEdit.text())
        #     auth.setPassword(passwordDialog.m_passwordLineEdit.text())
        # else:
        #     # Set authenticator null if dialog is cancelled
        #     *auth = QAuthenticator()
