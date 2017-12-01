#!/bin/bash

# Linux
uname_out="$(uname -s)"
case "$uname_out" in 
  Linux* )
    case "${ARCH}" in
      (32)
        _file="chimera-${PKG_VERSION}-linux.bin"
        _filepath="linux/${_file}"
        _installdir="UCSF-Chimera-${PKG_VERSION}"
      ;;
      (64)
        _file="chimera-${PKG_VERSION}-linux_x86_64.bin"
        _filepath="linux_x86_64/${_file}"
        _installdir="UCSF-Chimera64-${PKG_VERSION}"
      ;;
    esac
  ;;
# MacOS X
  Darwin* )
    case "${ARCH}" in
      (32)
        _file="chimera-${PKG_VERSION}-mac.dmg"
        _filepath="mac/${_file}"
        _installdir="UCSF-Chimera-${PKG_VERSION}"
      ;;
      (64)
        _file="chimera-${PKG_VERSION}-mac64.dmg"
        _filepath="mac64/${_file}"
        _installdir="UCSF-Chimera64-${PKG_VERSION}"
      ;;
    esac
  ;;
# Emulated Windows
  CYGWIN*|MINGW*|MSYS*)
    case "${ARCH}" in
      (32)
        _file="chimera-${PKG_VERSION}-win32.exe"
        _filepath="win32/${_file}"
        _installdir="UCSF-Chimera-${PKG_VERSION}"
      ;;
      (64)
        _file="chimera-${PKG_VERSION}-win64.exe"
        _filepath="win64/${_file}"
        _installdir="UCSF-Chimera64-${PKG_VERSION}"
      ;;
    esac
  ;;
esac

download(){
  cd "${SRC_DIR}"
  set +x
  echo 'IMPORTANT: By downloading you accept the UCSF Chimera Non-Commercial Software License Agreement!'
  echo 'IMPORTANT: The license agreement can be found here: http://www.cgl.ucsf.edu/chimera/license.html'
  echo 'IMPORTANT: If you do not agree, please press Ctrl-C now.'
  echo 'IMPORTANT: Downloading in 10 seconds...'

  sleep 10
  set -x
  _downloader="https://www.rbvi.ucsf.edu/chimera/cgi-bin/secure/chimera-get.py"
  _download=`curl -s -F file="${_filepath}" -F choice=Accept "${_downloader}" | grep href | sed -E 's/.*href="(.*)">/\1/'`
  curl "https://www.rbvi.ucsf.edu""${_download}" -o "${_file}"
}

installation_linux() {
  cd "${SRC_DIR}"

  # Prepare the directory structure.
  install -dm755 "${PREFIX}/lib"

  # Run the installer.
  chmod +x "${_file}"
  echo "${PREFIX}/lib/${_installdir}" | "./${_file}"
}

installation_mac() {
  cd "${SRC_DIR}"

  _mountdir=$(echo `hdiutil mount "${_file}" | tail -1 | awk '{$1=$2=""; print $0}'` | xargs -0 echo) \
  && installer -pkg "${_mountdir}/"*.pkg -target "${PREFIX}/lib/${_installdir}" \
  && hdiutil detach "${_mountdir}"
}

installation_win() {
  cd "${SRC_DIR}"
  cmd.exe /C "START /WAIT ${_file} /SILENT /NOICONS /SUPPRESSMSGBOXES /DIR=""${PREFIX}\\Library\\${_installdir}"""
}

softlink() {
  ln -s "${PREFIX}/lib/${_installdir}/bin/chimera" "${PREFIX}/bin/chimera"
}

softlink_win() {
  ln -s "${PREFIX}\\Library\\${_installdir}\\bin\\chimera.exe" "${PREFIX}\\Scripts\\chimera.exe"
}

download
# Linux
uname_out="$(uname -s)"
case "$uname_out" in 
  Linux* )
    installation_linux
    softlink
  ;;
# MacOS X
  Darwin* )
    installation_mac
    softlink
  ;;
# Emulated Windows
  CYGWIN*|MINGW*|MSYS*)
    installation_win
    softlink_win
  ;;
esac