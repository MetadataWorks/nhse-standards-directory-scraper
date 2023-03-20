from selenium import webdriver
import time 
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
import chromedriver_autoinstaller


######   importing modules
from scraping_structures.scrape_structure1 import page_structure_1
from scraping_structures.scrape_structure2 import page_structure_2
from pyxl.pyxl import create_excel
from change_detection.detect_data_changes import compare_current_data_with_last_scraped_data, get_last_scraped_file



keys = ['Persistent ID', 'Title', 'Alternate name', 'Type', 'Abstract', 'Release date',
        'Effective from', 'Applies to', 'Impacts on', 'Conformance date', 'Contact Point', 'Keywords',
        'DoiName', 'Feedback', 'Alternate identifier', 'Description', 'Associated Media', 'Is Part Of',
        'References', 'Relation', 'Publisher Identifier', 'Publisher Name', 'Publisher Logo',
        'Publisher Description', 'Publisher Contact Point', 'Registration Status', 'Scope', 
        'Contributor', 'Sponsor', 'SRO', 'Business Lead', 'Technical committee', 'Approval Date',	
        'Mandate', 'Legal authority',' Endorsed by', 'License', 'Post implementation review date', 
        'Reviews', 'Data Status', 'Data Access']


absolute_keywords = ['community health', 'dentistry', 'hospital','a&e / emergency department', 
                        'inpatient', 'outpatient', 'mental health', 'patient-facing', 'pharmacy', 
                        'gp / primary care', 'transport / infrastructure', 'social care', 
                        'urgent and emergency care', 'ambulance services', 'nhs 111', 
                        'a&e / emergency department', 'ooh gp']




def scrape_apis():

    try:
        options = ChromeOptions()
        options.add_argument("--headless")
        print("INSTALLING DRIVER")
        chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                            # and if it doesn't exist, download it automatically,
                                            # then add chromedriver to path
        print("driver installed")

        driver = webdriver.Chrome(options = options)


        driver.get('https://digital.nhs.uk/developer/api-catalogue')
        time.sleep(2)
        print('site accessed')

        try:
            driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection').click()
            time.sleep(2)
            print('accpeted cookies')


        except:
            print("couldn't find accept cookies button")


        try:
            api_entries = driver.find_elements(By.CSS_SELECTOR,'div[data-api-catalogue-entry]')
            print(f"Found {len(api_entries)} api entries on the page")

        except:
            print("couldn't find api entries")
        

        if 'api_entries' in locals():
            api_data = []

            for api_num in range(0, len(api_entries)):

                print(f'scraping api # {api_num+1}')
                api_entry = {}
                api = api_entries[api_num]
                
                try:
                    api_heading = api.find_element(By.TAG_NAME, 'h2').find_element(By.TAG_NAME, 'a')
                except:
                    print('couldnot find api heading')
                
                try:
                    api_url = api_heading.get_attribute('href')
                    api_entry[keys[0]] = api_url
                except:
                    api_entry[keys[0]] = 'NA'
                
                try:
                    api_title = api_heading.text
                    api_entry[keys[1]] = api_title
                except:
                    api_entry[keys[1]] = "NA"
                

                try:
                    api_entry[keys[2]] = 'NA'
                    api_entry[keys[3]] = 'Technical standards and specifications'
                    api_entry[keys[4]] = 'NA'
                    api_entry[keys[5]] = 'NA'
                    api_entry[keys[6]] = 'NA'
                    

                    api_entry[keys[7]] = 'NA' 
                    keyword_tags = []
                    try:
                        keyword_tags = api.find_elements(By.CLASS_NAME, 'nhsd-a-tag--bg-light-grey')
                        keyword_tags = [keyword.text.strip() for keyword in keyword_tags]
                    except:
                        print(f"couldn't find keyword tags in this api entry ({api_title})")
                    

                    for tag in keyword_tags:
                        if tag.lower() in absolute_keywords:
                            api_entry[keys[7]] = tag
                            break


                    api_entry[keys[8]] = 'NA'
                    api_entry[keys[9]] = 'NA'


                    api_entry[keys[10]] = "api.management@nhs.net"

                    if api_title == "Care Connect FHIR API standards":
                        api_entry[keys[10]] = 'admin@interopen.org'

                    if api_title == "HL7 FHIR UK Core":
                        api_entry[keys[10]] = 'secretariat@hl7.org.uk'
                    

                    api_entry[keys[11]] = ', '.join(keyword_tags)
                    api_entry[keys[12]] = 'NA'
                    api_entry[keys[13]] = 'NA'
                    api_entry[keys[14]] = 'NA'


                    try:
                        api_entry[keys[15]] = api.find_element(By.TAG_NAME, 'p').text
                    except:
                        api_entry[keys[15]] = 'NA'
                    

                    status_tags = []
                    try:
                        span_tags = api.find_elements(By.TAG_NAME, 'span')
                    except:
                        print('couldnot find tag elements')
                    
                    if 'span_tags' in locals():
                        try:
                            for span in span_tags:
                                if 'nhsd-a-tag--bg-light-grey' not in span.get_attribute('class'):

                                    status = span.text

                                    if status.lower() in ['alpha', 'beta', 'draft']:
                                        status = 'IN DEVELOPMENT'
                                    elif status.lower() == 'in production':
                                        status = 'ACTIVE'

                                    status_tags.append(status)
                        except:
                            print('couldnot scrape status tags')
                    


                    print("####      Navigating to API page to scrape further sections       ####")
                    api_heading.click()
                    time.sleep(2)

                    try:
                        driver.find_element(By.ID, 'api-description')
                        structure_1 = False
                    except:
                        structure_1 = True

                    
                    if structure_1 == True:
                        print('page structure: 1')
                        api_entry = page_structure_1(driver, api_entry, keys)

                    else:
                        print('page structure: 2')
                        api_entry = page_structure_2(driver, api_entry, keys)


                    driver.back()
                    driver.refresh()
                    time.sleep(3)
                    print('back to homepage')


                    ####     defaults
                    api_entry[keys[20]] = 'https://ror.org/03am1eg44'
                    api_entry[keys[21]] = "NHS Digital"
                    api_entry[keys[22]] = 'https://nhs-prod.global.ssl.fastly.net/webfiles/1676894911965/images/nhs-digital-logo-social.jpg'
                    api_entry[keys[23]] = 'https://digital.nhs.uk/'
                    api_entry[keys[24]] = 'mailto:api.management@nhs.net'
                    

                    if api_title == "Care Connect FHIR API standards":
                        api_entry[keys[20]] = 'https://twitter.com/INTEROPenAPI'
                        api_entry[keys[21]] = 'INTEROPen'
                        api_entry[keys[22]] = 'https://pbs.twimg.com/profile_banners/731591066516885508/1498660571/1500x500'
                        api_entry[keys[23]] = 'https://twitter.com/INTEROPenAPI'
                        api_entry[keys[24]] = ' admin@interopen.org'
                    

                    elif api_title == "HL7 FHIR UK Core":
                        api_entry[keys[20]] = 'https://www.hl7.org.uk/'
                        api_entry[keys[21]] = 'HL7 UK'
                        api_entry[keys[22]] = 'https://www.hl7.org.uk/wp-content/uploads/HL7UK_Media/Images/Pale_red_hl7_logo_2019-25-percent-2.jpg'
                        api_entry[keys[23]] = 'https://www.hl7.org.uk/register/about-hl7-uk/hl7-uk/'
                        api_entry[keys[24]] = 'mailto:secretariat@hl7.org.uk'
                    


                    api_entry[keys[25]] = 'NA'
                    
                    if status_tags != []:
                        api_entry[keys[25]] = ', '.join(status_tags)
                

                    
                    ## setting NA from field#26 to field#38
                    for i in range(26, 39):
                        api_entry[keys[i]] = 'NA'
                    
                    api_entry[keys[39]] = 'None'   #### template has None in field 40


                    if 'api_url' in locals():
                        api_entry[keys[40]] = api_url
                    else:
                        api_entry[keys[40]] = 'NA'
                    

                    api_data.append(api_entry)
                    # print(api_data)
                    print(f"scraped the api named {api_entry['Title']}")

                except Exception as e:
                    print(e)
                    print(f'couldnot scrape this api ({api_title})')
                

                print('#####   refreshing api entries    ######')
                api_entries = driver.find_elements(By.CSS_SELECTOR,'div[data-api-catalogue-entry]')
                

                # if api_num==1:
                #     break


        driver.quit()

        
        print("#####      writing data into excel    ######")

        if 'api_data' in locals():
            if api_data != []:
                try:
                    ## first getting the last saved file cause the current file is going to be created in the next line
                    last_scraped_data_file = get_last_scraped_file()

                    data_file, current_comparison_file = create_excel(api_data, keys)
                    print('successfully saved APIs data at: ', data_file)

                    print('last_scraped_data_file: ', last_scraped_data_file)
                    print('current_scraped_data_file: ', current_comparison_file)

                    try:
                        compare_current_data_with_last_scraped_data(current_comparison_file, last_scraped_data_file)

                    except Exception as e:
                        print(e)
                        print('Error occurred while comparing last scraped and current data')

                
                except Exception as e:
                    print(e)
                    print('error while writing data into excel/csv file')

    except:
        print('something went wrong')




print('########        CALLING API SCRAPER           #########')

scrape_apis()

