from rapidfuzz import fuzz,process
import math,re,numpy as np,pandas as pd
import re

def comparison_count(one_d_arr_1,one_d_arr_2):
	if (one_d_arr_2.size != one_d_arr_2.size):
		raise Exception('Comparison Count Error; the two 1D arrays have mismatched lengths')
	# return sum((one_d_arr_1.tolist()[i]==one_d_arr_2.tolist()[i]) and one_d_arr_2.tolist()[i]==1 for i in range(len(one_d_arr_1.tolist())))
	return ((one_d_arr_1 & one_d_arr_2).sum())

def get_match_ratio(str_1,str_2):
	return fuzz.ratio(str_1,str_2)


def euclidean_distance(one_d_arr_1,one_d_arr_2):
	if (len(one_d_arr_2) != len(one_d_arr_2)):
		raise Exception('Eucidean Distance Error; the two 1D arrays have mismatched lengths')
	return np.linalg.norm(one_d_arr_2-one_d_arr_1)


def extract_values(one_d_arr, indices):
	return one_d_arr[indices]

def sort_template_by_rank(distance_template):
	return sorted(distance_template, key=lambda r:r[0])

def compute_distances(query_data_1d, train_data_2d, distance_template):
	sorted_distance_template = sort_template_by_rank(distance_template)
	distances_computed = list()
	pattern_d_ratio = re.compile('d(\d+)')
	for id_, data in enumerate(train_data_2d):
		distance_values =list()
		for *_, indices, method, d_ratio,multiplier in sorted_distance_template:
			values_query = extract_values(query_data_1d, indices)
			values_train = extract_values(data, indices)
			if method == 'e':
				distance = euclidean_distance(values_query.astype(np.float64),values_train.astype(np.float64))
			elif method == 'f':
				distance = get_match_ratio(values_query,values_train)   
			elif method == 'c':
				try:
					distance = comparison_count(values_query.astype(np.int64),values_train.astype(np.int64))
				except:

					distance = comparison_count(values_query.astype(np.int64),values_train.astype(np.int64))                    
			elif method == 'n':
				distance = abs(float(values_query)-float(values_train))
			elif method == 's':
				distance = round(values_train/int(pattern_d_ratio.findall(d_ratio)[0]))
			if method != 's':
				if pattern_d_ratio.findall(d_ratio)[0] == "1":
					distance = distance
				else:
					distance = round(distance / int(pattern_d_ratio.findall(d_ratio)[0]))
			distance_values.append((distance,multiplier))
		distances_computed.append((id_, distance_values))
	return distances_computed

def sort_distances_computed(distances_computed):
	def sorter(x):
		sorting_list = list()
		for v,m in x[1]:
			sorting_list.append(v*m)
		return sorting_list
	return sorted(distances_computed, key=sorter)



def extract_n_neighbours_data(extracting_indices_1d, train_data_2d,k):
	if k > len(extracting_indices_1d):
		raise Exception('K Error; k > avaailable train data')
	if k == -1:
		return train_data_2d[extracting_indices_1d]
	else:
		return train_data_2d[extracting_indices_1d[:k]]

def extract_recommended_distances(sorted_distances_computed,k):
	if k > len(sorted_distances_computed):
		raise Exception('K Error; k > avaailable train data')
	if k == -1:
		return list(j for *_,j in sorted_distances_computed)
	else:
		return list(j for *_,j in sorted_distances_computed[:k])

def extract_recommeded_indices(sorted_distances_computed, k):

	if k > len(sorted_distances_computed):
		raise Exception('K Error; k > available train data')
	if k == -1:
		return list(i for i,*_ in sorted_distances_computed)
	else:
		return list(i for i,*_ in sorted_distances_computed[:k])


def compile_final_output(label_data, recommended_data_2d,recommeded_distances,recommeded_names):
	final_label = [*label_data,'Movie Title']
	final_data = np.hstack((recommended_data_2d,recommeded_names[:,np.newaxis]))
	return pd.DataFrame(data=final_data, columns=final_label)


def model_knn(k_neighbours, train_data_2d, query_data_1d,train_data_movie_titles_1d,distance_template, label_data=None):
	distances_computed = compute_distances(query_data_1d,train_data_2d,distance_template)
	sorted_distances_computed = sort_distances_computed(distances_computed)
	extracting_indices = list(i for i,*_ in sorted_distances_computed)
	recommended_data_2d = extract_n_neighbours_data(extracting_indices, train_data_2d, k_neighbours)
	recommeded_distances = extract_recommended_distances(sorted_distances_computed, k_neighbours)
	recommeded_indices = extract_recommeded_indices(sorted_distances_computed,k_neighbours)
	recommeded_names = train_data_movie_titles_1d[recommeded_indices]
	return compile_final_output(label_data,recommended_data_2d,recommeded_distances,recommeded_names),recommeded_distances

