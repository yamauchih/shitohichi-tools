#
# BeautifulSoup example code from
# http://stackoverflow.com/questions/5629773/python-html-parsing-with-beautiful-soup-and-filtering-stop-words
#

import urllib2
import BeautifulSoup

def main():
    url = "http://allrecipes.com/Recipe/Slow-Cooker-Pork-Chops-II/Detail.aspx"
    data = urllib2.urlopen(url).read()
    bs = BeautifulSoup.BeautifulSoup(data)

    ingreds = bs.find('div', {'class': 'ingredients'})
    ingreds = [s.getText().strip('123456789.,/\ ') for s in ingreds.findAll('li')]

    fname = 'PorkRecipe.txt'
    with open(fname, 'w') as outf:
        outf.write('\n'.join(ingreds))

if __name__=="__main__":
    main()
