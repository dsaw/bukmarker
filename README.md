# bukmarker
> Command line integrated bookmark manager 

Bukmarker can add, update, delete and search bookmarks quickly from the command line. It also can automatically import bookmarks from Chrome and Firefox browsers. It supports exporting bookmarks to various formats.

## Installation



## Usage example

Adding bookmarks is simple, use --add. Optionally, tags and description can be specified.

`$ python bukmarker.py --add www.another-site.com `

Editing an already stored bookmark is done similarly.

`$ python bukmarker.py --modify www.another-site.com anotherSite `

Search need an URL only. 
 
 ```
 $ python bukmarker.py --search https://www.skytorrents.in/
Searching for https://www.skytorrents.in/...
Search results of https://www.skytorrents.in/ are
url https://www.skytorrents.in/
- Sky torrents a Privacy focused torrent search engine
>
+
```

Searching using tags can also be done. To return bookmarks with ANY of the tags, pass in a tag list starting with , . For bookmarks with ALL of the tags, pass in + respectively.

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
Distributed under the MIT license.

Inspired from [Buku](https://github.com/jarun/Buku)


