# NHS_digital_scraper


## Clone the repository
##### git clone https://github.com/tezeract-ai/NHS_digital_scraper.git


## Set up the Python Environment
Create a conda environment and install the requirements.txt file. Open the terminal inside your cloned folder
##### conda create -n nhs_env python==3.9.16
##### conda activate nhs_env
##### pip install -r requirements.txt


## Run the NHS Digital API Scraper
Inside the terminal, run the following command at the cloned directory
##### python api_scraper.py


## Data format and directory
NHS digital scraper will scrape the APIs data from https://digital.nhs.uk/developer/api-catalogue.
It will save all the scraped data in xlsx and csv format.
You can find these files inside a folder named scraped_data.
