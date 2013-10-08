from urlparse import urlparse
import re

def Tokenise(url):
    token_word=re.split('\W+',url)
    #print token_word
    no_ele=sum_len=largest=0
    for ele in token_word:
    	l=len(ele)
        sum_len+=l
        if l>0:					## for empty element exclusion in average length
        	no_ele+=1
        if largest<l:
        	largest=l
    return [float(sum_len)/no_ele,no_ele,largest]

def Laxical_feature_extract(url_input):
	Feature={}
	tokens_words=re.split('\W+',url_input)				#Extract bag of words stings delimited by (.,/,?,,=,-,_)
	#print tokens_words,len(tokens_words)

	#token_delimit1=re.split('[./?=-_]',url_input)
	#print token_delimit1,len(token_delimit1)

	obj=urlparse(url_input)
	host=obj.netloc
	path=obj.path

	Feature['URL']=url_input
	Feature['host']=obj.netloc
	Feature['path']=obj.path

	Feature['Length_of_url']=len(url_input)					
	Feature['Length_of_host']=len(host)
	Feature['No_of_dots']=url_input.count('.')

	Feature['avg_token_length'],Feature['token_count'],Feature['largest_token']=Tokenise(url_input)
	Feature['avg_domain_token_length'],Feature['domain_token_count'],Feature['largest_domain']=Tokenise(host)
	Feature['avg_path_token'],Feature['path_token_count'],Feature['largest_path']=Tokenise(path)
	
	return Feature

def main():
	#url=raw_input("Enter URL")
	url_input="https://www.google.co.in/search?q=split+python&oq=split+python&aqs=chrome41j0j7&sourceid=chrome&espvd=0&es_sm=3&ie=UTF-8"
	feature=Laxical_feature_extract(url_input)
	for i in feature:
		print i+" : "+str(feature[i])

main()