from datagov import *

def test_first_page():
    listing_url = DataGovAppDirectory.listing_url() + "1"
    page = requests.get(listing_url).text
    soup = BeautifulSoup(page)
    directory = DataGovAppDirectory(soup)

    pp = pprint.PrettyPrinter(indent = 2)

    for app in directory.details(listing_url):
        pp.pprint(app.visit())

    """
    for url in directory.detail_urls():
        print url
        app = DataGovAppDetail(url)
        pp.pprint(app.visit())
    """

def scrape(start_page=1):
    t = TabWriter("output/datagov.tab")
    t.write_headers()

    for page in range(start_page, DataGovAppDirectory.num_pages()+1):
        listing_url = DataGovAppDirectory.listing_url() + str(page)
        page = requests.get(listing_url).text
        soup = BeautifulSoup(page)
        directory = DataGovAppDirectory(soup)
        print listing_url
        for app in directory.details(listing_url):
            t.write_row(app)

    """
    for page in range(start_page, DataGovAppDirectory.num_pages()+1):
        listing_url = DataGovAppDirectory.listing_url() + str(page)
        page = requests.get(listing_url).text
        soup = BeautifulSoup(page)
        directory = DataGovAppDirectory(soup)
        for url in directory.detail_urls():
            print url
            app = DataGovAppDetail(url)
            t.write_row(app)
    """

#test_first_page()
scrape()