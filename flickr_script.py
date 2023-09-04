
from flickrapi import FlickrAPI
import urllib
from PIL import Image
import requests
import os
from dotenv.main import load_dotenv

load_dotenv()
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']


MODEL_NAME = os.environ['MODEL_NAME']



flickr = FlickrAPI(
    API_KEY,
    API_SECRET,
    format='parsed-json'
)

queries = [
    'dogs animal pet',
    'cats animal pet'
]
MAX_SIZE = 30000
DATASET_SIZE = 2000
MAX_PER_PAGE = 500


# All the extra data that I want to have
extras = 'description, license, date_upload, date_taken, owner_name, icon_server, original_format, last_update, geo, tags, machine_tags, o_dims, views, media, path_alias, url_sq, url_t, url_s, url_q, url_m, url_n, url_z, url_c, url_l, url_o'


def main():

    # search
    print('Queries: ', queries)
    for query in queries:
        total_pages = DATASET_SIZE / MAX_PER_PAGE
        current_page = 1
        while current_page <= total_pages:
            photos = flickr.photos.search(
                text=query,  # Search term
                per_page=MAX_PER_PAGE,  # Number of results per page #max = 500
                extras=extras,
                page=current_page,
                privacy_filter=1,  # public photos
                safe_search=1  # is safe
            )
            photos_array = photos['photos']['photo']
            # print(photos_array)
            download_photos(photos_array, query)
            current_page += 1


def download_photos(photos, query):
    # Download all photos
    i = 0
    if not os.path.exists('dataset_flickr/' + query):
        os.makedirs('dataset_flickr/' + query)

    for photo in photos:
        if 'url_c' in photo:
            print('Downloading image No: ', i, ' Query: ',
                  query, ' \nTags: ', photo['tags'] , 'Machine Tags: ', photo['machine_tags'])
            url = photo['url_c']
            urllib.request.urlretrieve(
                url, "dataset_flickr/" + query + '/' + photo['id'] + ".jpg")
            i += 1
        if i >= DATASET_SIZE:
            break


if __name__ == "__main__":
    main()
