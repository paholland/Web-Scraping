def scrape():
    from bs4 import BeautifulSoup 
    from splinter import Browser
    import requests
    import pandas as pd
    import re
    import time 


    #Path to the chromedriver/windows used here
    # executable_path = {'executable_path': '/Users/hello/Downloads/chromedriver_win32/chromedriver'}
    # browser = Browser("chrome", **executable_path)
    executable_path = {"executable_path": "chromedriver.exe"}
    browser =  Browser("chrome", **executable_path, headless=False)

    #dictionary creation
    mars_data = {}                
    
    #NASA News
    #web url to scrape: news titles and paragraphs
    mtm_url_one = 'http://mars.nasa.gov/news'

    browser.visit(mtm_url_one)

    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=3)
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        news_title = slide_elem.find("div", class_="content_title").get_text()
        news_p = slide_elem.find( "div", class_="article_teaser_body").get_text()
    except:
        print('Title is not found')

    # browser.visit(mtm_url_one)

    #html page with browser and bs object
    # mtm_url_one_html = browser.html
    # mtm_data_soup_site1 = BeautifulSoup(mtm_url_one_html, 'html.parser')
    # time.sleep(2)
    #scrape the NASA Mars news and collect
    # news_title = mtm_data_soup_site1.find('ul',class_= 'item_list').find('li', class_="slide").find('div',class_='content_title').text
    # news_p = mtm_data_soup_site1.find('ul', class_='item_list').find('li',class_='slide').find('div',class_='article_teaser_body').text 
    
    mars_data['title']= news_title
    mars_data['news_p']= news_p   

    ## Visit the url for JPL Featured Space Image/page to scrape: image
    mtm_url_two= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mtm_url_two)

    #find the image url to the full size .jpg image
    full_image_found= browser.find_by_id('full_image')
    full_image_found.click()

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    time.sleep(2)
    # browser.links.find_by_partial_text('more info')

    browser.click_link_by_partial_text('more info')
  

    #html page with browser and bs object
    mtm_url_two_html = browser.html
    mtm_data_soup_site2 = BeautifulSoup(mtm_url_two_html,'html.parser')

    # ----------------------------------------- here

    #scrape the featured image 
    try:
        featured_image_url = mtm_data_soup_site2.find('figure', class_= "lede").find("a")['href']
    except AttributeError as attr:
        print(attr) 

    # save a complete url string for the full size .jpg image
    complete_url = 'https://www.jpl.nasa.gov' + featured_image_url
    mars_data["featured_image_url"]=complete_url
       

    #Weather

    mtm_url_three= 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mtm_url_three)  
    time.sleep(2)
    # html page with browser and bs object
    mtm_url_three_html = browser.html
    mtm_data_soup_site3 = BeautifulSoup(mtm_url_three_html, 'html.parser')
   

    # re module helps to specify the rules for the set of possible strings that we want to match
    import re
    #find the tweet under data-name
    result = mtm_data_soup_site3.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})

    try:
        result1 = result.find("p", "tweet-text").get_text()
        
    except AttributeError:

        pattern = re.compile(r'sol')
        result1 = mtm_data_soup_site3.find('span', text=pattern).text

    mars_data["weather"]= result1

    #Facts
    # Mars Facts

    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet 
    # including Diameter, Mass, etc.
    mtm_url_four = 'https://space-facts.com/mars/'
    df = pd.read_html(mtm_url_four)[0]
    df.columns =['fact','value']
    df

   #reset index on the left
    df.set_index("fact",inplace=True)

    #Convert df to html table string
    marsfacts_html=df.to_html()

 
    mars_data["facts"]= marsfacts_html
      

    #Hemisphere
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser').find_all("a",class_ = "itemLink product-item")
    hemi_titles = []
    for i in soup:
        title = i.find("h3").text
        #link= i["href"] 
    # or i.a["href"]
        hemi_titles.append(title)
    # return hemi_titles

    mtm_url_five = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mtm_url_five)

    hemisphere_image_urls = []
    hemisphere = {}
    for x in range(len(hemi_titles)): 
    #     hemisphere = {}
        try:
            browser.click_link_by_partial_text(hemi_titles[x])
        except:
            browser.find_link_by_text('2').first.click()
            browser.click_link_by_partial_text(hemi_titles[x])
        
        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']

        hemisphere['title'] = browser.find_by_css("h2.title").text

        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)
        browser.visit(mtm_url_five)

    mars_data["hem_image_urls"]= hemisphere_image_urls
    

    return mars_data


