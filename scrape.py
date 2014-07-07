from rome import *

def test_first_page():
    listing_url = RomeAppDirectory.listing_url() + "0"
    page = requests.get(listing_url).text
    soup = BeautifulSoup(page)
    directory = RomeAppDirectory(soup)

    pp = pprint.PrettyPrinter(indent = 2)

    """
    for app in directory.detail_urls(listing_url):
        pp.pprint(app.visit())
    """

    for url in directory.detail_urls():
        print url
        app = RomeAppDetail(url)
        pp.pprint(app.visit())

def scrape(start_page=0):
    t = TabWriter("output/rome.tab")
    t.write_headers()

    """
    for page in range(start_page, RomeAppDirectory.num_pages()+1):
        listing_url = RomeAppDirectory.listing_url() + str(page)
        page = requests.get(listing_url).text
        soup = BeautifulSoup(page)
        directory = RomeAppDirectory(soup)
        print listing_url
        for app in directory.detail_urls(listing_url):
            t.write_row(app)
    """

    for page in range(start_page, RomeAppDirectory.num_pages()+1):
        listing_url = RomeAppDirectory.listing_url() + str(page)
        page = requests.get(listing_url).text
        soup = BeautifulSoup(page)
        directory = RomeAppDirectory(soup)
        for url in directory.detail_urls():
            print url
            app = RomeAppDetail(url)
            t.write_row(app)

#test_first_page()
scrape()