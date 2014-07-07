from italy import *

def test_first_page():
    listing_url = ItalyAppDirectory.listing_url() + "0"
    page = requests.get(listing_url).text
    soup = BeautifulSoup(page)
    directory = ItalyAppDirectory(soup)

    pp = pprint.PrettyPrinter(indent = 2)

    """
    for app in directory.detail_urls(listing_url):
        pp.pprint(app.visit())
    """

    for url in directory.detail_urls():
        print url
        app = ItalyAppDetail(url)
        pp.pprint(app.visit())

def scrape(start_page=0):
    t = TabWriter("output/italy.tab")
    t.write_headers()

    """
    for page in range(start_page, ItalyAppDirectory.num_pages()+1):
        listing_url = ItalyAppDirectory.listing_url() + str(page)
        page = requests.get(listing_url).text
        soup = BeautifulSoup(page)
        directory = ItalyAppDirectory(soup)
        print listing_url
        for app in directory.detail_urls(listing_url):
            t.write_row(app)
    """

    for page in range(start_page, ItalyAppDirectory.num_pages()+1):
        listing_url = ItalyAppDirectory.listing_url() + str(page)
        page = requests.get(listing_url).text
        soup = BeautifulSoup(page)
        directory = ItalyAppDirectory(soup)
        for url in directory.detail_urls():
            print url
            app = ItalyAppDetail(url)
            t.write_row(app)

#test_first_page()
scrape()