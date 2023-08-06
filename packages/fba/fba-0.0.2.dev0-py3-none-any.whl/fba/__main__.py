# __main__.py

from .parsers import *
from .utilities import open_by_suffix
from .map import *
from .filter import is_matched, filter_matching
from .count import generate_matrix


def main():
    args = parse_args()

    if (args.command == 'extract'):
        print('not ready yet')

    elif (args.command == 'map'):

        analyze_feature_barcoding(
            cb_file=args.whitelist,
            fb_file=args.feature_ref,
            read1_file=args.read1,
            read2_file=args.read2,
            summarized_feature_barcoding_result=args.output,
            num_threads=args.threads,
            temp_directory=args.output_directory
        )

    elif (args.command == 'filter'):

        filter_matching(
            matching_file=args.input,
            matching_filtered_file=args.output,
            cell_barcode_pos_start=args.cell_barcode_pos_start,
            cell_barcode_mismatching_threshold=args.cell_barcode_mismatches,
            cell_barcode_left_shift=args.cell_barcode_left_shift,
            cell_barcode_right_shift=args.cell_barcode_right_shift,
            cell_barcode_extra_sequence=args.cell_barcode_extra_sequence,
            cell_barcode_extra_sequence_num_mismatches=args.cell_barcode_extra_sequence_mismatches,
            feature_barcode_pos_start=args.feature_barcode_pos_start,
            feature_barcode_mismatching_threshold=args.feature_barcode_mismatches,
            feature_barcode_left_shift=args.feature_barcode_left_shift,
            feature_barcode_right_shift=args.feature_barcode_right_shift,
            feature_barcode_extra_sequence=args.feature_barcode_extra_sequence,
            feature_barcode_extra_sequence_num_mismatches=args.feature_barcode_extra_sequence_mismatches
        )

    elif (args.command == 'count'):

        matrix_feature_barcode = generate_matrix(
            matching_file=args.input,
            umi_length=args.umi_length,
            umi_deduplication_method=args.umi_deduplication_method,
            umi_deduplication_threshold=args.umi_mismatches
        )

        matrix_feature_barcode.to_csv(
            path_or_buf=args.output,
            compression='infer'
        )

    elif (args.command == 'demultiplex'):
        print('not ready yet')

    elif (args.command == 'qc'):
        print('not ready yet')

    elif (args.command == 'kallisto_wrapper'):
        print('not ready yet')


if __name__ == "__main__":
    main()
