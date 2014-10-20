
from south.db import db
from cms.plugins.link.models import *

class Migration:
    
    def forwards(self, orm):
        db.rename_column('link_link', 'link', 'url')
    
    
    def backwards(self, orm):
        db.rename_column('link_link', 'url', 'link')
    
  
