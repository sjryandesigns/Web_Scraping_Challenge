# Import dependencies

from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

# Initialize browser/chromedriver

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)

# Code for scraping web data and storing in dictionary

def scrape_info():
    browser = init_browser()
    mars_dict = {}

    # Visit the NASA Mars News site and scrape headline
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    time.sleep(1)

    news_html = browser.html
    news_soup = bs(news_html,'html.parser')

    news_list = news_soup.find('ul', class_='item_list')
    first_item = news_list.find('li', class_='slide')

    news_title = first_item.find('div', class_='content_title').text
    news_p = first_item.find('div', class_='article_teaser_body').text

    mars_dict["mars_newstitle"] = news_title
    mars_dict["mars_paragraph"] = news_p


    # Visit the JPL website and scrape the featured image

    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)

    time.sleep(1)

    img_html = browser.html
    jpl_soup = bs(img_html,"html.parser")

    image_url = jpl_soup.find('div',class_='carousel_container').article.footer.a['data-fancybox-href']
    link = "https:"+jpl_soup.find('div', class_='jpl_logo').a['href'].rstrip('/')
    featured_image_url = link + image_url

    mars_dict["feature_image"] = featured_image_url

    # Visit space facts and scrap the mars facts table

    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    time.sleep(1)
    
    mars_facts_html = browser.html
    mars_facts_soup = bs(mars_facts_html, 'html.parser')

    tables=pd.read_html(mars_facts_url)
    facts_df=tables[0]
    facts_df.columns = ["Description", "Value"]
    mars_html_table = facts_df.to_html()

    mars_dict["mars_table"] = mars_html_table

    # Scrape images of Mars' hemispheres from the USGS site

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    time.sleep(1)

    hemisphere_image_urls = []

    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
    
        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()
        time.sleep(1)
    
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
    
        # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.links.find_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
         
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
    
        # Navigate Backwards
        browser.back()

    mars_dict["hemisphere_imgs"] = hemisphere_image_urls 

    browser.quit()

    return mars_dict
