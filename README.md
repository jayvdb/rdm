<a href="https://github.com/innolitics/rdm/actions/workflows/tests.yml/">
  <img src="https://github.com/innolitics/rdm/actions/workflows/tests.yml/badge.svg?branch=main">
</a>

# Regulatory Documentation Manager

## Quick Start

```
pip install rdm[github]
rdm init
cd regulatory
make
# regulatory documents stored in the "release" directory

# if pandoc is installed, you can also run
make pdfs
make docs
```

## Introduction

Our Regulatory Documentation Manager (RDM) is a set of templates and python scripts for generating regulatory documents for software that is a, or is embedded in, medical devices.

*RDM is especially well-suited for early-stage software-only medical devices.*

To use RDM, one needs to know how to use Markdown and Git. For this reason, as projects and teams grow, and as people who are unfamiliar with these tools join the team, you may want to migrate some or all of the your documents to another format (e.g., Microsoft Word). RDM provides a simple mechanism for doing this when the time comes. Typically, documents which are only touched by developers will remain in RDM, but many other documents will be converted to Word Files and stored in a separate Document Management System.

## Professional Support

RDM is developed by [Innolitics](https://innolitics.com). We're a small development firm that writes software for medical devices.

We provide professional support for companies implementing RDM as their regulatory documentation solution, starting at $5,500/year. We can provide training, custom integrations, and workflow optimization for your software development team. Email us at [sales@innolitics.com](mailto:sales@innolitics.com) or call us at [+1 (512) 967-6088](tel:+1-512-967-6088) to learn more.

## Our Philosophy on Regulations

Engineering is about optimizing. To do it one must first know what is being optimized.

Some students go to school because they need the degree to get a job.  These students optimize their actions to get the best grades for the least amount of work.

The best students go to school to learn, and while they often try to get good grades, they optimize their actions so as to learn as much as they can.

Likewise, some companies follow regulations to get certified to sell their products.  They optimize everything they do to get past the regulators for the lowest cost.

The best companies follow the regulations with a degree of faith that these regulations will make their products better and safer.

## Typical Workflow

RDM is designed to be used within a typical software development workflow.  When a new project is started, developers

1. Install RDM using `pip install rdm`
2. Generate a set of documents, which are stored in the git repository, using `rdm init`
3. Edit configuration variables in the generated files
4. Write _software requirements_ in a YAML file, also stored in the git repository
5. Generate a top-level architecture document, also stored in the repository, which may subdivide the project into smaller _software items_
6. Tickets (e.g. GitHub Issues) are labeled with one or more requirement ids
7. Each commit messages must include a reference to the ticket that is being worked on
8. Pull requests must be reviewed, and certain standardized comments are placed in reviews to confirm validation
9. Write new architecture documents as new _software items_ are implemented
10. Once a new _release_ is cut, generate a set of IEC62304 documents using `rdm release`
11. Run `rdm gap [some checklist] release/*.md` to check for missing items
12. These markdown files can then be converted to PDFs (`make pdfs`) or Word documents (`make docs`)

## Our Design Goals for RDM

1. Provide an simple mechanism to migrate away from RDM to more complex tools.
2. Provide a set of template regulatory documents that covers common use-cases.
3. Focus on software developers ease-of-use; the plan documents are intended to read and used frequently by the software developers on the team.  Thus, wherever there was a tradeoff between making it easy to read for developers vs regulators/auditors, we optimized for developers.  For example, we re-order IEC62304 sections to follow a more logical order for developers at the cost of being less parallel to IEC62304's structure.
4. Easy auditablility.  In order to make it easier for regulators/auditors to read the document, we include auditor comments and links back to IEC62304.  These links and notes are hidden by default, but there is a flag that enables turning them on.  This way, we can use the "official" version without comments during our day-to-day work, but we can give the auditors two copies—both the "official" version and the "auditor" version that has all these extra notes. The auditor notes make it easier to tweak the existing templates, since you will know whether a section of the template is required or not.
5. Provide readable documents; e.g., other 62304 templates include many short deeply nested sub-sections.  We use a maximum of two levels of nesting.  We also provide flags (e.g., for different safety classes) that prune out irrelevant parts of the document, so that the documents only include what is necessary for the particular project.
6. Provide beautiful documents.  We believe making beautiful looking documents will encourage people to read and update them.

## Dependencies

- Python 3.5+
- Make
- Jinja2 2.7+
- PyYAML
- gitpython
- pygithub (optional, required when using GitHub as your project manager)
- Pandoc 2.14 and pdflatex (optional, required for PDF generation)

## Installation

`pip install rdm`

or, if you need GitHub support:

`pip install rdm[github]`

## User Guide

Run `rdm init` to generate a set of base documents for a project.  By default these documents are placed in the current working directory in a new directory named `regulatory`, including:

- A `Makefile` for compiling documents.
- A `config.yml` file for configuring RDM.
- Regulatory document templates are in the `documents` directory.
- Data used for generating templates is stored in YAML files within the `data` directory.
- Images are stored in the `images` directory
- Temporarily generated files are stored in `tmp`.
- The final compiled release documents are stored in the `release` directory.

## Document Formats

Release documents are produced in two different formats:

1. [GitHub-Flavored Markdown](https://guides.github.com/features/mastering-markdown/) with standardized YAML front matter
2. PDFs

Typically, the current markdown version of the relevant documents are stored in the git repository, so that they can be easily browsed and linked to by developers.

Compile the release markdown documents by running `make`.

The PDF versions are generated for submission to regulatory bodies or for upload to other document control systems.

Compile the release PDF documents by running `make pdfs`.

## Templating and Data Files

The markdown files support basic templating using the [Jinja templating language](http://jinja.pocoo.org/docs/latest/templates/). Data loaded from yaml files in the `data` directory are provided for context while rendering.

We make a few modifications to the default Jinja templating.

### First Pass Output

We add `first_pass_output` to the rendering context, which is useful when you need to inspect the rendered document to generate, e.g., definition lists. This object has two useful properties:

- `first_pass_output.source` contains the complete output of a first pass generation of the document.
- `first_pass_output.lines` contains the same output as list of lines.

### Extensions

We also support [extensions](http://jinja.pocoo.org/docs/2.10/extensions/). Extensions are set using the `md_extensions` configuration paramater in `config.yml`. See the Markdown Extensions section for details about available markdown extensions.

## YAML Front Matter

The Markdown document format contains YAML front matter, which is used to generate the title page, headers, and footers in the associated PDFs.

For example, your markdown YAML front matter may be:

```
---
id: PLAN-001
revision: 1
title: Software Plan
---
```

The required `title` value is used for the document title page and in the header.

The required `id` value is the document id. This is show in the title page and in the header.

The optional `revision` value is printed on the title page and in the header, if present. Revisions are not typically required for records.

The manufacturer name, which must be specified in `system.yml` data document, is also show on the title page.

## Images

Both the markdown and PDFs support images. An image in a markdown document will look like:

```
![image label](./images/my-image.png)
```

Images are stretched to full page width and must be able to fit within a single page of a PDF document for the formatting to look normal. The path to the images must be relative to the Makefile (per the pandoc `resource-path` setting).

Links to images are preserved in the markdown but are downloaded when compiling word documents or PDFs (using pandoc's `extract-media` setting).

Note that markdown does not support having spaces in links, thus image names can not have spaces.

Also note that the PDFs don't support SVG files. A Python script, in conjunction with some Makefile customizations, can be used to convert SVGs to PNGs if needed.

## Project Management Backends

The FDA, and other regulatory bodies, require records to prove that you are following your development process. Typically, the data needed to produce these records is captured in one more software development project management tools. We often use GitHub or Jira. When putting together a 510(k) or other regulatory documentation, it is helpful to have a mechanism for moving this data into an appropriate document format.

RDM assists in this process by providing project management backends. These backends can be customized and configured in `config.yml`. Essentially, they pull data from a project management tool and dump it into a YAML file with a standardized format. The YAML file can then be used, like any other data file, to render templates.

### GitHub Pull Request Backend

TODO: Write out documentation about this.

### GitHub Issue Backend

TODO: Write out documentation about this.

## Markdown Extensions

### Auditor Notes Extension

We have added some features to make it more convenient to include regulatory auditor notes.  Auditor notes are references to ISO standards and regulations, which are convenient for auditors as well as people who are adapting templates for their own needs (the notes will tell you which parts of the template are required).

Auditor notes are specified with double square brackets:

```
Some specification [[62304:6.2.4]].
```

Auditor notes are included in the default templates, but are stripped out by the `rdm.md_extensions.AuditNoteExclusionExtension` extension.

The auditor notes plugin strips leading white before the audit note. Thus, the above example, when the extension is enabled, becomes:

```
Some specification.
```

### Section Numbers Extension

The `SectionNumberExtension` will automatically add section numbering. This will convert section number markdown like

```html
## Some Topic
```

to

```
## 2.1 Some Topic
```

### Vocabulary Extension

The `VocabularyExtension` extends `first_pass_output` to include a dictionary of words found in the trial first pass. The set of words can then be accessed as a jinja variable using `{{ first_pass_output.words }}`. More convenient is testing whether a particular word is in the document:

```html
{% if first_pass_output.has('foobot') %}
*foobot*: Automated process that implements foo.
{% endif %}
```

The above definition of the example word `foobot` would only be included if the full document actually uses the word. Case insensitive versions of `words` and `has` are available as `words_ignore_case` and `has_ignore_case`.

## Audit Checklists

We include several checklists for various standards.  These are used by the
`rdm gap` command to check output documents for appropriate references to a
given standard.

Here is the contents of the provided `62304_2015_class_b` checklist:

```
# Audit checklist for IEC62304 version 2006 AMD1:2015 Class B products
#
# This checklist is not a substitute for reading, understanding, and
# implementing the associated standard. The descriptive phrase following each
# keyword reference is intended only as a helpful mnemonic for locating and
# recalling the referenced section of the standard.
#
include 62304_2015_class_a
include 62304_base_class_b
62304:5.1.12.a Identification and avoidance of common software defects: identify
62304:5.1.12.b Identification and avoidance of common software defects: document
62304:5.6.2 Verify software integration
62304:5.6.3 Software integration testing
62304:5.6.4 Software integration testing content
62304:5.6.5 Evaluate integration test procedures
```

The `rdm gap` command audits a set of text files:

```
rdm gap 62304_2015_class_b regulatory/release/*.md
```

If any checklist keywords (e.g., `62304.5.6.5`) are absent from the provided
text files, the command will return with a non-zero exit code and list which
items are missing. The checklist items are searched for anywhere within the
text files. We recommend incorporating this check into a continuous integration
server.

You can print the expanded contents of a checklist using `rdm gap checklist`.

You can list the builtin checklists with `rdm gap --list`.

To provide a custom checklist, use a file path for the first argument.

The checklist format is described in detail [here](./docs/checklist-format.md).

## RDM's Limitations

- The default templates were written with small software teams in mind (e.g., 2 - 5 developers).
- Only supports GitHub as your project manager (we plan on adding support for Gitlab, Jira, Trello, and Pivotal over time)
- Assumes that the risk management process is stored elsewhere (we plan on adding support for ISO14971's risk management process soon)
- Only supports a single _software system_
- Only support using git as your version control system
- Assumes the whole software system is in a single git repository
- Default templates assume the whole software system has a single safety classification

## Future Work

- Add support for more project management backends, such as Gitlab, Jira, Trello, Pivotal, and others.
- Add templates for the usability standard ISO62366
- Provide templates for a basic quality management systems that fulfill ISO13485
- Provide templates for 510(k) submissions
- Continue to streamline the workflow
- Provide more thorough examples

## Who Uses RDM?

- We use it at [Innolitics](https://innolitics).
- A couple of our clients have used it and have successfully submitted 510(k)s using documents produced by it. One client also passed an IEC62304 [Intertek](https://www.intertek.com) Audit using the documents produced by RDM.

**If you use RDM, please let us know.**
