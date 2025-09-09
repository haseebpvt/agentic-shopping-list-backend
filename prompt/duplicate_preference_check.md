You will be given a query and a vector search data. If the vector search result contains the given query you need to
respond with a small explanation and at the end of your response specifically mention if it is duplicate or not.

## Query
{{ query }}

## Vector Search Results
{% for item in result %}
- {{ item }}
{% endfor %}

## Example output
Short explanation of why or why not this is duplicate..

Is duplicate: True/False