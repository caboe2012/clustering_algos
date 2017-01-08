'''Application 3 - Clustering Algos'''
import math
import random
import alg_cluster
import Week3_Project as project
import matplotlib.pyplot as plt
import time
import urllib2
import alg_clusters_matplotlib


_111_DATA_FILE = "unifiedCancerData_111.csv"
_290_DATA_FILE = "unifiedCancerData_290.csv"
_896_DATA_FILE = "unifiedCancerData_896.csv"
_3108_DATA_FILE = "unifiedCancerData_3108.csv"

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"

def gen_random_clusters(num_clusters):
	list_o_clusters = [alg_cluster.Cluster(set([]), random.uniform(-1,1), random.uniform(-1,1), 0,0) for _dmy in range(num_clusters)]
	return list_o_clusters

def plot_random_clusters(cluster_list):
	x = []
	y = []
	for cluster in cluster_list:
		x.append(cluster.horiz_center())
		y.append(cluster.vert_center())
	plt.xlim(-1,1)
	plt.ylim(-1,1)
	#plt.scatter(x, y, "blue", label = "X")
	plt.scatter(x,y,c="red", marker="1")#, label = "Y")
	plt.xlabel("Horizontal Coordinates")
	plt.ylabel("Vertical Coordinates")
	plt.title("Random Clusters")
	#plt.legend(loc="upper right")
	print "Plotting now..."
	plt.show()

def compute_run_times(num_iterations):
	iteration_count = []
	slow_times = []
	fast_times = []
	for idx in range(2,num_iterations):
		iteration_count.append(idx)
		current_cluster_list = gen_random_clusters(idx)
		start_slow = time.time()
 		project.slow_closest_pair(current_cluster_list)
		current_slow_time = time.time() - start_slow
		slow_times.append(current_slow_time)
		
		start_fast = time.time()
		project.fast_closest_pair(current_cluster_list)
		current_fast_time = time.time() - start_fast
		fast_times.append(current_fast_time)
	return iteration_count, slow_times, fast_times

def plot_run_times(iteration_list, slow_list, fast_list):
	'''Q1 answer'''
	plt.plot(iteration_list, slow_list, "-r", label="slow run times")
	plt.plot(iteration_list, fast_list, "-b", label = "fast run times")
	plt.xlabel("Number of Initial Clusters")
	plt.ylabel("Function Rime Time (s)")
	plt.title("Compute Times of Slow Closest Pair vs Fast Closest Pair")
	plt.legend(loc="upper left")
	print "Plotting the slow and fast run times now"
	plt.show()

def Q2_Q3_Q5_Q6_viz(data_file, clustering_algo, num_clusters, num_iterations, centers):
	'''Questions 2-6 Answer'''
	data_table = project.load_data_table(data_file)
	singleton_list = []
	for line in data_table:
	    singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
	if clustering_algo == "h":
		cluster_list = project.hierarchical_clustering(singleton_list, num_clusters)
		print "Displaying", len(cluster_list), "hierarchical clusters"
	elif clustering_algo == "k":
		cluster_list = project.kmeans_clustering(singleton_list, num_clusters, num_iterations)
		print "Displaying", len(cluster_list), "kmeans clusters"
	else:	
		print "Clustering method not recognized.\nPlease use 'h' for hierarchical_clustering\nor use 'k' for kmeans_clustering"   
		return
	alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, centers) #False to remove cluster centers.  True to include them

def Q4_answer():
	'''Assuming that k-means always uses a small number of fixed iterations, k-means is the faster clustering method 
	 when the numer of output clusters is a small number compared to the number of input clusters.  This happens 
	 because as the number of iterations (q) and the number of output clusters (k) become smaller and smaller in comparison 
	 to the size of input clusters (n), the asymptotic runtime for kmeans approximates to n.  In contrast, with hierarchical clustering, 
	 as the number of output clusters becomes smaller and smaller in comparison to the size of the input clusters, the 
	 asymptotic run time for hierarchical clustering approxmiates to the square of the input size (ie, n*n).'''	
	pass

def Q7_compute_distortion(cluster_list, data_table):
	total_distortion = 0
	for cluster in cluster_list:
		current_distortion = cluster.cluster_error(data_table)
		total_distortion += current_distortion
	return total_distortion

def Q7_run(data_file, num_clusters, num_iterations):
	'''The distortion for the hierarchical cluster in Q5 (111 counties, 9 clusters) is 1.75163886916e+11
	   The distortion for the kmeans cluster in Q6 (111 counties, 9 clusters, 5 iterations) is 2.71254226924e+11
	   Q7_run(_111_DATA_FILE, 9, 5)''' 
	data_table = project.load_data_table(data_file)
	
	kmeans_cluster_list = project.run_example(data_table, "k", num_clusters, num_iterations)
	hier_cluster_list = project.run_example(data_table, "h", num_clusters, num_iterations)
	
	hier_distortion = Q7_compute_distortion(hier_cluster_list, data_table)
	print "The hierarchical distortion is", hier_distortion
	
	kmeans_distortion = Q7_compute_distortion(kmeans_cluster_list, data_table)
	print "The kmeans distortion is", kmeans_distortion
	
	return hier_distortion, kmeans_distortion 

def Q8_answer():
	'''Both hierarchical and kmeans produce three clusters on the west coast.  The clusters for hierarchical clustering
	are centered in the middle of three major population areas on the West Coast- Seattle-Tacoma in Wasington, the San Fransicso Bay Area in northen
	California and the major cities of Southern California such as LA and San Diego.  However, population size is not a factor in this centering 
	of hierarchical clustering.  The centers for hierarchical clustering are strictly a reflection of euclidean distances of the various points to each other.  
	This is due to the fact that each point starts out as it's own cluster - and cluster center - and then proceeds to merge with closest pairs soley based on distance.  
	Conversely, with kmeans clustering the northen-most cluster is no longer centered in the Seattle-Tacoma area, but rather is located in between 
	San Fransicso and the Seattle-Tacoma area.  This is due to the fact that population size IS a factor in determing the kmeans centers
	since the 16 centers are initiaizled based on the 16 cities with the largest populations.  Therefore, as the kmeans runs, points will be grouped 
	not strictly based on distance to each other, but distance to one of the 16 FIPS with the largest population size.  In this case, it appears that either
	Seattle-Tacoma OR a city in the San Fransicso Bay Area had one of the largest 16 population sizes.  Therefore, only one cluster center 
	was created for all the major population areas of the northern West Coast - from San Francisco to Washington - and, as a resutl, the final cluster center 
	is located between the two major population areas in San Francisco and Seattle-Tacoma.''' 

def Q9_answer():
	'''Given that distortion is a based on the distance of each point to it's cluster center, hierarchical clustering requires less human supervision 
	to minimize distortion since distance is the only factor in determining how to merge individual points to each cluster and since population doesn't play a role in initiaizling
	cluster centers.'''
	

#Q7_run(_111_DATA_FILE, 9, 5)
#a = alg_cluster.cluster_error(_111_DATA_FILE)
#print len(a)
#iters, slow, fast = compute_run_times(200)
#plot_run_times(iters, slow, fast)
#plot_random_clusters(temp)
