#!/bin/bash
# usage: ocr.sh <dir with book.pdf>  -> pages/p-NNN.txt + book.txt (with ==== page N ==== markers)
set -e; cd "$1"; mkdir -p img pages
pdftoppm -r 200 -gray -png book.pdf img/p
ls img/*.png | xargs -P "$(nproc)" -I{} sh -c 'b=$(basename {} .png); [ -s pages/$b.txt ] || OMP_THREAD_LIMIT=1 tesseract {} pages/$b -l fas --psm 6 >/dev/null 2>&1'
: > book.txt; for f in $(ls pages/*.txt | sort); do n=$(basename $f .txt | sed 's/p-0*//'); echo "==== page $n ====" >> book.txt; cat $f >> book.txt; done
rm -rf img; wc -c book.txt
