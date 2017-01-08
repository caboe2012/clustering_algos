''' Week3 Project '''
import math
import alg_cluster

#0 ZIP
#1 X (HORIZ)
#2 Y (VERT)
#3 Population
#4 Risk

_111_DATA = "unifiedCancerData_111.csv"
_290_DATA = "unifiedCancerData_290.csv"
_896_DATA = "unifiedCancerData_896.csv"
_3108_DATA = "unifiedCancerData_3108.csv"

#Clust = create_singleton_list(csv_file)
#Clust.sort(key = lambda cluster: cluster.horiz_center())
#temp = Clust[0:3]
#print temp
#print fast_closest_pair(Clust)



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

def slow_closest_pair(cluster_list):
	'''Takes a list of Cluster objects and returns a closest pair slowly
	where the pair is represented by the tuple (dist, idx1, idx2) 
	with idx1 < idx2 where dist is the distance between the closest 
	pair cluster_list[idx1] and cluster_list[idx2].'''
	#counter = 0
	_dist = float("inf")
	_idx1 = -1
	_idx2 = -1
	_closest_pair = (_dist,_idx1,_idx2)
	for _idx1 in range(len(cluster_list)):
		for _idx2 in range(len(cluster_list)):
			if _idx1 != _idx2:
				_current_dist = cluster_list[_idx1].distance(cluster_list[_idx2])
				if _current_dist < _closest_pair[0]:
					_dist = _current_dist
					_closest_pair = (_dist,_idx1,_idx2)
	return _closest_pair

def closest_pair_strip(cluster_list, horiz_center, half_width):
	'''Takes a list of Cluster objects and two floats horiz_center and half_width. 
	horiz_center specifies the horizontal position of the center line for a vertical strip. 
	half_width specifies the maximal distance of any point in the strip from the center line'''
	_indicies = [i for i in range(len(cluster_list)) if (abs(cluster_list[i].horiz_center()-horiz_center) < half_width)]
	#print _indicies
	_temp = [cluster_list[j].vert_center() for j in _indicies]
	_sorted_indicies = [_idx for (_y_val, _idx) in sorted(zip(_temp,_indicies))]
	(_dist, _idx1, _idx2) = (float('inf'), -1, -1)
	for _outer in range(0,len(_indicies)-1):
		for _inner in range(_outer+1,min(_outer+4,len(_indicies))):
			(_dist, _idx1, _idx2) = min((_dist, _idx1, _idx2), (cluster_list[_sorted_indicies[_outer]].distance(cluster_list[_sorted_indicies[_inner]]), _sorted_indicies[_outer], _sorted_indicies[_inner]))
			_first = min(_idx1, _idx2)
			_second = max(_idx1,_idx2)
			_idx1 = _first
			_idx2 = _second
	return (_dist, _idx1, _idx2)

#print closest_pair_strip(temp_cluster, center, w)


def fast_closest_pair(cluster_list):
	'''Takes a list of Cluster objects and quickly returns a closest pair 
	where the pair is represented by the tuple (dist, idx1, idx2) 
	with idx1 < idx2 where dist is the distance between the closest 
	pair cluster_list[idx1] and cluster_list[idx2].'''
	cluster_list.sort(key = lambda cluster: cluster.horiz_center())
	_cluster_length = len(cluster_list)
	if _cluster_length <= 3:
		(_dist,_idx1,_idx2) = slow_closest_pair(cluster_list)
	else:
		_middle = int(math.floor(_cluster_length/2.))
		_left_half = cluster_list[0:_middle]
		_left_half.sort(key = lambda cluster: cluster.horiz_center())
		_right_half = cluster_list[_middle:_cluster_length]
		_right_half.sort(key = lambda cluster: cluster.horiz_center())
		
		(_left_dist,_left_idx1,_left_idx2) = fast_closest_pair(_left_half)
		(_right_dist,_right_idx1,_right_idx2) = fast_closest_pair(_right_half)

		(_dist, _idx1, _idx2) = min((_left_dist,_left_idx1,_left_idx2), (_right_dist,_right_idx1+_middle,_right_idx2+_middle))
#		print cluster_list[_middle-1].horiz_center()
#		print cluster_list[_middle].horiz_center()
		_mid_point = 0.5*(cluster_list[_middle-1].horiz_center()+cluster_list[_middle].horiz_center())
#		print _mid_point
#		print
		(_dist,_idx1, _idx2) = min((_dist, _idx1, _idx2), closest_pair_strip(cluster_list, _mid_point, _dist))
	return (_dist, _idx1, _idx2)


def create_singleton_list(data_file):
	'''Loads the cancer risk table and converts the list of FIPS into Cluster Objects'''
	data_table = load_data_table(data_file)
	singleton_list = []
	for line in data_table:
	    singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
	return singleton_list

def hierarchical_clustering(cluster_list, num_clusters):
	'''Takes a list of Cluster objects and applies hierarchical clustering as described 
	in the pseudo-code HierarchicalClustering from Homework 3 to this list of clusters. 
	This clustering process should proceed until num_clusters clusters remain. 
	The function then returns this list of clusters.'''
	_cluster_length = len(cluster_list)
	_cluster_set = cluster_list[:]
	#print len(_cluster_set)
	#print
	while len(_cluster_set) > num_clusters:
		_closest_two = fast_closest_pair(_cluster_set)
		#print _closest_two
		_cluster_set[_closest_two[1]].merge_clusters(_cluster_set[_closest_two[2]])
		_cluster_set.pop(_closest_two[2])
	return _cluster_set

def kmeans_clustering(cluster_list, num_clusters, num_iterations):
	''' Takes a list of Cluster objects and applies k-means clustering as described in the pseudo-code 
	KMeansClustering from Homework 3 to this list of clusters. This function should compute an initial 
	list of clusters (line 2 in the pseudo-code) with the property that each cluster consists of a single 
	county chosen from the set of the num_cluster counties with the largest populations. The function 
	should then compute num_iterations of k-means clustering and return this resulting list of clusters'''
	_cluster_length = len(cluster_list)
	_temp = cluster_list[:]
	#_cluster_copy = cluster_list[:]
	_temp.sort(key = lambda cluster: cluster.total_population()) 
	_k_centers = _temp[-(num_clusters):]
#	ans = -1
	#print _k_centers
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
#		ans = _k_initial_sets
	return _k_centers


#print Clust
#Clust.sort(key = lambda cluster: cluster.horiz_center())
#temp = Clust[0:24]
#for each in temp[14:18]:
#	print each
#print fast_closest_pair(Clust)


def run_example(data_table, method, num_clusters, num_iterations):
	''' GIVE IT A BREAK'''
	singleton_list = []
	for line in data_table:
	    singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
	if method == "h":
		_ans = hierarchical_clustering(singleton_list, num_clusters)
	elif method == "k":
		_ans = kmeans_clustering(singleton_list, num_clusters, num_iterations)
	else:
		print "Clustering method not recognized.\n  Please use 'h' for hierarchical_clustering\n or use 'k' for kmeans_clustering"   
		return
	#for _each in _ans:
	#	print _each
	return _ans

#run_example()
#a= hierarchical_clustering(temp, 2)
#cluster_list = create_singleton_list(csv_file)
#cluster_list.sort(key = lambda cluster: cluster.horiz_center())
#print cluster_list

#print create_singleton_list(_290_DATA)
#print _290Clust
#print slow_closest_pair(Clust) - WORKS CORRECTLY!















