from pymongo import MongoClient


class Mongo(object):
  
  @staticmethod
  def write_mongo(game):

    # Create the client
    client = MongoClient('localhost', 27017)

    # Connect to our database
    db = client['topgamer']

    # Fetch our series collection
    series_collection = db['games']

    data = {
      "Name": game.title,
      "Price": game.price,
      "Image": game.url_photo,
      "Description": game.description,
      "RealeaseDate": game.release_date,
      "Developer": game.developer,
      "Publisher": game.publisher,
      "OperatingSystem": game.operating_system,
      "VideoCard": game.graphics,
      "DiskSpace": game.memory,
      "Mark": game.rating,
      "SteamLink": game.url_steam
    }

    result = series_collection.insert_one(data).inserted_id