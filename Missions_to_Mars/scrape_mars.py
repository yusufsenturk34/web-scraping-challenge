from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd



def init_browser(): 
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()


    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = bs(response.text,'html.parser')

    
    news_title = soup.find('div', class_= "content_title").find('a').text.strip()
    news_parag = soup.find('div', class_= "rollover_description_inner").text.strip()

    
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

   
    html_image = browser.html
    soup = bs(html_image, 'html.parser')

    
    featured_image_sub_url = soup.find('div',class_='carousel_items')('article')[0]['style'].\
        replace('background-image: url(','').replace(');','')[1:-1]

   
    main_url = 'https://www.jpl.nasa.gov'

    
    featured_image_url = main_url + featured_image_sub_url

    
    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet_url)

    
    last_tweets = soup.find_all('div', class_='js-tweet-text-container')

    mars_weather = ""
    
    for tweet in last_tweets:
        tweet_text = tweet.p.text
    
        
        if 'Sol' and 'winds' and 'pressure' in tweet_text:
            mars_weather = tweet_text
            break
        else:
            pass
   
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    tables = pd.read_html(facts_url)

    
    mars_facts_raw = tables[1]

    
    mars_facts=mars_facts_raw.rename(columns={0:'Fact',1:'Value'}).set_index('Fact').copy()

    
    mars_facts_html = mars_facts.to_html()
    
    hemisph_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisph_url)

    html_hemisph = browser.html
    soup = bs(html_hemisph, 'html.parser')


    items = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    hemispheres_main_url = 'https://astrogeology.usgs.gov'


    for i in items: 
        
        title = i.find('h3').text
    
        
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
        
        browser.visit(hemispheres_main_url + partial_img_url)
    
        
        partial_img_html = browser.html
    
        
        soup = bs( partial_img_html, 'html.parser')
    
        
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
        
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    mars_data = {
        "Mars_News_Title": news_title,
        "Mars_News_Paragraph": news_parag,
        "Mars_Featured_Image": featured_image_url,
        "Mars_Weather_Data": mars_weather,
        "Mars_Facts": mars_facts_html,
        "Mars_Hemisphere_Images": hemisphere_image_urls
    }

    browser.quit()

    return mars_data