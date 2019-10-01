import math


# Font size distribution algorithms
LOGARITHMIC, LINEAR = 1, 2


def _calculate_thresholds(min_weight, max_weight, steps):
    delta = (max_weight - min_weight) / float(steps)
    return [min_weight + i * delta for i in range(1, steps + 1)]


def _calculate_tag_weight(weight, max_weight, distribution):
    """
    Logarithmic tag weight calculation is based on code from the
    `Tag Cloud`_ plugin for Mephisto, by Sven Fuchs.

    .. _`Tag Cloud`: http://www.artweb-design.de/projects/mephisto-plugin-tag-cloud
    """

    if distribution == LINEAR or max_weight == 1:
        return weight
    elif distribution == LOGARITHMIC:
        return math.log(weight) * max_weight / math.log(max_weight)
    raise ValueError("Invalid distribution algorithm specified: %s." % distribution)


def calculate_cloud(tags, steps=6, distribution=LOGARITHMIC, group_by=10):

    if len(tags) > 0:
        counts = [tag.count for tag in tags]
        min_weight = float(min(counts))
        max_weight = float(max(counts))
        thresholds = _calculate_thresholds(min_weight, max_weight, steps)

        groups = []
        for i in range(steps):
            groups.append(0)

        hidden = []
        for i in range(steps):
            hidden.append(0)

        for tag in tags:
            weight_set = False
            tag_weight = _calculate_tag_weight(tag.count, max_weight, distribution)
            for i in range(steps):

                if not weight_set and tag_weight <= thresholds[i]:
                    tag.weight = i + 1
                    groups[i] += 1
                    weight_set = True

        total = 0
        cnt = steps - 1
        for i in reversed(groups):
            hide_level = 0
            for x in range(1, steps + 1):
                if total > group_by * x:
                    hide_level += 1
            hidden[cnt] = hide_level
            total += i
            cnt -= 1

        for tag in tags:
            try:
                tag.hide_level = hidden[tag.weight - 1]
            except Exception as e:
                pass

    return tags
