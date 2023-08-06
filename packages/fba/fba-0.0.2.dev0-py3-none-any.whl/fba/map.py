# map.py

import gzip
import subprocess
import pysam
from Bio.SeqIO.QualityIO import FastqGeneralIterator
from pathlib import Path
from .utilities import open_by_suffix


def preprocess_reads(read1_file, read2_file, preprocessed_read_file):
    """
    Prepare reads.
    """

    read1_iter = FastqGeneralIterator(open_by_suffix(file_name=read1_file))
    read2_iter = FastqGeneralIterator(open_by_suffix(file_name=read2_file))

    with gzip.open(filename=preprocessed_read_file, mode='wt') as f:

        for ((read1_name, read1_seq, read1_qual),
             (_, read2_seq, read2_qual)) in zip(read1_iter, read2_iter):

            read1_name = read1_name.split(' ')

            read_name = '_'.join([read1_name[0], read2_seq, read2_qual])
            read_name = ' '.join([read_name] + read1_name[1:])

            fastq_entry = '\n'.join(
                [
                    '@' + read_name,
                    read1_seq,
                    '+',
                    read1_qual
                ]
            )

            f.write(fastq_entry + '\n')


def cb2fa(x, fasta_file):
    """
    """
    with open_by_suffix(file_name=x, mode='r') as f:

        with open_by_suffix(file_name=fasta_file, mode='w') as fo:
            for line in f:
                i = line.rstrip().split('-')[0]
                fo.write('>' + i + '\n' + i + '\n')


def fb2fa(x, fasta_file):
    """
    """
    with open_by_suffix(file_name=x, mode='r') as f:

        with open_by_suffix(file_name=fasta_file, mode='w') as fo:
            for line in f:
                i = line.rstrip().split('\t')
                fo.write('>' + '_'.join(i) + '\n' + i[1] + '\n')


def get_binary_path(binary_name):
    """Get binary path.

    : return path to the binary
    """
    binary_path = subprocess.run(['which', binary_name],
                                 stdout=subprocess.PIPE,
                                 universal_newlines=True).stdout.rstrip()

    if Path(binary_path).is_file():
        return binary_path

    else:
        raise FileNotFoundError(binary_name + 'not found in  $PATH\n')


def build_bt2_index(fasta_file,
                    bt2_index_base):
    """
    """
    process = subprocess.Popen([get_binary_path(binary_name='bowtie2-build'),
                                fasta_file,
                                bt2_index_base],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True)

    for line in process.stdout:
        yield line


def align_reads(fastq_file,
                bt2_index_base,
                alignment_file,
                num_threads=1):
    """
    """

    bowtie2_align_parameter = '--local -L8 --ma 4 -D20 -R3 -N1 -i S,1,0.50'
    bowtie2_align_parameter = ' '.join(
        ['-p', str(num_threads), bowtie2_align_parameter]
    )

    cmd = [
        get_binary_path(binary_name='bowtie2'),
        bowtie2_align_parameter,
        ' '.join(['-x', str(bt2_index_base), '-U', str(fastq_file)]),
        '|',
        get_binary_path(binary_name='samtools'),
        'view -uS - | ',
        get_binary_path(binary_name='samtools'),
        'sort -o',
        str(alignment_file),
        '-'
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    for line in process.stderr:
        yield line


def get_indel_count_from_cigar(cigartuples):
    """
    """
    num_insertions = [i[1] for i in cigartuples if i[0] == 1]
    num_deletions = [i[1] for i in cigartuples if i[0] == 2]

    if num_insertions:
        num_insertions = num_insertions[0]
    else:
        num_insertions = 0

    if num_deletions:
        num_deletions = num_deletions[0]
    else:
        num_deletions = 0

    return num_insertions, num_deletions


def extract_cell_barcode_alignment(alignment_file,
                                   preprocessed_read_file):
    """
    """
    samfile = pysam.AlignmentFile(alignment_file,
                                  mode='rb')

    with gzip.open(filename=preprocessed_read_file, mode='wt') as f:
        for aln in samfile.fetch(until_eof=True, multiple_iterators=True):

            if aln.flag == 0:
                matching_positions_string = ':'.join(
                    [str(i)
                     for i in [aln.query_alignment_start,
                               aln.query_alignment_end]]
                )

                num_mismatches = aln.get_tag(tag='XM')
                num_insertions, num_deletions = \
                    get_indel_count_from_cigar(cigartuples=aln.cigartuples)
                matching_description_string = ':'.join(
                    [str(i)
                     for i in [num_mismatches, num_insertions, num_deletions]]
                )

                read_name, read2_seq, read2_qual = aln.query_name.split('_')
                read_name = '_'.join([read_name,
                                      aln.query_sequence,
                                      aln.reference_name,
                                      matching_positions_string,
                                      matching_description_string])

                fastq_entry = '\n'.join(
                    [
                        '@' + read_name,
                        read2_seq,
                        '+',
                        read2_qual
                    ]
                )

                f.write(fastq_entry + '\n')

        samfile.close()


def summarize_feature_barcode_alignment(alignment_file,
                                        result_file):
    """
    """
    samfile = pysam.AlignmentFile(alignment_file,
                                  mode='rb')

    with open_by_suffix(file_name=result_file, mode='w') as f:
        f.write('\t'.join(
            [
                'read1_seq',
                'cell_barcode',
                'cb_matching_pos',
                'cb_matching_description',
                'read2_seq',
                'feature_barcode',
                'fb_matching_pos',
                'fb_matching_description'
            ]
        ) + '\n')

        for aln in samfile.fetch(until_eof=True,
                                 multiple_iterators=True):

            if aln.flag == 0 and aln.mapping_quality >= 10:
                matching_positions_string = ':'.join(
                    [str(i)
                        for i in [aln.query_alignment_start,
                                  aln.query_alignment_end]]
                )

                num_mismatches = aln.get_tag(tag='XM')
                num_insertions, num_deletions = \
                    get_indel_count_from_cigar(cigartuples=aln.cigartuples)
                matching_description_string = ':'.join(
                    [str(i)
                        for i in [num_mismatches,
                                  num_insertions,
                                  num_deletions]]
                )

                _, read1_seq, cell_barcode, \
                    matching_positions_string1, \
                    matching_description_string1 = aln.query_name.split('_')

                matching_entry = '\t'.join(
                    [
                        read1_seq,
                        cell_barcode,
                        matching_positions_string1,
                        matching_description_string1,
                        aln.query_sequence,
                        aln.reference_name,
                        matching_positions_string,
                        matching_description_string
                    ]
                )

                f.write(matching_entry + '\n')
    samfile.close()


def analyze_feature_barcoding(cb_file,
                              fb_file,
                              read1_file,
                              read2_file,
                              summarized_feature_barcoding_result,
                              num_threads=1,
                              temp_directory='barcode_mapping'):
    """
    """
    temp_directory = Path(temp_directory)
    temp_directory.mkdir(exist_ok=False)

    # preprocess reads
    preprocess_reads(
        read1_file=read1_file,
        read2_file=read2_file,
        preprocessed_read_file=temp_directory / 'preprocessed.fastq.gz'
    )

    # prepare cb fasta
    cell_barcode_fasta_file = temp_directory / 'cell_barcode_ref.fasta'
    cb2fa(x=cb_file,
          fasta_file=cell_barcode_fasta_file)

    # create cb index
    cell_barcode_bt2_index_name = temp_directory / 'cell_barcode_ref'

    log_iter = build_bt2_index(fasta_file=cell_barcode_fasta_file,
                               bt2_index_base=cell_barcode_bt2_index_name)
    with open_by_suffix(file_name=temp_directory / 'bowtie2_build_cb.log', mode='w') as f:
        for line in log_iter:
            f.write(line)

    # align cb
    cell_barcode_alignment_file = temp_directory / 'cell_barcode_sorted.bam'
    log_iter = align_reads(
        fastq_file=temp_directory / 'preprocessed.fastq.gz',
        bt2_index_base=cell_barcode_bt2_index_name,
        alignment_file=cell_barcode_alignment_file,
        num_threads=num_threads
    )
    with open_by_suffix(file_name=temp_directory / 'bowtie2_align_cb.log', mode='w') as f:
        for line in log_iter:
            f.write(line)
    pysam.index(str(cell_barcode_alignment_file),
                str(cell_barcode_alignment_file) + '.bai')

    # get read2
    processed_read_file = temp_directory / 'read2_processed.fastq.gz'
    extract_cell_barcode_alignment(
        alignment_file=cell_barcode_alignment_file,
        preprocessed_read_file=processed_read_file
    )

    # prepare fb fasta
    feature_barcode_fasta_file = temp_directory / 'feature_barcode_ref.fasta'
    fb2fa(x=fb_file,
          fasta_file=feature_barcode_fasta_file)

    # create fb index
    feature_barcode_bt2_index_name = temp_directory / 'feature_barcode_ref'
    log_iter = build_bt2_index(fasta_file=feature_barcode_fasta_file,
                               bt2_index_base=feature_barcode_bt2_index_name)
    with open_by_suffix(file_name=temp_directory / 'bowtie2_build_fb.log', mode='w') as f:
        for line in log_iter:
            f.write(line)

    # align fb
    feature_barcode_alignment_file = temp_directory / 'feature_barcode_sorted.bam'
    log_iter = align_reads(
        fastq_file=processed_read_file,
        bt2_index_base=feature_barcode_bt2_index_name,
        alignment_file=feature_barcode_alignment_file,
        num_threads=num_threads

    )
    with open_by_suffix(file_name=temp_directory / 'bowtie2_align_fb.log', mode='w') as f:
        for line in log_iter:
            f.write(line)
    pysam.index(str(feature_barcode_alignment_file),
                str(feature_barcode_alignment_file) + '.bai')

    # summarize
    summarize_feature_barcode_alignment(
        alignment_file=feature_barcode_alignment_file,
        result_file=summarized_feature_barcoding_result
    )


if __name__ == '__main__':
    pass
