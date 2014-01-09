import pandas
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
import numpy
from sklearn import svm
from sklearn import cross_validation as cv
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

	train[train_cols] = preprocessing.scale(train[train_cols])
	query[train_cols] = preprocessing.scale(query[train_cols])
	
	print clf.fit(train[train_cols], train['malicious'])
	scores = cv.cross_val_score(clf, train[train_cols], train['malicious'], cv=30)
	print('Estimated score SVM: %0.5f (+/- %0.5f)' % (scores.mean(), scores.std() / 2))

	query['result']=clf.predict(query[train_cols])
	
	print query[['URL','result']]

# Called from gui
def forest_classifier_gui(train,query,train_cols):

	rf = RandomForestClassifier(n_estimators=150)

	print rf.fit(train[train_cols], train['malicious'])

	query['result']=rf.predict(query[train_cols])

	print query[['URL','result']].head(2)
	return query['result']

def forest_classifier(train,query,train_cols):

	rf = RandomForestClassifier(n_estimators=150)

	print rf.fit(train[train_cols], train['malicious'])
	scores = cv.cross_val_score(rf, train[train_cols], train['malicious'], cv=30)
	print('Estimated score RandomForestClassifier: %0.5f (+/- %0.5f)' % (scores.mean(), scores.std() / 2))

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

def gui_caller(db,test_db):
	
	query_csv = pandas.read_csv(test_db)
	cols_to_keep,train_cols=return_nonstring_col(query_csv.columns)
	#query=query_csv[cols_to_keep]

	train_csv = pandas.read_csv(db)
	cols_to_keep,train_cols=return_nonstring_col(train_csv.columns)
	train=train_csv[cols_to_keep]

	return forest_classifier_gui(train_csv,query_csv,train_cols)	

