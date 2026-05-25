#!/usr/bin/env python3
"""
Conversione semplificata: LaTeX Book → HTML professionale
Legge il file LaTeX e genera un HTML bello e stampabile come PDF
"""

import re
import sys

# Leggi il file LaTeX
try:
    with open('Qwen_latex_20260525_q1q77517p.txt', 'r', encoding='utf-8', errors='ignore') as f:
        latex_content = f.read()
except FileNotFoundError:
    print("Errore: Qwen_latex_20260525_q1q77517p.txt non trovato!")
    sys.exit(1)

print(f"✓ Letto {len(latex_content)} caratteri da LaTeX")

# Rimuovi preambolo LaTeX fino a \begin{document}
content_match = re.search(r'\\begin\{document\}', latex_content)
if content_match:
    latex_content = latex_content[content_match.end():]

# Rimuovi \end{document}
latex_content = re.sub(r'\\end\{document\}', '', latex_content)

# Gestisci gli ambienti itemize/enumerate
def parse_lists(text):
    """Convertere liste itemize/enumerate in HTML"""
    result = []
    in_itemize = False
    in_enumerate = False
    
    for line in text.split('\n'):
        line = line.strip()
        
        # Skip linee vuote multiple
        if not line:
            continue
            
        # Inizio itemize
        if '\\begin\{itemize\}' in line or '\\begin{itemize}' in line:
            in_itemize = True
            result.append('<ul class="itemize">')
            continue
        # Fine itemize
        elif '\\end\{itemize\}' in line or '\\end{itemize}' in line:
            in_itemize = False
            result.append('</ul>')
            continue
        # Inizio enumerate
        elif '\\begin\{enumerate\}' in line:
            in_enumerate = True
            result.append('<ol class="enumerate">')
            continue
        # Fine enumerate
        elif '\\end\{enumerate\}' in line:
            in_enumerate = False
            result.append('</ol>')
            continue
        # Item
        elif '\\item' in line:
            item_text = line.replace('\\item', '').strip()
            if item_text.startswith('[') and ']' in item_text:
                item_text = item_text[item_text.find(']')+1:].strip()
            result.append(f'<li>{clean_latex(item_text)}</li>')
            continue
            
        result.append(line)
    
    return '\n'.join(result)

def clean_latex(text):
    """Pulisce comandi LaTeX base"""
    # Rimuovi comandi math mode
    text = re.sub(r'\$.*?\$', lambda m: m.group(0).replace('$', ''), text)
    text = re.sub(r'\\\[.*?\\\]', '', text)
    text = re.sub(r'\\\(.*?\\\)', '', text)
    
    # Sostituisci ambienti
    text = text.replace('\\centering', '')
    text = text.replace('\\textbf', '<strong>')
    text = text.replace('\\textit', '<em>')
    text = text.replace('\\emph', '<em>')
    text = text.replace('\\textcolor', '<span style="color:')
    text = text.replace('{red}', '#d00">')
    text = text.replace('{green}', '#060">')
    text = text.replace('{blue}', '#006">')
    text = text.replace('{black}', '#000">')
    text = re.sub(r'\}', '</span>', text, count=1)
    
    # Rimuovi altri comandi LaTeX
    text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    text = re.sub(r'\{|\}', '', text)
    
    return text

# Parsing base delle sezioni
sections = []
current_section = []
in_table = False

for line in latex_content.split('\n'):
    line = line.strip()
    
    # Salta commenti e comandi
    if line.startswith('%') or not line:
        continue
    
    # Section
    if line.startswith('\\section'):
        if current_section:
            sections.append(('\n'.join(current_section), 'section'))
            current_section = []
        title = re.sub(r'\\section\*?\{', '', line)
        title = title.replace('}', '')
        current_section.append(f'<h1>{title}</h1>')
        continue
    
    # Subsection
    if line.startswith('\\subsection'):
        title = re.sub(r'\\subsection\*?\{', '', line)
        title = title.replace('}', '')
        current_section.append(f'<h2>{title}</h2>')
        continue
    
    # Subsubsection
    if line.startswith('\\subsubsection'):
        title = re.sub(r'\\subsubsection\*?\{', '', line)
        title = title.replace('}', '')
        current_section.append(f'<h3>{title}</h3>')
        continue
    
    # Paragraph
    if line.startswith('\\paragraph'):
        title = re.sub(r'\\paragraph\*?\{', '', line)
        title = title.replace('}', '')
        current_section.append(f'<h4>{title}</h4>')
        continue
    
    # Parola chiave (textbf)
    line = re.sub(r'\\textbf\{([^}]+)\}', r'<strong>\1</strong>', line)
    line = re.sub(r'\\textit\{([^}]+)\}', r'<em>\1</em>', line)
    
    # Pulisci
    line = clean_latex(line)
    
    if line:
        current_section.append(f'<p>{line}</p>')

if current_section:
    sections.append(('\n'.join(current_section), 'section'))

# Genera HTML finale
html = '''<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analisi del Sistema Monetario e Bancario Contemporaneo</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: Georgia, 'Times New Roman', serif; 
            font-size: 12pt; 
            line-height: 1.6; 
            color: #333;
            max-width: 210mm;
            margin: 0 auto;
            padding: 20px;
            background: #fafafa;
        }
        h1 { 
            font-size: 24pt; 
            color: #1a1a2e; 
            border-bottom: 3px solid #1a1a2e;
            padding-bottom: 10px;
            margin: 30px 0 20px 0;
            page-break-before: always;
        }
        h2 { 
            font-size: 18pt; 
            color: #16213e; 
            border-left: 5px solid #0f3460;
            padding-left: 15px;
            margin: 25px 0 15px 0;
            page-break-after: avoid;
        }
        h3 { 
            font-size: 14pt; 
            color: #0f3460; 
            margin: 20px 0 10px 0;
            font-weight: bold;
        }
        h4 {
            font-size: 12pt;
            color: #533483;
            margin: 15px 0 8px 0;
            font-weight: bold;
        }
        p { 
            margin: 8px 0; 
            text-align: justify;
            hyphens: auto;
        }
        ul, ol { 
            margin: 10px 0 10px 20px; 
        }
        li {
            margin: 5px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 10pt;
        }
        th, td {
            border: 1px solid #333;
            padding: 8px;
            text-align: left;
            vertical-align: top;
        }
        th {
            background: #1a1a2e;
            color: white;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background: #f5f5f5;
        }
        blockquote {
            border-left: 4px solid #e94560;
            margin: 15px 0;
            padding: 10px 20px;
            background: #f9f9f9;
            font-style: italic;
        }
        code {
            font-family: 'Courier New', monospace;
            background: #eee;
            padding: 2px 6px;
        }
        .page-break { page-break-before: always; }
        @media print {
            body { background: white; }
            h1, h2, h3 { page-break-after: avoid; }
        }
    </style>
</head>
<body>
'''

# Aggiungi contenuto
for content, sect_type in sections:
    html += content

html += '''
</body>
</html>
'''

# Salva
output_file = 'ebook_sistema_monetario.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✓ Ebook generato: {output_file}")
print(f"  - Apri nel browser")
print(f"  - Stampa come PDF (Ctrl+P)")
print(f"  - Oppure carica su Amazon KDP")