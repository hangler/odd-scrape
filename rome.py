from scrape_helper import *
import pprint
import time

class RomeAppDirectory(AbstractAppDirectory):

    @classmethod
    def listing_url(self):
        return "http://dati.comune.roma.it/applicazioni?page="

    @classmethod
    def detail_url_prefix(self):
        return "http://dati.comune.roma.it"

    @classmethod
    def full_url(self, url_fragment):
        return self.detail_url_prefix() + url_fragment

    @classmethod
    def num_pages(self):
        return 7

    def detail_urls(self):
        detail_pages = []
        for row in self.soup.find('ul', {'class': 'applicazioni'}).findAll('li'):
            detail_url = row.find('a').get('href')
            detail_pages.append(self.full_url(detail_url))
        return detail_pages

class RomeAppDetail(AbstractAppDetail):

    def app_detail_url(self):
        return self.page_url

    def g_title(self):
        return self.soup.find('h1', {'class': 'applicazioni'}).text.strip()

    def g_url(self):
        pass

    def g_summary(self):
        first_para = self.soup.find('div', {'class': 'testo'}).find('p')
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
        pass
    
    def g_source_code_url(self):
        pass
    
    def g_platforms(self):
        platforms = []
        for div in self.soup.find('div', {'class': 'info'}).findAll('div', {'class': 'sx'}):
            if "Device:" in div.text:
                all_devices = div.findNext('div').text
                for device in all_devices.split("/"):
                    if "web" in device:
                        platforms.append("Web")
            elif "Sistema Operativo:" in div.text:
                all_platforms = div.findNext('div').text
                for platform in all_platforms.split(","):
                    platform = platform.strip()
                    if ("iPhone" in platform or "iPad" in platform) and "iOS" not in platforms:
                        platforms.append("iOS")
        return platforms

    def g_technology(self):
        pass
    
    # Doesn't show information on the dev; just whether they're private or public
    def g_developers(self):
        for div in self.soup.find('div', {'class': 'info'}).findAll('div', {'class': 'sx'}):
            if "Produttore:" in div.text:
                return div.findNext('div').text.strip()
    
    # Doesn't show information on the data source; just the city that 
    def g_data_sources(self):
        pass