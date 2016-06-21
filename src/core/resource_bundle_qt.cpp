/****************************************************************************
**
** Copyright (C) 2016 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the QtWebEngine module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:LGPL$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** GNU Lesser General Public License Usage
** Alternatively, this file may be used under the terms of the GNU Lesser
** General Public License version 3 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPL3 included in the
** packaging of this file. Please review the following information to
** ensure the GNU Lesser General Public License version 3 requirements
** will be met: https://www.gnu.org/licenses/lgpl-3.0.html.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 2.0 or (at your option) the GNU General
** Public license version 3 or any later version approved by the KDE Free
** Qt Foundation. The licenses are as published by the Free Software
** Foundation and appearing in the file LICENSE.GPL2 and LICENSE.GPL3
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-2.0.html and
** https://www.gnu.org/licenses/gpl-3.0.html.
**
** $QT_END_LICENSE$
**
****************************************************************************/

#include "base/command_line.h"
#include "content/public/common/content_switches.h"
#include "ui/base/resource/resource_bundle.h"
#include "web_engine_library_info.h"

namespace ui {

void ResourceBundle::LoadCommonResources()
{
    // We repacked the resources we need and installed them. now let chromium mmap that file.
    AddDataPackFromPath(WebEngineLibraryInfo::getPath(QT_RESOURCES_PAK), SCALE_FACTOR_NONE);
    AddDataPackFromPath(WebEngineLibraryInfo::getPath(QT_RESOURCES_100P_PAK), SCALE_FACTOR_100P);
    AddDataPackFromPath(WebEngineLibraryInfo::getPath(QT_RESOURCES_200P_PAK), SCALE_FACTOR_200P);
    AddOptionalDataPackFromPath(WebEngineLibraryInfo::getPath(QT_RESOURCES_DEVTOOLS_PAK), SCALE_FACTOR_NONE);
}

gfx::Image& ResourceBundle::GetNativeImageNamed(int resource_id)
{
    LOG(WARNING) << "Unable to load image with id " << resource_id;
    NOTREACHED();  // Want to assert in debug mode.
    return GetEmptyImage();
}

}  // namespace ui
