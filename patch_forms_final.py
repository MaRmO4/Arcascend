path = '/Users/marioarcata/Desktop/arcascend/public/index.html'
html = open(path).read()

# Find and extract the full tab-forms panel
forms_start = html.find('<div id="tab-forms"')
depth = 0
i = forms_start
while i < len(html):
    if html[i:i+4] == '<div':
        depth += 1
    elif html[i:i+6] == '</div>':
        depth -= 1
        if depth == 0:
            forms_end = i + 6
            break
    i += 1

forms_panel = html[forms_start:forms_end]
print('Panel length:', len(forms_panel))

# Remove from current location
html = html[:forms_start] + html[forms_end:]

# Place it just before </body>
html = html.replace('</body>', forms_panel + '\n</body>')

open(path, 'w').write(html)
print('DONE - forms panel moved to before </body>')
print('forms in html:', 'tab-forms' in html)
