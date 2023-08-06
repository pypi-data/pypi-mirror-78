import sys
import os
import re
import numpy as np
import math
import scipy
import silhouetteRank.spatial_genes as spatial_genes
import subprocess
from shutil import copyfile
from operator import itemgetter
from scipy.spatial.distance import squareform, pdist
from scipy.stats import percentileofscore
from sklearn.metrics import roc_auc_score
from sklearn.cluster import KMeans

def read_matrix():
	f_expr = "expression.txt"
	f_Xcen = "Xcen.good"

	sys.stderr.write("Reading gene expression...\n")
	f = open(f_expr)
	h = f.readline().rstrip("\n").split("\t")[1:]
	num_cell = len(h)
	num_gene = 0
	for l in f:
		l = l.rstrip("\n")
		num_gene+=1
	f.close()

	expr = np.empty((num_gene, num_cell), dtype="float32")
	genes = []
	f = open(f_expr)
	f.readline()
	ig = 0
	for l in f:
		l = l.rstrip("\n")
		ll = l.split("\t")
		gene = ll[0]
		genes.append(gene)
		expr[ig,:] = [float(v) for v in ll[1:]]
		ig+=1
	f.close()

	sys.stderr.write("Reading cell coordinates...\n")
	f = open(f_Xcen)
	Xcen = np.empty((num_cell, 2), dtype="float32")
	f.readline()
	ic = 0
	for l in f:
		l = l.rstrip("\n")
		ll = l.split("\t")
		Xcen[ic,:] = [float(ll[1]), float(ll[2])]
		ic+=1
	f.close()
	return expr, genes, Xcen
 
def read_frequency(expr=None, genes=None, Xcen=None, frequency_file=None, read_from_file=True, outdir="", examine_top=0.05):
	num_cell = Xcen.shape[0]
	ncell = num_cell
	ex = int((1.0-examine_top)*100.0)
	pattern_size = {}
	for ig,g in enumerate(genes):
		cutoff = np.percentile(expr[ig,:], ex)
		clust = np.zeros((ncell), dtype="int32")
		gt_eq = np.where(expr[ig,:]>=cutoff)[0]
		lt = np.where(expr[ig,:]<cutoff)[0]
		t_size = gt_eq.shape[0]
		if cutoff==0:
			gt_eq = np.where(expr[ig,:]>cutoff)[0]
			lt = np.where(expr[ig,:]<=cutoff)[0]
			t_size = gt_eq.shape[0]
		clust[gt_eq] = 1
		clust[lt] = 2
		pattern_size.setdefault(t_size, 0)
		pattern_size[t_size]+=1

	freq = []
	if read_from_file==False:	
		fw = open("%s/gene.freq.good.txt" % outdir, "w")
		for s in pattern_size:
			fw.write("%d %d\n" % (pattern_size[s], s))
		fw.close()
		sizes = []
		for s in pattern_size:
			sizes.append(s)
			#frequency
			for i in range(pattern_size[s]):
				freq.append(s)
	else:
		f_frequency = frequency_file
		f = open(f_frequency)
		sizes = []
		for l in f:
			l = l.rstrip("\n")
			ll = l.split(" ")
			sizes.append(int(ll[1]))
			for i in range(int(ll[0])):
				freq.append(int(ll[1]))
		f.close()

	kmeans = KMeans(n_clusters = 10, random_state=0, n_init=1000, verbose=0).fit(np.array([freq]).T)
	cc = []
	for c in kmeans.cluster_centers_:
		cc.append(int(c[0]))
	by_cluster = {}
	for ind,c in enumerate(kmeans.labels_):
		by_cluster.setdefault(cc[c], [])
		by_cluster[cc[c]].append(freq[ind])

	if not os.path.isdir(outdir):
		os.mkdir(outdir)
	if not os.path.isdir("%s/good" % outdir):
		os.mkdir("%s/good" % outdir)
	
	for ind,v in enumerate(cc):
		fw = open("%s/good/%d" % (outdir, ind), "w")
		t_str = ";".join(["%d" % bc for bc in set(by_cluster[v])])
		fw.write("%d %d %s\n" % (1, v, t_str))
		fw.close()
	
	return list(by_cluster.keys())
	
if __name__=="__main__":
	rbp_p = float(sys.argv[1])
	examine_top = float(sys.argv[2])

	matrix_type = "dissim" # sim or dissim
	result = subprocess.call("Rscript --version", shell=True)
	if result==127:
		print("Rscript is not found")
		sys.exit(1)	

	outdir = "result_sim_5000_%.2f_%.3f" % (rbp_p, examine_top)
	if matrix_type=="dissim":
		outdir = "result_5000_%.2f_%.3f" % (rbp_p, examine_top)
	if not os.path.isdir(outdir):
		os.mkdir(outdir)

	alist = ["%d" % x for x in list(range(10))]
	size_to_do = []
	for i in alist:
		f = open("%s/good/%s" % (outdir,i))
		line = f.readline().rstrip("\n").split(" ")
		target = int(line[1])
		f.close()

		if not os.path.isfile("%s/par.%d" % (outdir, target)):
			size_to_do.append(target)
			continue
		
		f = open("%s/par.%d" % (outdir,target))
		n_scale = float(f.readline().rstrip("\n").split("\t")[1])
		n_shape = float(f.readline().rstrip("\n").split("\t")[1])
		f.close()
		if n_shape>=0:
			size_to_do.append(target)
			continue

		if not os.path.isfile("%s/%d" % (outdir, target)):
			size_to_do.append(target)
			continue
		
		scores = []
		f = open("%s/%d" % (outdir, target))
		for l in f:
			l = l.rstrip("\n")
			scores.append(float(l))
		f.close()
		if len(scores)!=5000:
			size_to_do.append(target)

	if size_to_do==[]:
		sys.exit(0)

	expr, genes, Xcen = read_matrix()
	ncell = Xcen.shape[0] 

	sys.stdout.write("Calculate all pairwise Euclidean distance between cells using their physical coordinates\n")
	euc = squareform(pdist(Xcen, metric="euclidean"))
	sys.stdout.write("Rank transform euclidean distance, and then apply exponential transform\n")
	t_matrix = spatial_genes.rank_transform_matrix(euc, reverse=False, rbp_p=rbp_p, matrix_type=matrix_type)
	sys.stdout.write("Compute silhouette metric per gene\n")

	source_path = os.path.dirname(silhouetteRank.__file__)
	if not os.path.isfile("%s/do_gpd.R" % outdir):
		copyfile("%s/do_gpd.R", "%s/do_gpd.R" % (source_path, outdir))

	res = spatial_genes.random_pattern(matrix=t_matrix, matrix_type=matrix_type, num_cell = ncell, sizes=size_to_do, trials_per_gene=5000, run_gpd=True, outdir=outdir)
