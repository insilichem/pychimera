#!/bin/bash

# Linux
if [ "$(uname -s)" == "Linux" ]; then
    case "${ARCH}" in
      (32)
        _file="chimera-${PKG_VERSION}-linux_osmesa.bin"
        _filepath="linux_osmesa/${_file}"
        _installdir="UCSF-Chimera-${PKG_VERSION}-headless"
      ;;
      (64)
        _file="chimera-${PKG_VERSION}-linux_x86_64_osmesa.bin"
        _filepath="linux_x86_64_osmesa/${_file}"
        _installdir="UCSF-Chimera64-${PKG_VERSION}-headless"
      ;;
    esac
fi

download(){
  cd "${SRC_DIR}"
  set +x
  echo 'IMPORTANT: By downloading you accept the UCSF Chimera Non-Commercial Software License Agreement!'
  echo 'IMPORTANT: The license agreement can be found here: https://rbvi.ucsf.edu/chimera/license.html'
  echo 'IMPORTANT: If you do not agree, please press Ctrl-C now.'
  echo 'IMPORTANT: Downloading in 10 seconds...'

  sleep 10
  set -x
  _download_url="https://rbvi.ucsf.edu/chimera/cgi-bin/secure/chimera-get.py"
  _ident="$(curl -s -F file="${_filepath}" -F choice=Accept "${_download_url}" | grep 'ident' | grep -Po '(?<=value=").*(?=")')"
  curl -L -F file="${_filepath}" -F ident="${_ident}" -F choice='Notified' -F download='Start Download' "${_download_url}" -o "${_file}"
}

installation() {
  cd "${SRC_DIR}"

  # Prepare the directory structure.
  install -dm755 "${PREFIX}/lib"

  # Run the installer.
  chmod +x "${_file}"
  echo "${PREFIX}/lib/${_installdir}" | "./${_file}"
}

softlink() {
  cd "${SRC_DIR}"
  ln -s "${PREFIX}/lib/${_installdir}/bin/chimera" "${PREFIX}/bin/chimera-headless"
}

download
installation
softlink