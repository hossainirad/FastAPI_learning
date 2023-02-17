#!/bin/bash

# variables
#DOMAIN=https://plastex.co.ir
#SSH_ROOT=1245
#BACK_DIR=/opt/backup/file_$NOW
#
#if [-z $BACK_DIR]; then
#  echo "Already exist!"
#else
#  mkdir -p $BACK_DIR
#fi

# disable ufw and mast
#systemctl stop ufw
#systemctl disable ufw
#systemctl mask ufw





sudo apt update && sudo apt upgrade -y
#apt install curl nginx fail2ban