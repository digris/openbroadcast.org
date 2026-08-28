# Migration Roadmap

## Goals

### Project recovery and documentation

- [x] Incubate `next` branch
- [x] Prepare the repository for AI-assisted development
- [x] Add repository-level agent instructions and validation conventions
- [x] Add historical project documentation and archived source material
- [x] Refresh the main README and document the current project state
- [x] Add a migration roadmap
- [x] Establish reproducible Python and frontend development workflows
- [x] Add initial linting, formatting, and regression-test infrastructure

### Python 3 migration

- [ ] Remove the Python 2.7 runtime requirement
- [ ] Bring the application up on a supported Python 3 baseline
- [ ] Reach a stable intermediate target around Python 3.9 / Django 1.11
- [ ] Remove or replace Python-2-only dependencies
- [ ] Remove compatibility shims that are no longer required
- [ ] Verify core application behavior under Python 3

The intermediate target is intentionally conservative: first make the existing
application run reliably on a substantially newer Python environment without
combining that work with a large framework or data-model migration.

### Infrastructure and deployment

- [ ] Run the application stack on a recent Debian release
- [ ] Re-establish a reproducible deployment process
- [ ] Bring required backend services up on supported versions
- [ ] Preserve the existing database and storage layout where practical
- [ ] Avoid large data migrations during the initial platform lift
- [ ] Restore automated checks / CI for the migrated runtime
- [ ] Document development, deployment, backup, and recovery procedures

### Legacy code reduction

- [ ] Remove unused application code and dead features
- [ ] Remove obsolete vendored dependencies where upstream packages can be used
- [ ] Reduce `obp_core/legacy_apps/` to dependencies that genuinely require local patches
- [ ] Remove remaining references to Django CMS
- [ ] Remove obsolete configuration, templates, static assets, and service integrations
- [ ] Identify historical subsystems that are no longer part of the current product

### Functional recovery

- [ ] Get the application approximately 90% operational on the intermediate stack
- [ ] Restore the main music-library workflows
- [ ] Restore playlist and scheduling workflows
- [ ] Restore required metadata/import/export functionality
- [ ] Restore required background-processing tasks
- [ ] Validate the frontend against the migrated backend
- [ ] Document known broken or intentionally retired functionality

The target here is not feature-for-feature restoration of every historical
capability. Functionality that is unused or no longer relevant may be removed
instead of migrated.

## Modernization after functional recovery

The following work should generally happen only after the application is stable
on the intermediate Python/Django platform.

### API modernization

- [ ] Replace Tastypie with Django REST Framework
- [ ] Replace Dajax/Dajaxice endpoints with normal HTTP/API endpoints
- [ ] Consolidate duplicated or obsolete API surfaces
- [ ] Add regression coverage around migrated API behavior

### Frontend modernization

- [ ] Remove unnecessary manual jQuery usage
- [ ] Replace legacy AJAX patterns with maintained browser APIs or application APIs
- [ ] Remove Nunjucks where it no longer provides value
- [ ] Reduce obsolete frontend build/runtime dependencies
- [ ] Remove frontend code belonging to retired features

### Framework modernization

- [ ] Move beyond Django 1.11 in controlled increments
- [ ] Replace dependencies that block newer Django versions
- [ ] Remove compatibility code after each supported-version transition
- [ ] Keep schema and data migrations separately reviewable from framework upgrades

## Later work

T.B.C.

Likely areas include:

- dependency consolidation
- authentication and permissions cleanup
- background-job modernization
- media-processing cleanup
- storage modernization
- frontend architecture
- test coverage
- observability
- deployment automation
- security hardening