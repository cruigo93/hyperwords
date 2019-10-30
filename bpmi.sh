wget http://mattmahoney.net/dc/text8.zip
unzip text8.zip
CORPUS=text8

scripts/clean_corpus.sh $CORPUS > $CORPUS.clean

mkdir w5.sub
python hyperwords/corpus2pairs.py  ${CORPUS}.clean > w5.sub/pairs
scripts/pairs2counts.sh w5.sub/pairs > w5.sub/counts
python hyperwords/counts2vocab.py w5.sub/counts

python hyperwords/counts2pmi.py --t 1 w5.sub/counts w5.sub/pmi

