from scrape_helper import *
import pprint
import time

class ItalyAppDirectory(AbstractAppDirectory):

    @classmethod
    def listing_url(self):
        return "http://www.dati.gov.it/cerca/type/applicazione?solrsort=ds_created%20desc&page="

    @classmethod
    def num_pages(self):
        return 19

    def detail_urls(self):
        detail_pages = []
        for row in self.soup.find('ol', {'class': 'apachesolr_search-results'}).findAll('li'):
            detail_url = row.find('a').get('href')
            detail_pages.append(detail_url)
        return detail_pages

class ItalyAppDetail(AbstractAppDetail):

    def app_detail_url(self):
        return self.page_url

    def g_title(self):
        return self.soup.find('h1', {'class': 'title'}).text.strip()

    def g_url(self):
        all_links = self.soup.find('fieldset', {'class': 'group-link-applicazione'}).findAll('a')
        length = len(all_links)
        return (all_links[length - 1]).get('href').replace("\t", "")

    def g_summary(self):
        first_para = self.soup.find('div', {'class': 'field-name-body'}).find('p')
        summary = first_para.text
        for item in first_para.next_siblings:
            if item.name is None:
                summary = summary + "\n"
            elif item.get('class') is None:
                summary = summary + "\n" + item.text
            else:
                break
        return summary.replace("\t", "")
    
    def g_lang(self):
        return "IT"
    
    def g_country(self):
        return "Italy"
    
    def g_created_for(self):
        try:
            return self.soup.find('div', {'class': 'field-name-field-pa-produttrice'}).find('div', {'class': 'field-item'}).text
        except AttributeError:
            pass
    
    def g_source_code_url(self):
        pass
    
    def g_platforms(self):
        try:
            platforms = []
            for row in self.soup.find('div', {'class': 'field-name-field-tipo-applicazione'}).findAll('li'):
                platform = row.text.lower()
                if "android" in platform:
                    platforms.append("Android")
                if "iphone" in platform:
                    platforms.append("iOS")
                if "web" in platform:
                    platforms.append("Web")
                if "windows" in platform:
                    platforms.append("Windows Phone")
            return platforms
        except AttributeError:
            pass

    def g_technology(self):
        pass
    
    # Doesn't show information on the dev; just whether they're private or public
    def g_developers(self):
        pass
    
    # Doesn't show information on the data source; just the city that 
    def g_data_sources(self):
        pass