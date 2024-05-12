| TEST |![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ju-c-lopes/model-blog-platform/test.yml?branch=platform&event=push&style=flat&label=Actions-Push-Tests) |
| COVERAGE | https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/ju-c-lopes/gistblogmodel/raw/covbadge.json |

---

# Starting the Model Blog Website
<hr>

<p>This project intend being a platform to create posts for a website, building the templates, their components and providing informations of posts to optimize SEO tags</p>

<p>For this project, it's been used <em>Django</em>, <em>SQLite</em> and <em>JavaScript</em> so far.</p>

<p>Let's try it</p>

<hr>

### Steps

* Project Initiated
* Made Header and Menu funtionality
* Made Our Team Page
* Made card profile which is userd in Author Page and Our Team Page
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

<p>This functionality checks if the password contain Upper character, Number, Special character, and length between 10 and 16 characters.</p>
<p>Beyond that, finish register button is activated only if this requirements are accomplished and the first password and confirmation are the same.</p>
<p>However, this doesn't prevent malicious user modify the function through DevTools and submit an unsafe password, therefore we worked to prevent bad requests</p>

---

## Backend password check

<p>To prevent these possible bad requests, we validate passwords submited into a view, checking the requirements, registring only if requirements were accomplished</p>
<p>The view were tested, checking if it works appropriately</p>

---
