

from selenium.webdriver.common.by import By



def page_structure_2(driver, api_entry, keys):


    ###   setting default to NA, incase we go in except block, we'll return NA

    api_entry[keys[16]] = 'NA'
    api_entry[keys[17]] = 'NA'
    api_entry[keys[18]] = 'NA'
    api_entry[keys[19]] = 'NA'


    try:
        api_desc = driver.find_element(By.ID, 'api-description')


        ##### getting associated media links

        try:
            additional_guidance = api_desc.find_element(By.ID, 'api-description__additional-guidance')
        except:
            print("couldnot find additional guidance")

            
        if 'additional_guidance' in locals():
            try:
                next_heading = additional_guidance.find_element(By.XPATH, "following-sibling::h2")
                next_id = next_heading.get_attribute('id')
                # print(next_id)

            except:
                print('no next heading after additional_guidance')


        if 'next_id' in locals():
            try:
                all_elements_in_AG = api_desc.find_elements(By.XPATH, f'//*[preceding-sibling::h2[@id="api-description__additional-guidance"] and following-sibling::h2[@id="{next_id}"]]')
                print('all_elements_in_AG: ', len(all_elements_in_AG))

            except Exception as e:
                print(e)
                print("couldnot find any element in additional_guidance")

        else:
            try:
                all_elements_in_AG = api_desc.find_elements(By.XPATH, f'//*[preceding-sibling::h2[@id="api-description__additional-guidance"]]')
                print('all_elements_in_AG: ', len(all_elements_in_AG))

            except Exception as e:
                print(e)
                print("couldnot find any element in additional_guidance")
        

        if 'all_elements_in_AG' in locals():
            try:
                url_boxes = []
                for element in all_elements_in_AG:
                    url_boxes += element.find_elements(By.CLASS_NAME, 'nhsd-a-box-link')

                print('guidance url_boxes: ', len(url_boxes))

            except:
                print("couldnot find any url_box in guidance")


        if 'url_boxes' in locals() and url_boxes!=[]:
            try:
                media_links = []
                for box in url_boxes:
                    media_links.append(box.get_attribute('href'))

            except:
                print("couldnot get the media links from the guidance url_boxes")
            

            if media_links!=[]:
                print('media_links: ', media_links)
                api_entry[keys[16]] = ', '.join(media_links)
        



        ##### getting technology links
        
        try:
            tech = api_desc.find_element(By.ID, 'api-description__technology')
        except:
            print("couldnot find technology")


        if 'tech' in locals():
            try:
                next_heading = tech.find_element(By.XPATH, "following-sibling::h2")
                next_id = next_heading.get_attribute('id')
                # print(next_id)

            except:
                print('no next heading after technology')

            
        if 'next_id' in locals():
            try:
                all_elements_in_tech = api_desc.find_elements(By.XPATH, f'//*[preceding-sibling::h2[@id="api-description__technology"] and following-sibling::h2[@id="{next_id}"]]')
                print('all_elements_in_tech: ', len(all_elements_in_tech))

            except Exception as e:
                print("couldnot find any element in techology")

        else:
            try:
                all_elements_in_tech = api_desc.find_elements(By.XPATH, f'//*[preceding-sibling::h2[@id="api-description__technology"]]')
                print('all_elements_in_tech: ', len(all_elements_in_tech))

            except Exception as e:
                print("couldnot find any element in techology")
        

        if 'all_elements_in_tech' in locals():
            try:
                all_urls_in_tech = []
                for element in all_elements_in_tech:
                    all_urls_in_tech += element.find_elements(By.TAG_NAME, 'a')

                print('all_urls_in_tech: ', len(all_urls_in_tech))

            except:
                print("couldnot find any url in techology")


        if 'all_urls_in_tech' in locals() and all_urls_in_tech!=[]:
            try:
                tech_urls = []
                for tech_url in all_urls_in_tech:
                    if 'technolo' in tech_url.get_attribute('href'):
                        tech_urls.append(tech_url.get_attribute('href'))

            except:
                print("couldnot get the tech links from technology section")
            

            if tech_urls!=[]:
                print('tech_urls: ', tech_urls)
                api_entry[keys[18]] = ', '.join(tech_urls)
        



        ##### getting related apis
        
        try:
            related_apis = api_desc.find_element(By.ID, 'api-description__related-apis')
        except:
            print("couldnot find related_apis")


        if 'related_apis' in locals():
            try:
                next_heading = related_apis.find_element(By.XPATH, "following-sibling::h2")
                next_id = next_heading.get_attribute('id')
                # print(next_id)

            except:
                print('no next heading after related_apis')
        

        if 'next_id' in locals():
            try:
                all_elements_in_rel_apis = api_desc.find_elements(By.XPATH, f'//*[preceding-sibling::h2[@id="api-description__related-apis"] and following-sibling::h2[@id="{next_id}"]]')
                print('all_elements_in_rel_apis: ', len(all_elements_in_rel_apis))

            except Exception as e:
                print("couldnot find any element in related-apis")

        else:
            try:
                all_elements_in_rel_apis = api_desc.find_elements(By.XPATH, f'//*[preceding-sibling::h2[@id="api-description__related-apis"]]')
                print('all_elements_in_rel_apis: ', len(all_elements_in_rel_apis))

            except Exception as e:
                print("couldnot find any element in related-apis")
        

        if 'all_elements_in_rel_apis' in locals():
            try:
                related_apis_links = []
                for element in all_elements_in_rel_apis:
                    related_apis_links += element.find_elements(By.TAG_NAME, 'a')

                print('related_apis_links: ', len(related_apis_links))
                
                rel_api_urls = [url.get_attribute('href') for url in related_apis_links]

                if rel_api_urls != []:
                    print('rel_api_urls: ',rel_api_urls)
                    api_entry[keys[19]] = ', '.join(rel_api_urls)

            except:
                print("couldnot find any url in related_apis")
    

    except:
        print("Error while scraping through this api page")

    

    return api_entry