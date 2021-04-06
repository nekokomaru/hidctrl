#!/bin/bash

DEST=/etc/systemd/system

BIN=gpio2cmd
EXT=.service

if [ ! -z "$1" ] && [ "$1" = 'install' ]; then

  # service
  echo 'install service'
  if [ -f ${BIN}${EXT} ]; then
    install -m 644 ${BIN}${EXT} ${DEST}
    systemctl daemon-reload
    systemctl enable ${BIN}
#    systemctl start ${BIN}
  fi

elif [ ! -z "$1" ] && [ "$1" = 'uninstall' ]; then

  # uninstall service
  echo 'uninstall service'
  systemctl stop ${BIN}
  systemctl disable ${BIN}
  if [ -f ${DEST}/${BIN}${EXT} ]; then
    rm ${DEST}/${BIN}${EXT}
    systemctl daemon-reload
  fi
fi
