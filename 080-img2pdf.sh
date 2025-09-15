#!/usr/bin/env bash

src=070-page-numbers
dst=080-img2pdf.pdf

if ! [ -e $dst ]; then
  # img2pdf --output $dst --pagesize A4 --border 0cm $src/*.png cover.jpg back.jpg
  img2pdf --output $dst --pagesize A4 --border 0cm $src/*.png cover.jpg back.jpg
fi
