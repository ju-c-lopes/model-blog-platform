---
applyTo: '**/*.html'
---
Provide project context and coding guidelines that AI should follow when generating code, answering questions, or reviewing changes.

# Template Tags HTML for Django Instructions

This project uses Django template tags in its HTML files. When generating or modifying HTML code, please ensure that you correctly implement Django template tags and syntax.

All tags must be created in oneline, without line breaks.
Example:
```html
{% if user.is_authenticated and user.is_active %}
    <p>Welcome, {{ user.username }}!</p>
{% else %}
    <p>Please log in.</p>
{% endif %}
```
Incorrect:
```html
{% if user.is_authenticated %} {{
    user.username }}!
{% else %}
    <p>Please log in.</p>
{% endif %}
```

or

```html
{% if user.is_authenticated and
    user.is_active
%}
    <p>Welcome, {{ user.username }}!</p>
{% else %}
    <p>Please log in.</p>
{% endif %}
```

When using template tags, ensure that:

- Open tags like `{%` and `{{` are always closed with `%}` and `}}` respectively, an always in the same line, don't break line never, even line becomes too long.

Why is these instructions so important?
- These instructions are crucial because incorrect usage of Django template tags can lead to syntax errors, rendering issues, raising exceptions in debug check for web browser interpretation, and not being able to load the page.
