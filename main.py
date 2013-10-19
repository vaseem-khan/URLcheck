from urlparse import urlparse
import re
import urllib2
from xml.dom import minidom


def Tokenise(url):

        token_word=re.split('\W+',url)
        #print token_word
        no_ele=sum_len=largest=0
        for ele in token_word:
                l=len(ele)
                sum_len+=l
                if l>0:                                        ## for empty element exclusion in average length
                        no_ele+=1
                if largest<l:
                        largest=l
        return [float(sum_len)/no_ele,no_ele,largest]


def sitepopularity(host):

        xmlpath='http://data.alexa.com/data?cli=10&dat=snbamz&url='+host
        #print xmlpath
        try:
                xml= urllib2.urlopen(xmlpath)
                dom =minidom.parse(xml)
                #dom.getElementsByTagName('POPULARITY')[0].attributes['TEXT'].value
                rank_host= dom.getElementsByTagName('REACH')[0].attributes['RANK'].value
                #country=dom.getElementsByTagName('COUNTRY')[0].attributes['CODE'].value
                rank_country= dom.getElementsByTagName('COUNTRY')[0].attributes['RANK'].value
                return [rank_host,rank_country]

        except:
                return [-1,-1]


def Security_sensitive(tokens_words):

    sec_sen_words=['confirm', 'account', 'banking', 'secure', 'ebayisapi', 'webscr', 'login', 'signin']
    cnt=0
    for ele in sec_sen_words:
        if(ele in tokens_words):
            cnt+=1;

    return cnt


def Check_IPaddress(tokens_words):

    cnt=0;
    for ele in tokens_words:
        if unicode(ele).isnumeric():
            cnt+=1
        else:
            if cnt>=4 :
                return True
            else:
                cnt=0;
    return False


def feature_extract(url_input):

        Feature={}
        tokens_words=re.split('\W+',url_input)       #Extract bag of words stings delimited by (.,/,?,,=,-,_)
        #print tokens_words,len(tokens_words)

        #token_delimit1=re.split('[./?=-_]',url_input)
        #print token_delimit1,len(token_delimit1)

        obj=urlparse(url_input)
        host=obj.netloc
        path=obj.path

        Feature['URL']=url_input

        Feature['rank_host'],Feature['rank_country'] =sitepopularity(host)

        Feature['host']=obj.netloc
        Feature['path']=obj.path

        Feature['Length_of_url']=len(url_input)
        Feature['Length_of_host']=len(host)
        Feature['No_of_dots']=url_input.count('.')

        Feature['avg_token_length'],Feature['token_count'],Feature['largest_token'] = Tokenise(url_input)
        Feature['avg_domain_token_length'],Feature['domain_token_count'],Feature['largest_domain'] = Tokenise(host)
        Feature['avg_path_token'],Feature['path_token_count'],Feature['largest_path'] = Tokenise(path)

        Feature['sec_sen_word_cnt'] = Security_sensitive(tokens_words)
        Feature['IPaddress_presence'] = Check_IPaddress(tokens_words)

        return Feature


def main():

        url_input="https://www.google.co.in/search?q=split+python&oq=split+python&aqs=chrome41j0j7&sourceid=chrome&espvd=0&es_sm=3&ie=UTF-8"
        #url_input=raw_input("Enter URL")

        feature=feature_extract(url_input)

        for i in feature:
                print i+" : "+str(feature[i])

main()
