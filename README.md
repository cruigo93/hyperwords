# Modified Hyperwords (BPMI, NPMI)
## original: [here](https://bitbucket.org/omerlevy/hyperwords/src/default/)
packages needed:
- python2.7
- numpy
- scipy
- docopt

## create bpmi:
- cleaning

`scripts/clean_corpus.sh $CORPUS > $CORPUS.clean` 
- creating counts

`mkdir w5.sub`

`python hyperwords/corpus2pairs.py  ${CORPUS}.clean > w5.sub/pairs`

`scripts/pairs2counts.sh w5.sub/pairs > w5.sub/counts`

`python hyperwords/counts2vocab.py w5.sub/counts`

- creating BPMI

`python hyperwords/counts2pmi.py --t 1 w5.sub/counts w5.sub/pmi`

`t` (0 - PMI, 1 - BPMI)
