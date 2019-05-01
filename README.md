### [ReScience C](https://rescience.github.io/) article template

This repository contains the Latex (optional) template for writing a ReScience
C article and the (mandatory) YAML metadata file. For the actual article,
you're free to use any software you like as long as you enforce the proposed
PDF style. A tool is available for the latex template that produces latex
definitions from the metadata file. If you use another software, make sure that
metadata and PDF are always synced.


#### Usage

For a submission, fill in information in
[metadata.yaml](./metadata.yaml), modify [content.tex](content.tex)
and type:

```bash
$ make 
```

After acceptance, fill in [metadata.yaml](./metadata.yaml) with information provided by the editor and type:

```bash
$ make
```

