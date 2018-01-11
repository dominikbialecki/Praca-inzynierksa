from beets.plugins import BeetsPlugin
from beets.ui import Subcommand
from beets.library import  Item
import beets.mediafile as mediafile
class FooPlugin(BeetsPlugin):
    def __init__(self):
        field = mediafile.MediaField(
        mediafile.MP3DescStorageStyle(u'foo'),
        mediafile.StorageStyle(u'foo')
        )
        self.add_media_field('foo', field)
        
        
FooPlugin()
item = Item.from_path('~/Dokumenty/music/music_l/Jula/Na Krawedzi/01 Tylko Ty.mp3')
item['foo'] == 'ham'
item.write()
    
