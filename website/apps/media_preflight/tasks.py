# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import logging

from cacheops import invalidate_obj
from celery import shared_task

from . import service_client


logger = logging.getLogger(__name__)


@shared_task
def run_preflight_check_task(preflight_check_id):

    from .models import PreflightCheck

    preflight_check = PreflightCheck.objects.get(id=preflight_check_id)

    logger.info("Media id: {} - run preflight check".format(preflight_check.media.id))

    try:
        result = service_client.run_check(media=preflight_check.media)
        checks = result.get("checks", {})
        warnings = []
        errors = result.get("errors", [])

        decoded_duration = checks.get("decoded_duration", None)
        master_duration = preflight_check.media.master_duration

        if decoded_duration and master_duration:
            diff = abs(decoded_duration - master_duration)
            if diff > 5.0:
                errors.append(
                    "duration mismatch: {:.2f}s".format(diff),
                )
            elif diff > 2.0:
                warnings.append(
                    "duration mismatch: {:.2f}s".format(diff),
                )

        preflight_check.status = PreflightCheck.STATUS_COMPLETED
        preflight_check.checks = checks
        preflight_check.warnings = warnings
        preflight_check.errors = errors
        preflight_check.save()

    except service_client.PreflightServiceException as e:
        logger.warning("error running preflight check: {}".format(e))

        preflight_check.status = PreflightCheck.STATUS_ERROR
        preflight_check.checks = {}
        preflight_check.warnings = []
        preflight_check.errors = ["{}".format(e)]
        preflight_check.save()

    invalidate_obj(preflight_check)
