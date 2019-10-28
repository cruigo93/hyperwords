#!/bin/sh

# # Download and install word2vecf
# if [ ! -f word2vecf ]; then
#     scripts/install_word2vecf.sh
# fi


# Download corpus. We chose a small corpus for the example, and larger corpora will yield better results.
# wget http://www.statmt.org/wmt14/training-monolingual-news-crawl/news.2010.en.shuffled.gz
# gzip -d news.2010.en.shuffled.gz
# CORPUS=text

# # Clean the corpus from non alpha-numeric symbols
# scripts/clean_corpus.sh $CORPUS > $CORPUS.clean


# # Create two example collections of word-context pairs:

# # A) Window size 2 with "clean" subsampling
# mkdir w2.sub
# python hyperwords/corpus2pairs.py  ${CORPUS}.clean > w2.sub/pairs
# scripts/pairs2counts.sh w2.sub/pairs > w2.sub/counts
# python hyperwords/counts2vocab.py w2.sub/counts


# # Calculate PMI matrices for each collection of pairs
# python hyperwords/counts2pmi.py  w2.sub/counts w2.sub/pmi

KK=25
# # Create embeddings with SVD
python hyperwords/pmi2svd.py --k ${KK} NPMI w2.sub/pmi w2.sub/nsvd
cp w2.sub/pmi.words.vocab w2.sub/nsvd.words.vocab
cp w2.sub/pmi.contexts.vocab w2.sub/nsvd.contexts.vocab

echo "k = " ${KK} 
# Evaluate on Word Similarity
echo
echo "WS353 Results" 
echo "-------------"

# python hyperwords/ws_eval.py  PPMI w2.sub/pmi testsets/ws/ws353.txt
python hyperwords/ws_eval.py --k ${KK}  NPMI w2.sub/pmi testsets/ws/ws353.txt
# python hyperwords/ws_eval.py  BPMI w2.sub/pmi testsets/ws/ws353.txt
# python hyperwords/ws_eval.py  SVD w2.sub/bsvd testsets/ws/ws353.txt
python hyperwords/ws_eval.py --k ${KK}  SVD w2.sub/nsvd testsets/ws/ws353.txt
# python hyperwords/ws_eval.py --w+c SGNS w2.sub/sgns testsets/ws/ws353.

# Evaluate on Analogies
echo
echo "Google Analogy Results"
echo "----------------------"

# python hyperwords/analogy_eval.py PPMI w2.sub/pmi testsets/analogy/google.txt
python hyperwords/analogy_eval.py --k ${KK} NPMI w2.sub/pmi testsets/analogy/google.txt
# python hyperwords/analogy_eval.py BPMI w2.sub/pmi testsets/analogy/google.txt
# python hyperwords/analogy_eval.py  SVD w2.sub/bsvd testsets/analogy/google.txt
python hyperwords/analogy_eval.py --k ${KK} SVD w2.sub/nsvd testsets/analogy/google.txt
