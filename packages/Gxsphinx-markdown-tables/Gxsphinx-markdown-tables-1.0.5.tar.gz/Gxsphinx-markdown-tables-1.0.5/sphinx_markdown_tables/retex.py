#!/usr/bin/env python3

import os
import sys


def main():
    in_file = sys.argv[1]
    new_file = "new_file.tex"
    
    def check_pdf_tex(pdf_tex):
        new_pdf_tex = 'new_' + pdf_tex
        ft = open(pdf_tex, 'r')
        fn = open(new_pdf_tex, 'w')
        while 1:
            line = ft.readline()
            if line.find('_') >= 0 and line.find('\includegraphics') <= 0:
                fn.write(line.replace('_', '\\_').replace('&', '\\&'))
            elif line.find('&') >= 0 and line.find('\put') <= 0:
                fn.write(line.replace('&', '\\&').replace('_', '\\_'))
            else:
                fn.write(line)
            if not line:
                break
        ft.close()
        fn.close()
        mv_cmd = 'mv ' + new_pdf_tex + ' ' + pdf_tex
        os.system(mv_cmd)
    
    fi = open(in_file, 'r')
    fo = open(new_file, 'w')
    table_start = 0
    while 1:
        line = fi.readline()
        if line.find('\\sphinxattablestart') >= 0:
            table_start = 1
        if line.find('\\sphinxattableend') >= 0:
            table_start = 0
        if line.startswith('\\sphinxincludegraphics') and \
                line.find('.svg') >= 0 and line.find('.drawio') < 0:
            reg_name = line.split('{{')[1].split('}')[0]
            print(reg_name)
            svg_cmd = "inkscape -D -z --file=" + reg_name + ".svg --export-pdf=" + \
                    reg_name + ".pdf --export-latex"
            os.system(svg_cmd)
            check_pdf_tex(reg_name + '.pdf_tex')
    
            msg = '\\FloatBarrier\n'
            msg += '\\begin{figure}[htbp]\n\\centering\n\\def\\svgwidth{\\columnwidth}\n'
            msg += '\\footnotesize\n'
            msg += '\\input{' + reg_name + '.pdf_tex}\n'
            msg += '\\caption{寄存器' + reg_name.replace("_", "\\_") + '}\n'
            msg += '\\end{figure}\n'
            msg += '\\FloatBarrier\n'
            fo.write(msg)
            print(line, end = '')
        elif line.startswith('\\sphinxincludegraphics') and \
                line.find('.svg') >= 0 and line.find('.drawio') >= 0:
            svg_path = line.split('{{')[1].split('}')[0]
            svg_name = os.path.basename(svg_path)
            new_svg_name = svg_name.replace('.drawio', '')
            os.system("cp " + svg_name + '.svg ' + new_svg_name + '.svg')
            svg_cmd = "inkscape -D -z --file=" + new_svg_name + ".svg --export-pdf=" + \
                    new_svg_name + ".pdf --export-latex"
            os.system(svg_cmd)
            check_pdf_tex(new_svg_name + '.pdf_tex')
    
            msg = '\\FloatBarrier\n'
            msg += '\\begin{figure}[htbp]\n\\centering\n\\def\\svgwidth{\\columnwidth}\n'
            msg += '\\footnotesize\n'
            msg += '\\input{' + new_svg_name + '.pdf_tex}\n'
            msg += '\\caption{寄存器' + new_svg_name.replace("_", "\\_") + '}\n'
            msg += '\\end{figure}\n'
            msg += '\\FloatBarrier\n'
            fo.write(msg)
            print(line, end = '')
        elif line.startswith('\\sphinxstylestrong'):
            fo.write(line)
            fo.write('\\\\' +  '\n')
        #elif line.find('reset\\_value') >= 0:
        #    tmp = line.strip('\n').split('reset\\_value')
        #    msg = tmp[0] + '\n\\\\\n' + 'reset\\_value' + tmp[1] + '\n' + '\\\\\n'
        #    fo.write(msg)
        elif line.find('地址偏移') >= 0 and line.find('默认值') >= 0:
            tmp = line.strip('\n').split('默认值')
            msg = tmp[0] + '\n\\\\\n' + '默认值' + tmp[1] + '\n' + '\\\\\n'
            fo.write(msg)
        elif line.startswith('\\usepackage{xeCJK}'):
            msg = line
            #msg += '\\usepackage{hyperref}\n'
            msg += '\\usepackage[section]{placeins}\n'
            msg += '\\usepackage{setspace}\n'
            msg += '\\usepackage{tabularx}\n'
            msg += '\\usepackage{array}\n'
            msg += '\\usepackage{longtable}\n'
            msg += '\\usepackage[table]{xcolor}\n'
            msg += '\\renewcommand\\arraystretch{1.5}\n'
            msg += '\\renewcommand\\baselinestretch{1.5}\n'
            fo.write(msg)
        else:
            fo.write(line)
        if not line:
            break
    fi.close()
    fo.close()
    mv_cmd = 'mv ' + new_file + ' ' + in_file
    print(mv_cmd)
    os.system(mv_cmd)

if __name__ == "__main__":
    main()
