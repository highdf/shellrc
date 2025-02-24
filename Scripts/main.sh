#! /bin/bash

pacman --sync clash python git

export http_proxy='http://127.0.0.1:7890'
export https_proxy='http://127.0.0.1:7890'
clash &
