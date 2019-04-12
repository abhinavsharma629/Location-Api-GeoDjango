# GeoLocation

    GeoLocation contains Apis' for different Geolocation Mapping And Analysis purposes (eg:- Like google Maps Api's)

### Api Features!
- ###### Create Two APIs in flask : Get,Post.
    - Post : Post latitude,longitude of any location with pin code + address + city and you can     add new pin code in db. This api will be /post_location. Remember to check if pin code
        already exists or if there are existing latitude+longitude THAT ARE CLOSE ENOUGH TO BE THE SAME (dont assume that they will exactly be the same.)
        EndPoint:- **/post_location**
    
    - **Get** : There are two GET apis. Given a location, fetch all the nearby pin codes within a radius. For example, I can ask - give me all points within 5km radius
    of (45.12, 71.12) . To do this there are two methods implemented:-
        - **Mathematical computation of radius**. Endpoint:- **/get_using_self?query**

        - **Using postgres "earthdistance"** to compute all points in 5km radius.
              EndPoint:- **/get_using_postgres?query**
        - Test results between /get_using_postgres and  /get_using_self.
            - For testing results between /get_using_postgres and  /get_using_self another         EndPoint is created /compareSelfWithPostgres that compares the results of both self     and Postgres that were stored in the respective databases and gives the json         comparison.
            
    - **A Geojson is a json file which defines shapes of locations** - for example the shape of          delhi, gurgaon, etc. This geojson is used to define delhi and its areas.
        Parse this json, and load the boundaries latitude and longitude (geometry -> coordinates) into postgresql in a new table. you can use any structure. **Two Methods** Used For this:-
        
        - **Parsed The data from the Given geojson file** and stored the polygons geometry in the        database corresponding to the name of the location.
        
        -  **Used Open Street Map Api for getting the json data** scraped the data using beautiful        soup and loaded the polygon representation of the boundaries to the database.
    - In this API : given a latitude/longitude, it will tell you which place it falls within.
    **EndPoint:- /geoJsonParse**
    
-   ###### Written testcases (using the test framework in your language. using a test framework).


### Installation
    - Assumptions Made:- 
        - The very near locations for /post_Location end point are the ones lying within 1km of radius/range
        - map.geojson was provided for uploading for the last /latitude_longitude api.
    To upload data in database use postgres import method for uploading a large csv file.
    Then visit the /addPoint Url to store geometry representation of the data.
    Then use other end-points.
    To run the tests you have to first create a geospatial database with postgis extention enabled, and then run the tests.
