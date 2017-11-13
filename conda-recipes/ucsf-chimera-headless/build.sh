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
else
    echo "Headless UCSF Chimera is only available for Linux"
    exit 1
fi

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