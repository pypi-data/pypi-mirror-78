# count.py

import numpy as np
import pandas as pd
from umi_tools import UMIClusterer
from collections import Counter
from .utilities import open_by_suffix


def generate_matrix(matching_file,
                    umi_length=12,
                    umi_deduplication_method='directional',
                    umi_deduplication_threshold=1):
    """
    unique, percentile, cluster, adjacency, directional
    """
    matrix_feature_barcode = {}

    with open_by_suffix(file_name=matching_file) as f:
        next(f)

        for line in f:
            i = line.rstrip().split('\t')

            read_seq = i[0]
            cell_barcode = i[1]
            feature_barcode = i[5]

            cell_barcode_pos = [int(ii) for ii in i[2].split(':')]
            umi_pos_end = cell_barcode_pos[1] + umi_length

            if len(read_seq) >= umi_pos_end:
                umi_seq = read_seq[cell_barcode_pos[1]:umi_pos_end].encode()

            if cell_barcode not in matrix_feature_barcode:
                matrix_feature_barcode[cell_barcode] = {}

            if feature_barcode not in matrix_feature_barcode[cell_barcode]:
                matrix_feature_barcode[cell_barcode][feature_barcode] = []

            matrix_feature_barcode[cell_barcode][
                feature_barcode].append(umi_seq)

    cell_barcodes = sorted(matrix_feature_barcode.keys())
    feature_barcodes = sorted(
        set([ii
             for i in matrix_feature_barcode
             for ii in matrix_feature_barcode[i]])
    )

    clusterer = UMIClusterer(cluster_method=umi_deduplication_method)
    for i in matrix_feature_barcode:
        for ii in feature_barcodes:

            umis = matrix_feature_barcode[i].setdefault(ii, None)
            if umis:
                matrix_feature_barcode[i][ii] = len(
                    clusterer(Counter(umis),
                              threshold=umi_deduplication_threshold)
                )
            else:
                matrix_feature_barcode[i][ii] = 0

    matrix_feature_barcode = {i: [matrix_feature_barcode[i][ii]
                                  for ii in feature_barcodes]
                              for i in cell_barcodes}
    matrix_feature_barcode = pd.DataFrame.from_dict(matrix_feature_barcode,
                                                    orient='columns')
    matrix_feature_barcode.index = feature_barcodes

    return matrix_feature_barcode


if __name__ == '__main__':
    pass
