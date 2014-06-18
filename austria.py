from scrape_helper import *
import pprint
import time

class AustriaAppDirectory(AbstractAppDirectory):

    @classmethod
    def listing_url(self):
        return "http://www.data.gv.at/anwendungen/page/"

    @classmethod
    def num_pages(self):
        return 25

    def detail_urls(self):
        detail_pages = []
        for row in self.soup.find('ul', {'class': 'entryAnwendungen'}).findAll('li'):
            detail_url = row.find('a').get('href')
            detail_pages.append(detail_url)
        return detail_pages

class AustriaAppDetail(AbstractAppDetail):

    def app_detail_url(self):
        return self.page_url

    def g_title(self):
        return self.soup.find('h1', {'class': 'nomargin'}).find('span').text

    def g_url(self):
        return self.soup.find('a', {'class': 'buttonBlue'}).get('href')

    def g_summary(self):
        first_para = self.soup.find('div', {'class': 'contentText'}).find('p')
        summary = first_para.text
        for item in first_para.next_siblings:
            if item.name is None:
                summary = summary + "\n"
            elif item.get('class') is None:
                summary = summary + "\n" + item.text
            else:
                break
        return summary
    
    def g_lang(self):
        return "DE"
    
    def g_country(self):
        return "Austria"
    
    def g_created_for(self):
        pass
    
    def g_source_code_url(self):
        pass
    
    def g_platforms(self):
        platforms = []
        for h3 in self.soup.find('div', {'id': 'contentSidebar'}).findAll('h3'):
            if "Systeme" in h3.text:
                for item in h3.next_siblings:
                    if item.name is not None and 'p' in item.name:
                        for link in item.findAll('a'):
                            index = link.get('href').find("applicationsystem") + len("applicationsystem=")
                            platform = link.get('href')[index:]
                            if "android" in platform:
                                platforms.append("Android")
                            if "ios" in platform:
                                platforms.append("iOS")
                            if "browser" in platform:
                                platforms.append("Web")
                            if "windows" in platform:
                                platforms.append("Windows Phone")
                        break
        return platforms

    def g_technology(self):
        pass
    
    def g_developers(self):
        developers = []

        developer = None
        
        name = None
        email = None
        homepage = None

        for h3 in self.soup.find('div', {'id': 'contentSidebar'}).findAll('h3'):
            if "Kontakt" in h3.text:
                for item in h3.next_siblings:
                    if len(item) > 1:
                        if item.name is not None and 'p' in item.name:
                            email_at_index = item.text.find("@")
                            if email_at_index:
                                email_begin_index = item.text.rfind(" ", 0, email_at_index) + 1
                                email_end_index = item.text.find(" ", email_at_index)
                                email = item.text[email_begin_index:email_end_index].strip()
                            link = item.find('a')
                            if link:
                                homepage = link.get('href')
                        else:
                            if not name:
                                name = item.strip()

        if name:
            developer = Developer(is_organization=False, name=name, country="Austria", email=email, homepage=homepage)

        developers.append(developer)
        return developers
    
    def g_data_sources(self):
        data_sources = []

        if self.soup.find('table'):
            for row in self.soup.find('table').findAll('tr'):
                link = row.find('a')
                if link:
                    url = link.get('href')
                    link_text = link.text
                    index_of_first_parenthesis = link_text.find("(")
                    name = link_text[:index_of_first_parenthesis]
                    source = link_text[index_of_first_parenthesis+1:-1]
                    data_source = DataSource(name, country=self.g_country(), url=url, organization=source)
                    data_sources.append(data_source)
        
        return data_sources