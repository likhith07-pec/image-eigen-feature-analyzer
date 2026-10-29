import re
import html

def markdown_to_html(md_text):
    # Convert \newpage to page breaks
    md_text = md_text.replace(r'\newpage', '<div class="page-break"></div>')
    
    # Simple regex-based markdown converter suitable for standard report format
    lines = md_text.split('\n')
    html_lines = []
    in_code = False
    code_block = []
    in_table = False
    table_lines = []

    for line in lines:
        if line.startswith('```'):
            if in_code:
                in_code = False
                code_content = html.escape('\n'.join(code_block))
                html_lines.append(f'<pre><code>{code_content}</code></pre>')
                code_block = []
            else:
                in_code = True
                code_block = []
            continue

        if in_code:
            code_block.append(line)
            continue

        # Table detection
        if line.strip().startswith('|') and line.strip().endswith('|'):
            if not in_table:
                in_table = True
                table_lines = [line]
            else:
                table_lines.append(line)
            continue
        else:
            if in_table:
                in_table = False
                # Process table
                html_table = ['<div class="table-container"><table>']
                for r_idx, t_line in enumerate(table_lines):
                    cells = [c.strip() for c in t_line.strip().split('|')[1:-1]]
                    if r_idx == 1 and all(set(c).issubset({'-', ':', ' '}) for c in cells):
                        continue # separator line
                    tag = 'th' if r_idx == 0 else 'td'
                    row_html = '<tr>' + ''.join(f'<{tag}>{html.escape(c)}</{tag}>' for c in cells) + '</tr>'
                    html_table.append(row_html)
                html_table.append('</table></div>')
                html_lines.extend(html_table)
                table_lines = []

        # Headings
        if line.startswith('# '):
            html_lines.append(f'<h1>{line[2:].strip()}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:].strip()}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{line[4:].strip()}</h3>')
        elif line.startswith('#### '):
            html_lines.append(f'<h4>{line[5:].strip()}</h4>')
        elif line.startswith('> '):
            html_lines.append(f'<blockquote>{line[2:].strip()}</blockquote>')
        elif line.strip() == '---':
            html_lines.append('<hr>')
        elif line.strip().startswith('* ') or line.strip().startswith('- '):
            html_lines.append(f'<li>{line.strip()[2:]}</li>')
        elif line.strip() == '':
            html_lines.append('<p></p>')
        else:
            # Inline bold/code
            processed = line
            # Convert [INSERT FIGURE...] to a callout box
            if '[INSERT FIGURE' in processed:
                processed = f'<div class="figure-placeholder"><strong>📷 {processed}</strong></div>'
            html_lines.append(f'<p>{processed}</p>')

    if in_table and table_lines:
        html_table = ['<div class="table-container"><table>']
        for r_idx, t_line in enumerate(table_lines):
            cells = [c.strip() for c in t_line.strip().split('|')[1:-1]]
            if r_idx == 1 and all(set(c).issubset({'-', ':', ' '}) for c in cells):
                continue
            tag = 'th' if r_idx == 0 else 'td'
            row_html = '<tr>' + ''.join(f'<{tag}>{html.escape(c)}</{tag}>' for c in cells) + '</tr>'
            html_table.append(row_html)
        html_table.append('</table></div>')
        html_lines.extend(html_table)

    content = '\n'.join(html_lines)
    
    # Replace inline bold and italic
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>EigenLab - Academic Mini-Project Report</title>
<style>
    @page {{
        size: A4;
        margin: 2.54cm;
    }}
    body {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 12pt;
        line-height: 1.6;
        color: #111;
        max-width: 850px;
        margin: 0 auto;
        padding: 40px;
        background: #fff;
    }}
    .page-break {{
        page-break-after: always;
        break-after: page;
        margin-top: 40px;
        border-top: 1px dashed #ccc;
    }}
    @media print {{
        .page-break {{
            border-top: none;
            margin-top: 0;
        }}
        body {{
            padding: 0;
            max-width: 100%;
        }}
    }}
    h1 {{
        font-size: 18pt;
        text-align: center;
        text-transform: uppercase;
        margin-top: 24pt;
        margin-bottom: 12pt;
        color: #000000;
    }}
    h2 {{
        font-size: 15pt;
        margin-top: 18pt;
        margin-bottom: 9pt;
        border-bottom: 1px solid #000000;
        padding-bottom: 4px;
        color: #000000;
    }}
    h3 {{
        font-size: 13pt;
        margin-top: 14pt;
        margin-bottom: 6pt;
        color: #000000;
    }}
    p {{
        text-align: justify;
        text-justify: inter-word;
        margin-bottom: 8pt;
    }}
    blockquote {{
        border-left: 3px solid #000000;
        padding-left: 15px;
        margin-left: 0;
        font-style: italic;
        color: #111111;
        background: #fafafa;
        padding-top: 8px;
        padding-bottom: 8px;
    }}
    .figure-placeholder {{
        background: #ffffff;
        border: 1px dashed #666666;
        padding: 16px;
        margin: 18px 0;
        text-align: center;
        font-family: 'Times New Roman', Times, serif;
        color: #000000;
        border-radius: 4px;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 16pt 0;
        font-size: 10.5pt;
        border-top: 2px solid #000000;
        border-bottom: 2px solid #000000;
    }}
    th, td {{
        border: none;
        border-bottom: 1px solid #cccccc;
        padding: 8px 10px;
        text-align: left;
    }}
    th {{
        border-bottom: 1.5px solid #000000;
        background-color: #ffffff;
        font-weight: bold;
        color: #000000;
    }}
    pre {{
        background: #fcfcfc;
        border: 1px solid #e0e0e0;
        padding: 12px;
        overflow-x: auto;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 10pt;
        line-height: 1.4;
        border-radius: 4px;
    }}
    code {{
        font-family: 'Consolas', 'Courier New', monospace;
        background: #f5f5f5;
        padding: 2px 4px;
        border-radius: 3px;
    }}
    hr {{
        border: none;
        border-top: 1px solid #000000;
        margin: 20pt 0;
    }}
    li {{
        margin-bottom: 4pt;
    }}
</style>
</head>
<body>
{content}
</body>
</html>
"""
    return html_doc

with open('docs/IEEE_MINI_PROJECT_REPORT.md', 'r', encoding='utf-8') as f:
    text = f.read()

html_output = markdown_to_html(text)

with open('docs/IEEE_MINI_PROJECT_REPORT.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

print("Successfully generated docs/IEEE_MINI_PROJECT_REPORT.html")
