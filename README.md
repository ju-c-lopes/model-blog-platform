| TEST | ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ju-c-lopes/model-blog-platform/test.yml?branch=platform&event=push&style=flat&label=Actions-Push-Tests) |
| --- | --- |
| COVERAGE | [![Coverage Status](./coverage-badge.svg)](./reports/coverage/index.html) |

---

# Starting the Model Blog Website
---

> This project intend being a platform to create posts for a website, building the templates, their components and providing informations of posts to optimize SEO tags

> For this project, it's been used _Django_, _SQLite_ and _JavaScript_ so far.

> Let's try it!

---

### Steps

* Project Initiated
* Made Header and Menu functionality
* Made Our Team Page
* Made card profile which is used in Author Page and Our Team Page
* Made author edit profile (needs more functionality later)
* Made edit social media profile functionality with messages return
* Rewrite the user custom model which has been used to create author and reader profiles
* Made Sign Up page with reader and author type register
* Made Reader edit profile (more simple than author)
* Made login page
* Made Password validation with JavaScript
* Setting show hide password on Login Page
* Made Password validation in a view Django
* Made test to check if view password validation works

---

## Screenshot

<figure>
<img src="./website/static/img/pass-valid.gif" style="width: 200px;" alt="Password Validation using JavaScript" title ="Password Validation using Javascript">
<figcaption>Password Validation using Javascript</figcaption>
</figure><br><br>

---

## Front-end password check

> This functionality checks if the password contain Upper character, Number, Special character, and length between 10 and 16 characters.
> Beyond that, finish register button is activated only if this requirements are accomplished and the first password and confirmation are the same.
> However, this doesn't prevent malicious user modify the function through DevTools and submit an unsafe password, therefore we worked to prevent bad requests

---

## Backend password check

> To prevent these possible bad requests, we validate passwords submited into a view, checking the requirements, registring only if requirements were accomplished
> The view were tested, checking if it works appropriately

---
