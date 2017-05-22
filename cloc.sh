#!/bin/sh

cloc --exclude-dir="site-static" website static


# git ls-files | while read f; do git blame --line-porcelain $f | grep '^author '; done | sort -f | uniq -ic | sort -n
