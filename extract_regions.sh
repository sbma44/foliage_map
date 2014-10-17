#!/bin/sh

echo "-- extracting data from $1"

in_filename=$1
in_filename_basename=`basename -s.gif $in_filename`

i=0
for color in '#189613' '#eff023' '#e0b211' '#e76b08' '#b52a29' '#634e1d'; do
    out_filename="$PWD/work/$in_filename_basename-$i-composite.tif"
    extract_filename="$PWD/work/$in_filename_basename-$i-extract.tif"

    # mask, alpha
    convert -quiet $in_filename $PWD/mask.png -alpha Off -compose CopyOpacity -colorspace sRGB -composite $extract_filename
    mogrify -quiet -fill transparent -fuzz "10%" +opaque "$color" $extract_filename
    mogrify -quiet -fill Off -fuzz "10%" +opaque "$color" $extract_filename
    mogrify -quiet -transparent "#000000" $extract_filename
    
    # georeference
    sh $PWD/georeference.sh $extract_filename

    # extract vector
    rio -q shapes --mask $extract_filename > $PWD/json/$in_filename_basename-$i.json
    
    # buffer operation to smooth out shape
    python bufunbuf.py $PWD/json/$in_filename_basename-$i.json $PWD/json/$in_filename_basename-$i-done.json && rm $PWD/json/$in_filename_basename-$i.json
    
    ((i=i+1))
done
