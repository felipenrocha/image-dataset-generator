
from flickrapi import FlickrAPI
import urllib
from PIL import Image
import requests
import os
import sys
import csv

from dotenv.main import load_dotenv
import math
from query_reader import Queries
import threading
import argparse

load_dotenv()
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
MODEL_NAME = os.environ['MODEL_NAME']
DATASET_SIZE = int(os.environ['DATASET_SIZE'])
BASE_PATH = os.getcwd() + '\\'

DATASET_PATH = BASE_PATH + 'dataset_flickr/'





flickr = FlickrAPI(
    API_KEY,
    API_SECRET,
    format='parsed-json'
)


MAX_PER_PAGE = 500  # max images per flickr request


class FlickrScript:
    # class that manages the flickr api queries
    def __init__(self,  extras='description, license, date_upload, date_taken, owner_name, icon_server, original_format, last_update, geo, tags, machine_tags, o_dims, views, media, path_alias, url_sq, url_t, url_s, url_q, url_m, url_n, url_z, url_c, url_l, url_o'):
        self.queries = Queries()  # queries list
        self.extras = extras     # All the extra data that I want to have
        self.threads = []    # threds list
        self.geotag = False
        if  sys.argv[1] == '-g': # get geotag option
            self.geotag = True 
            print(f'Geotag Option: {self.geotag}\nAdditional metadata containing the latitude and longitude of each photo will be saved.')
        else:
            print(f'Geotag Option: {self.geotag}\n')


    def download(self):
                
        #threading to download each class simultaneously
        for query in self.queries.getQueries():
            self.threads.append(threading.Thread(
                target=self.downloadPhotos, args=(query,)))
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()



    def downloadPhotos(self, query):
        total_downloaded = 0
        current_page = 1
        final_page = 1
        self.unwanted_tags = query['unwanted_tags']

        while (total_downloaded < DATASET_SIZE) and (current_page <= final_page):

            photos = flickr.photos.search(
                text=query['name'],  # Search term
                per_page=MAX_PER_PAGE,  # Number of results per page #max = 500
                extras=self.extras,
                page=current_page,
                privacy_filter=1,  # public photos
                safe_search=1  # is safe
            )
            total_results = photos['photos']['total']
            photos = photos['photos']['photo']
            final_page = math.ceil(total_results / MAX_PER_PAGE)
            self.downloadPage(photos, query, total_downloaded)
            current_page += 1

    def downloadPage(self, photos, query, total_downloaded):
        # Download all photos from photos list


        # create dataset folder
        if not os.path.exists(DATASET_PATH + query['name']):
            os.makedirs(DATASET_PATH + query['name'])

        #loop through photos 
        for photo in photos:
            # check if theres an available url to be downloaded and check if theres any unwanted tags in photo
            if ('url_c' in photo) and not self.checkUnwantedTags(photo) and (total_downloaded < DATASET_SIZE):
                
                print('Downloading image No: ', total_downloaded, ' Dataset Size: ',  DATASET_SIZE,
                      '\n Query: ', query['name'], 'Tags: ', photo['tags'])
                
                
                url = photo['url_c'] # get url to download]

                # check if file already exists: (remove repetitions)
                if (photo['id'] + '.jpg') not in os.listdir(DATASET_PATH + query['name'] + '/'):
                    urllib.request.urlretrieve(
                        url, DATASET_PATH + query['name'] + '/' + photo['id'] + ".jpg")  # download image and save it to folder 
                    total_downloaded += 1
                    self.addMetadata(photo, query['name'])  # if geotag option -> also add to the csv file  the lat and lng of the image.
                    
                               
                               
                               

    def addMetadata(self, photo, name): # void to add to metadata file
        # the csv file will have 3 columns: id_of_image.jpg, lat, lng (more data can be added later with this method)

        if self.geotag: # TODO: add information based on CLIP model of image (cleaning data).
            if not os.path.isfile(DATASET_PATH + '/' + name + '/' + 'metadata' + '.csv' ): # check if file csv exists
                 # create file
                with open(DATASET_PATH + '/' + name + '/' + 'metadata' + '.csv' , 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)  # Create a CSV writer object
                    header_row = ['id', 'lat', 'lng']
                    csv_writer.writerow(header_row)

            # Use 'a' mode to open the file for appending
            with open(DATASET_PATH + '/' + name + '/' + 'metadata' + '.csv', 'a', newline='') as csvfile:
                # Create a CSV writer object
                csv_writer = csv.writer(csvfile)
                row = [photo['id']+'.jpg', photo['latitude'], photo['longitude']]
                # Write the data to the CSV file
                csv_writer.writerow(row)
    def checkUnwantedTags(self, photo):
        # checks if photo has any of the unwanted tags in its metadata
        # return true if it has unwanted tags

        #check if geotag option is true
        if self.geotag:

            # geotag option:
            if 'latitude' in photo and 'longitude' in photo:

                # the photo has geotag information:
                lat = photo['latitude']
                lng = photo['longitude']
                # check if its diff then 0
                if lat == 0 and lng == 0:
                    return True
                return False
            else:
                return True


        for tag in self.unwanted_tags:
            if tag in photo['tags']:
                return True
        return False


def main():

    flickr_script = FlickrScript()
    flickr_script.download()


if __name__ == "__main__":
    main()
