from scrape_helper import *
import pprint
import time

class DataGovAppDirectory(AbstractAppDirectory):

    @classmethod
    def listing_url(self):
        return "http://www.data.gov/applications?q=&currentpage="

    @classmethod
    def detail_url_prefix(self):
        return "http://data.london.gov.uk"

    @classmethod
    def full_url(self, url_fragment):
        return self.detail_url_prefix() + url_fragment

    @classmethod
    def num_pages(self):
        return 35

    def detail_urls(self):
        pass

    def details(self, page_url):
        details = []
        for row in self.soup.find('div', {'class': 'Mobile-post'}).findAll('div', {'class': 'webcontainer'}):
            title = row.find('h2').text.strip()
            url = row.find('a').get('href')
            summary = row.find('div', {'class': 'content'}).text.strip()
            detail = DataGovAppDetail(page_url, title, url, summary)
            details.append(detail)
        return details

class DataGovAppDetail(AbstractAppDetail):

    def __init__(self, page_url, title, url, summary):
        self.page_url = page_url
        self.title = title
        self.url = url
        self.summary = summary

    def g_title(self):
        return self.title

    def g_url(self):
        return self.url

    def g_summary(self):
        return self.summary
    
    def g_lang(self):
        return "EN"
    
    def g_country(self):
        return "United States"
    
    def g_created_for(self):
        pass
    
    def g_source_code_url(self):
        pass
    
    def g_platforms(self):
        pass

    def g_technology(self):
        pass
    
    def g_developers(self):
        pass
    
    def g_data_sources(self):
        pass