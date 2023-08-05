import click

from fgbio_postprocessing import simplex_filter


@click.command()
@click.option("--input_bam", required=True, help="Path to bam to be filtered")
@click.option("--output_filename", required=True, help="Name of output bam")
@click.option("--min_simplex_reads", required=False, default=3, help="Minimum number of simplex reads to pass filter")
def filter_simplex(input_bam, output_filename, min_simplex_reads):
    """
    Filter bam file to only simplex reads with `min_simplex_reads` on one strand
    """
    simplex_filter.filter_simplex(input_bam, output_filename, min_simplex_reads)
    