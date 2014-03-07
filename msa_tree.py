#!/usr/bin/python
import sys
import os
import subprocess
from Bio import AlignIO
from Bio.Align.Applications import ClustalwCommandline

inputseqfile = sys.argv[1]
msa = sys.argv[2]
tree = sys.argv[3]

def clustalw(inputseqfile, outputmsafile):

    """Make a multiple sequence alignment with clustalw"""

    clustalw = "/usr/bin/clustalw"
    clustalw_cline = ClustalwCommandline(clustalw, infile=inputseqfile)
    stdout, stderr = clustalw_cline()
    outf = inputseqfile.split(".")[0]
    outff = outf + ".aln"
    align = AlignIO.read(outff, "clustal")
    align = AlignIO.convert(outff, "clustal", outputmsafile, "fasta")
    

def mafft(inputseqfile, outputmsafile):
    
    """Make a multiple sequence alignment with MAFFT"""
    
    command_msa = 'mafft --retree 2 --reorder ' + inputseqfile + ' > ' + outputmsafile
    os.system(command_msa)
    #os.system("mafft --retree 2 --reorder ks.fasta > ks.mafft.fasta")
    #subprocess.call(['mafft --retree 2 --reorder', 'ks.fasta', '>', 'ks.mafft.fasta']) not currently working


def raxml(outputmsafile):

    """Build a tre from the MSA with RaxML"""
    
    outputtreefile = str(outputmsafile.split(".")[0]) + "." + msa + ".raxml.nwk"
    command_tree = 'raxmlHPC-AVX -n ' + outputtreefile + ' -s ' + outputmsafile + ' -m PROTCATJTT -p 12345'
    os.system(command_tree)

def fasttree(outputmsafile):

    """Build a tre from the MSA with Fasttree"""
    
    outputtreefile = str(outputmsafile.split(".")[0]) + "." + msa + ".fasttree.nwk"
    command_tree = 'fasttree < ' + outputmsafile + ' > ' + outputtreefile + ' -gamma'
    os.system(command_tree)
    #os.system("fasttree < ks.mafft.fasta > ks.mafft.fasttree.nwk -gamma")

def main():


    if msa == 'clustalw':
        outputmsafile = str(inputseqfile.split(".")[0]) + ".clustalw.fasta"
        clustalw(inputseqfile, outputmsafile)
        if tree == 'fasttree':
            fasttree(outputmsafile)
        if tree == 'raxml':
            raxml(outputmsafile)
        
    if msa == 'mafft':
        outputmsafile = str(inputseqfile.split(".")[0]) + ".mafft.fasta"
        mafft(inputseqfile, outputmsafile)
        if tree == 'fasttree':
            fasttree(outputmsafile)
        if tree == 'raxml':
            raxml(outputmsafile)
        

if __name__ == "__main__":
    main()
