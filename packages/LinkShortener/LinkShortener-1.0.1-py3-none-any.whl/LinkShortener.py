from multipledispatch import dispatch
from bs4 import BeautifulSoup
import requests
import sys

baseurl = "https://tinyurl.com/create.php?source=indexpage&url="

"""LinkShortener will automatically shorten links thanks to tinyurl.com. 
    You can also make links with custom aliases."""


@dispatch(str)
def shorten(url):
    source = requests.get(baseurl + url).text
    soup = BeautifulSoup(source, features="html.parser")
    try:
        shortened_link = soup.find("a", {"id": "copy_div"})
        return shortened_link["href"]

    except TypeError:
        print("URL invalid or alias not available")
        exit(1)


@dispatch(str, str)
def shorten(url, alias):
    source = requests.get(baseurl + url + "&alias=" + alias).text
    soup = BeautifulSoup(source, features="html.parser")
    try:
        shortened_link = soup.find("a", {"id": "copy_div"})
        return shortened_link["href"]

    except TypeError:
        print("URL invalid / Alias not available")
        exit(1)


if __name__ == '__main__':
    try:
        print(shorten(str(sys.argv[1]), str(sys.argv[2])))

    except IndexError:
        try:
            print(shorten((str(sys.argv[1]))))
        except IndexError:
            print("Not enough arguments specified... exiting")
            exit(1)
