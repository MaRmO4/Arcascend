path = '/Users/marioarcata/Desktop/arcascend/intake.html'
html = open(path).read()

# Find the hardcoded fields section - between </div> after form-head and the submit button
# Replace everything between form-head closing and submit button with dynamic container
old_fields_start = html.find('</div>\n    </div>\n    <div class="section">')
if old_fields_start == -1:
    old_fields_start = html.find('</div>\n  </div>\n  <div class="section">')

submit_btn = html.find('<button class="submit-btn"')
print('Fields start:', old_fields_start)
print('Submit btn:', submit_btn)

# Get the section between form-head and submit button
old_fields = html[old_fields_start:submit_btn]
print('Old fields length:', len(old_fields))
print('First 100:', old_fields[:100])
