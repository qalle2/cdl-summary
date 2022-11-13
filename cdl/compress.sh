rm -f *.png
gzip -9fk *.cdl
for f in *.cdl; do python3 ../cdl2png.py $f $f.png; done
