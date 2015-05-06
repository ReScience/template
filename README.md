### ReScience submission template repository

This is the submission template repository for the
[Re**Science** journal](https://github.com/ReScience/ReScience/wiki).

### How to build the PDF ?

In a console, type:

```
pandoc --standalone                      \
       --template=rescience-template.tex \
       --latex-engine=pdflatex paper.md  \
       --output paper.pdf
```
