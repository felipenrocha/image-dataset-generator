## Image Classifier Dataset Generator

Framework that generates a set of images based on the queries.txt file,
each query is considered a class that will be used to generate a model later.


### Usage:
#### Using the donwload Module


You can write the queries to be searched in flickr and bing in 'queries.txt',
each line thats starts with + is a class and query to be searched in the databases.


For example, if we wanted to search a database of pictures of cats we could
write something like this:

    + (cats animal pet cat) -(people photographer family dog dogs mouse fox rat mice rabbit bunny guinea-pig guineapig wolf squirrel monkey woman women men man) 

The text after the bullet '-' is a list of all unwanted tags for each query.

After writing your queries, you need to add a Flickr API key in the .env
file that you can get in https://www.flickr.com/services/api/, alongside the API_KEY you need to change your model name, and the size of the dataset for each class.

Lastly, you need to download the libraries. From the root project in your python environment run:

            
            $ pip install -r requirements.txt

            

To run the download scripts run the 'script' file:

         
            $  python src/download/flickr_script.py 
            $  python src/download/bing_script.py

        

Done! You're now downloading the images and can generate a dataset for an Image Classifier with ease.


You can also activate the geotag mode by passing the -g argument  while running the flickr script (only available for flickr script) this option will add additional data for each photo, its latitude and longitude:

            $  python src/download/flickr_script.py -g




#### TODO:
- [x] Documentação Readme Download
- [x] Tags Indesejadas retiradas
- [x] Implementação Leitura queries.txt
- [x] Threading download Flickr
- [ ] Implementação modo geotags (recolher lat, lng => salvar pais em csv (sera utilizado dps no modelo))
- [ ] Interface de utilização
