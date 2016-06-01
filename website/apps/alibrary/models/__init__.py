#-*- coding: utf-8 -*-

import reversion
from basemodels import (MigrationMixin, Relation, Profession, Agency,
                        License, Service, Distributor, AgencyScope, Daypart)
from artistmodels import (Artist, ArtistProfessions, NameVariation,
                          ArtistMembership, ArtistAlias)
from labelmodels import Label
from mediamodels import Media, MediaExtraartists, MediaArtists
from playlistmodels import (Playlist, PlaylistMedia, PlaylistItem,
                            PlaylistItemPlaylist, Season, Weather, Series)
from releasemodels import (Release, ReleaseExtraartists, ReleaseAlbumartists,
                           ReleaseMedia)

reversion.register(Media)
reversion.register(Release)
reversion.register(Artist)
reversion.register(Label)
