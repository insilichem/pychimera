#!/bin/bash

PKG_VERSION="1.13.1"

[[ $ARCH = 32 ]] && echo "32-bit builds are not supported anymore" && exit 1;

# Linux
uname_out="$(uname -s)"
case "$uname_out" in
  Linux* )
    _file="chimera-${PKG_VERSION}-linux_x86_64.bin"
    _filepath="linux_x86_64/${_file}"
    _installdir="UCSF-Chimera64-${PKG_VERSION}"
    _hash="80d2c95f78c603da3acda42f4bbceca0" # v1.13.1
    _agent="Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0"
  ;;
# MacOS X
  Darwin* )
    _file="chimera-${PKG_VERSION}-mac64.dmg"
    _filepath="mac64/${_file}"
    _installdir="UCSF-Chimera64-${PKG_VERSION}"
    _hash="62251f8677846e367de3cab4b5b1e8af" # v1.13.1
    _agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
  ;;
# Emulated Windows
  CYGWIN*|MINGW*|MSYS*|*windows*)
    _file="chimera-${PKG_VERSION}-win64.exe"
    _filepath="win64/${_file}"
    _installdir="Chimera_${PKG_VERSION}"
    _hash="1cb7f1f4138fc4ff34a5c3383623b4a4" # v1.13.1
    _agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931"
  ;;
  *)
    echo "Platform ${uname_out} not supported"
    exit 1
  ;;
esac

_downloader="https://www.rbvi.ucsf.edu/chimera/cgi-bin/secure/chimera-get.py"

download_unix(){
  n=0;
  until [ $n -ge 10 ]; do
    _download=$(command curl -A "${_agent}" -F file=${_filepath} -F choice=Accept "${_downloader}" | grep href | sed -E 's/.*href="(.*)">/\1/');
    sleep 3;
    command curl -A "${_agent}" "https://www.cgl.ucsf.edu${_download}" -o "${_file}";
    echo "${_hash}  ${_file}" | md5sum -c --strict --quiet && break;
    n=$[$n+1];
    sleep 3;
  done;
  echo "${_hash}  ${_file}" | md5sum -c --strict --quiet || exit 1;
}

download_win(){
  _download=$(command curl -A "${_agent}" -F file=${_filepath} -F choice=Accept "${_downloader}" | grep href | sed -E 's/.*href="(.*)">/\1/');
  sleep 3;
  command curl -A "${_agent}" "https://www.cgl.ucsf.edu${_download}" -o "${_file}";
}

installation_linux() {
  chmod +x "${_file}";
  echo "$HOME/chimera" | "./${_file}";
}

installation_mac() {
  cd "${SRC_DIR}"
  hdiutil convert "${_file}" -format UDRW -o chimerarw
  _mountdir=$(echo `hdiutil attach -mountpoint "$HOME/chimera" chimerarw.dmg | tail -1 | awk '{$1=$2=""; print $0}'` | xargs -0 echo)
}

installation_win() {
  cd "${SRC_DIR}"
  cmd.exe /C "START /WAIT ${_file} /VERYSILENT /DIR=$CHIMERADIR"
}


set +x
echo 'IMPORTANT: By downloading you accept the UCSF Chimera Non-Commercial Software License Agreement!'
echo 'IMPORTANT: The license agreement can be found here: http://www.cgl.ucsf.edu/chimera/license.html'
echo 'IMPORTANT: If you do not agree, please press Ctrl-C now.'
echo 'IMPORTANT: Downloading in 10 seconds...'
sleep 10
set -x

# Linux
case "$uname_out" in
  Linux* )
    download_unix
    installation_linux
  ;;
# MacOS X
  Darwin* )
    alias md5sum='md5 -r'
    download_unix
    installation_mac
  ;;
# Emulated Windows
  CYGWIN*|MINGW*|MSYS*|*windows*)
    download_win
    installation_win
  ;;
  *)
    echo "Platform ${uname_out} not supported"
    exit 1
  ;;
esac