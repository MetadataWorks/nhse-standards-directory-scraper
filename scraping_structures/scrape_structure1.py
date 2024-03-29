
from selenium.webdriver.common.by import By



def page_structure_1(driver, api_entry, keys):

    ###   setting default to NA, incase we go in except block, we'll return NA

    api_entry[keys[16]] = 'NA'
    api_entry[keys[17]] = 'NA'
    api_entry[keys[18]] = 'NA'
    api_entry[keys[19]] = 'NA'



    try:

        ##### getting associated media links
        try:
            additional_guidance = driver.find_element(By.ID, 'additional-guidance')
        except:
            print("couldnot find additional guidance")
            pass
        

        if 'additional_guidance' in locals():
            try:
                url_boxes = additional_guidance.find_elements(By.CLASS_NAME, 'nhsd-a-box-link')
            except:
                print("couldnot find any links in additional guidance")
        

        if 'url_boxes' in locals():

            try:
                media_links = []
                for box in url_boxes:
                    media_links.append(box.get_attribute('href'))

            except:
                print("couldnot get the media links from the guidance url_boxes")
                pass
            

            if media_links!=[]:
                print('media_links: ', media_links)
                api_entry[keys[16]] = ', '.join(media_links)
                


        ##### getting technology links

        try:
            tech = driver.find_element(By.ID, 'technology')
        except:
            print("couldnot find technology")
            pass
        

        if 'tech' in locals():

            try:
                all_urls_in_tech = tech.find_elements(By.TAG_NAME, 'a')
                print('all_urls_in_tech: ', len(all_urls_in_tech))

            except:
                print("couldnot find any url in techology")
                pass
        

        if 'all_urls_in_tech' in locals():

            try:
                tech_urls = []

                for tech_url in all_urls_in_tech:
                    if 'technolo' in tech_url.get_attribute('href'):
                        tech_urls.append(tech_url.get_attribute('href'))

            except:
                print("couldnot get the tech links from technology section")
                pass
            

            if tech_urls!=[]:
                print('tech urls: ', tech_urls)
                api_entry[keys[18]] = ', '.join(tech_urls)
        


        ##### getting related apis
        try:
            print('trying related apis')
            related_apis = driver.find_element(By.ID, 'related-apis')

        except:
            print("couldnot find related_apis")
            pass
        

        if 'related_apis' in locals():
            try:
                related_apis_links = related_apis.find_elements(By.TAG_NAME, 'a')
                print('related_apis_links: ', len(related_apis_links))

                rel_api_urls = [url.get_attribute('href') for url in related_apis_links]

                if rel_api_urls != []:
                    print('rel_api_urls: ', rel_api_urls)
                    api_entry[keys[19]] = ', '.join(rel_api_urls)

            except:
                print("couldnot find any url in related_apis")
                pass
    

    except Exception as e:
        print("Error while scraping through this api page",e)



    return api_entry
