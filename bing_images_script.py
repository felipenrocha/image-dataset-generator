
import concurrent.futures
from bing_image_downloader import downloader
import threading



# queries = [
#     "brazil tourism city daystreets (NOT face) (NOT flag) (NOT map) (NOT logo) ((distrito federal) or bahia or (rio de janeiro) or (sao paulo) or (minas gerais))  ground-level photo",
#     "japan tourism city day streets (NOT face) (NOT flag) (NOT map) (NOT logo) (tokyo or Yokohama or Kyoto or Osaka) ground-level photo",
#     "france tourism city day streets buildings (NOT face) (NOT flag) (NOT map) (NOT logo) ground-level photo buildings",
#     "(united kingdom) day tourism city streets buildings(NOT face) (NOT flag) (NOT map) (NOT logo) ground-level photo buildings",
#     "(united states) day tourism city streets buildings(NOT face) (NOT flag) (NOT map) (NOT logo) ground-level photo buildings",
#     "germany tourism city streets buildings(NOT face) (NOT flag) (NOT map) (NOT logo) ground-level photo buildings",
#     "(south korea) tourism city streets buildings(NOT face) (NOT flag) (NOT map) (NOT logo) ground-level photo buildings",
#     "chile tourism city streets buildings(NOT face) (NOT flag) (NOT map) (NOT logo) ground-level photo buildings",
#     "argentina tourism city streets buildings(NOT face) (NOT flag) (NOT map) (NOT logo) ground-level photo buildings"

# ]


queries = [

    '(photo of dog) dog',
    '(photo of cat) cat'
]


DATASET_SIZE = 300

threads = list()


def download(query, index):
    print("Thread:", index, "Dowloading")
    downloader.download(query, limit=DATASET_SIZE,  output_dir='dataset_bing',
                        adult_filter_off=True, force_replace=False, timeout=60)

# threading

def main():
    i = 0
    t1 = threading.Thread(target=download, args=(queries[0], 1,))
    t2 = threading.Thread(target=download, args=(queries[1], 2,))
    # t3 = threading.Thread(target=download, args=(queries[2], 2,))
    # t4 = threading.Thread(target=download, args=(queries[3], 2,))
    # t5 = threading.Thread(target=download, args=(queries[4], 2,))
    # t6 = threading.Thread(target=download, args=(queries[5], 2,))
    # t7 = threading.Thread(target=download, args=(queries[6], 2,))
    # t8 = threading.Thread(target=download, args=(queries[7], 2,))
    # t9 = threading.Thread(target=download, args=(queries[8], 2,))

    t1.start()
    t2.start()
    # t3.start()
    # t4.start()
    # t5.start()
    # t6.start()
    # t7.start()
    # t8.start()
    # t9.start()

    t1.join()
    t2.join()
    # t3.join()
    # t4.join()
    # t5.join()
    # t6.join()
    # t7.join()
    # t8.join()
    # t9.join()

    # both threads completely execute
    print("Done!")


if __name__ == "__main__":
    main()
