#!/bin/sh

palette="./palette.png"

filters="fps=23,scale=iw:-1:flags=lanczos"
echo $3
ffmpeg -v warning -i $1 -vf "$filters,palettegen" -y $palette
ffmpeg -v warning -i $1 -i $palette -lavfi "$filters [x]; [x][1:v] paletteuse" -y $2
