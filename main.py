import csv
import Feature_extraction as urlfeature
import trainer as tr
def resultwriter(feature,output_dest):
    flag=True
    with open(output_dest,'wb') as f:
        for item in feature:
            w = csv.DictWriter(f, item[1].keys())
            if flag:
                w.writeheader()
                flag=False
            w.writerow(item[1])

def process_URL_list(file_dest,output_dest):
    feature=[]
    with open(file_dest) as file:
        for line in file:
            url=line.split(',')[0].strip()
            malicious_bool=line.split(',')[1].strip()
            if url!='':
                print 'working on: '+url           #showoff 
                ret_dict=urlfeature.feature_extract(url)
                ret_dict['malicious']=malicious_bool
                feature.append([url,ret_dict]);
    resultwriter(feature,output_dest)

def process_test_list(file_dest,output_dest):
    feature=[]
    with open(file_dest) as file:
        for line in file:
            url=line.strip()
            if url!='':
                print 'working on: '+url           #showoff 
                ret_dict=urlfeature.feature_extract(url)
                feature.append([url,ret_dict]);
    resultwriter(feature,output_dest)

#change
def process_test_url(url,output_dest):
    feature=[]
    url=url.strip()
    if url!='':
        print 'working on: '+url           #showoff 
        ret_dict=urlfeature.feature_extract(url)
        feature.append([url,ret_dict]);
    resultwriter(feature,output_dest)


def main():
        #process_URL_list('URL.txt','url_features.csv')
        process_test_list("query.txt",'query_features.csv')
        #tr.train('url_features.csv','url_features.csv')         #arguments:(input_training feature,test/query traning features)
        tr.train('url_features.csv','query_features.csv')      #testing with urls in query.txt
