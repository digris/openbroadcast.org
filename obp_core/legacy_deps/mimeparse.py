# mimeparse.py
"""MIME-Type Parser

NOTE: used by old tastypie - ported tp python 3.9+ here.
      remove once tasypie / api-v1 is removed.

This module provides basic functions for handling mime-types. It can handle
matching mime-types against a list of media-ranges. See section 14.1 of
the HTTP specification [RFC 2616] for a complete explanation.

http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.1
"""

from __future__ import annotations

__version__ = "0.1.3"
__author__ = "Joe Gregorio"
__email__ = "joe@bitworking.org"
__credits__ = ""


def parse_mime_type(mime_type: str):
    """Parse a mime-type into (type, subtype, params).

    For example:
        'application/xhtml;q=0.5'
    becomes:
        ('application', 'xhtml', {'q': '0.5'})
    """
    parts = mime_type.split(";")
    params = {}

    for param in parts[1:]:
        param = param.strip()
        if not param:
            continue
        if "=" in param:
            key, value = param.split("=", 1)
            params[key.strip()] = value.strip()

    full_type = parts[0].strip()

    # Java URLConnection sometimes sends Accept: *
    if full_type == "*":
        full_type = "*/*"

    mime_parts = full_type.split("/", 1)
    if len(mime_parts) == 1:
        mime_parts.append("*")

    main_type, subtype = mime_parts
    return main_type.strip(), subtype.strip(), params


def parse_media_range(media_range: str):
    """Parse a media range into (type, subtype, params).

    Ensures that params always contains a valid 'q' value.
    Invalid or missing q values are normalized to '1'.
    """
    main_type, subtype, params = parse_mime_type(media_range)

    try:
        q = float(params.get("q", "1"))
    except (TypeError, ValueError):
        q = 1.0

    if q < 0 or q > 1:
        q = 1.0

    params["q"] = str(q).rstrip("0").rstrip(".") if q != 1.0 else "1"
    return main_type, subtype, params


def fitness_and_quality_parsed(mime_type: str, parsed_ranges):
    """Find the best match for a given mime-type against parsed media ranges.

    Returns:
        (fitness, q)
    where:
        fitness = -1 and q = 0 if no match is found.
    """
    best_fitness = -1
    best_fit_q = 0.0

    target_type, target_subtype, target_params = parse_media_range(mime_type)

    for main_type, subtype, params in parsed_ranges:
        type_match = main_type == target_type or main_type == "*" or target_type == "*"
        subtype_match = (
            subtype == target_subtype or subtype == "*" or target_subtype == "*"
        )

        if type_match and subtype_match:
            param_matches = sum(
                1
                for key, value in target_params.items()
                if key != "q" and key in params and value == params[key]
            )

            fitness = 0
            if main_type == target_type:
                fitness += 100
            if subtype == target_subtype:
                fitness += 10
            fitness += param_matches

            if fitness > best_fitness:
                best_fitness = fitness
                best_fit_q = float(params["q"])

    return best_fitness, best_fit_q


def quality_parsed(mime_type: str, parsed_ranges):
    """Return the q value of the best match against parsed media ranges."""
    return fitness_and_quality_parsed(mime_type, parsed_ranges)[1]


def quality(mime_type: str, ranges: str):
    """Return the q value of a mime-type against a header string.

    Example:
        >>> quality(
        ...     'text/html',
        ...     'text/*;q=0.3, text/html;q=0.7, text/html;level=1, '
        ...     'text/html;level=2;q=0.4, */*;q=0.5'
        ... )
        1.0
    """
    parsed_ranges = [parse_media_range(r) for r in ranges.split(",")]
    return quality_parsed(mime_type, parsed_ranges)


def best_match(supported, header: str):
    """Return the best match from a list of supported mime-types.

    The supported list should be sorted in order of increasing desirability,
    so that later entries win in case of equal fitness/q.
    """
    parsed_header = [parse_media_range(r) for r in _filter_blank(header.split(","))]
    weighted_matches = []

    for pos, mime_type in enumerate(supported):
        weighted_matches.append(
            (fitness_and_quality_parsed(mime_type, parsed_header), pos, mime_type)
        )

    weighted_matches.sort()
    return (
        weighted_matches[-1][2]
        if weighted_matches and weighted_matches[-1][0][1]
        else ""
    )


def _filter_blank(items):
    for s in items:
        if s.strip():
            yield s
