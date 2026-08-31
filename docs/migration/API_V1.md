# Legacy Tastypie API (v1) Inventory

## Summary

The legacy API is still mounted and materially used. `config/urls.py` exposes the
default Tastypie `Api()` instance below `/api/`, which produces the `/api/v1/`
namespace. `config/urls_api.py` registers 20 resources. Four additional
Tastypie resources are not registered directly but are embedded by other v1
resources.

DRF is mounted separately below `/api/v2/`. It overlaps much of the library,
scheduler, profiles, exporter, rating, and event surface, but it is not yet a
drop-in replacement for the active playlist editor, importer, media stream,
mixdown callback, or channel `on-air` contracts.

Production access-log evidence in `data/tmp/api-v1-usage.txt` confirms active
use by the current browser application, a mixdown service, and an external
Python service. The capture aggregates all retained Nginx `access.log*` files;
it does not include the retention period or status codes. A request count proves
that a route was requested, not that it returned successfully. Query parameters
and credentials are intentionally not reproduced here.

Archived pages under `docs/history/archive-org/` were excluded as evidence of
current use, as required by `docs/history/AGENTS.md`.

## Wiring

- `config/urls.py:52-55` mounts Tastypie at `/api/` and DRF at `/api/v2/`.
- `config/urls_api.py:22-65` creates the default Tastypie API and registers the
  v1 resources.
- Registered resources normally expose list, schema, set, and detail routes
  below `/api/v1/<resource_name>/`, subject to each resource's allowed methods.
- `prepend_urls()` methods add the custom actions summarized below.
- Some models generate Tastypie URLs through `get_api_url()` and Pushy signal
  registration. Registration and relationship use therefore matter even when
  there is no ordinary Python import or literal `/api/v1/` consumer string.
- `config/urls_apiv2.py` composes the current DRF APIs from the application-level
  `apiv2/urls.py` modules.

## Resource inventory

Production counts below are normalized totals from the method-and-URL section
of `data/tmp/api-v1-usage.txt`. Very small curl/browser-only counts are treated
as probes or manual checks, not as proof of an application consumer.

| Resource | v1 URL and notable actions | Current consumers / production evidence | DRF equivalent | Confidence | Suggested action |
| --- | --- | --- | --- | --- | --- |
| `api_base.BaseResource` (`obp_core/api_base/api.py:11`) | `/api/v1/base/`; `version`, `register-component`, `get-stream-parameters` | No repository consumer found. Three unattributed browser/curl requests. | No complete equivalent | no repository consumer found | Needs status-coded runtime verification; likely removable if the requests are probes. |
| `MediaResource` (`obp_core/alibrary/api/mediaapi.py:22`) | `/api/v1/library/track/`; detail actions `vote`, `stats`, `stream.mp3` | Playlist relations and model-generated URLs. 135 production requests: 134 `stream.mp3` requests from the Mixdown Agent and one probable probe. | `/api/v2/alibrary/media/` overlaps CRUD; statistics/rating exist separately; no confirmed stream replacement | confirmed used | Keep temporarily; implement and migrate the stream contract before removal. |
| `SimpleMediaResource` (`obp_core/alibrary/api/mediaapi.py:242`) | `/api/v1/library/simpletrack/` | Embedded through `PlaylistItemResource`; no direct production request. | `/api/v2/alibrary/media/` | probably used | Keep with the legacy playlist representation, then migrate to the DRF media serializer. |
| `ReleaseResource` (`obp_core/alibrary/api/releaseapi.py:25`) | `/api/v1/library/release/`; detail `stats` | Embedded in playlist items and exposed through model/resource links. Two curl-only production requests. | `/api/v2/alibrary/release/` and statistics API | probably used | Migrate generated links and nested representations to DRF before removal. |
| `SimpleReleaseResource` (`obp_core/alibrary/api/releaseapi.py:105`) | `/api/v1/library/simplerelease/` | No current repository or production consumer found. | `/api/v2/alibrary/release/` | no repository consumer found | Likely removable now, after a status-coded observation window. |
| `ArtistResource` (`obp_core/alibrary/api/artistapi.py:18`) | `/api/v1/library/artist/`; detail `stats` | Nested/resource links. Four production detail reads came from current upload pages; one additional request was a probe. | `/api/v2/alibrary/artist/` and statistics API | confirmed used | Keep with the importer; migrate upload-page lookups to existing DRF. |
| `LabelResource` (`obp_core/alibrary/api/labelapi.py:16`) | `/api/v1/library/label/` | Nested in media/resource links; no direct production request. | `/api/v2/alibrary/label/` | probably used | Migrate relationship URLs/serializers to existing DRF before removal. |
| `PlaylistItemPlaylistResource` (`obp_core/alibrary/api/playlistapi.py:42`) | `/api/v1/library/playlistitem/` | Legacy playlist editor. 569 production mutations: 512 PUT and 57 DELETE. | Playlist v2 overlaps representation but lacks a demonstrated drop-in item-mutation contract | confirmed used | Do not remove; implement/migrate the editor mutation contract first. |
| `PlaylistResource` (`obp_core/alibrary/api/playlistapi.py:65`) | `/api/v1/library/playlist/`; `set-current`, detail/list `collect`, `reorder`, `mixdown-complete` | Playlist editor, importer, Pushy/model URLs, and Mixdown Agent. 1,324 production requests: 1,097 detail GET, 219 reorder, 7 mixdown callbacks, and one probable probe. | `/api/v2/alibrary/playlist/` partially overlaps | confirmed used | Keep temporarily; migrate editor and mixdown contracts as one dependency group. |
| `SimplePlaylistResource` (`obp_core/alibrary/api/playlistapi.py:339`) | `/api/v1/library/simpleplaylist/`; `set-current` | Only stale/legacy frontend references found; no active invocation or production request. | `/api/v2/alibrary/playlist/` | no repository consumer found | Likely removable after a focused browser/network check. |
| `ImportFileResource` (`obp_core/importer/api.py:12`) | `/api/v1/importfile/` | Current upload UI. 1,515 production requests: 1,305 GET, 130 PUT, 76 POST, and 4 DELETE. | None | confirmed used | Keep; implement a DRF replacement before migrating the upload UI. |
| `ImportResource` (`obp_core/importer/api.py:150`) | `/api/v1/import/`; detail `import-all`, `apply-to-all`, `retry-pending` | Current upload UI. 323 production requests: 300 detail GET, 21 `apply-to-all`, and 2 `import-all`. | None | confirmed used | Keep; implement a DRF replacement and migrate together with `ImportFileResource`. |
| `ExportItemResource` (`obp_core/exporter/api.py:23`) | `/api/v1/exportitem/` | Current legacy exporter code posts through `/exporter/legacy/`; no production API request in the captured window. | `/api/v2/exporter/export/` overlaps the combined workflow | confirmed used | Migrate the legacy exporter consumer to DRF, then remove. |
| `ExportResource` (`obp_core/exporter/api.py:99`) | `/api/v1/export/` | Current legacy exporter page lists and mutates exports; no production API request in the captured window. | `/api/v2/exporter/export/` | confirmed used | Migrate the legacy exporter consumer to existing DRF, then remove. |
| `abcast.api.baseapi.ChannelResource` (`obp_core/abcast/api/baseapi.py:32`) | `/api/v1/abcast/channel/`; detail `schedule`, `history`, `on-air`, `program` | 11,633 production GETs to `channel/:id/on-air/` from a Python service client. Pushy also generates the route. | DRF emission, flattened-schedule, history, and playout-schedule overlap; no exact confirmed `on-air` replacement | confirmed used | Do not remove; identify and migrate the external service to a tested DRF contract. |
| `abcast.api.baseapi.BaseResource` (`obp_core/abcast/api/baseapi.py:364`) | `/api/v1/abcast/base/`; 12 playout/configuration actions including stream settings, Liquidsoap status, bootstrap, schedule, and `on-air` | No repository HTTP caller. Three browser/curl requests look manual; external playout use remains possible. | Partial scheduler/playout overlap only | uncertain/dynamic | Needs runtime verification per action; implement replacements for any live playout calls. |
| `EmissionResource` (`obp_core/abcast/api/schedulerapi.py:70`) | `/api/v1/abcast/emission/`; detail `reschedule`, `update` | Pushy/model-generated URLs and legacy relationships. One curl-only production request is not application evidence. | `/api/v2/abcast/emission/` plus scheduler endpoints | probably used | Migrate generated links and verify external consumers before removing v1. |
| `UserResource` (`obp_core/profiles/api/userapi.py:21`) | `/api/v1/auth/user/`; `login`, `register`, `validate-registration`, `get-or-create-social-user` | No repository consumer found. One production login POST used Axios with no referer, indicating a possible external/dynamic caller. | `/api/v2/api-token-auth/` is only a partial equivalent | uncertain/dynamic | Identify the Axios caller and required auth flows before removal. |
| `VoteResource` (`obp_core/arating/api/vote.py:22`) | `/api/v1/rating/vote/<content-type>/<id>[/<vote>][/<user>]/` | Test/smoke reference only; one curl-only production request. | `/api/v2/rating/rating/<content-type>:<uuid>/` | no repository consumer found | Migrate/retire the smoke test and likely remove after status-coded verification. |
| `EventResource` (`obp_core/atracker/api/event.py:22`) | `/api/v1/atracker/event/<content-type>/<uuid>[/<action>][/<user>]/` | No current repository or production consumer found. | `/api/v2/atracker/event/<content-type>:<uuid>/` | no repository consumer found | Likely removable now after a short observation window. |

## Nested, unregistered resources

These classes have no independent registered v1 endpoint. They remain relevant
because Tastypie embeds them while serializing registered parent resources.

| Resource | How it is reached | Confidence | Suggested action |
| --- | --- | --- | --- |
| `PlaylistItemResource` (`obp_core/alibrary/api/playlistapi.py:23`) | Full nested `item` inside `PlaylistItemPlaylistResource`; emits the content object's generated API URL. | confirmed used | Keep while the v1 playlist editor is active; migrate the nested representation with it. |
| `DaypartResource` (`obp_core/alibrary/api/playlistapi.py:59`) | Full nested `dayparts` inside `PlaylistResource`. | uncertain/dynamic | Verify whether current playlist payloads contain dayparts; remove only with the parent migration. |
| Scheduler `PlaylistResource` (`obp_core/abcast/api/schedulerapi.py:48`) | Full generic relation inside `EmissionResource`; its local resource name is `simpleplaylist`, but it is not registered. | uncertain/dynamic | Replace through the DRF emission serializer before deleting. |
| `ProfileResource` (`obp_core/profiles/api/profileapi.py:19`) | Registration is commented out; instantiated/nested by User/Emission legacy serialization paths. | uncertain/dynamic | Prefer existing DRF profiles; remove after legacy serializer paths no longer instantiate it. |

## Production findings

The strongest current dependencies are:

1. Channel `on-air`: 11,633 Python-service requests.
2. Importer: 1,838 requests across Import and ImportFile, including writes and
   deletes from current upload-page referers.
3. Playlist editing: 1,893 requests across Playlist and PlaylistItemPlaylist,
   including reorder, PUT, and DELETE operations from current editor pages.
4. Mixdown: 134 media streams, 28 playlist reads included in the Playlist total,
   and 7 `mixdown-complete` callbacks.
5. Artist: four detail lookups from current upload pages.

The log also contains generic vulnerability-scanner paths below `/api/v1/`
such as configuration, credential, `.env`, Git, and PHP probes. These are not
Tastypie resources. Isolated curl/browser hits on valid resource roots are
therefore not treated as proof of application use.

## Conclusions

### Quick wins

The lowest-risk initial candidates are:

1. `SimpleReleaseResource` — no repository consumer, no production request,
   and an existing DRF release API.
2. `EventResource` — no repository or production consumer and an existing DRF
   event endpoint.
3. `SimplePlaylistResource` — no active consumer or production request, subject
   to a focused browser check.
4. `VoteResource` — only a smoke-test reference and one curl probe; DRF already
   provides the overlapping feature.
5. `api_base.BaseResource` — no consumer and only unattributed/manual-looking
   requests, subject to status-coded verification.

### Do not remove yet

- Channel and its `on-air` action.
- Import and ImportFile.
- Playlist, PlaylistItemPlaylist, nested playlist resources, Media
  `stream.mp3`, and `mixdown-complete`.
- Artist while the upload UI still performs direct v1 lookups.
- Export and ExportItem until the legacy exporter page is migrated.
- Emission and related generated URLs until Pushy and external consumers have
  been checked.

### Runtime verification needed

- Capture at least 30 days of normalized route, method, status, timestamp,
  referer class, and user-agent class. The current report lacks status and time
  range.
- For Base and Abcast Base, aggregate each custom action separately. A sustained
  absence of successful 2xx/3xx calls would distinguish dead actions from
  authenticated external integrations.
- For User, locate the Axios login caller using request timing, source address
  or trusted proxy identity, and response status. Exercise login, registration,
  validation, and social-login flows while watching the network panel.
- For SimplePlaylist, open every playlist creation/edit/current-playlist flow
  and verify that no request or dynamically generated resource URI targets
  `/api/v1/library/simpleplaylist/`.
- For nested resources, inspect representative successful Playlist and Emission
  responses to determine which nested serializers are actually materialized.

### Proposed removal order

1. SimpleRelease and Event.
2. SimplePlaylist, Vote, and the generic BaseResource after focused runtime
   verification.
3. User after identifying or retiring the external Axios caller.
4. Export and ExportItem after migrating the legacy exporter page.
5. Import, ImportFile, and their direct library lookups as one migration group.
6. Playlist, PlaylistItemPlaylist, nested resources, Media streaming, and
   mixdown callbacks as one migration group.
7. Emission and other scheduler resource links after DRF link migration.
8. Channel and Abcast Base last, after all external playout/service clients have
   been migrated and observed on v2.
