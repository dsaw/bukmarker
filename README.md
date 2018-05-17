# Bukmarker
> Command line integrated bookmark manager 

  [![Build Status][travis-image]][travis-url]

Bukmarker can add, update, delete and search bookmarks quickly from the command line. It also can automatically import bookmarks from Chrome and Firefox browsers. It supports exporting bookmarks to various formats.

## Installation

### Dependencies

| Feature | Dependency |
| --- | --- |
| Scripting language | Python 3.6+ |
| HTTP(S) | urllib |
| Database | sqlite3 |
| Import browser exported html | beautifulsoup4 |

To install package dependencies, run pip3.

`$ pip install beautifulsoup4`

Clone bukmarker from github as usual or download as a zip file.

To run tests, cd to project root first and type:

`$ python setup.py test`


## Usage example

Adding bookmarks is simple, use `--add`. Optionally title, tags and description can be specified.

`$ python bukmarker.py --add www.another-site.com --title another site --desc just some site`

Editing an already stored bookmark is done similarly.
If title is not specifed, bukmarker will automatically fetch it for you. 

`$ python bukmarker.py --modify www.another-site.com anotherSite `

Search needs an URL only (Note that **-** is **title**, **>** are **tags**, **+** is the **description**) .

 ```
 $ python bukmarker.py --search https://www.skytorrents.in/
Searching for https://www.skytorrents.in/...
Search results of https://www.skytorrents.in/ are
url https://www.skytorrents.in/
- Sky torrents a Privacy focused torrent search engine
>
+
```

Searching using tags can also be done. To return bookmarks with **ANY** of the tags, pass in a tag list starting with **,** . For bookmarks with **ALL** of the tags, pass in **+** respectively.

``` 
$ python bukmarker.py --search --tags , django pagerank
url www.google.com
-
> search,pagerank
+
===

url https://scribles.net/deploying-existing-django-app-to-heroku/
- Deploying existing Django App to Heroku
> ,django
+
===
```

Deleting a bookmark is simple as before.

```
$ python bukmarker.py --delete www.gone.com/
Deleted www.gone.com successfully

```

For operations with tags, pass a separate list to `--tags`. You can run add, modify, delete and append with tags option.

```
$ python bukmarker.py --append https://scribles.net/deploying-existing-django-app-to-heroku/ --tags django
Bookmark https://scribles.net/deploying-existing-django-app-to-heroku/ successfully updated
```

Auto-import will prompt for Chrome and Firefox.

```
$ python bukmarker.py --ai
Import from google chrome bookmarks?(y/n)y
Import from firefox bookmarks?(y/n)n
Import is complete
```

Currently, you can export bookmarks as a html file.

```
$ python bukmarker.py --export
302 bookmarks exported successfully
```

## Meta

Devesh Sawant – [@WhoSawDevesh](https://twitter.com/WhoSawDevesh)

Blog post about [project](https://wp.me/p3i9xR-1D)

Distributed under the GPLv3 license.

Inspired from [Buku](https://github.com/jarun/Buku)

<!-- Markdown link & img dfn's -->

[travis-image]: https://travis-ci.org/dsaw/bukmarker.svg?branch=master
[travis-url]: https://travis-ci.org/dsaw/bukmarker#
