from london import *

def test_first_page():
    listing_url = LondonAppDirectory.listing_url() + "0"
    page = requests.get(listing_url).text
    soup = BeautifulSoup(page)
    directory = LondonAppDirectory(soup)

    pp = pprint.PrettyPrinter(indent = 2)

    for url in directory.detail_urls():
        print url
        app = LondonAppDetail(url)
        pp.pprint(app.visit())

def scrape():
    t = TabWriter("sample/london.tab")
    t.write_headers()

    for page in range(0, LondonAppDirectory.num_pages()+1):
        listing_url = LondonAppDirectory.listing_url() + str(page)
        page = requests.get(listing_url).text
        soup = BeautifulSoup(page)
        directory = LondonAppDirectory(soup)
        for url in directory.detail_urls():
            print url
            app = LondonAppDetail(url)
            t.write_row(app)

scrape()