class Game(object):

  def __init__(self, title='', price=0.0, url_photo='', genre='', description='', release_date='',
               developer='', publisher='', operating_system='', processor=[], memory='', graphics=[],
               storage='', language=[], rating=0, url_steam=''):
    self.title = title
    self.price = price
    self.url_photo = url_photo
    self.genre = genre
    self.description = description
    self.release_date = release_date
    self.developer = developer
    self.publisher = publisher
    self.operating_system = operating_system
    self.processor = processor
    self.memory = memory
    self.graphics = graphics
    self.storage = storage
    self.language = language
    self.rating = rating
    self.url_steam = url_steam



  def __str__(self):
    pass
