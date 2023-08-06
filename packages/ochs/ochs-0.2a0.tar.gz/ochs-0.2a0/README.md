# PyBlog

[![vsartor](https://circleci.com/gh/vsartor/ochs.svg?style=shield)](https://github.com/vsartor/ochs) [![codecov](https://codecov.io/gh/vsartor/ochs/branch/master/graph/badge.svg)](https://codecov.io/gh/vsartor/ochs)

A Python tool for building static, templated blogs with Markdown.

This tool in currently undergoing initial development.

## Brief Introduction

PyBlog is designed around simple, handwritten HTML templates, handwritten stylesheets and Markdown posts.

Its source directory contains four folders: `settings`, `templates`, `posts` and `resources`.

The `resources` folders holds resources that are copied into the target folder. For example, if there's a `stylesheet.css` file in the root of the `resources` folder, it will be located in the root directory of the website.

### Settings

The settings folders holds four different YAML files.

* `variables.yaml`: Specifying variables that can be used to fill in the templates.

```YAML
- name: "title"
  value: "My Blog"
- name: "base_url"
  value: "https://myblog.com"
```

* `templates.yaml`: Specifying where templates are located and an associated alias. The template files are located in the `templates` folder.

```YAML
- name: "home"
  file: "home.html"
- name: "about_me"
  file: "about-me.html"
- name: "post"
  file: "post.html"
- name: "head"
  file: "head-v2.html"
```

* `pages.yaml`: Specifying static pages are built, and whether they hold content relating to posts.

```YAML
- name: "home"
  template: "home"
  url: "index.html"
  blog: false
- name: "about"
  template: "aboutme-v2"
  url: "about.html"
  blog: false
- name: "posts"
  template: "posts"
  url: "posts.html"
  blog: true
```

* `posts.yaml`: Specifying post information, including the location of the preview and content markdown files, located in the `posts` folder, and which template should be used to fill in the post content.

```YAML
- title: "Lorem Ipsum I"
  date: "2020-08-01"
  author: "Victhor Sartório"
  preview: "lorem_ipsum_1_preview.md"
  content: "lorem_ipsum_1.md"
  url: "lorem_ipsum_1.html"
  template: "post"
- title: "Lorem Ipsum II"
  date: "2020-08-02"
  author: "Victhor Sartório"
  preview: "lorem_ipsum_2_preview.md"
  content: "lorem_ipsum_2.md"
  url: "lorem_ipsum_2.html"
  template: "post"
```

### Templates

Templates are HTML files that may include three kinds of macros. The first two are simple variables and templates.

* Variables are indicated by `@{<variable_name>}`.
* Templates are indicated by `${<template_name>}`.

_Example of a template with variables and other embedded templates:_
```HTML
${head}

<body>
${header}

    <p>Page in construction. Go back to <a href="@{base_url}">the homepage</a>.</p>
</body>
``` 

The other kinds of macros relate to post informations. First, look at the example of a simple homepage below:

```HTML
${head}

<body>
${header}

	#{post-start}:3
	<div class="post-preview-body">
		<div class="post-title"><a href="#{post-url}">#{post-title}</a></div>
		<div class="post-subtitle">By #{post-author} in #{post-date}</div>
		<div class="post-preview">#{post-preview}</div>
	</div>
	#{post-end}
</body>
```

First of all, the `#{post-start}:3` and `#{post-end}` macros delimit an HTML block that will be repeated `3` times. Each of the blocks will have the information replaced relating to the `3` most recent posts.

Further, some variables are substituted by the post information derived from the `posts.yaml`, file. These are indicated by `#{post-<field_name>}`.

## Running

To run, one may set `OCHS_SOURCE` and `OCHS_TARGET` in the enviroment, pointing to the source and target directories, respectively. Then, one may simply run `blog build`.
