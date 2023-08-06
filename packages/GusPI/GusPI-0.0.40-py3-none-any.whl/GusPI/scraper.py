import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import pandas as pd

def YelpBizInfo(CUISINES):

  biz=[]
  aggregateRating=[]
  priceRange=[]
  streetAddress=[]
  addressLocality=[]
  addressRegion=[]
  postalCode=[]
  yelp=[]

  for name in CUISINES:

    for cp in np.arange(0,1):

      url = "http://www.yelp.com/biz/" + name + "?start=" + str(cp*20)
      html = urlopen(url)
      soup = BeautifulSoup(html, 'html.parser')
      metas_biz = soup.findAll("meta",{"itemprop":"name"})
      metas_aggregateRating = soup.find_all("meta",{"itemprop":"ratingValue"})
      metas_priceRange = soup.find_all("meta",{"itemprop":"priceRange"})

      biz.append(name)
      aggregateRating.extend(i for i in [meta_aggregateRating.attrs['content'] for meta_aggregateRating in metas_aggregateRating[0:1] if 'itemprop' in meta_aggregateRating.attrs])
      priceRange.extend(i for i in [meta_priceRange.attrs['content'] for meta_priceRange in metas_priceRange if 'itemprop' in meta_priceRange.attrs])
      streetAddress.extend(i.text for i in soup.findAll("span",{"itemprop":"streetAddress"}))
      addressLocality.extend(i.text for i in soup.findAll("span",{"itemprop":"addressLocality"}))
      addressRegion.extend(i.text for i in soup.findAll("span",{"itemprop":"addressRegion"}))
      postalCode.extend(i.text for i in soup.findAll("span",{"itemprop":"postalCode"}))
      time.sleep(1)


  biz = pd.DataFrame(biz)
  aggregateRating = pd.DataFrame(aggregateRating)
  priceRange = pd.DataFrame(priceRange)
  streetAddress = pd.DataFrame(streetAddress)
  addressLocality = pd.DataFrame(addressLocality)
  addressRegion = pd.DataFrame(addressRegion)
  postalCode = pd.DataFrame(postalCode)

  yelp = pd.concat([biz, aggregateRating,  priceRange,  streetAddress, addressLocality, addressRegion, postalCode], axis=1, ignore_index=True)
  yelp.columns = ['biz','aggregateRating','priceRange', 'streetAddress', 'addressLocality', 'addressRegion', 'postalCode']

  export = yelp.to_csv("BizInfo" + ".csv")


def YelpReview(CUISINES):
    for name in CUISINES:

      date=[]
      author=[]
      #rating=[]
      review=[]
      yelp=[]

      for cp in np.arange(0,10):

        url = "http://www.yelp.com/biz/" + name + "?start=" + str(cp*20)
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        metas_author = soup.findAll("meta",{"itemprop":"author"})
        #metas_ratingValue = soup.find_all("meta",{"itemprop":"ratingValue"})
        metas_date = soup.find_all("meta",{"itemprop":"datePublished"})

        date.extend(i for i in [meta_date.attrs['content'] for meta_date in metas_date if 'itemprop' in meta_date.attrs])
        author.extend(i for i in [meta_author.attrs['content'] for meta_author in metas_author if 'itemprop' in meta_author.attrs])
        #rating.extend(i for i in [meta_ratingValue.attrs['content'] for meta_ratingValue in metas_ratingValue[1:21] if 'itemprop' in meta_ratingValue.attrs])
        review.extend(i.text for i in soup.findAll("p",{"itemprop":"description"}))
        time.sleep(1)


      date = pd.DataFrame(date)
      author = pd.DataFrame(author)
      #rating = pd.DataFrame(rating)
      review = pd.DataFrame(review)

      yelp = pd.concat([date, author,  review], axis=1, ignore_index=True)
      yelp.columns = ['date','author','review']

      export = yelp.to_csv(name + ".csv")
