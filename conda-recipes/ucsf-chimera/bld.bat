#!/bin/bash

case "${ARCH}" in
  (32)
    _file="chimera-${PKG_VERSION}-win32.exe"
    _filepath="win32/${_file}"
    _installdir="Chimera ${PKG_VERSION}"
  ;;
  (64)
    _file="chimera-${PKG_VERSION}-win64.exe"
    _filepath="win64/${_file}"
    _installdir="Chimera ${PKG_VERSION}"
  ;;
esac

download(){
  cd "${SRC_DIR}"

  echo 'IMPORTANT: By downloading you accept the UCSF Chimera Non-Commercial Software License Agreement!'
  echo 'IMPORTANT: The license agreement can be found here: https://rbvi.ucsf.edu/chimera/license.html'
  echo 'IMPORTANT: If you do not agree, please press Ctrl-C now.'
  echo 'IMPORTANT: Downloading in 10 seconds...'

  sleep 10
  
  _download_url="https://rbvi.ucsf.edu/chimera/cgi-bin/secure/chimera-get.py"
  _ident="$(curl -s -F file="${_filepath}" -F choice=Accept "${_download_url}" | grep 'ident' | grep -Po '(?<=value=").*(?=")')"
  curl -L -F file="${_filepath}" -F ident="${_ident}" -F choice='Notified' -F download='Start Download' "${_download_url}" -o "${_file}"
}

installation() {
  cd "${SRC_DIR}"

  # Prepare the directory structure.
  install -dm755 "${LIBRARY_LIB}"

  # Run the installer.
  chmod +x "${_file}"
  echo "${LIBRARY_LIB}/${_installdir}" | "./${_file}"
}

softlink() {
  cd "${SRC_DIR}"
  ln -s "${LIBRARY_LIB}/${_installdir}/bin/chimera.exe" "${SCRIPTS}/chimera.exe"
}

download
installation
softlink