from flask import Flask, render_template
import requests
import json
from secrets import api_key

app = Flask(__name__)

@app.route('/name/<nm>')
def hello_name(nm):
    story_list_json = get_stories('technology')
    headlines = get_headlines(story_list_json)
    # my_list=headlines
    return render_template('name.html', name=nm, my_list=headlines)

@app.route('/')
def home():
    return ("<h1> Welcome!<h1>" )

def params_unique_combination(baseurl, params):#combine URL and parameter for key as cache dictionary
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_" + "_".join(res)

def make_request_using_cache(baseurl, params):#will check if request id is in dictionary
    unique_ident = params_unique_combination(baseurl, params)
    # Make the request and cache the new data
    resp = requests.get(baseurl, params)
    results = json.loads(resp.text)#convery request into txt, then load into json file
    # #Ads in function to get timestamp of last called request
    # CACHE_DICTION[unique_ident]['cache_timestamp'] = datetime.now().timestamp()
    # dumped_json_cache = json.dumps(CACHE_DICTION) #dump dictionary into string
    # fw = open(CACHE_FNAME,"w") #wirte string into file
    # fw.write(dumped_json_cache)
    # fw.close() # Close the open file
    return results

# gets stories from a particular section of NY times
def get_stories(section):
    baseurl = 'https://api.nytimes.com/svc/topstories/v2/'
    extendedurl = baseurl + section + '.json'
    params={'api-key': api_key}
    return make_request_using_cache(extendedurl, params)

def get_headlines(story_list_json):
    results = story_list_json['results']
    print_format = []
    for r in results[:5]:
        title=r['title']
        url=r['url']
        statement=str(title + ' ' +"("+url+")")
        print_format.append(statement)
    return print_format

# story_list_json = get_stories('technology')
# headlines = get_headlines(story_list_json)
# for h in headlines:
#     print(h)
# for h in headlines:
#     print(h)

#store in list of strings
#for loop on html
#ol for ordered story_list_json

if __name__ == '__main__':
    app.run(debug=True)
