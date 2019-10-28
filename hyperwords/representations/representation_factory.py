from embedding import SVDEmbedding, EnsembleEmbedding, Embedding
from explicit import PositiveExplicit, BinExplicit, NoExplicit, NegExplicit


def create_representation(args):
    rep_type = args['<representation>']
    path = args['<representation_path>']
    neg = int(args['--neg'])
    w_c = args['--w+c']
    eig = float(args['--eig'])
    k = int(args['--k'])
    
    if rep_type == 'PPMI':
        if w_c:
            raise Exception('w+c is not implemented for PPMI.')
        else:
            return PositiveExplicit(path, True, neg=neg)

    elif rep_type == 'PMI':
        if w_c:
            raise Exception('w+c is not implemented for PPMI.')
        else:
            return NoExplicit(path, True, k)

    elif rep_type == 'BPMI':
        if w_c:
            raise Exception('w+c is not implemented for PPMI.')
        else:
            return BinExplicit(path, True)

    elif rep_type == 'NPMI':
        if w_c:
            raise Exception('w+c is not implemented for PPMI.')
        else:
            return NegExplicit(path, True)

    elif rep_type == 'SVD':
        if w_c:
            return EnsembleEmbedding(SVDEmbedding(path, False, eig, False), SVDEmbedding(path, False, eig, True), True)
        else:
            return SVDEmbedding(path, True, eig)
        
    else:
        if w_c:
            return EnsembleEmbedding(Embedding(path + '.words', False), Embedding(path + '.contexts', False), True)
        else:
            return Embedding(path + '.words', True)
