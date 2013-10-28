from urlparse import urlparse
import re
import urllib2
from xml.dom import minidom
import csv

def Tokenise(url):

        if url=='':
            return [0,0,0]
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


def find_ele_with_attribute(dom,ele,attribute):
    for subelement in dom.getElementsByTagName(ele):
        if subelement.hasAttribute(attribute):
            return subelement.attributes[attribute].value
    return -1
        

def sitepopularity(host):

        xmlpath='http://data.alexa.com/data?cli=10&dat=snbamz&url='+host
        #print xmlpath
        try:
            xml= urllib2.urlopen(xmlpath)
            dom =minidom.parse(xml)
            rank_host=find_ele_with_attribute(dom,'REACH','RANK')
            #country=find_ele_with_attribute(dom,'REACH','RANK')
            rank_country=find_ele_with_attribute(dom,'COUNTRY','RANK')
            return [rank_host,rank_country]

        except:
            return [-1,-1]


def Security_sensitive(tokens_words):

    sec_sen_words=['confirm', 'account', 'banking', 'secure', 'ebayisapi', 'webscr', 'login', 'signin']
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
    
def web_content_features(url):
    wfeatures={}
    response = urllib2.urlopen(url)
    source_code = response.read()
    #print source_code[:500]
    response.close()

    wfeatures['html_cnt']=source_code.count('<html')
    wfeatures['hlink_cnt']=source_code.count('<a href=')
    wfeatures['iframe_cnt']=source_code.count('<iframe')
    #suspicious javascript functions count
    total_cnt=0
    wfeatures['eval_cnt']=source_code.count('eval(')
    total_cnt+=wfeatures['eval_cnt']
    wfeatures['escape_cnt']=source_code.count('escape(')
    total_cnt+=wfeatures['escape_cnt']
    wfeatures['link_cnt']=source_code.count('link(')
    total_cnt+=wfeatures['link_cnt']
    wfeatures['underescape_cnt']=source_code.count('underescape(')
    total_cnt+=wfeatures['underescape_cnt']
    wfeatures['exec_cnt']=source_code.count('exec(')
    total_cnt+=wfeatures['exec_cnt']
    wfeatures['search_cnt']=source_code.count('search(')
    total_cnt+=wfeatures['search_cnt']
    wfeatures['total_jfun_cnt']=total_cnt
    return wfeatures


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

def resultwriter(feature):
    flag=True
    with open('results.csv','wb') as f:
        for item in feature:
            w = csv.DictWriter(f, item[1].keys())
            if flag:
                w.writeheader()
                flag=False
            w.writerow(item[1])

def process_URL_list():
    feature=[]
    with open("URL.txt") as file:
        for line in file:
            url=line.strip()
            if url!='':
                feature.append([url,feature_extract(url)]);
    resultwriter(feature)

def main():
        process_URL_list()
           
main()
