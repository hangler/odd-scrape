from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
import inspect
import requests

def xstr(s):
    if s is None:
        return ''
    return s

class Developer(object):

    def __init__(self, is_organization, name, country=None, email=None, homepage=None):
        self.is_organization = is_organization
        self.name = name
        self.country = country
        self.email = email
        self.homepage = homepage

    def __unicode__(self):
        return u"[%s, %s (%s, %s)]" % (self.name, self.country, self.email, self.homepage)


class DataSource(object):

    def __init__(self, name, country=None, url=None, organization=None, description=None):
        self.name = name
        self.country = country
        self.url = url
        self.organization = organization
        self.description = description

    def __unicode__(self):
        return u"[%s (%s, %s) %s]" % (self.name, xstr(self.organization), self.country, self.url)

class AbstractAppDirectory(object):
    __metaclass__ = ABCMeta

    def __init__(self, soup):
        self.soup = soup

    @abstractmethod
    def detail_urls(self):
        pass

    @abstractmethod
    def listing_url(self):
        pass

    @abstractmethod
    def num_pages(self):
        pass

class AbstractAppDetail(object):
    __metaclass__ = ABCMeta

    def __init__(self, page_url):
        self.page_url = page_url
        self.page = requests.get(page_url).text
        self.soup = BeautifulSoup(self.page)

    @classmethod
    def headers(self):
        headers = []
        for func in inspect.getmembers(self, predicate=inspect.ismethod):
            if "g_" in func[0]:
                function_name = func[0][2:] # Strip g_ prefix from function name
                headers.append(function_name)
        return "\t".join(headers) + "\n"

    def visit(self):
        values = {}
        for func in inspect.getmembers(self, predicate=inspect.ismethod):
            if "g_" in func[0]:
                function_name = func[0][2:] # Strip g_ prefix from function name
                values[function_name] = func[1]()
        #   if isinstance(attr_value, types.FunctionType):
        #        print attr_value
        return values

    def g_app_detail_url(self):
        return self.page_url

    @abstractmethod
    def g_title(self):
        pass

    @abstractmethod
    def g_url(self):
        pass

    @abstractmethod
    def g_summary(self):
        pass

    @abstractmethod
    def g_lang(self):
        pass

    @abstractmethod
    def g_country(self):
        pass

    @abstractmethod
    def g_created_for(self):
        pass

    @abstractmethod
    def g_source_code_url(self):
        pass
    
    @abstractmethod
    def g_platforms(self):
        pass

    @abstractmethod
    def g_technology(self):
        pass

    @abstractmethod
    def g_developers(self):
        pass

    @abstractmethod
    def g_data_sources(self):
        pass

class TabWriter(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, text, tab=True, mode="a"):
        f = open(self.file_name, mode)
        f.write(text.encode('utf-8'))
        f.close()

    def write_headers(self):
         self.write(AbstractAppDetail.headers(), tab=False, mode="w")

    def write_row(self, app_detail):
        row = ""
        if isinstance(app_detail, AbstractAppDetail):
            app_data = app_detail.visit()
            for k in sorted(app_data):
                value = app_data[k]
                if isinstance(value, list):
                    row = row + ", ".join(unicode(x) for x in value) + "\t"
                elif value is None:
                    row = row + "\t"
                else:
                    row = row + value.replace("\n", "") + "\t"
        row = row + "\n"
        self.write(row, tab=False)  
