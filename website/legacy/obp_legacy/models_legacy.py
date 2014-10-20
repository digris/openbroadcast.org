# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class ElggCalendarEvents(models.Model):
    ident = models.IntegerField(primary_key=True)
    owner = models.IntegerField()
    calendar = models.IntegerField()
    title = models.CharField(max_length=765, blank=True)
    description = models.TextField()
    access = models.CharField(max_length=765, blank=True)
    location = models.CharField(max_length=150, blank=True)
    date_start = models.IntegerField()
    date_end = models.IntegerField()
    class Meta:
        db_table = u'elgg_calendar_events'

class ElggCcAccess(models.Model):
    id = models.IntegerField(primary_key=True)
    gunid = models.CharField(max_length=765, blank=True)
    token = models.BigIntegerField(null=True, blank=True)
    chsum = models.CharField(max_length=96, blank=True)
    ext = models.CharField(max_length=384, blank=True)
    type = models.CharField(max_length=60, blank=True)
    parent = models.BigIntegerField(null=True, blank=True)
    owner = models.IntegerField(null=True, blank=True)
    ts = models.DateTimeField()
    class Meta:
        db_table = u'elgg_cc_access'

class ElggCcGunid(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=765, blank=True)
    objid = models.IntegerField(null=True, blank=True)
    gunid = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'elgg_cc_gunid'

class ElggCcTransport(models.Model):
    id = models.IntegerField(primary_key=True)
    trtoken = models.CharField(max_length=48, blank=True)
    direction = models.CharField(max_length=384, blank=True)
    state = models.CharField(max_length=384, blank=True)
    trtype = models.CharField(max_length=384, blank=True)
    lock = models.CharField(max_length=3, blank=True)
    target = models.CharField(max_length=765, blank=True)
    rtrtok = models.CharField(max_length=48, blank=True)
    mdtrtok = models.CharField(max_length=48, blank=True)
    gunid = models.BigIntegerField(null=True, blank=True)
    pdtoken = models.BigIntegerField(null=True, blank=True)
    url = models.CharField(max_length=765, blank=True)
    localfile = models.CharField(max_length=765, blank=True)
    fname = models.CharField(max_length=765, blank=True)
    title = models.CharField(max_length=765, blank=True)
    expectedsum = models.CharField(max_length=96, blank=True)
    realsum = models.CharField(max_length=96, blank=True)
    expectedsize = models.IntegerField(null=True, blank=True)
    realsize = models.IntegerField(null=True, blank=True)
    uid = models.IntegerField(null=True, blank=True)
    errmsg = models.CharField(max_length=765, blank=True)
    jobpid = models.IntegerField(null=True, blank=True)
    start = models.DateTimeField()
    starttime = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'elgg_cc_transport'

class ElggCmBaskets(models.Model):
    userid = models.IntegerField(unique=True)
    baskets = models.TextField()
    updated = models.DateTimeField()
    migrated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'elgg_cm_baskets'

class ElggCmContainer(models.Model):
    ident = models.IntegerField(primary_key=True)
    x_ident = models.IntegerField()
    body = models.TextField()
    content_list = models.TextField()
    container_type = models.CharField(max_length=150)
    date_time = models.IntegerField()
    target_duration = models.CharField(max_length=30)
    duration = models.DecimalField(max_digits=14, decimal_places=4)
    sub_type = models.IntegerField()
    best_broadcast_segment = models.CharField(max_length=1200)
    best_broadcast_daytime = models.CharField(max_length=60)
    best_broadcast_weekday = models.CharField(max_length=60)
    livesession_license = models.IntegerField()
    played = models.IntegerField()
    rotation_include = models.IntegerField()
    rebroadcast_url = models.CharField(max_length=1536)
    class Meta:
        db_table = u'elgg_cm_container'

class ElggCmFile(models.Model):
    ident = models.IntegerField(primary_key=True)
    file = models.CharField(max_length=765)
    x_ident = models.IntegerField()
    posted = models.IntegerField()
    filetype = models.CharField(max_length=240)
    class Meta:
        db_table = u'elgg_cm_file'

class ElggCmLog(models.Model):
    ident = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=60)
    content_ident = models.IntegerField()
    action = models.CharField(max_length=180)
    user_ident = models.IntegerField()
    timestamp = models.IntegerField()
    class Meta:
        db_table = u'elgg_cm_log'

class ElggCmMaster(models.Model):
    ident = models.IntegerField(primary_key=True)
    owner = models.IntegerField()
    editor = models.IntegerField()
    lastupdater = models.IntegerField()
    type = models.CharField(max_length=60)
    title = models.TextField()
    intro = models.TextField()
    access = models.CharField(max_length=60, blank=True)
    access_write = models.CharField(max_length=60)
    lastupdate = models.IntegerField()
    posted = models.IntegerField()
    is_history = models.IntegerField()
    index = models.TextField()
    status = models.IntegerField()
    duration = models.IntegerField()
    notes = models.IntegerField()
    revnumber = models.IntegerField()
    locked = models.IntegerField()
    locked_userident = models.IntegerField()
    migrated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'elgg_cm_master'

class ElggCmMedias(models.Model):
    id = models.IntegerField(primary_key=True)
    x_id = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    published = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=60, blank=True)
    notes = models.TextField(blank=True)
    filesize = models.IntegerField(null=True, blank=True)
    fileformat = models.CharField(max_length=36, blank=True)
    dataformat = models.CharField(max_length=36, blank=True)
    channels = models.IntegerField(null=True, blank=True)
    sample_rate = models.IntegerField(null=True, blank=True)
    bitrate = models.IntegerField(null=True, blank=True)
    channelmode = models.CharField(max_length=36, blank=True)
    bitrate_mode = models.CharField(max_length=36, blank=True)
    lossless = models.IntegerField(null=True, blank=True)
    encoder_options = models.CharField(max_length=36, blank=True)
    compression_ratio = models.DecimalField(null=True, max_digits=14, decimal_places=4, blank=True)
    encoding = models.CharField(max_length=36, blank=True)
    path = models.CharField(max_length=3072, blank=True)
    sourcepath = models.CharField(max_length=3072, blank=True)
    parentdirectory = models.CharField(max_length=750, blank=True)
    filename = models.CharField(max_length=750, blank=True)
    pipeline_status = models.IntegerField()
    has_flac_default = models.IntegerField()
    has_mp3_default = models.IntegerField()
    has_mp3_64 = models.IntegerField()
    has_mp3_128 = models.IntegerField()
    has_mp3_320 = models.IntegerField()
    has_peakfile = models.IntegerField()
    has_peakfile_raw = models.IntegerField()
    has_peakfile_mp3 = models.IntegerField()
    lock = models.IntegerField()
    class Meta:
        db_table = u'elgg_cm_medias'

class ElggCmRelations(models.Model):
    ident = models.IntegerField(primary_key=True)
    c_ident_master = models.IntegerField()
    c_ident_slave = models.IntegerField()
    relation_type = models.IntegerField()
    user_ident = models.IntegerField()
    class Meta:
        db_table = u'elgg_cm_relations'

class ElggCmText(models.Model):
    ident = models.IntegerField(primary_key=True)
    body = models.TextField()
    x_ident = models.IntegerField()
    posted = models.IntegerField()
    class Meta:
        db_table = u'elgg_cm_text'

class ElggCmWordlist(models.Model):
    word_text = models.CharField(max_length=150, primary_key=True)
    word_id = models.IntegerField()
    word_common = models.IntegerField()
    class Meta:
        db_table = u'elgg_cm_wordlist'

class ElggCmWordmatch(models.Model):
    content_ident = models.IntegerField()
    word_id = models.IntegerField()
    title_match = models.IntegerField()
    class Meta:
        db_table = u'elgg_cm_wordmatch'

class ElggComments(models.Model):
    ident = models.IntegerField(primary_key=True)
    object_id = models.IntegerField()
    object_type = models.CharField(max_length=384)
    owner = models.IntegerField()
    postedname = models.CharField(max_length=384)
    body = models.TextField()
    posted = models.IntegerField()
    class Meta:
        db_table = u'elgg_comments'

class ElggContentFlags(models.Model):
    ident = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=384)
    class Meta:
        db_table = u'elgg_content_flags'

class ElggDatalists(models.Model):
    ident = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=96)
    value = models.TextField()
    class Meta:
        db_table = u'elgg_datalists'

class ElggFeedPosts(models.Model):
    ident = models.IntegerField(primary_key=True)
    posted = models.CharField(max_length=192)
    added = models.IntegerField()
    feed = models.IntegerField()
    title = models.TextField()
    body = models.TextField()
    url = models.CharField(max_length=765)
    class Meta:
        db_table = u'elgg_feed_posts'

class ElggFeedSubscriptions(models.Model):
    ident = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    feed_id = models.IntegerField()
    autopost = models.CharField(max_length=9)
    autopost_tag = models.CharField(max_length=384)
    class Meta:
        db_table = u'elgg_feed_subscriptions'

class ElggFeeds(models.Model):
    ident = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=384)
    feedtype = models.CharField(max_length=48)
    name = models.TextField()
    tagline = models.CharField(max_length=384)
    siteurl = models.CharField(max_length=384)
    last_updated = models.IntegerField()
    class Meta:
        db_table = u'elgg_feeds'

class ElggFileFolders(models.Model):
    ident = models.IntegerField(primary_key=True)
    owner = models.IntegerField()
    files_owner = models.IntegerField()
    parent = models.IntegerField()
    name = models.CharField(max_length=384)
    access = models.CharField(max_length=60)
    handler = models.CharField(max_length=96)
    class Meta:
        db_table = u'elgg_file_folders'

class ElggFileMetadata(models.Model):
    ident = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=765)
    value = models.TextField()
    file_id = models.IntegerField()
    class Meta:
        db_table = u'elgg_file_metadata'

class ElggFiles(models.Model):
    ident = models.IntegerField(primary_key=True)
    owner = models.IntegerField()
    files_owner = models.IntegerField()
    folder = models.IntegerField()
    community = models.IntegerField()
    title = models.CharField(max_length=765)
    originalname = models.CharField(max_length=765)
    description = models.CharField(max_length=765)
    location = models.CharField(max_length=765)
    access = models.CharField(max_length=60)
    size = models.IntegerField()
    time_uploaded = models.IntegerField()
    handler = models.CharField(max_length=96)
    class Meta:
        db_table = u'elgg_files'

class ElggFilesIncoming(models.Model):
    ident = models.IntegerField(primary_key=True)
    installid = models.CharField(max_length=96)
    intentiondate = models.IntegerField()
    size = models.BigIntegerField()
    foldername = models.CharField(max_length=384)
    user_id = models.IntegerField()
    class Meta:
        db_table = u'elgg_files_incoming'

class ElggFriends(models.Model):
    ident = models.IntegerField(primary_key=True)
    owner = models.IntegerField(unique=True)
    friend = models.IntegerField()
    status = models.CharField(max_length=12)
    class Meta:
        db_table = u'elgg_friends'

class ElggFriendsRequests(models.Model):
    ident = models.IntegerField(primary_key=True)
    owner = models.IntegerField(unique=True)
    friend = models.IntegerField(unique=True)
    class Meta:
        db_table = u'elgg_friends_requests'

class ElggGroupMembership(models.Model):
    ident = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(unique=True)
    group_id = models.IntegerField(unique=True)
    class Meta:
        db_table = u'elgg_group_membership'

class ElggGroups(models.Model):
    ident = models.IntegerField(primary_key=True)
    owner = models.IntegerField()
    name = models.CharField(max_length=384)
    access = models.CharField(max_length=60)
    class Meta:
        db_table = u'elgg_groups'

class ElggIcons(models.Model):
    ident = models.IntegerField(primary_key=True)
    owner = models.IntegerField()
    filename = models.CharField(max_length=384)
    description = models.CharField(max_length=765)
    class Meta:
        db_table = u'elgg_icons'

class ElggInvitations(models.Model):
    ident = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=384)
    email = models.CharField(max_length=384)
    code = models.CharField(max_length=384)
    owner = models.IntegerField()
    added = models.IntegerField()
    class Meta:
        db_table = u'elgg_invitations'

class ElggIpoolData(models.Model):
    ident = models.IntegerField(primary_key=True)
    owner = models.IntegerField()
    title = models.TextField()
    description = models.TextField()
    body = models.TextField()
    access = models.CharField(max_length=60, blank=True)
    longitude = models.IntegerField()
    latitude = models.IntegerField()
    posted = models.IntegerField()
    class Meta:
        db_table = u'elgg_ipool_data'

class ElggLicences(models.Model):
    ident = models.IntegerField(primary_key=True)
    page_ident = models.IntegerField()
    name = models.CharField(max_length=384)
    modify_time = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'elgg_licences'

class ElggLicencesAcceptedCmMaster(models.Model):
    licences_ident = models.ForeignKey(ElggLicences, db_column='licences_ident')
    object_ident = models.IntegerField()
    accept_time = models.DateTimeField()
    licence_time = models.DateTimeField()
    class Meta:
        db_table = u'elgg_licences_accepted_cm_master'

class ElggLicencesAcceptedMlMedias(models.Model):
    licences_ident = models.ForeignKey(ElggLicences, db_column='licences_ident')
    object_ident = models.IntegerField()
    accept_time = models.DateTimeField()
    licence_time = models.DateTimeField()
    class Meta:
        db_table = u'elgg_licences_accepted_ml_medias'

class ElggLicencesAcceptedMlRelease(models.Model):
    licences_ident = models.ForeignKey(ElggLicences, db_column='licences_ident')
    object_ident = models.IntegerField()
    accept_time = models.DateTimeField()
    licence_time = models.DateTimeField()
    class Meta:
        db_table = u'elgg_licences_accepted_ml_release'

class ElggLicencesAcceptedUsers(models.Model):
    licences_ident = models.ForeignKey(ElggLicences, db_column='licences_ident')
    object_ident = models.IntegerField()
    accept_time = models.DateTimeField()
    licence_time = models.DateTimeField()
    class Meta:
        db_table = u'elgg_licences_accepted_users'

class ElggLicencesArchived(models.Model):
    ident = models.IntegerField(primary_key=True)
    page_ident = models.IntegerField()
    user_ident = models.IntegerField()
    uri = models.CharField(max_length=384)
    title = models.CharField(max_length=384)
    content = models.TextField()
    version_time = models.DateTimeField()
    class Meta:
        db_table = u'elgg_licences_archived'

class ElggMessages(models.Model):
    ident = models.IntegerField(primary_key=True)
    title = models.TextField()
    body = models.TextField()
    from_id = models.IntegerField()
    to_id = models.IntegerField()
    posted = models.IntegerField()
    status = models.CharField(max_length=18)
    hidden_from = models.CharField(max_length=3)
    hidden_to = models.CharField(max_length=3)
    class Meta:
        db_table = u'elgg_messages'

class ElggMlf2Banlists(models.Model):
    name = models.CharField(max_length=765)
    list = models.TextField()
    class Meta:
        db_table = u'elgg_mlf2_banlists'

class ElggMlf2Categories(models.Model):
    id = models.IntegerField(primary_key=True)
    order_id = models.IntegerField()
    category = models.CharField(max_length=765)
    description = models.CharField(max_length=765)
    accession = models.IntegerField()
    class Meta:
        db_table = u'elgg_mlf2_categories'

class ElggMlf2Entries(models.Model):
    id = models.IntegerField(unique=True)
    pid = models.IntegerField()
    tid = models.IntegerField()
    uniqid = models.CharField(max_length=765)
    time = models.DateTimeField()
    last_reply = models.DateTimeField()
    edited = models.DateTimeField()
    edited_by = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=765)
    subject = models.CharField(max_length=765)
    category = models.IntegerField()
    email = models.CharField(max_length=765)
    hp = models.CharField(max_length=765)
    location = models.CharField(max_length=765)
    ip = models.CharField(max_length=765)
    text = models.TextField()
    tags = models.CharField(max_length=765)
    show_signature = models.IntegerField(null=True, blank=True)
    email_notification = models.IntegerField(null=True, blank=True)
    marked = models.IntegerField(null=True, blank=True)
    locked = models.IntegerField(null=True, blank=True)
    sticky = models.IntegerField(null=True, blank=True)
    views = models.IntegerField(null=True, blank=True)
    spam = models.IntegerField(null=True, blank=True)
    spam_check_status = models.IntegerField(null=True, blank=True)
    edit_key = models.CharField(max_length=765)
    startpoint = models.FloatField(null=True, blank=True)
    endpoint = models.FloatField(null=True, blank=True)
    threadtype = models.CharField(max_length=30)
    class Meta:
        db_table = u'elgg_mlf2_entries'

class ElggMlf2EntriesCache(models.Model):
    cache_id = models.IntegerField(primary_key=True)
    cache_text = models.TextField()
    class Meta:
        db_table = u'elgg_mlf2_entries_cache'

class ElggMlf2Logincontrol(models.Model):
    time = models.DateTimeField()
    ip = models.CharField(max_length=765)
    logins = models.IntegerField()
    class Meta:
        db_table = u'elgg_mlf2_logincontrol'

class ElggMlf2Pages(models.Model):
    id = models.IntegerField(primary_key=True)
    order_id = models.IntegerField()
    title = models.CharField(max_length=765)
    content = models.TextField()
    menu_linkname = models.CharField(max_length=765)
    access = models.IntegerField()
    class Meta:
        db_table = u'elgg_mlf2_pages'

class ElggMlf2Settings(models.Model):
    name = models.CharField(max_length=765)
    value = models.CharField(max_length=765)
    class Meta:
        db_table = u'elgg_mlf2_settings'

class ElggMlf2Smilies(models.Model):
    id = models.IntegerField(primary_key=True)
    order_id = models.IntegerField()
    file = models.CharField(max_length=300)
    code_1 = models.CharField(max_length=150)
    code_2 = models.CharField(max_length=150)
    code_3 = models.CharField(max_length=150)
    code_4 = models.CharField(max_length=150)
    code_5 = models.CharField(max_length=150)
    title = models.CharField(max_length=765)
    class Meta:
        db_table = u'elgg_mlf2_smilies'

class ElggMlf2Userdata(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_type = models.IntegerField()
    user_name = models.CharField(max_length=765)
    user_real_name = models.CharField(max_length=765)
    gender = models.IntegerField()
    birthday = models.DateField()
    user_pw = models.CharField(max_length=765)
    user_email = models.CharField(max_length=765)
    email_contact = models.IntegerField(null=True, blank=True)
    user_hp = models.CharField(max_length=765)
    user_location = models.CharField(max_length=765)
    signature = models.CharField(max_length=765)
    profile = models.TextField()
    logins = models.IntegerField()
    last_login = models.DateTimeField()
    last_logout = models.DateTimeField()
    user_ip = models.CharField(max_length=765)
    registered = models.DateTimeField()
    thread_order = models.IntegerField()
    user_view = models.IntegerField()
    sidebar = models.IntegerField()
    fold_threads = models.IntegerField()
    thread_display = models.IntegerField()
    new_posting_notification = models.IntegerField(null=True, blank=True)
    new_user_notification = models.IntegerField(null=True, blank=True)
    time_difference = models.IntegerField(null=True, blank=True)
    user_lock = models.IntegerField(null=True, blank=True)
    auto_login_code = models.CharField(max_length=765)
    pwf_code = models.CharField(max_length=765)
    activate_code = models.CharField(max_length=765)
    class Meta:
        db_table = u'elgg_mlf2_userdata'

class ElggMlf2UserdataCache(models.Model):
    cache_id = models.IntegerField(primary_key=True)
    cache_signature = models.TextField()
    cache_profile = models.TextField()
    class Meta:
        db_table = u'elgg_mlf2_userdata_cache'

class ElggMlf2Useronline(models.Model):
    ip = models.CharField(max_length=45)
    time = models.IntegerField()
    user_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'elgg_mlf2_useronline'

class ElggPages(models.Model):
    ident = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=384, unique=True)
    uri = models.CharField(max_length=384)
    parent = models.IntegerField()
    weight = models.IntegerField()
    title = models.TextField()
    content = models.TextField()
    owner = models.IntegerField()
    access = models.CharField(max_length=60)
    class Meta:
        db_table = u'elgg_pages'

class ElggPasswordRequests(models.Model):
    ident = models.IntegerField(primary_key=True)
    owner = models.IntegerField()
    code = models.CharField(max_length=384)
    class Meta:
        db_table = u'elgg_password_requests'

class ElggPreprodRelations(models.Model):
    ident = models.IntegerField(primary_key=True)
    c_ident_master = models.IntegerField()
    c_ident_slave = models.IntegerField()
    relation_type = models.IntegerField()
    class Meta:
        db_table = u'elgg_preprod_relations'

class ElggPreprodRsegment(models.Model):
    ident = models.IntegerField(primary_key=True)
    body = models.TextField()
    x_ident = models.IntegerField()
    posted = models.IntegerField()
    class Meta:
        db_table = u'elgg_preprod_rsegment'

class ElggPreprodRtransmission(models.Model):
    ident = models.IntegerField(primary_key=True)
    body = models.TextField()
    x_ident = models.IntegerField()
    posted = models.IntegerField()
    class Meta:
        db_table = u'elgg_preprod_rtransmission'

class ElggProfileData(models.Model):
    ident = models.IntegerField(primary_key=True)
    owner = models.IntegerField()
    access = models.CharField(max_length=60)
    name = models.CharField(max_length=765)
    value = models.TextField()
    class Meta:
        db_table = u'elgg_profile_data'

class ElggRiver(models.Model):
    ident = models.IntegerField(primary_key=True)
    userid = models.IntegerField()
    object_id = models.IntegerField()
    object_owner = models.IntegerField()
    object_type = models.CharField(max_length=384)
    access = models.CharField(max_length=384)
    string = models.TextField()
    ts = models.IntegerField()
    class Meta:
        db_table = u'elgg_river'

class ElggRoleCommunity(models.Model):
    ident = models.IntegerField(primary_key=True)
    role = models.CharField(max_length=150)
    communities = models.CharField(max_length=1500)
    class Meta:
        db_table = u'elgg_role_community'

class ElggRolePermissions(models.Model):
    ident = models.IntegerField(primary_key=True)
    role = models.CharField(max_length=150)
    permissions = models.CharField(max_length=1500)
    class Meta:
        db_table = u'elgg_role_permissions'

class ElggRoleProfessions(models.Model):
    ident = models.IntegerField(primary_key=True)
    role = models.CharField(max_length=150)
    professions = models.CharField(max_length=1500)
    class Meta:
        db_table = u'elgg_role_professions'

class ElggSchedule(models.Model):
    ident = models.IntegerField(primary_key=True)
    starttime = models.IntegerField()
    duration = models.IntegerField()
    source = models.CharField(max_length=60)
    source_ident = models.IntegerField()
    added = models.IntegerField()
    last_edit = models.IntegerField()
    endtime = models.IntegerField()
    user_ident = models.IntegerField()
    status = models.IntegerField()
    played = models.IntegerField()
    class Meta:
        db_table = u'elgg_schedule'

class ElggScheduleLog(models.Model):
    ident = models.IntegerField(primary_key=True)
    logtag = models.CharField(max_length=300)
    data1 = models.TextField()
    data2 = models.TextField()
    s_ident = models.IntegerField()
    sesskey = models.CharField(max_length=120)
    user_ident = models.IntegerField()
    day = models.IntegerField()
    activitydate = models.IntegerField()
    river_ident = models.IntegerField()
    pl_ident = models.IntegerField()
    class Meta:
        db_table = u'elgg_schedule_log'

class ElggScheduleUdata(models.Model):
    ident = models.IntegerField(primary_key=True)
    userident = models.IntegerField()
    day = models.CharField(max_length=36)
    dtype = models.CharField(max_length=150)
    class Meta:
        db_table = u'elgg_schedule_udata'

class ElggStreamTokens(models.Model):
    id = models.IntegerField(primary_key=True)
    token = models.CharField(max_length=96)
    class Meta:
        db_table = u'elgg_stream_tokens'

class ElggTags(models.Model):
    ident = models.IntegerField(primary_key=True)
    tag = models.CharField(max_length=384)
    tagtype = models.CharField(max_length=60)
    ref = models.IntegerField()
    access = models.CharField(max_length=60)
    owner = models.IntegerField()
    class Meta:
        db_table = u'elgg_tags'

class ElggTemplateElements(models.Model):
    ident = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=384)
    content = models.TextField()
    template_id = models.IntegerField()
    class Meta:
        db_table = u'elgg_template_elements'

class ElggTemplates(models.Model):
    ident = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=384)
    owner = models.IntegerField()
    public = models.CharField(max_length=9)
    shortname = models.CharField(max_length=384)
    class Meta:
        db_table = u'elgg_templates'

class ElggTimetabledigrisData(models.Model):
    elgg_timetabledigris_ident = models.IntegerField(primary_key=True)
    elgg_timetabledigris_txt = models.TextField()
    class Meta:
        db_table = u'elgg_timetabledigris_data'

class ElggToptags(models.Model):
    ident = models.IntegerField(primary_key=True)
    tag = models.TextField()
    tagident = models.IntegerField(null=True, blank=True)
    type = models.TextField()
    class Meta:
        db_table = u'elgg_toptags'

class ElggUserFlags(models.Model):
    ident = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    flag = models.CharField(max_length=192)
    value = models.CharField(max_length=192)
    class Meta:
        db_table = u'elgg_user_flags'

class ElggUsers(models.Model):
    ident = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=384)
    password = models.CharField(max_length=96)
    email = models.CharField(max_length=384)
    name = models.CharField(max_length=384)
    icon = models.IntegerField()
    active = models.CharField(max_length=9)
    alias = models.CharField(max_length=384)
    code = models.CharField(max_length=96)
    icon_quota = models.IntegerField()
    file_quota = models.IntegerField()
    template_id = models.IntegerField()
    owner = models.IntegerField()
    user_type = models.CharField(max_length=384)
    moderation = models.CharField(max_length=12)
    last_action = models.IntegerField()
    template_name = models.CharField(max_length=384)
    join_date = models.IntegerField(null=True, blank=True)
    reg_ip = models.CharField(max_length=45, blank=True)
    fb_id = models.CharField(max_length=72, unique=True, blank=True)
    updated = models.DateTimeField()
    migrated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'elgg_users'

class ElggUsersAlias(models.Model):
    ident = models.IntegerField(primary_key=True)
    installid = models.CharField(max_length=96)
    username = models.CharField(max_length=96)
    firstname = models.CharField(max_length=192)
    lastname = models.CharField(max_length=192)
    email = models.CharField(max_length=384)
    user_id = models.IntegerField()
    class Meta:
        db_table = u'elgg_users_alias'

class ElggWatchlist(models.Model):
    ident = models.IntegerField(primary_key=True)
    owner = models.IntegerField()
    object_id = models.IntegerField()
    object_type = models.CharField(max_length=384)
    class Meta:
        db_table = u'elgg_watchlist'

class ElggWeblogComments(models.Model):
    ident = models.IntegerField(primary_key=True)
    post_id = models.IntegerField()
    owner = models.IntegerField()
    postedname = models.CharField(max_length=384)
    body = models.TextField()
    posted = models.IntegerField()
    class Meta:
        db_table = u'elgg_weblog_comments'

class ElggWeblogPosts(models.Model):
    ident = models.IntegerField(primary_key=True)
    owner = models.IntegerField()
    weblog = models.IntegerField()
    icon = models.IntegerField()
    access = models.CharField(max_length=60)
    posted = models.IntegerField()
    title = models.TextField()
    body = models.TextField()
    class Meta:
        db_table = u'elgg_weblog_posts'

class ElggWeblogWatchlist(models.Model):
    ident = models.IntegerField(primary_key=True)
    owner = models.IntegerField()
    weblog_post = models.IntegerField()
    class Meta:
        db_table = u'elgg_weblog_watchlist'

class ElggWidgetData(models.Model):
    ident = models.IntegerField(primary_key=True)
    widget = models.IntegerField()
    name = models.CharField(max_length=384)
    value = models.TextField()
    class Meta:
        db_table = u'elgg_widget_data'

class ElggWidgets(models.Model):
    ident = models.IntegerField(primary_key=True)
    owner = models.IntegerField()
    type = models.CharField(max_length=384)
    location = models.CharField(max_length=384)
    location_id = models.IntegerField()
    wcolumn = models.IntegerField()
    display_order = models.IntegerField()
    access = models.CharField(max_length=384)
    class Meta:
        db_table = u'elgg_widgets'

class ElggXblog(models.Model):
    ident = models.IntegerField(primary_key=True)
    x_modul = models.CharField(max_length=60, blank=True)
    x_ident = models.IntegerField()
    blog_ident = models.IntegerField()
    class Meta:
        db_table = u'elgg_xblog'

