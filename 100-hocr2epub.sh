#!/usr/bin/env bash

set -eux

dst=$(basename "$0" .sh).epub

doc_title="$(head -n1 readme.md | sed 's/^#\s*//')"

if [ -e "$dst" ]; then
  echo "error: output exists: $dst"
  exit 1
fi

args=(
  hocr-to-epub-fxl
  --output "$dst"
  --scale 0.5
  --image-format avif
  --text-format svg
  --doc-title "$doc_title"
  *-ocr/*.hocr
)

"${args[@]}" "$@"
echo "done $dst"

rm -rf $dst.unzip
mkdir $dst.unzip
cd $dst.unzip
unzip -q ../$dst
cd ..

echo "done $dst.unzip/index.html"
