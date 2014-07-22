This is a simple script to get Apple AppStore reviews for you iOS application.

INSTALL
Need python version 2.6 at least, not compatible with python 3.0. Additional modules: elementtree and argparse are required. To install this modules:
% sudo easy_install elementtree
% sudo easy_install argparse
The output is given with UTF-8 charsets; if you are scraping non-english AppStore set the environment to use UTF:
% export LANG=en_US.UTF-8
% export PYTHONIOENCODING=utf-8

USAGE
AppStoreReviews.py [-h] [-i AppId] [-c "Name"] [-l]
1) Get reviews for application id = 322550986
% AppStoreReviews.py -i 322550986
2) Get reviews for application id = 322550986 in specific AppStore
% AppStoreReviews.py -i 322550986 -c "united states"
3) Get the list of known appstores
% AppStoreReviews.py -l

USE AS A MODULE
You can use it as a module in your python program. Just import it and use getReviews(appStoreId, appId) function to retrieve reviews for given country and application.

FUNCTIONS
    getReviews(appStoreId, appId)
        returns list of reviews for given AppStore ID and application Id
        return list format: [{"topic": unicode string, "review": unicode string, "rank": int}]

COPYRIGHTS
    Apple AppStore reviews scrapper
    version 2011-04-12
    Tomek "Grych" Gryszkiewicz, grych@tg.pl
    http://www.tg.pl

    based on "Scraping AppStore Reviews" blog by Erica Sadun
     - http://blogs.oreilly.com/iphone/2008/08/scraping-appstore-reviews.html
    AppStore codes are based on "appstore_reviews" by Jeremy Wohl
     - https://github.com/jeremywohl/iphone-scripts/blob/master/appstore_reviews


