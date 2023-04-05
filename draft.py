(mitohifi_env) mu2@tol-head1:/lustre/scratch123/tol/teams/tola/users/mu2/mitohifi-dev2023/MitoHiFi$ more mitohifi2.py 
import concurrent.futures
from concurrent.futures import wait
import logging
import shutil
import subprocess
import time
import warnings
import pandas as pd
import argparse
import parse_blast
from Bio import SeqIO
import sys
import os
import cleanUpCWD
from compareGenesLists import compare_genes_dicts
from createCoveragePlot import map_potential_contigs, map_final_mito, get_contigs_to_map, get_contigs_headers, split_mapping_by_contig, create_coverage_plot
import fetch
import fetch_mitos
import filterfasta
import findFrameShifts
import fixContigHeaders
import functools
import rotation
import getMitoLength
import getReprContig
from getGenesList import get_genes_list
from gfa2fa import gfa2fa
from parallel_annotation import process_contig, process_contig_02
from parallel_annotation_mitos import process_contig_mitos, process_contig_02_mitos
import shlex
from circularizationCheck import circularizationCheck, get_circo_mito
import alignContigs
import plot_coverage
import plot_annotation

def main():
    
    __version__ = '3.0.0'
    start_time = time.time()

    parser = argparse.ArgumentParser(prog='MitoHiFi')
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    #mutually_exclusive_group = required.add_mutually_exclusive_group(required=True)    
    #mutually_exclusive_group.add_argument("-r", help= "-r: Pacbio Hifi Reads from your species", metavar='<reads>.fasta')
    #mutually_exclusive_group.add_argument("-c", help= "-c: Assembled fasta contigs/scaffolds to be searched to find mitogenome", metavar='<contigs>.fasta')
    required.add_argument("-c", help= "-c: Assembled fasta contigs/scaffolds to be searched to find mitogenome", metavar='<contigs>.fasta')
    required.add_argument("-f", help= "-f: Close-related Mitogenome is fasta format", required = "True", metavar='<relatedMito>.fasta')
    required.add_argument("-g", help= "-k: Close-related species Mitogenome in genebank format", required = "True", metavar='<relatedMito>.gbk')
    required.add_argument("-t", help= "-t: Number of threads for (i) hifiasm and (ii) the blast search", required = "True", type=int, metavar='<THREADS>')    
    optional.add_argument("-d", help="-d: debug mode to output additional info on log", action="store_true")    
    optional.add_argument("-a", help="-a: Choose between animal (default) or plant", default="animal", choices=["animal", "plant", "fungi"])
    optional.add_argument("-p", help="-p: Percentage of query in the blast match with close-related mito", type=int, default=50, metavar='<PERC>')
    optional.add_argument("-m", help="-m: Number of bits for HiFiasm bloom filter [it maps to -f in HiFiasm] (default = 0)", type=int, default=0, metavar='<BLOOM FILTER>')
    optional.add_argument("--max-read-len", help="Maximum lenght of read relative to related mito (default = 1.0x related mito length)", type=float, default=1.0)
    optional.add_argument("--mitos", help="Use MITOS2 for annotation (opposed to default MitoFinder", action="store_true")
    optional.add_argument('--circular-size', help='Size to consider when checking for circularization', type=int, default=7000)
    optional.add_argument('--circular-offset', help='Offset from start and finish to consider when looking for circularization', type=int, default=7000)
    optional.add_argument('-winSize', help='Size of windows to calculate coverage over the final_mitogenom', type=int, default=300)
    optional.add_argument('-covMap', help='Minimum mapping quality to filter reads when building final coverage plot', type=int, default=0)
    optional.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    optional.add_argument("-o", help="""-o: Organism genetic code following NCBI table (for mitogenome annotation):
    1. The Standard Code 2. The Vertebrate MitochondrialCode 3. The Yeast Mitochondrial Code 
    4. The Mold,Protozoan, and Coelenterate Mitochondrial Code and the Mycoplasma/Spiroplasma Code 5. The Invertebrate Mitochondrial Code 
    6. The Ciliate, Dasycladacean and Hexamita Nuclear Code 9. The Echinoderm and Flatworm Mitochondrial Code 10. The Euplotid Nuclear Code 
    11. The Bacterial, Archaeal and Plant Plastid Code 12. The Alternative Yeast Nuclear Code 13. The Ascidian Mitochondrial Code 
    14. The Alternative Flatworm Mitochondrial Code 16. Chlorophycean Mitochondrial Code 21. Trematode Mitochondrial Code 
    22. Scenedesmus obliquus Mitochondrial Code 23. Thraustochytrium Mitochondrial Code 24. Pterobranchia Mitochondrial Code 
    25. Candidate Division SR1 and Gracilibacteria Code 
        """, type=str, default='1', metavar='<GENETIC CODE>')
    args = parser.parse_args()
    
    # Set log message format
    FORMAT='%(asctime)s [%(levelname)s] %(message)s'

    if args.d: # If in debug mode
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
                            format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
    else:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                            format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
    
    # Welcome message
    logging.info("Welcome to MitoHifi v2. Starting pipeline...")
    logging.debug("Running MitoHiFi on debug mode.")
    
    # Measure the length of the related mitogenome 
    rel_mito_len = getMitoLength.get_mito_length(args.f)
    rel_mito_num_genes = getMitoLength.get_mito_genes(args.g)
    logging.info("Length of related mitogenome is: {} bp".format(rel_mito_len))
    logging.info("Number of genes on related mitogenome: {}".format(rel_mito_num_genes))
    
    # If input are reads, map them to the related mitogenome and assemble the mapped ones
#     if args.r:
#         logging.info("Running MitoHifi pipeline in reads mode...")
#         logging.info("1. First we map your Pacbio HiFi reads to the close-related mitogenome")
#         minimap_cmd = ["minimap2", "-t", str(args.t), "--secondary=no", "-ax", "map-hifi", args.f] + shlex.split(args.r) 
#         samtools_cmd = ["samtools", "view", "-@", str(args.t), "-b", "-F4", "-F", "0x800", "-o", "reads.HiFiMapped.bam"] 
#         logging.info(" ".join(minimap_cmd) + " | " + " ".join(samtools_cmd))        
#         minimap = subprocess.Popen(minimap_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
#         #mapped_reads_f = open("reads.HiFiMapped.bam", "w")
#         subprocess.run(samtools_cmd, stderr=subprocess.STDOUT, stdin=minimap.stdout)
#         minimap.wait()
#         minimap.stdout.close()
        
#         try:
#             f = open("reads.HiFiMapped.bam")
#         except FileNotFoundError:
#             sys.exit("""No reads.HiFiMapped.bam file.
#             An error may have occurred when mapping reads to the close-related mitogenome""")
#         finally:
#             f.close()

#         logging.info("2. Now we filter out any mapped reads that are larger than the reference mitogenome to avoid NUMTS")
#         bam2fasta_cmd = ["samtools", "fasta", "reads.HiFiMapped.bam"]
#         logging.info("2.1 First we convert the mapped reads from BAM to FASTA format:")
#         logging.info(" ".join(bam2fasta_cmd) + " > gbk.HiFiMapped.bam.fasta")
#         mapped_fasta_f = open("gbk.HiFiMapped.bam.fasta", "w")
#         subprocess.run(bam2fasta_cmd, stdout=mapped_fasta_f, stderr=subprocess.DEVNULL)
#         before_filter = fetch.get_num_seqs("gbk.HiFiMapped.bam.fasta")
#         logging.info(f"Total number of mapped reads: {before_filter}")
        
#         max_read_len = round(args.max_read_len * rel_mito_len)
#         logging.info(f"2.2 Then we filter reads that are larger than {max_read_len} bp")
#         filterfasta.filterFasta(minLength=max_read_len, neg=True, inStream="gbk.HiFiMapped.bam.fasta",
#                                 outPath="gbk.HiFiMapped.bam.filtered.fasta", log=False)
        
#         try:
#             f = open("gbk.HiFiMapped.bam.filtered.fasta")
#         except FileNotFoundError:
#             sys.exit("""No gbk.HiFiMapped.bam.filtered.fasta file.
#             An error may have occurred when filtering reads larger than the reference mitogenome""")
#         finally:
#             f.close()

#         after_filter = fetch.get_num_seqs("gbk.HiFiMapped.bam.filtered.fasta")
#         logging.info(f"Number of filtered reads: {after_filter}")

#         logging.info("3. Now let's run hifiasm to assemble the mapped and filtered reads!")
        
#         hifiasm_cmd = ["hifiasm", "--primary", "-t", str(args.t), "-f", str(args.m), 
#                     "-o", "gbk.HiFiMapped.bam.filtered.assembled",
#                     "gbk.HiFiMapped.bam.filtered.fasta"]

#         logging.info(" ".join(hifiasm_cmd))
#         with open("hifiasm.log", "w") as hifiasm_log_f:
#             subprocess.run(hifiasm_cmd, stderr=subprocess.STDOUT, stdout=hifiasm_log_f)       

#         f1 = None
#         f2 = None
#         try:
#             f1 = open("gbk.HiFiMapped.bam.filtered.assembled.p_ctg.gfa")
#             f2 = open("gbk.HiFiMapped.bam.filtered.assembled.a_ctg.gfa")
#         except FileNotFoundError:
#             sys.exit("""No gbk.HiFiMapped.bam.filtered.assembled.[a/p]_ctg.gfa file(s).
#             An error may have occurred when assembling reads with HiFiasm.""")
#         finally:
#             f1.close()
#             f2.close()
        
#         # convert Hifiasm assemblies (primary and alternate) from GFA to FASTA format
#         gfa2fa("gbk.HiFiMapped.bam.filtered.assembled.p_ctg.gfa", "gbk.HiFiMapped.bam.filtered.assembled.p_ctg.fa")
#         gfa2fa("gbk.HiFiMapped.bam.filtered.assembled.a_ctg.gfa", "gbk.HiFiMapped.bam.filtered.assembled.a_ctg.fa")

#         with open("hifiasm.contigs.fasta", "w") as hifiasm_f:
#             subprocess.run(["cat", "gbk.HiFiMapped.bam.filtered.assembled.p_ctg.fa", "gbk.HiFiMapped.bam.filtered.assembled.a_ctg.fa"], stdout=hifiasm_f)
        
#         contigs = "hifiasm.contigs.fasta"
    
    logging.info("Running MitoHifi pipeline in contigs mode...")
    logging.info("1. Fixing potentially conflicting FASTA headers")
    original_contigs = args.c
    fixContigHeaders.fix_headers(original_contigs, "fixed_header_contigs.fasta")
        
    os.remove(original_contigs) # remove original contig file  
    shutil.move("fixed_header_contigs.fasta", original_contigs) # replace original contigs file by the version that has the headers fixed
        
    contigs = original_contigs
    
        # Set number for the current step (for improving understanding of the log)
    # On reads mode, it should be 4; on contigs mode, 2    
#    if args.r:
#        step = 4
#    else:
#        step = 2 

#    logging.info(f"{step}. Let's run the blast of the contigs versus the close-related mitogenome")

    makeblastdb_cmd = ["makeblastdb", "-in", args.f, "-dbtype", "nucl"]
#    logging.info(f"{step}.1. Creating BLAST database:")
#    logging.info(" ".join(makeblastdb_cmd))
    subprocess.run(makeblastdb_cmd, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
#    logging.info("Makeblastdb done.")
    
    blast_cmd = ["blastn", "-query", contigs, "-db", args.f, "-num_threads", str(args.t),
                "-out", "contigs.blastn", "-outfmt", "6 std qlen slen"]
#    logging.info(f"{step}.2. Running blast of contigs against close-related mitogenome:")
#    logging.info(" ".join(blast_cmd))
    subprocess.run(blast_cmd, stderr=subprocess.STDOUT)
#    logging.info("Blast done.")

    try:
        f = open("contigs.blastn")
    except FileNotFoundError:
        sys.exit("""No contigs.blastn file.
        An error may have occurred when BLASTing contigs against close-related mitogenome""")
    finally:
        f.close()    

#    step += 1
#    logging.info(f"{step}. Filtering BLAST output to select target sequences")

    #the next script parses a series of conditions to exclude blast with NUMTs. 
    if args.a == "plant":
        ## if species is a plant, set minimum query percentage equal to 0% of related mito 
        ## and maximum query lenght 10 times the lenght of the related
        parse_blast.parse_blast(query_perc=args.p, min_query_perc=0, max_query_len=10)
    else:
        ## if species is an animal, set minimum query percentage equal to 80% of related mito
        ## and maximum query length 5 times the length of the related (default values from 
        ## parse_blast function
        parse_blast.parse_blast(query_perc=args.p, max_query_len=5)

    # select contigs to be circularized
    # first look for contigs in parsed_blast.txt
    contigs_ids = parse_blast.get_contigs_ids("parsed_blast.txt")

    # if we don't find contigs in parse_blast.txt 
    # look for contigs in parsed_blast_all.txt
    if len(contigs_ids) == 0:
        contigs_ids = parse_blast.get_contigs_ids("parsed_blast_all.txt")

    # if we can't find any contigs even in parsed_blast_all.txt, then we exit the pipeline
    if len(contigs_ids) == 0:
        sys.exit("""Attention!
'parsed_blast.txt' and 'parsed_blast_all.txt' files are empty.
The pipeline has stopped !! You need to run further scripts to check if you have mito reads pulled to a large NUMT!""")

    logging.info("Filtering BLAST finished. A list of the filtered contigs was saved on ./contigs_filtering/contigs_ids.txt file")

    # records all contigs kept for the downstream steps in a file called 'contigs_ids.txt'
    with open("contigs_ids.txt", "w") as f:
        for contig_id in contigs_ids:
            f.write(contig_id + "\n")

    # removes file that contains history of circularization of it already exists
    try:
        os.remove('all_contigs.circularisationCheck.txt')
    except OSError:
        pass
        step += 1
    logging.info(f"{step}. Now we are going to circularize, annotate and rotate each filtered contig. Those are potential mitogenome(s).")
    
    # Set maximum contig size accepted by mitofinder when annotating the contigs
    max_contig_size = 10*rel_mito_len

    threads_per_contig = 1
    if args.t // len(contigs_ids) > 1:
        threads_per_contig = args.t // len(contigs_ids)

    logging.debug(f"Threads per contig={threads_per_contig}")
    logging.debug(f"Thresholds for circularization: circular size={args.circular_size} | circular offset={args.circular_offset}")
    logging.debug(f"Thresholds for annotation (MitoFinder): maximum contig size={max_contig_size}")
    #from parallel_annotation import process_contig, process_contig_02
    #from parallel_annotation_mitos import process_contig_mitos, process_contig_02_mitos
    #functools.partial - fazer anotacao em paralelo. Permite q de como input uma funcao e cada virgula sao argumentos necessarios. 
    #
    if args.mitos:
        logging.info("Annotation will be done using MITOS2")
        if args.a == "fungi":
            refseq_db = "refseq89f"
        else:
            refseq_db = "refseq89m"
        partial_process_contig = functools.partial(process_contig_mitos, threads_per_contig,
                                                   args.circular_size, args.circular_offset,
                                                   contigs, max_contig_size, args.g, args.o, refseq_db)
    else:
        logging.info("Annotation will be done using MitoFinder (default)")
        partial_process_contig = functools.partial(process_contig, threads_per_contig,
                                                   args.circular_size, args.circular_offset,
                                                   contigs, max_contig_size, args.g, args.o)
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(partial_process_contig, contigs_ids)
    
if __name__ == '__main__':
  main()
