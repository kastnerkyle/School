FILE=OSR_us_000_0010_8k.wav
for bit in 2 4 6 8 10 12; do
    for type in z m l u r c p; do 
        ./vector_quant.py -b $bit -$type -vv -s $FILE
    done
    for type in m l; do
        ./mu_quant.py -b $bit -$type -vv $FILE
    done
done
