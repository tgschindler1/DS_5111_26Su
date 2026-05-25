#!/usr/bin/bash

USER="tgschinder1@gmail.com"
NAME="tgschinder1"

git config --global --list

git config --global user.email ${USER} 
git config --global user.name  ${NAME} 

git config --global --list
