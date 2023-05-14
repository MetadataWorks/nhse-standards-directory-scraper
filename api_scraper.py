from selenium import webdriver
import time 
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions


######   importing modules
from scraping_structures.scrape_structure1 import page_structure_1
from scraping_structures.scrape_structure2 import page_structure_2
from pyxl.pyxl import create_excel
from change_detection.detect_data_changes import compare_current_data_with_last_scraped_data, get_last_scraped_file


''' this is the previous order of keys '''
# keys = ['Persistent ID', 'Title', 'Alternate name', 'Type', 'Abstract', 'Release date',
#         'Effective from', 'Applies to', 'Impacts on', 'Conformance date', 'Contact Point', 'Keywords',
#         'DoiName', 'Feedback', 'Alternate identifier', 'Description', 'Associated Media', 'Is Part Of',
#         'References', 'Relation', 'Publisher Identifier', 'Publisher Name', 'Publisher Logo',
#         'Publisher Description', 'Publisher Contact Point', 'Registration Status', 'Scope', 
#         'Contributor', 'Sponsor', 'SRO', 'Business Lead', 'Technical committee', 'Approval Date',	
#         'Mandate', 'Legal authority',' Endorsed by', 'License', 'Post implementation review date', 
#         'Reviews', 'Data Status', 'Data Access']


absolute_keywords = ['community health', 'dentistry', 'hospital','a&e / emergency department', 
                        'inpatient', 'outpatient', 'mental health', 'patient-facing', 'pharmacy', 
                        'gp / primary care', 'transport / infrastructure', 'social care', 
                        'urgent and emergency care', 'ambulance services', 'nhs 111', 
                        'a&e / emergency department', 'ooh gp']




def scrape_apis():

    try:
        options = ChromeOptions()
        options.add_argument("--headless")

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.maximize_window()

        driver.get('https://digital.nhs.uk/developer/api-catalogue')
        time.sleep(2)
        print('site accessed')

        try:
            driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection').click()
            time.sleep(2)
            print('accepted cookies')

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
                    api_entry['Persistent ID'] = api_url
                except:
                    api_entry['Persistent ID'] = 'NA'
                
                try:
                    api_title = api_heading.text
                    api_entry['Title'] = api_title
                except:
                    api_entry['Title'] = "NA"
                

                try:
                    api_entry['Type'] = 'Technical_standards_and_specifications'
                    api_entry['Abstract'] = 'NA'


                    api_entry['Contact Point'] = "api.management@nhs.net"

                    if api_title == "Care Connect FHIR API standards":
                        api_entry['Contact Point'] = 'admin@interopen.org'

                    if api_title == "HL7 FHIR UK Core":
                        api_entry['Contact Point'] = 'secretariat@hl7.org.uk'
                    

                    keyword_tags = []
                    try:
                        keyword_tags = api.find_elements(By.CLASS_NAME, 'nhsd-a-tag--bg-light-grey')
                        keyword_tags = [keyword.text.strip() for keyword in keyword_tags]
                    except:
                        print(f"couldn't find keyword tags in this api entry ({api_title})")
                    
                    api_entry['Keywords'] = ', '.join(keyword_tags)


                    api_entry['Release date'] = 'NA'
                    api_entry['Effective from'] = 'NA'
                    

                    api_entry['Applies to'] = 'NA' 
                    for tag in keyword_tags:
                        if tag.lower() in absolute_keywords:
                            api_entry['Applies to'] = tag
                            break


                    api_entry['Impacts on'] = 'NA'
                    api_entry['Conformance date'] = 'NA'

                    api_entry['DoiName'] = 'NA'
                    api_entry['Alternate name'] = 'NA'


                    # api_entry['Feedback'] = 'NA'
                    # api_entry['Alternate identifier'] = 'NA'


                    try:
                        api_entry['Description'] = api.find_element(By.TAG_NAME, 'p').text
                    except:
                        api_entry['Description'] = 'NA'
                    

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
                        api_entry = page_structure_1(driver, api_entry)

                    else:
                        print('page structure: 2')
                        api_entry = page_structure_2(driver, api_entry)


                    driver.back()
                    driver.refresh()
                    time.sleep(1)
                    print('back to homepage')


                    ####     defaults
                    api_entry['Publisher Identifier'] = 'https://ror.org/03am1eg44'
                    api_entry['Publisher Name'] = "NHS Digital"
                    api_entry['Publisher Description'] = 'https://digital.nhs.uk/'
                    api_entry['Publisher Contact Point'] = 'api.management@nhs.net'
                    api_entry['Publisher Logo'] = 'https://nhs-prod.global.ssl.fastly.net/webfiles/1676894911965/images/nhs-digital-logo-social.jpg'
                    
                    
                    if api_title == "Care Connect FHIR API standards":
                        api_entry['Publisher Identifier'] = 'https://twitter.com/INTEROPenAPI'
                        api_entry['Publisher Name'] = 'INTEROPen'
                        api_entry['Publisher Description'] = 'https://twitter.com/INTEROPenAPI'
                        api_entry['Publisher Contact Point'] = 'admin@interopen.org'
                        api_entry['Publisher Logo'] = 'https://pbs.twimg.com/profile_banners/731591066516885508/1498660571/1500x500'
                        

                    elif api_title == "HL7 FHIR UK Core":
                        api_entry['Publisher Identifier'] = 'https://www.hl7.org.uk/'
                        api_entry['Publisher Name'] = 'HL7 UK'
                        api_entry['Publisher Description'] = 'https://www.hl7.org.uk/register/about-hl7-uk/hl7-uk/'
                        api_entry['Publisher Contact Point'] = 'secretariat@hl7.org.uk'
                        api_entry['Publisher Logo'] = 'https://www.hl7.org.uk/wp-content/uploads/HL7UK_Media/Images/Pale_red_hl7_logo_2019-25-percent-2.jpg'
                        

                    
                    ## setting NA from field#26 to field#38
                    for i in ['Scope', 'Contributor', 'Sponsor', 'SRO', 'Business Lead', 'Technical committee', 
                              'Approval Date', 'Post implementation review date']:
                        
                        api_entry[i] = 'NA'
                    

                    api_entry['Registration Status'] = 'NA'
                    
                    if status_tags != []:
                        api_entry['Registration Status'] = ', '.join(status_tags)
                

                    for i in ['Registration authority', 'Status', 'Mandated', 'Trusted by', 'Reviews', 'Legal authority']:

                        api_entry[i] = 'NA'
                        


                    api_entry['Data Status'] = 'External'   #### template has None in field 40


                    if 'api_url' in locals():
                        api_entry['Data Access'] = api_url
                    else:
                        api_entry['Data Access'] = 'NA'
                    

                    api_data.append(api_entry)
                    # print(api_data)
                    print(f"scraped the api named {api_entry['Title']}")

                except Exception as e:
                    print(e)
                    print(f'couldnot scrape this api ({api_title})')
                

                print('#####   refreshing api entries    ######')
                api_entries = driver.find_elements(By.CSS_SELECTOR,'div[data-api-catalogue-entry]')
                

                # if api_num==2:
                #     break


        driver.quit()

        
        print("#####      writing data into excel    ######")

        if 'api_data' in locals():
            if api_data != []:
                try:
                    ## first getting the last saved file cause the current file is going to be created in the next line
                    last_scraped_data_file = get_last_scraped_file()

                    data_file, current_comparison_file = create_excel(api_data)
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

