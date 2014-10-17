#!/bin/sh

rm -rf json
rm -rf work
mkdir json
mkdir work

for in_filename in $(ls $1); do
    in_filename_basename=`basename -s.gif $in_filename`
    i=0
    for color in '#189613' '#eff023' '#e0b211' '#e76b08' '#b52a29' '#634e1d'; do
        out_filename="$PWD/work/$in_filename_basename-$i-composite.tif"
        extract_filename="$PWD/work/$in_filename_basename-$i-extract.tif"

        # mask, alpha
        convert $in_filename $PWD/mask.png -alpha Off -compose CopyOpacity -colorspace sRGB -composite $extract_filename
        mogrify -fill transparent -fuzz "10%" +opaque "$color" $extract_filename
        mogrify -fill Off -fuzz "10%" +opaque "$color" $extract_filename
        mogrify -transparent "#000000" $extract_filename
        
        # georeference
        sh $PWD/georeference.sh $extract_filename

        # extract vector
        rio shapes --mask $extract_filename > $PWD/json/$in_filename_basename-$i.json
        
        # buffer operation to smooth out shape
        python bufunbuf.py $PWD/json/$in_filename_basename-$i.json $PWD/json/$in_filename_basename-$i-done.json && rm $PWD/json/$in_filename_basename-$i.json
        
        ((i=i+1))
    done
done
    