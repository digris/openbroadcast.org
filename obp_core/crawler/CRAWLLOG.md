# Temporary Collecting Crawler Results / Stats


### Crawl for Track mb_id's


#### Stats before

 - Num. relations total:  
   `Relation.objects.all().nocache().count()`: 411880
   `Media.objects.filter(relations__service='musicbrainz').nocache().count()`: 80324
   
   
    # 15:45
    ./manage.py crawler_cli crawl_releases_for_media_mbid
    
    # 15:58
    Total mb ids added:    26413
    
    
Added 26'413 mb id's to tracks!!

 - Num. relations total:  
   `Relation.objects.all().count()`: 438713
   `Media.objects.filter(relations__service='musicbrainz').nocache().count()`: 107157




#### Stats afterwards

### Crawl for Metadata (Musicbrainz)

 - Num. relations total:  
   `Relation.objects.all().nocache().count()`: 438713
 - ISRC:  
   `Media.objects.exclude(Q(isrc__isnull=True) | Q(isrc='')).nocache().count()`: 20327
 - ISNI:  
   `Artist.objects.exclude(Q(isni_code__isnull=True) | Q(isni_code='')).nocache().count()`: 3669
 - IPI:  
   `Artist.objects.exclude(Q(ipi_code__isnull=True) | Q(ipi_code='')).nocache().count()`: 3648
      
    # 16:00 - 
    ./manage.py crawler_cli crawl_musicbrainz artist
    
    #Total updated objects:    1178
    #Total updated properties: 4943
    
    ./manage.py crawler_cli crawl_musicbrainz label
    
    #Total updated objects:    4751
    #Total updated properties: 5127
    
    ./manage.py crawler_cli crawl_musicbrainz release
    
    #Total updated objects:    678
    #Total updated properties: 819
    
    ./manage.py crawler_cli crawl_musicbrainz media
    
    #Total updated objects:    3147
    #Total updated properties: 3147
        

### Crawl for Metadata (discogs)
    
    ./manage.py crawler_cli crawl_discogs label


### Crawl for Artwork

 - Images:  
   `Artist.objects.exclude(Q(main_image__isnull=True) | Q(main_image='')).nocache().count()`: 32670  
   `Label.objects.exclude(Q(main_image__isnull=True) | Q(main_image='')).nocache().count()`: 6244  
   `Release.objects.exclude(Q(main_image__isnull=True) | Q(main_image='')).nocache().count()`: 20811 
   
    ./manage.py crawler_cli crawl_artwork artist
    # 32989
    
    ./manage.py crawler_cli crawl_artwork label
    # 6319


### Stats Summary


 - Summary:  
   `Relation.objects.all().nocache().count()`: 441748
   `Media.objects.filter(relations__service='musicbrainz').nocache().count()`: 107157
   `Media.objects.exclude(Q(isrc__isnull=True) | Q(isrc='')).nocache().count()`: 23474
   `Artist.objects.exclude(Q(isni_code__isnull=True) | Q(isni_code='')).nocache().count()`: 3669
   `Artist.objects.exclude(Q(ipi_code__isnull=True) | Q(ipi_code='')).nocache().count()`: 4225
   `Artist.objects.exclude(Q(main_image__isnull=True) | Q(main_image='')).nocache().count()`: 32989
   `Label.objects.exclude(Q(main_image__isnull=True) | Q(main_image='')).nocache().count()`: 6319
   `Release.objects.exclude(Q(main_image__isnull=True) | Q(main_image='')).nocache().count()`: 20815
