
{% for template in templates %}
{{ template.inner|safe }}
{% endfor %}
