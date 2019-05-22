import os
import re
import subprocess
import shutil

from rdm.util import print_error

import yaml


def yaml_gfm_to_tex(input_filename, context, output_file):
    '''
    This function uses Pandoc to convert our Github flavored markdown into
    latex.  We then alter this latex and insert a title, headers, etc. based on
    the yaml front matter.  A lot of the code in this module is fragile because
    it depends on the precise formatting of the Latex document generated by
    Pandoc, but it should work well enough for now.
    '''
    with open(input_filename, 'r') as input_file:
        input_text = input_file.read()
    markdown, front_matter = _extract_yaml_front_matter(input_text)
    tex = _convert_with_pandoc(markdown)
    tex_lines = tex.split('\n')

    add_margins(tex_lines, front_matter, context)
    add_title_and_toc(tex_lines, front_matter, context)
    add_header_and_footer(tex_lines, front_matter, context)
    handle_images(tex_lines, front_matter, context)

    output_file.write('\n'.join(tex_lines))


def _extract_yaml_front_matter(raw_string):
    parts = raw_string.split('---\n')
    if len(parts) < 3:
        raise ValueError('Invalid YAML front matter')
    front_matter_string = parts[1]
    template_string = '---\n'.join(parts[2:])
    try:
        front_matter = yaml.load(front_matter_string, Loader=yaml.SafeLoader)
    except yaml.YAMLError as e:
        raise ValueError('Invalid YAML front matter; improperly formatted YAML: {}'.format(e))
    return template_string, front_matter


def _convert_with_pandoc(markdown):
    p = subprocess.run(
        ['pandoc', '-f', 'gfm', '-t', 'latex', '--standalone',
         '-V', 'urlcolor=blue', '-V', 'linkcolor=black'],
        input=markdown,
        encoding='utf-8',
        stdout=subprocess.PIPE,
        universal_newlines=True
    )
    if p.returncode != 0:
        raise ValueError('Pandoc failed to convert markdown to latex')
    else:
        return p.stdout


def add_title_and_toc(tex_lines, front_matter, context):
    begin_document_index = tex_lines.index(r'\begin{document}')
    _insert_liness(tex_lines, begin_document_index + 1, [
        r'\maketitle',
        r'\thispagestyle{empty}',
        r'\tableofcontents',
        r'\pagebreak',
    ])
    _insert_liness(tex_lines, begin_document_index, [
        r'\title{' + front_matter['title'] + r' \\ ',
        r'\large ' + front_matter['id'] + ', Rev. ' + str(front_matter['revision']) + '}',
        r'\date{\today}',
        r'\author{' + front_matter['manufacturer_name'] + '}',
    ])


def add_header_and_footer(tex_lines, front_matter, context):
    begin_document_index = tex_lines.index(r'\begin{document}')
    _insert_liness(tex_lines, begin_document_index + 1, [
        r'\thispagestyle{empty}',
    ])
    _insert_liness(tex_lines, begin_document_index, [
        r'\usepackage{fancyhdr}',
        r'\usepackage{lastpage}',
        r'\pagestyle{fancy}',
        r'\lhead{' + front_matter['title'] + '}',
        r'\rhead{' + front_matter['id'] + ', Rev. ' + str(front_matter['revision']) + '}',
        r'\cfoot{Page \thepage\ of \pageref{LastPage}}',
    ])


def add_margins(tex_lines, front_matter, context):
    try:
        document_class_index = tex_lines.index(r'\documentclass[]{article}')
    except ValueError:
        document_class_index = tex_lines.index(r'\documentclass[')
        if tex_lines[document_class_index + 1] == ']{article}':
            document_class_index += 1
        else:
            raise
    tex_lines.insert(document_class_index + 1, r'\usepackage[margin=1.25in]{geometry}')


def _insert_liness(existing, index, new_lines):
    for line in reversed(new_lines):
        existing.insert(index, line)


svg_pattern = re.compile(r'^\\includegraphics{\.\./(?P<path>.*\.svg)}$')
img_pattern = re.compile(r'^\\includegraphics{\.\./(?P<path>.*)}$')


def handle_images(tex_lines, front_matter, context):
    '''
    We want to support including images in two contexts:

    1. GitHub flavored markdown
    2. Inside PDF documents

    Each context has conflicting constraints. We translate between each approach
    as best we can here.

    The markdown allows URLs to images hosted elsewhere, while
    LaTeX does not.  We (will) solve this by downloading images to `./tmp`.

    The markdown requires relative paths from the document where the image is
    used, to the for location of the image file.  It seems that LaTeX does not
    (although there may be a way to make it work).  We solve this by
    translating and copying the images to `./tmp`.

    The markdown supports SVGs, while LaTeX does not.  Thus, we convert SVGs
    into PDFs, and save them within `./tmp`.  Note that the SVG to PDF
    conversion is not perfect, and that there are some features of SVGs that are not supported, such as:

    - Masks
    - Style sheets
    - Color gradients
    - Embedded bitmaps
    '''
    # TODO: make the path handling more generic. Currently it assumes the CWD
    # is in `regulatory`, that the image path in the markdown is in `../images/` and is
    # placed into `regulatory/tmp/images/`.  E.g., resolve the relative URL
    # from the document's path, then flatten the full path into a single path,
    # and copy it into tmp
    # TODO: handle downloading externally hosted images
    for index, line in enumerate(tex_lines):
        line_contains_img = img_pattern.search(line)
        if line_contains_img:
            input_path = line_contains_img.group('path')
            if not os.path.isfile(input_path):
                print_error("Image does not exist: " + os.path.abspath(input_path))

            input_directory, input_filename_w_ext = os.path.split(input_path)
            output_directory = os.path.join('./tmp/', input_directory)
            os.makedirs(output_directory, exist_ok=True)

            line_contains_svg = svg_pattern.search(line)
            if line_contains_svg:
                input_filename, _ = os.path.splitext(input_filename_w_ext)
                output_path = os.path.join(output_directory, input_filename + '.pdf')
                svg_to_pdf(input_path, output_path)
            else:
                output_path = os.path.join(output_directory, input_filename_w_ext)
                shutil.copyfile(input_path, output_path)

            tex_lines[index] = r'\includegraphics[width=0.95\textwidth]{' + output_path + '}'


def svg_to_pdf(svg_filename, pdf_filename):
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
    drawing = svg2rlg(svg_filename)
    renderPDF.drawToFile(drawing, pdf_filename)
