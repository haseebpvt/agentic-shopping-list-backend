You will be given a **query** and a list of **vector search results**.  
Your task is to check whether the query is already contained within the vector search results.  

### Instructions:
1. Compare the query with the vector search results.  
2. If the query is found in the results, provide a short explanation of why it is a duplicate.  
3. If the query is not found, provide a short explanation of why it is not a duplicate.  
4. At the end of your response, clearly state:  
   - `Is duplicate: True` if it is a duplicate.  
   - `Is duplicate: False` if it is not a duplicate.  

---

## Query
{{ query }}

## Vector Search Results
{% for item in result %}
- {{ item }}
{% endfor %}

---

## Example Output
The query matches one of the vector search results because both describe the same concept in similar wording.  

Is duplicate: True
