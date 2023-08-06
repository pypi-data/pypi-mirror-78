# filter.py

import regex
from .utilities import open_by_suffix


def compile_regex_ref_barcodes_single(sequence, num_mismatches=1):
    """
    """
    ref_sequence = regex.compile(f'({sequence}){{e<={num_mismatches}}}',
                                 regex.BESTMATCH)

    return ref_sequence


def is_matched(x,
               barcode_pos_start,
               mismatching_threshold=1,
               left_shift=0,
               right_shift=0,
               sequence_regex=None):
    """
    """

    read_seq, barcode, matching_pos, matching_description = x
    matching_pos = [int(i) for i in matching_pos.split(':')]
    matching_description = [int(i) for i in matching_description.split(':')]

    num_mismatches = len(barcode.split('_')[-1]) - \
        (matching_pos[1] - matching_pos[0]) + \
        sum(matching_description)

    if num_mismatches <= mismatching_threshold:

        if (barcode_pos_start - left_shift) <= matching_pos[0] <= (barcode_pos_start + left_shift):
            barcode_pos_end = barcode_pos_start + len(barcode.split('_')[-1])

            if (barcode_pos_end - right_shift) <= matching_pos[1] <= (barcode_pos_end + right_shift):

                if sequence_regex:
                    if sequence_regex.search(read_seq):
                        return True
                else:
                    return True


def filter_matching(matching_file,
                    matching_filtered_file,
                    cell_barcode_pos_start=0,
                    cell_barcode_mismatching_threshold=2,
                    cell_barcode_left_shift=1,
                    cell_barcode_right_shift=1,
                    cell_barcode_extra_sequence=None,
                    cell_barcode_extra_sequence_num_mismatches=None,
                    feature_barcode_pos_start=10,
                    feature_barcode_mismatching_threshold=2,
                    feature_barcode_left_shift=1,
                    feature_barcode_right_shift=1,
                    feature_barcode_extra_sequence=None,
                    feature_barcode_extra_sequence_num_mismatches=None):
    """
    """
    with open_by_suffix(file_name=matching_file) as f:
        header_line = next(f)

        with open_by_suffix(file_name=matching_filtered_file, mode='w') as fo:
            fo.write(header_line)

            for line in f:
                i = line.rstrip().split('\t')

                cell_barcode_matching = i[:4]

                if cell_barcode_extra_sequence and cell_barcode_extra_sequence_num_mismatches:
                    cell_barcode_sequence_regex = \
                        compile_regex_ref_barcodes_single(
                            cell_barcode_extra_sequence,
                            num_mismatches=cell_barcode_extra_sequence_num_mismatches
                        )
                else:
                    cell_barcode_sequence_regex = None

                cell_barcode_passed = is_matched(
                    x=cell_barcode_matching,
                    barcode_pos_start=cell_barcode_pos_start,
                    mismatching_threshold=cell_barcode_mismatching_threshold,
                    left_shift=cell_barcode_left_shift,
                    right_shift=cell_barcode_right_shift,
                    sequence_regex=cell_barcode_sequence_regex
                )

                if cell_barcode_passed:
                    feature_barcode_matching = i[4:]

                    if feature_barcode_extra_sequence and feature_barcode_extra_sequence_num_mismatches:
                        feature_barcode_sequence_regex = \
                            compile_regex_ref_barcodes_single(
                                feature_barcode_extra_sequence,
                                num_mismatches=feature_barcode_extra_sequence_num_mismatches
                            )
                    else:
                        feature_barcode_sequence_regex = None

                    feature_barcode_passed = is_matched(
                        x=feature_barcode_matching,
                        barcode_pos_start=feature_barcode_pos_start,
                        mismatching_threshold=feature_barcode_mismatching_threshold,
                        left_shift=feature_barcode_left_shift,
                        right_shift=feature_barcode_right_shift,
                        sequence_regex=feature_barcode_sequence_regex
                    )

                    if feature_barcode_passed:
                        fo.write(line)


if __name__ == '__main__':
    pass
