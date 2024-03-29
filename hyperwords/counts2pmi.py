from docopt import docopt
from scipy.sparse import dok_matrix, csr_matrix
import numpy as np

from representations.matrix_serializer import save_matrix, save_vocabulary, load_count_vocabulary


def main():
    args = docopt("""
    Usage:
        counts2pmi.py [options] <counts> <output_path>
    
    Options:
        --cds NUM    Context distribution smoothing [default: 1.0]
        --t NUM    type of pmi (0 - pmi, 1 - bpmi) [default: 0]
    """)
    
    counts_path = args['<counts>']
    vectors_path = args['<output_path>']
    t = int(args['--t'])
    cds = float(args['--cds'])
    
    counts, iw, ic = read_counts_matrix(counts_path)
    if t == 0:
        pmi = calc_pmi(counts, cds)
    elif t == 1:
        pmi = calc_bpmi(counts, cds)

    save_matrix(vectors_path, pmi)
    save_vocabulary(vectors_path + '.words.vocab', iw)
    save_vocabulary(vectors_path + '.contexts.vocab', ic)


def read_counts_matrix(counts_path):
    """
    Reads the counts into a sparse matrix (CSR) from the count-word-context textual format.
    """
    words = load_count_vocabulary(counts_path + '.words.vocab')
    contexts = load_count_vocabulary(counts_path + '.contexts.vocab')
    words = list(words.keys())
    contexts = list(contexts.keys())
    iw = sorted(words)
    ic = sorted(contexts)
    wi = dict([(w, i) for i, w in enumerate(iw)])
    ci = dict([(c, i) for i, c in enumerate(ic)])
    
    counts = csr_matrix((len(wi), len(ci)), dtype=np.float32)
    tmp_counts = dok_matrix((len(wi), len(ci)), dtype=np.float32)
    update_threshold = 100000
    i = 0
    with open(counts_path) as f:
        for line in f:
            count, word, context = line.strip().split()
            if word in wi and context in ci:
                tmp_counts[wi[word], ci[context]] = int(count)
            i += 1
            if i == update_threshold:
                counts = counts + tmp_counts.tocsr()
                tmp_counts = dok_matrix((len(wi), len(ci)), dtype=np.float32)
                i = 0
    counts = counts + tmp_counts.tocsr()
    
    return counts, iw, ic


def calc_pmi(counts, cds):
    """
    Calculates e^PMI; PMI without the log().
    """
    sum_w = np.array(counts.sum(axis=1))[:, 0]
    sum_c = np.array(counts.sum(axis=0))[0, :]
    if cds != 1:
        sum_c = sum_c ** cds
    sum_total = sum_c.sum()
    sum_w = np.reciprocal(sum_w) # going 1 / x
    sum_c = np.reciprocal(sum_c)
    pmi_ones = csr_matrix(counts)
    pmi_ones = multiply_by_rows(pmi_ones, sum_w)
    pmi_ones = multiply_by_columns(pmi_ones, sum_c)
    pmi = pmi_ones * sum_total 
    return pmi

def calc_bpmi(counts, cds):
    """
    Calculates e^PMI; PMI without the log().
    """
    sum_w = np.array(counts.sum(axis=1))[:, 0]
    sum_c = np.array(counts.sum(axis=0))[0, :]
    if cds != 1:
        sum_c = sum_c ** cds
    sum_total = sum_c.sum()
    sum_w = np.reciprocal(sum_w) 
    sum_c = np.reciprocal(sum_c)

    pmi_ones = csr_matrix(counts)
    pmi_ones = multiply_by_rows(pmi_ones, sum_w)
    pmi_ones = multiply_by_columns(pmi_ones, sum_c)
    pmi = pmi_ones * sum_total 
    pmi = pmi.toarray()
    bin_pmi = pmi
    bin_pmi[bin_pmi <= 0] = 0
    bin_pmi[bin_pmi > 0] = 1
    bin_pmi = csr_matrix(bin_pmi)
    return bin_pmi

def multiply_by_rows(matrix, row_coefs):
    normalizer = dok_matrix((len(row_coefs), len(row_coefs)))
    normalizer.setdiag(row_coefs)
    return normalizer.tocsr().dot(matrix)


def multiply_by_columns(matrix, col_coefs):
    normalizer = dok_matrix((len(col_coefs), len(col_coefs)))
    normalizer.setdiag(col_coefs)
    return matrix.dot(normalizer.tocsr())


if __name__ == '__main__':
    main()
