import re

from sphinx_markdown_tables import __version__

def get_str_len(in_str):
    str_len = 0
    for s in in_str:
        if s >= '\u4e00' and s <= '\u9fff':
            str_len += 2
        elif s >= '\uff00' and s <= '\uffef':
            str_len += 2
        else:
            str_len += 1
    return str_len

tex = ''

def create_tex_body(data):
    global tex
    tex += data[0] + '\n'
    for i in data[1:]:
        tex += '&\n' + i + '\n'
    tex += '\\\\%\n' + '\\hline\n'

# >>>>>>>>>>>>>>>>>>>

def create_tex_resize_tail():
    global tex
    tex += '\\end{tabulary}\n' + \
           '}\n' + \
           '\\par\n' + \
           '\\end{table*}\n' + \
           '\\FloatBarrier\n'
           #'\\sphinxattableend\\end{savenotes}\n'

def create_tex_resize_title(align, data):
    global tex
    #tex += '\\begin{savenotes}\\sphinxattablestart\n' + \
    tex += '\\FloatBarrier\n'+ \
           '\\begin{table*}\n' + \
           '\\tiny\n' + \
           '\\rowcolors{2}{gray!20}{white}\n' + \
           '\\centering\n' + \
           '\\resizebox{\\textwidth}{!}{\n' + \
           '\\begin{tabulary}{\\linewidth}[t]{|'
    for i in align:
        tex += i + '|'
    tex += '}\n\\hline\n'
    tex += '\\sphinxstyletheadfamily\n' + data[0] + '\n'
    for i in data[1:]:
        tex += '&\\sphinxstyletheadfamily\n' + i + '\n'
    tex += '\\\\%\n' + '\\hline\n'

def create_tex_resize_table(data):
    create_tex_resize_title(data[0], data[1])
    for i in data[2:]:
        create_tex_body(i)
    create_tex_resize_tail()

# >>>>>>>>>>>>>>>>>>>

def create_tex_long_tail():
    global tex
    tex += '\\end{longtable}\n' + \
           '\\par\n' + \
           '\\sphinxattableend\\end{savenotes}\n'

def create_tex_long_title(align, data):
    global tex
    tex += '\\begin{savenotes}\\sphinxattablestart\n' + \
           '\\rowcolors{2}{gray!20}{white}\n' + \
           '\\centering\n' + \
           '\\begin{longtable}[c]{|'
    for i in align:
        tex += i + '|'
    tex += '}\n\\hline\n'
    tex += '\\sphinxstyletheadfamily\n' + data[0] + '\n'
    for i in data[1:]:
        tex += '&\\sphinxstyletheadfamily\n' + i + '\n'
    tex += '\\\\%\n' + '\\hline\n'

def create_tex_long_table(data):
    create_tex_long_title(data[0], data[1])
    for i in data[2:]:
        create_tex_body(i)
    create_tex_long_tail()

# >>>>>>>>>>>>>>>>>>>

def create_tex_tail():
    global tex
    tex += '\\end{tabulary}\n' + \
           '\\par\n' + \
           '\\end{table*}\n'

def create_tex_title(align, data):
    global tex
    tex += '\\begin{table*}\n' + \
           '\\rowcolors{2}{gray!20}{white}\n' + \
           '\\centering\n' + \
           '\\begin{tabulary}{\\linewidth}[t]{|'
    for i in align:
        tex += i + '|'
    tex += '}\n\\hline\n'
    tex += '\\sphinxstyletheadfamily\n' + data[0] + '\n'
    for i in data[1:]:
        tex += '&\\sphinxstyletheadfamily\n' + i + '\n'
    tex += '\\\\%\n' + '\\hline\n'

def create_tex_table(data):
    create_tex_title(data[0], data[1])
    for i in data[2:]:
        create_tex_body(i)
    create_tex_tail()

# >>>>>>>>>>>>>>>>>>

def create_tex_x_tail():
    global tex
    tex += '\\end{tabularx}\n' + \
           '\\par\n' + \
           '\\end{table*}\n' + \
           '\\FloatBarrier\n'

def create_tex_x_title(align, data):
    global tex
    tex += '\\FloatBarrier\n' + \
           '\\begin{table*}\n' + \
           '\\rowcolors{1}{gray!20}{white}\n' + \
           '\\centering\n' + \
           '\\begin{tabularx}{\\textwidth}[t]{|'
    for i in align:
        if i == 'c':
            tex += 'X<{\\centering\\arraybackslash}|'
        elif i == 'l':
            tex += 'X<{\\raggedright\\arraybackslash}|'
        elif i == 'r':
            tex += 'X<{\\raggedleft\\arraybackslash}|'
    tex += '}\n\\hline\n'
    tex += '\\sphinxstyletheadfamily\n' + data[0] + '\n'
    for i in data[1:]:
        tex += '&\\sphinxstyletheadfamily\n' + i + '\n'
    tex += '\\\\%\n' + '\\hline\n'

def create_tex_x_table(data):
    create_tex_x_title(data[0], data[1])
    for i in data[2:]:
        create_tex_body(i)
    create_tex_x_tail()

# >>>>>>>>>>>>>>>>>>

def create_tex_des_title(data):
    global tex
    tex += '\\FloatBarrier\n' + \
           '\\begin{table*}[htbp]\n' + \
           '\\rowcolors{1}{gray!20}{white}\n' + \
           '\\centering\n' + \
           '\\begin{tabularx}{\\textwidth}[t]{|c|l|c|c|'
    tex += 'X<{\\raggedright\\arraybackslash}|'
    tex += '}\n\\hline\n'
    tex += '\\sphinxstyletheadfamily\n' + data[0] + '\n'
    for i in data[1:]:
        tex += '&\\sphinxstyletheadfamily\n' + i + '\n'
    tex += '\\\\%\n' + '\\hline\n'

def create_tex_des_table(data):
    create_tex_des_title(data[1])
    for i in data[2:]:
        create_tex_body(i)
    create_tex_x_tail()

# >>>>>>>>>>>>>>>>>>

def setup(app):
    app.connect('source-read', process_tables)
    return {'version': __version__,
            'parallel_read_safe': True}


def process_tables(app, docname, source):
    """
    Convert markdown tables to html, since recommonmark can't. This requires 3 steps:
        Snip out table sections from the markdown
        Convert them to html
        Replace the old markdown table with an html table

    This function is called by sphinx for each document. `source` is a 1-item list. To update the document, replace
    element 0 in `source`.
    """
    global tex
    import markdown
    md = markdown.Markdown(extensions=['markdown.extensions.tables'])
    table_processor = markdown.extensions.tables.TableProcessor(md.parser)

    raw_markdown = source[0]
    blocks = re.split(r'(\n{2,})', raw_markdown)

    for i, block in enumerate(blocks):
        if table_processor.test(None, block):
            data = get_table_msg(block)
            if len(data) >= 40:
                create_tex_long_table(data)
            elif len(data[0]) >=4:
                if len(data[0]) == 5 and data[1] == ['位域','变量名', '属性', '默认值', '描述']:
                    create_tex_des_table(data)
                else:
                    create_tex_resize_table(data)
            else:
                create_tex_x_table(data)
            blocks[i] = tex
            tex = ''
            #html = md.convert(block)
            #styled = html.replace('<table>', '<table border="1" class="docutils">', 1)  # apply styling
            #blocks[i] = styled

    # re-assemble into markdown-with-tables-replaced
    # must replace element 0 for changes to persist
    source[0] = ''.join(blocks)


def get_table_msg(block):
    data = []
    start = 0
    lines = block.strip('\n').split('\n')
    for line in lines:
        line = line.replace('&', '§')
        if line.find(':-') >= 0 or line.find('-:') >= 0 or line.find('--')>= 0:
            line = line.strip(' \n')
            tmp = line.strip('|').split('|')
            for i in range(len(tmp)):
                if tmp[i].find(':-') >= 0 and tmp[i].find('-:') < 0:
                    data[0][i] = 'l'
                elif tmp[i].find('-:') >= 0 and tmp[i].find(':-') < 0:
                    data[0][i] = 'r'
            continue
        if start == 1:
            line = line.strip(' \n')
            tmp = line.strip('|').split('|')
            data.append(tmp)
        if start == 0:
            start = 1
            align = []
            line = line.strip(' \n')
            tmp = line.strip('|').split('|')
            for i in tmp:
                align.append('c')
            data.append(align)
            data.append(tmp)
    return data

