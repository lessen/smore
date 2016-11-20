gawk 'BEGIN {OFS=FS=","}
NF < 10 { print; next}
   {
     gsub(/xh,/  ,"6,")
     gsub(/vh,/  ,"5,")
     gsub(/vl,/  ,"1,")
     gsub(/h,/   ,"4,")
     gsub(/n,/   ,"3,")
     gsub(/l,/   ,"2,")
     print }' $1

