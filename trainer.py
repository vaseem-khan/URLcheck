import pandas 
import statsmodels.api as sm
import numpy
from sklearn import svm
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning,
                        module="pandas", lineno=570)
import Feature_extraction as urlfeature
# read the data in
def return_nonstring_col(data_cols):
	cols_to_keep=[]
	train_cols=[]
	for col in data_cols:
		if col!='URL' and col!='host' and col!='path':
			cols_to_keep.append(col)
			if col!='malicious' and col!='result':
				train_cols.append(col)
	return [cols_to_keep,train_cols]


def train(db,test_db):
	data_csv = pandas.read_csv(db)

	# print "data_csv.describe()"
	# print data_csv.describe()
	# print data_csv.columns
	
	cols_to_keep,train_cols=return_nonstring_col(data_csv.columns)
	# print cols_to_keep
	# print train_cols
	data=data_csv[cols_to_keep]
	
	print "\n\n\ndata non string columns"
	print data.head()

	clf = svm.SVC()
	print "\n\n\nSVM fitting"
	print clf.fit(data[train_cols], data['malicious'])
	predict_query(clf,test_db)



def predict_query(clf,test_db):
	data = pandas.read_csv(test_db)
	
	cols_to_keep,train_cols=return_nonstring_col(data.columns)
	data_test=data[cols_to_keep]
	data["result"]=clf.predict(data_test[train_cols])
	print data[['URL','result']].head()
	# print "\n\n\nafter SVM head"
	# print data_test[['malicious','result']].head()
	# print "\n\n\nafter SVM tail"
	# print data_test[['malicious','result']].tail()

	# print "\n accuracy_score= ",
	# print accuracy_score(data_test['malicious'],data_test['result'])

#train('url_features.csv','url_features.csv')	#testing with traing data itself
#train('url_features.csv','query_features.csv')  #testing with urls in query.txt

#logistic regression statsmodels
# dummy_ranks = pandas.get_dummies(data['prestige'], prefix='prestige')
# print dummy_ranks.head()
# cols_to_keep = ['admit', 'gre', 'gpa']
# data = data[cols_to_keep].join(dummy_ranks.ix[:, 'prestige_2':])
# print data.head()
# #rescaling
# # for col in data.columns:
# # 	min=data[col].min()
# # 	max=data[col].max()
# # 	data[col]=data[col]-min
# # 	data[col]=data[col]/float(max-min)
# #standerdisatiom
# # for col in data.columns:
# # 	std=data[col].std()
# # 	data[col]=data[col]-data[col].mean()
# # 	data[col]=data[col]/std


# # histogram
# # data.hist()
# # pylab.show()


# data['intercept'] = 1.0

# train_cols =data.columns[1:]
# print data[train_cols].head()
# logit = sm.Logit(data['admit'], data[train_cols])
 
# # # fit the model
# result = logit.fit()

# print result.summary()

# data["probablity"]=result.predict(data[train_cols])
# print data[['admit','probablity']].head(20)
