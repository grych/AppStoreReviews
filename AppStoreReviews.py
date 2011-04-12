#!/usr/bin/env python
''' Apple AppStore reviews scrapper
    version 2011-04-12
    Tomek "Grych" Gryszkiewicz, grych@tg.pl
    http://www.tg.pl
    
    based on "Scraping AppStore Reviews" blog by Erica Sadun
     - http://blogs.oreilly.com/iphone/2008/08/scraping-appstore-reviews.html
    AppStore codes are based on "appstore_reviews" by Jeremy Wohl
     - https://github.com/jeremywohl/iphone-scripts/blob/master/appstore_reviews
'''
import urllib2
from elementtree import ElementTree
import sys
import string
import argparse

appStores = {
'Argentina':          143505,
'Australia':          143460,
'Belgium':            143446,
'Brazil':             143503,
'Canada':             143455,
'Chile':              143483,
'China':              143465,
'Colombia':           143501,
'Costa Rica':         143495,
'Croatia':            143494,
'Czech Republic':     143489,
'Denmark':            143458,
'Deutschland':        143443,
'El Salvador':        143506,
'Espana':             143454,
'Finland':            143447,
'France':             143442,
'Greece':             143448,
'Guatemala':          143504,
'Hong Kong':          143463,
'Hungary':            143482,
'India':              143467,
'Indonesia':          143476,
'Ireland':            143449,
'Israel':             143491,
'Italia':             143450,
'Korea':              143466,
'Kuwait':             143493,
'Lebanon':            143497,
'Luxembourg':         143451,
'Malaysia':           143473,
'Mexico':             143468,
'Nederland':          143452,
'New Zealand':        143461,
'Norway':             143457,
'Osterreich':         143445,
'Pakistan':           143477,
'Panama':             143485,
'Peru':               143507,
'Phillipines':        143474,
'Poland':             143478,
'Portugal':           143453,
'Qatar':              143498,
'Romania':            143487,
'Russia':             143469,
'Saudi Arabia':       143479,
'Schweiz/Suisse':     143459, 
'Singapore':          143464,
'Slovakia':           143496,
'Slovenia':           143499,
'South Africa':       143472,
'Sri Lanka':          143486,
'Sweden':             143456,
'Taiwan':             143470,
'Thailand':           143475,
'Turkey':             143480,
'United Arab Emirates'  :143481,
'United Kingdom':     143444,
'United States':      143441,
'Venezuela':          143502,
'Vietnam':            143471,
'Japan':              143462,
'Dominican Republic': 143508,
'Ecuador':            143509,
'Egypt':              143516,
'Estonia':            143518,
'Honduras':           143510,
'Jamaica':            143511,
'Kazakhstan':         143517,
'Latvia':             143519,
'Lithuania':          143520,
'Macau':              143515, 
'Malta':              143521,
'Moldova':            143523,  
'Nicaragua':          143512,
'Paraguay':           143513,
'Uruguay':            143514
}

def getReviews(appStoreId, appId):
    ''' returns list of reviews for given AppStore ID and application Id
        return list format: [{"topic": unicode string, "review": unicode string, "rank": int}]
    ''' 
    reviews=[]; stars=[]; topics=[]
    i=0
    while True: 
        (r,s,t)=_getReviewsForPage(appStoreId, appId, i)
        if len(r)==0: # funny do while emulation ;)
            break
        reviews.extend(r)
        stars.extend(s)
        topics.extend(t)
        i += 1
    if len(reviews)!=len(stars):
        print "UUPS! Spanish inquisition detected. Resistance is futile. This script is giving up."
        raise SystemExit
    output = []
    for i in range(len(reviews)):
        output.append({"review": reviews[i], "rank":stars[i], "topic":topics[i] })
    return output

def _getReviewsForPage(appStoreId, appId, pageNo):
    userAgent = 'iTunes/9.2 (Macintosh; U; Mac OS X 10.6)'
    front = "%d-1" % appStoreId
    url = "http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewContentsUserReviews?id=%s&pageNumber=%d&sortOrdering=4&onlyLatestVersion=false&type=Purple+Software" % (appId, pageNo)
    req = urllib2.Request(url, headers={"X-Apple-Store-Front": front,"User-Agent": userAgent})
    try:
        u = urllib2.urlopen(req, timeout=30)
    except urllib2.HTTPError:
        print "Can't connect to the AppStore, please try again later."
        raise SystemExit
    root = ElementTree.parse(u).getroot()
    reviews=[]; stars=[]; topics=[]
    for node in root.findall('{http://www.apple.com/itms/}View/{http://www.apple.com/itms/}ScrollView/{http://www.apple.com/itms/}VBoxView/{http://www.apple.com/itms/}View/{http://www.apple.com/itms/}MatrixView/{http://www.apple.com/itms/}VBoxView/{http://www.apple.com/itms/}VBoxView/{http://www.apple.com/itms/}VBoxView/{http://www.apple.com/itms/}TextView/{http://www.apple.com/itms/}SetFontStyle'):
        reviews.append(node.text)
    for node in root.findall('{http://www.apple.com/itms/}View/{http://www.apple.com/itms/}ScrollView/{http://www.apple.com/itms/}VBoxView/{http://www.apple.com/itms/}View/{http://www.apple.com/itms/}MatrixView/{http://www.apple.com/itms/}VBoxView/{http://www.apple.com/itms/}VBoxView/{http://www.apple.com/itms/}VBoxView/{http://www.apple.com/itms/}HBoxView/{http://www.apple.com/itms/}HBoxView/{http://www.apple.com/itms/}HBoxView'):
        try:
            alt = node.attrib['alt']
            st = int(alt.strip(' stars'))
        except KeyError:
            continue
        stars.append(st)
    for node in root.findall('{http://www.apple.com/itms/}View/{http://www.apple.com/itms/}ScrollView/{http://www.apple.com/itms/}VBoxView/{http://www.apple.com/itms/}View/{http://www.apple.com/itms/}MatrixView/{http://www.apple.com/itms/}VBoxView/{http://www.apple.com/itms/}VBoxView/{http://www.apple.com/itms/}VBoxView/{http://www.apple.com/itms/}HBoxView/{http://www.apple.com/itms/}TextView/{http://www.apple.com/itms/}SetFontStyle/{http://www.apple.com/itms/}b'):
        topics.append(node.text)
    u.close()
    return (reviews, stars, topics)
    
def _print_reviews(reviews, country):
    ''' returns (reviews count, sum rank)
    '''
    if len(reviews)>0:
        print "Reviews in %s:" % (country)
        sumRank = 0
        for review in reviews:
            for i in range(review["rank"]):
                sys.stdout.write ("*") # to avoid space or newline after print
            print " (%s) %s" % (review["topic"], review["review"])
            sumRank += review["rank"]
        print "Number of reviews in %s: %d, avg rank: %.2f\n" % (country, len(reviews), 1.0*sumRank/len(reviews))
        return (len(reviews), sumRank)
    else:
        return (0, 0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AppStoreReviewsScrapper command line.', epilog='To get your application Id look into the AppStore link to you app, for example http://itunes.apple.com/pl/app/autobuser-warszawa/id335042980?mt=8 - app Id is the number between "id" and "?mt=0"')
    parser.add_argument('-i', '--id', default=0, metavar='AppId', type=int, help='Application Id (see below)')
    parser.add_argument('-c', '--country', metavar='"Name"', type=str, default='all', help='AppStore country name (use -l to see them)')
    parser.add_argument('-l', '--list', action='store_true', default=False, help='AppStores list')
    args = parser.parse_args()
    if args.id == 0:
        parser.print_help()
        raise SystemExit
    country = string.capwords(args.country)
    countries=appStores.keys()
    countries.sort()
    if args.list:
        for c in countries:
            print c
    else:
        if (country=="All"):
            rankCount = 0; rankSum = 0
            for c in countries:
                reviews = getReviews(appStores[c], args.id)
                (rc,rs) = _print_reviews(reviews, c)
                rankCount += rc
                rankSum += rs
            print "\nTotal number of reviews: %d, avg rank: %.2f" % (rankCount, 1.0 * rankSum/rankCount)
        else:
            try:
                reviews = getReviews(appStores[country], args.id)
                _print_reviews(reviews, country)
            except KeyError:
                print "No such country %s!\n\nWell, it could exist in real life, but I dont know it." % country
            pass
        
