import math
import alg_cluster

_111_DATA = "unifiedCancerData_111.csv"
_290_DATA = "unifiedCancerData_290.csv"
_896_DATA = "unifiedCancerData_896.csv"
_3108_DATA = "unifiedCancerData_3108.csv"

def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    
    data = open(data_url, "r").read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]

def create_singleton_list(dat_file):
	'''Loads the cancer risk table and converts the list of FIPS into Cluster Objects'''
	data_table = load_data_table(dat_file)
	singleton_list = []
	for line in data_table:
	    singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
	return singleton_list

def kmeans_clustering(cluster_list, num_clusters, num_iterations):
	''' Takes a list of Cluster objects and applies k-means clustering as described in the pseudo-code 
	KMeansClustering from Homework 3 to this list of clusters. This function should compute an initial 
	list of clusters (line 2 in the pseudo-code) with the property that each cluster consists of a single 
	county chosen from the set of the num_cluster counties with the largest populations. The function 
	should then compute num_iterations of k-means clustering and return this resulting list of clusters'''
	_cluster_length = len(cluster_list) #line 1
	_temp = cluster_list[:] #line 2
	#_cluster_copy = cluster_list[:] 
	_temp.sort(key = lambda cluster: cluster.total_population()) #line 2
	_k_centers = _temp[-(num_clusters):] #line 2
	for _current_iteration in range(0,num_iterations):
		_k_initial_sets = [alg_cluster.Cluster(set([]),0,0,0,0) for _dmy in range(0,num_clusters)]
		for _point in range(0,_cluster_length):
			_min_dist = float('inf')
			_closest_center = -1
			for _k_idx in range(0, num_clusters):
				_current_dist = cluster_list[_point].distance(_k_centers[_k_idx])
				if _current_dist < _min_dist:
					_closest_center = _k_idx
					_min_dist = _current_dist
			_k_initial_sets[_closest_center].merge_clusters(cluster_list[_point])
			#dist = min([_inner_cluster_list[_inner1].distance(center, for center in _k_centers if ])
		for _each in range(0, num_clusters):
			_k_centers[_each] = _k_initial_sets[_each]
		return _k_centers
	


def run_example():
	''' GIVE IT A BREAK'''
	_csv_file = _290_DATA
	_clust = create_singleton_list(_csv_file)
	_ans = kmeans_clustering(_clust, 15, 1)
	for _each in _ans:
		print _each
	

run_example()