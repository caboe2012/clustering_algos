"""
Testing code for clustering methods in Project 3

hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

Import your solution code below as "student"
"""

import random
import urllib2

# Use CodeSkulptor or download these Python files for use on the desktop
import poc_simpletest      # http://www.codeskulptor.org/#poc_simpletest.py
import alg_cluster         # http://www.codeskulptor.org/#alg_cluster.py

import Algo_Thinking2_Project3_FINAL as student


############################################################
# Load data tables

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"
DATA_24_URL = DIRECTORY + "data_clustering/unifiedCancerData_24.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]



#########################################################################
# Helper function for converting list of clusters to set of county tuples

def set_of_county_tuples(cluster_list):
    """
    Input: A list of Cluster objects
    Output: Set of sorted tuple of counties corresponds to counties in each cluster
    """
    set_of_clusters = set([])
    for cluster in cluster_list:
        counties_in_cluster = cluster.fips_codes()
        
        # convert to immutable representation before adding to set
        county_tuple = tuple(sorted(list(counties_in_cluster)))
        set_of_clusters.add(county_tuple)
    return set_of_clusters


#############################################################################
# Testing code

def test_kmeans():
    """
    Test for k-means clustering
    kmeans_clustering should not mutate cluster_list, but make a new copy of each test anyways
    """
    
    # load small data table
    print
    print "Testing kmeans_clustering on 24 county set"
    data_24_table = load_data_table(DATA_24_URL)
        
    kmeansdata_24 = [[15, 1, set([('34017', '36061'), ('06037',), ('06059',), ('36047',), ('36081',), ('06071', '08031'), ('36059',), ('36005',), ('55079',), ('34013', '34039'), ('06075',), ('01073',), ('06029',), ('41051', '41067'), ('11001', '24510', '51013', '51760', '51840', '54009')])], 
                     [15, 3, set([('34017', '36061'), ('06037', '06059'), ('06071',), ('36047',), ('36081',), ('08031',), ('36059',), ('36005',), ('55079',), ('34013', '34039'), ('06075',), ('01073',), ('06029',), ('41051', '41067'), ('11001', '24510', '51013', '51760', '51840', '54009')])],
                     [15, 5, set([('34017', '36061'), ('06037', '06059'), ('06071',), ('36047',), ('36081',), ('08031',), ('36059',), ('36005',), ('55079',), ('34013', '34039'), ('06075',), ('01073',), ('06029',), ('41051', '41067'), ('11001', '24510', '51013', '51760', '51840', '54009')])],
                     [10, 1, set([('34017', '36061'), ('06029', '06037', '06075'), ('11001', '24510', '34013', '34039', '51013', '51760', '51840', '54009'), ('06059',), ('36047',), ('36081',), ('06071', '08031', '41051', '41067'), ('36059',), ('36005',), ('01073', '55079')])],
                     [10, 3, set([('34013', '34017', '36061'), ('06029', '06037', '06075'), ('08031', '41051', '41067'), ('06059', '06071'), ('34039', '36047'), ('36081',), ('36059',), ('36005',), ('01073', '55079'), ('11001', '24510', '51013', '51760', '51840', '54009')])],
                     [10, 5, set([('34013', '34017', '36061'), ('06029', '06037', '06075'), ('08031', '41051', '41067'), ('06059', '06071'), ('34039', '36047'), ('36081',), ('36059',), ('36005',), ('01073', '55079'), ('11001', '24510', '51013', '51760', '51840', '54009')])],
                     [5, 1, set([('06029', '06037', '06075'), ('01073', '11001', '24510', '34013', '34017', '34039', '36047', '51013', '51760', '51840', '54009', '55079'), ('06059',), ('36005', '36059', '36061', '36081'), ('06071', '08031', '41051', '41067')])],
                     [5, 3, set([('06029', '06037', '06075'), ('11001', '24510', '34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081', '51013'), ('08031', '41051', '41067'), ('06059', '06071'), ('01073', '51760', '51840', '54009', '55079')])],
                     [5, 5, set([('06029', '06037', '06075'), ('08031', '41051', '41067'), ('06059', '06071'), ('01073', '55079'), ('11001', '24510', '34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081', '51013', '51760', '51840', '54009')])]]    
        
    suite = poc_simpletest.TestSuite()    
    
    for num_clusters, num_iterations, expected_county_tuple in kmeansdata_24:
        
        # build initial list of clusters for each test since mutation is allowed
        cluster_list = []
        for idx in range(len(data_24_table)):
            line = data_24_table[idx]
            cluster_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

        # compute student answer
        student_clustering = student.kmeans_clustering(cluster_list, num_clusters, num_iterations)
        student_county_tuple = set_of_county_tuples(student_clustering)
        
        # Prepare test
        error_message = "\n"
        error_message += "Testing kmeans_custering on 24 county table, num_clusters = " + str(num_clusters)
        error_message += " num_iterations = " + str(num_iterations)
        error_message += "\nStudent county tuples: " + str(student_county_tuple)
        error_message += "\nExpected county tuples: " + str(expected_county_tuple)
        error_message += "\n"
        suite.run_test(student_county_tuple == expected_county_tuple, True, error_message)   

    suite.report_results()
    
test_kmeans()
        
        