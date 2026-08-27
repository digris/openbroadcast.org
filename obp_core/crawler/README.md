# crawler APP

provides functionality for data completion (e.g. via musicbrainz service)


## Workflows

### Acquire as many unique identifiers as possible

The primary identifier used on OBP is the respective Musicbrainz ID `mb_id`.
Having an `mb_id` assigned allows us to crawl for additional data.

#### Crawl for Track mb_id's

We have the situation that often *Releases* have an `mb_id` assigned (through manual editing process
or when assigned during import) - but not the containing *Tracks*.

    # usage
    ./manage.py crawler_cli crawl_releases_for_media_mbid


 - this command selets all *Releases* **with** a `mb_id` containing *Tracks* **without** `mb_id`.
 - then data from Musicbrainz is loaded, in the form of:  
   https://musicbrainz.org/ws/2/release/aa8c3de3-2a38-4355-9276-bb9a0a57bf5a/?fmt=json&inc=recordings
 - for every track - if `tracknumber` and `name` are equal - the `mb_id` is added as a *Relation*




#### Crawl for secondary identifiers

The platfom implements several other identifiers for the different content-types.

 - *Track*
   - `isrc`

 - *Artist*
   - `ipi_code`
   - `isni_code`

 - *Release*
   - `barcode`

 - *Label*
   - `labelcode`




    # usage
    ./manage.py crawler_cli crawl_identifiers <content type>
