#!/usr/bin/env bash

src1=080-img2pdf.pdf
src2=090-source-page.pdf
dst=100-join.pdf

pdftk $src1 $src2 cat output $dst
