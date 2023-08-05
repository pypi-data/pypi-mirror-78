#!/usr/bin/env python2.7

import re
import sys
import pysam
import os


def filter_simplex(input_bam, output_filename, min_simplex_reads):
    """
    Filter an fgbio collapsed bam to only consensus reads with representation on one strand.
    
    :param input_bam: string
    :param output_filename: string
    :param min_simplex_reads: int
    :return:
    """
    if not os.path.isfile(input_bam):
        sys.stderr.write("Input BAM file {0} does not exist.\n".format(input_bam))
        sys.exit(1)

    if not output_filename:
        base = os.path.basename(input_bam)
        output_filename =  re.sub(".bam$", "", base) + "_simplex.bam"
    
    bamfile = pysam.AlignmentFile(input_bam, "rb")
    simplex = pysam.AlignmentFile(output_filename, "wb", template=bamfile)
    
    for read in bamfile.fetch():
        try:
            strand1_dp=read.get_tag("aD")
            strand2_dp=read.get_tag("bD")
            consens_dp=read.get_tag("cD")
            # check duplex conditions
            if consens_dp >= min_simplex_reads and min(strand1_dp, strand2_dp) == 0:
                simplex.write(read)
        except:
            continue
    
    bamfile.close()
    simplex.close()
    try:
        pysam.index(output_filename, re.sub(".bam$", "", output_filename) + ".bai")
    except:
        sys.stderr.write("Could not index Simplex bam file {0}.\n".format(output_filename))
