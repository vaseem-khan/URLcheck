import pandas
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
import numpy
from sklearn import svm
from sklearn.metrics import accuracy_score
import matplotlib.pylab as plt
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning,
                        module="pandas", lineno=570)

def return_nonstring_col(data_cols):
	cols_to_keep=[]
	train_cols=[]
	for col in data_cols:
		if col!='URL' and col!='host' and col!='path':
			cols_to_keep.append(col)
			if col!='malicious' and col!='result':
				train_cols.append(col)
	return [cols_to_keep,train_cols]

def svm_classifier(train,query,train_cols):
	
	clf = svm.SVC()

	scaler = preprocessing.StandardScaler().fit(train[train_cols])
	scaler.transform(train[train_cols])
	
	print clf.fit(train[train_cols], train['malicious'])
	
	query['result']=clf.predict(query[train_cols])
	
	print query[['URL','result']]

def forest_classifier(train,query,train_cols):

	rf = RandomForestClassifier(n_estimators=150)

	print rf.fit(train[train_cols], train['malicious'])

	query['result']=rf.predict(query[train_cols])

	print query[['URL','result']]

def train(db,test_db):
	
	query_csv = pandas.read_csv(test_db)
	cols_to_keep,train_cols=return_nonstring_col(query_csv.columns)
	#query=query_csv[cols_to_keep]

	train_csv = pandas.read_csv(db)
	cols_to_keep,train_cols=return_nonstring_col(train_csv.columns)
	train=train_csv[cols_to_keep]

	svm_classifier(train_csv,query_csv,train_cols)
	
	forest_classifier(train_csv,query_csv,train_cols)

