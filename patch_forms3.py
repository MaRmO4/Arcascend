path = '/Users/marioarcata/Desktop/arcascend/public/index.html'
html = open(path).read()

# Find where main div is
main_idx = html.find('<div id="main"')
print('main div at:', main_idx)

# Find where tab-forms starts and remove it from current location
forms_start = html.find('<div id="tab-forms"')
print('tab-forms at:', forms_start)

# Find the closing of tab-forms by counting divs
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

print('tab-forms ends at:', forms_end)
print('panel length:', forms_end - forms_start)

# Extract the panel
forms_panel = html[forms_start:forms_end]
print('Panel preview:', forms_panel[:80])

# Remove from current location
html = html[:forms_start] + html[forms_end:]

# Insert right after <div id="main"...> opening tag
main_idx = html.find('<div id="main"')
main_end = html.find('>', main_idx) + 1
html = html[:main_end] + '\n' + forms_panel + '\n' + html[main_end:]

open(path, 'w').write(html)
print('DONE')
