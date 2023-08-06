import sys
import os
import re
import numpy as np
import subprocess
import math
import scipy
import spatial_genes
from shutil import copyfile
from operator import itemgetter
from scipy.spatial.distance import squareform, pdist
from scipy.stats import percentileofscore
from sklearn.metrics import roc_auc_score
from sklearn.cluster import KMeans
import argparse

def do_one(args):
	matrix_type = args.matrix_type
	rbp_p = args.rbp_p
	examine_top = args.examine_top
	result = subprocess.call("Rscript --version", shell=True)
	if result==127:
		sys.stderr.write("Rscript is not found")
		sys.exit(1)	

	if not os.path.isdir(args.output):
		os.mkdir(args.output)
	
	check_required = ["expr.npy", "Xcen.npy", "genes.npy", "t_matrix_%s_%.2f.npy" % (args.matrix_type, args.rbp_p)]
	for cr in check_required:
		if not os.path.isfile("%s/%s" % (args.output, cr)):
			sys.stderr.write("Cannot find %s. Need to run prep.py first.\n" % cr)
			sys.exit(1)
			break

	#expr, Xcen, genes, t_matrix = None, None, None, None
	sys.stderr.write("Using existing input binaries...\n")
	expr = np.load("%s/expr.npy" % args.output)
	Xcen = np.load("%s/Xcen.npy" % args.output)
	genes = np.load("%s/genes.npy" % args.output)
	t_matrix = np.load("%s/t_matrix_%s_%.2f.npy" % (args.output, args.matrix_type, args.rbp_p))	
	ncell = Xcen.shape[0] 

	outdir = "%s/result_sim_5000_%.2f_%.3f" % (args.output, rbp_p, examine_top)
	if matrix_type=="dissim":
		outdir = "%s/result_5000_%.2f_%.3f" % (args.output, rbp_p, examine_top)
	if not os.path.isdir(outdir):
		os.mkdir(outdir)
	if not os.path.isfile("%s/do_gpd.R" % outdir):
		sys.stderr.write("do_gpd.R does not exist.\n")
		sys.exit(1)

	if not os.path.isfile("%s/good/%s" % (outdir, args.query_index)):
		sys.stderr.write("file %s/good/%s does not exist.\n" % (outdir, args.query_index))
		sys.exit(1)
	f = open("%s/good/%s" % (outdir,args.query_index))
	line = f.readline().rstrip("\n").split(" ")
	target = int(line[1])
	f.close()
	res = spatial_genes.random_pattern(matrix=t_matrix, matrix_type=matrix_type, num_cell = ncell, sizes=[target], trials_per_gene=5000, run_gpd=True, outdir=outdir)

if __name__=="__main__":
	parser = argparse.ArgumentParser(description="evaluate.exact.one.2b.py: calculate silhouette score for randomly distributed spatial patterns", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("-r", "--rbp-p", dest="rbp_p", type=float, default=0.95, help="p parameter of RBP")
	parser.add_argument("-e", "--examine-top", dest="examine_top", type=float, default=0.05, help="top proportion of cells per gene to be 1's (expressed)")
	parser.add_argument("-m", "--matrix-type", dest="matrix_type", type=str, choices=["sim", "dissim"], help="whether to calculate similarity matrix or dissimilarity matrix", default="dissim")
	parser.add_argument("-o", "--output-dir", dest="output", type=str, default=".", help="output directory")
	parser.add_argument("-q", "--query-index", dest="query_index", type=int, required=True, help="which query to do (index)")

	args = parser.parse_args()
	do_one(args)
