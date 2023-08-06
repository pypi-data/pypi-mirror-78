# parser.py

import sys
import argparse
from . import __version__


def parse_args(args=sys.argv[1:]):

    # create top-level parser
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            'Tools for feature barcoding analyses\n'
            + "Version: "
            + __version__
        )
    )

    # create sub-level parser
    subparsers = parser.add_subparsers(
        title='functions',
        dest='command',
        metavar=''
    )

    add_extract_subparser(subparsers)
    add_map_subparser(subparsers)
    add_filter_subparser(subparsers)
    add_count_subparser(subparsers)
    add_demultiplex_subparser(subparsers)
    add_qc_subparser(subparsers)
    add_kallisto_subparser(subparsers)

    if len(sys.argv) > 1:
        if (sys.argv[1] == '--version' or sys.argv[1] == '-v'):
            print("fba version: %s" % __version__)
            exit()
    else:
        args = parser.parse_args(['-h'])
        exit()

    return parser.parse_args(args)


def add_extract_subparser(subparsers):
    parser = subparsers.add_parser(
        'extract',
        help='extract feature barcodes from fastq')


def add_map_subparser(subparsers):
    parser = subparsers.add_parser(
        'map',
        help='map feature barcodes from fastq')

    parser.add_argument(
        '-1',
        '--read1',
        dest='read1',
        required=True,
        type=str,
        help='specify fastq file for read 1'
    )

    parser.add_argument(
        '-2',
        '--read2',
        dest='read2',
        required=True,
        type=str,
        help='specify fastq file for read 2'
    )

    parser.add_argument(
        '-w', '--whitelist',
        dest='whitelist',
        required=True,
        type=str,
        help='specify a whitelist of accepted cell barcodes'
    )

    parser.add_argument(
        '-f', '--feature_ref',
        dest='feature_ref',
        required=True,
        type=str,
        help='specify a reference of feature barcodes'
    )

    parser.add_argument(
        '-o', '--output',
        dest='output',
        required=True,
        help='specify an output file'
    )

    parser.add_argument(
        '-p', '--threads',
        dest='threads',
        required=False,
        type=int,
        default=1,
        help='specify number of bowtie2 alignment threads to launch. The default is 1'
    )

    parser.add_argument(
        '--output_directory',
        dest='output_directory',
        required=False,
        type=str,
        default='barcode_mapping',
        help='specify an temp directory. The default is barcode_mapping'
    )


def add_filter_subparser(subparsers):
    parser = subparsers.add_parser(
        'filter',
        help='filter extracted/mapped feature barcodes')

    parser.add_argument(
        '-i',
        '--input',
        dest='input',
        required=True,
        type=str,
        help='specify an input file. The output of extract or map functions'
    )

    parser.add_argument(
        '-o',
        '--output',
        dest='output',
        required=True,
        type=str,
        help='specify an output file'
    )

    parser.add_argument(
        '-cb_s',
        '--cb_start',
        dest='cell_barcode_pos_start',
        required=False,
        type=int,
        default=0,
        help='specify expected cell barcode starting postion on read1. The default is 0'
    )

    parser.add_argument(
        '-cb_m',
        '--cb_mismatches',
        dest='cell_barcode_mismatches',
        required=False,
        type=int,
        default=2,
        help='specify cell barcode mismatching threshold. The default is 2'
    )

    parser.add_argument(
        '-cb_ls',
        '--cb_left_shift',
        dest='cell_barcode_left_shift',
        required=False,
        type=int,
        default=1,
        help='specify the maximum left shift allowed for cell barcode. The default is 1'
    )

    parser.add_argument(
        '-cb_rs',
        '--cb_right_shift',
        dest='cell_barcode_right_shift',
        required=False,
        type=int,
        default=1,
        help='specify the maximum right shift allowed for cell barcode. The default is 1'
    )

    parser.add_argument(
        '-cb_seq',
        '--cb_extra_sequence',
        dest='cell_barcode_extra_sequence',
        required=False,
        type=str,
        default=None,
        help='specify an extra constant sequence to filter on read1. The default is None'
    )

    parser.add_argument(
        '-cb_seq_m',
        '--cb_extra_sequence_mismatches',
        dest='cell_barcode_extra_sequence_mismatches',
        required=False,
        type=int,
        default=None,
        help='specify the maximun edit distance allowed for the extra constant sequence on read1 for filtering. The default is off'
    )

    parser.add_argument(
        '-fb_s',
        '--fb_start',
        dest='feature_barcode_pos_start',
        required=False,
        type=int,
        default=10,
        help='specify expected feature barcode starting postion on read2. The default is 10'
    )

    parser.add_argument(
        '-fb_m',
        '--fb_mismatches',
        dest='feature_barcode_mismatches',
        required=False,
        type=int,
        default=2,
        help='specify feature barcode mismatching threshold. The default is 2'
    )

    parser.add_argument(
        '-fb_ls',
        '--fb_left_shift',
        dest='feature_barcode_left_shift',
        required=False,
        type=int,
        default=1,
        help='specify the maximum left shift allowed for feature barcode. The default is 1'
    )

    parser.add_argument(
        '-fb_rs',
        '--fb_right_shift',
        dest='feature_barcode_right_shift',
        required=False,
        type=int,
        default=1,
        help='specify the maximum right shift allowed for feature barcode. The default is 1'
    )

    parser.add_argument(
        '-fb_seq',
        '--fb_extra_sequence',
        dest='feature_barcode_extra_sequence',
        required=False,
        type=str,
        default=None,
        help='specify an extra constant sequence to filter on read2. The default is None'
    )

    parser.add_argument(
        '-fb_seq_m',
        '--fb_extra_sequence_mismatches',
        dest='feature_barcode_extra_sequence_mismatches',
        required=False,
        type=int,
        default=None,
        help='specify the maximun edit distance allowed for the extra constant sequence on read2. The default is off'
    )


def add_count_subparser(subparsers):
    parser = subparsers.add_parser(
        'count',
        help='count feature barcodes per cell')

    parser.add_argument(
        '-i',
        '--input',
        dest='input',
        required=True,
        type=str,
        help='specify an input file'
    )

    parser.add_argument(
        '-o',
        '--output',
        dest='output',
        required=True,
        type=str,
        help='specify an output file'
    )

    parser.add_argument(
        '-ul',
        '--umi_length',
        dest='umi_length',
        required=False,
        type=int,
        default=12,
        help='specify the length of UMIs on read1. The default is 12'
    )

    parser.add_argument(
        '-um',
        '--umi_mismatches',
        dest='umi_mismatches',
        required=False,
        type=int,
        default=1,
        help='specify the maximun edit distance allowed for UMIs on read1. The default is 1'
    )

    parser.add_argument(
        '-ud',
        '--umi_deduplication_method',
        dest='umi_deduplication_method',
        required=False,
        type=str,
        default='directional',
        help='specify the UMI deduplication method (UMI_tools). The default is \'directional\''
    )


def add_demultiplex_subparser(subparsers):
    parser = subparsers.add_parser(
        'demultiplex',
        help='demultiplex based on feature barcoding'
    )


def add_qc_subparser(subparsers):
    parser = subparsers.add_parser(
        'qc',
        help='quality control of feature barcoding'
    )


def add_kallisto_subparser(subparsers):
    parser = subparsers.add_parser(
        'kallisto_wrapper',
        help='deploy kallisto and bustools for feature barcoding quantification'
    )
