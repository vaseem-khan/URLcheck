#URLcheck

Learning based Malicious Web Sites Detection

**ABSTRACT**

Malicious Web sites largely promote the growth of Internet criminal activities and constrain the development of Web services. As a result, there has been strong motivation to develop systemic solution to stopping the user from visiting such Web sites. 

We propose a learning based approach to classifying Web sites into 3 classes: Benign, Spam and Malicious.

Our mechanism only analyzes the Uniform Resource Locator (URL) itself without accessing the content of Web sites. 
Thus, it eliminates the run-time latency and the possibility of exposing users to the browser based vulnerabilities.
By employing learning algorithms, our scheme achieves better performance on generality and coverage compared with blacklisting service. 


## PROJECT APPROACH

URLs of the websites are separated into 3 classes:

* Benign: Safe websites with normal services.
* Spam: Website performs the act of attempting to flood the user with advertising or sites such as fake surveys and online dating etc.
* Malware: Website created by attackers to disrupt computer operation, gather sensitive information, or gain access to private computer systems.


### Feature Extraction
Given single URL, we extract its features and  categorize them into 3 classes:

**1. Lexical Features**

Lexical features are based on the observation that the URLs of many illegal sites look different, compared with legitimate sites. Analyzing lexical features enables us to capture the property for classification purposes. We first distinguish the two parts of a URL: the host name and the path, from which we extract bag-of-words (strings delimited by ‘/’,  ‘?’, ‘.’, ‘=’,  ‘-’ and  ‘ ’). 

We find that phishing   website  prefers  to have  longer  URL,  more  levels (delimited by dot), more tokens in domain  and  path, longer token. Besides, phishing and malware websites could pretend to be a benign  one by  containing popular brand names  as tokens other than those in second-level  domain. Considering phishing  websites and malware websites may use IP address directly so as  to cover  the  suspicious  URL,  which  is very rare in benign case. Also, phishing URLs are found to contain several suggestive word tokens(confirm,  account, banking, secure,  ebayisapi, webscr,  login,  signin), we check the presence of these security sensitive words and include the binary value in our features.

**2. Site popularity Features**

  Intuitively, malicious sites are always less popular than benign ones. For this reason, site popularity can be considered as an important feature. Traffic rank feature is acquired from Alexa.com. 

**3. Host-based Features**

Host-based features are based on the observation that malicious sites are always registered in less reputable hosting centers or regions.

### Training

All of URLs in the dataset are labeled. We used two supervised learning algorithms **random forest** and **support vector machine** to train using scikit-learn library.
