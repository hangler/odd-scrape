from scrape_helper import *
import pprint
import time

class LondonAppDirectory(AbstractAppDirectory):

    @classmethod
    def listing_url(self):
        return "http://data.london.gov.uk/datastore/inspirational-uses?page="

    @classmethod
    def detail_url_prefix(self):
        return "http://data.london.gov.uk"

    @classmethod
    def full_url(self, url_fragment):
        return self.detail_url_prefix() + url_fragment

    @classmethod
    def num_pages(self):
        return 17

    def detail_urls(self):
        detail_pages = []
        for row in self.soup.find('div', {'class': 'view-latest-apps'}).findAll('div', {'class': 'node'}):
            detail_url = row.find('h2').find('a').get('href')
            detail_pages.append(self.full_url(detail_url))
        return detail_pages

class LondonAppDetail(AbstractAppDetail):

    def g_title(self):
        return self.soup.find('div', {'class': 'contentarea'}).find('h1').text

    def g_url(self):
        try:
            return self.soup.find('div', {'class': 'content'}).find('a').get('href')
        except:
            pass

    def g_summary(self):
        first_para = self.soup.find('div', {'class': 'content'}).find('p')
        summary = first_para.text
        for item in first_para.next_siblings:
            if item.name is None:
                summary = summary + "\n"
            elif item.name is 'p':
                if item.text.startswith("Packages"):
                    break
                else:
                    summary = summary + "\n" + item.text
        return summary
    
    def g_lang(self):
        return "EN"
    
    def g_country(self):
        return "United Kingdom"
    
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
        data_sources = []

        if self.soup.find('div', {'class': 'content'}).find('ul'):
            for row in self.soup.find('div', {'class': 'content'}).find('ul').findAll('li'):
                link = row.find('a')
                if link:
                    url = LondonAppDirectory.full_url(link.get('href'))
                    name = link.text
                    data_source = DataSource(name, country=self.g_country(), url=url)
                    data_sources.append(data_source)
        
        return data_sources