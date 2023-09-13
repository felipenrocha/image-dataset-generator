
import concurrent.futures
from bing_image_downloader import downloader
import threading
import os
from dotenv.main import load_dotenv
from query_reader import Queries
load_dotenv()

MODEL_NAME = os.environ['MODEL_NAME']
DATASET_SIZE = int(os.environ['DATASET_SIZE'])
# bing usually stops to download images after 200-300 downloads so it can take ages if the dataset is bigger (i changed to less)
# it also uses threading, all queries are being downloaded at the sime time so you can just ctrl c if its taking too much time;


queries = Queries().getQueries()


threads = list()


class BingScript:
    # instance attribute
    def __init__(self, queries):
        self.queries = queries
        self.threads = []

    def run(self):
        for query in queries:
            self.threads.append(threading.Thread(
                target=self.download, args=(query['name'],)))     
        print(self.threads)     
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()

    def download(self, query):
        if not os.path.exists('dataset_bing'):
            os.makedirs('dataset_bing')
        downloader.download(query, limit=DATASET_SIZE,  output_dir='dataset_bing',
                            adult_filter_off=True, force_replace=False, timeout=60)

# threading


def main():
    bing_script = BingScript(queries)
    bing_script.run()

if __name__ == "__main__":
    main()
