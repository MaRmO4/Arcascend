path = '/Users/marioarcata/Desktop/arcascend/intake.html'
html = open(path).read()

# Find the first <div class="field"> and the submit button - replace everything between them
fields_start = html.find('<div class="field">')
submit_start = html.find('<button class="submit-btn"')

print('Fields start:', fields_start)
print('Submit start:', submit_start)

old_fields = html[fields_start:submit_start]
print('Replacing', len(old_fields), 'chars of hardcoded fields')

new_fields = '<div id="dynamic-fields"></div>\n    '

html = html[:fields_start] + new_fields + html[submit_start:]

# Now replace the entire <script> block with our dynamic version
old_script_start = html.find('<script>')
old_script_end = html.find('</script>') + 9
old_script = html[old_script_start:old_script_end]
print('Old script length:', len(old_script))

new_script = """<script>
var SUPABASE_URL = 'https://udzfpeztwgsynjhwjwic.supabase.co';
var SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVkemZwZXp0d2dzeW5qaHdqd2ljIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk2OTcwOTcsImV4cCI6MjA5NTI3MzA5N30.Eke_HxZtww3zVekkPMDydT90NkVWSltJjA2fr40oquQ';
var params = new URLSearchParams(window.location.search);
v
cat > /Users/marioarcata/Desktop/arcascend/patch_intake2.py << 'ENDOFSCRIPT'
path = '/Users/marioarcata/Desktop/arcascend/intake.html'
html = open(path).read()

# Find the first <div class="field"> and the submit button - replace everything between them
fields_start = html.find('<div class="field">')
submit_start = html.find('<button class="submit-btn"')

print('Fields start:', fields_start)
print('Submit start:', submit_start)

old_fields = html[fields_start:submit_start]
print('Replacing', len(old_fields), 'chars of hardcoded fields')

new_fields = '<div id="dynamic-fields"></div>\n    '

html = html[:fields_start] + new_fields + html[submit_start:]

# Now replace the entire <script> block with our dynamic version
old_script_start = html.find('<script>')
old_script_end = html.find('</script>') + 9
old_script = html[old_script_start:old_script_end]
print('Old script length:', len(old_script))

new_script = """<script>
var SUPABASE_URL = 'https://udzfpeztwgsynjhwjwic.supabase.co';
var SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVkemZwZXp0d2dzeW5qaHdqd2ljIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk2OTcwOTcsImV4cCI6MjA5NTI3MzA5N30.Eke_HxZtww3zVekkPMDydT90NkVWSltJjA2fr40oquQ';
var params = new URLSearchParams(window.location.search);
var TRAINER_ID = params.get('trainer') || 'a83ab75d-0b97-4729-9cf6-7630c2c03115';

var FALLBACK_QUESTIONS = [
  { id:'q_name',     label:'Full Name',                          type:'text',     required:true,  options:[] },
  { id:'q_phone',    label:'Phone Number',                       type:'tel',      required:true,  options:[] },
  { id:'q_email',    label:'Email Address',                      type:'email',    required:false, options:[] },
  { id:'q_goal',     label:'What is your primary fitness goal?', type:'textarea', required:true,  options:[] },
  { id:'q_level',    label:'Training experience level',          type:'select',   required:true,  options:['Beginner','Intermediate','Advanced'] },
  { id:'q_timeline', label:'What is your timeline?',             type:'select',   required:false, options:['ASAP','1-3 months','3-6 months','6+ months'] },
  { id:'q_style',    label:'Preferred training style',           type:'select',   required:false, options:['1-on-1','Small group','Online','No preference'] },
  { id:'q_injuries', label:'Any injuries or limitations?',       type:'textarea', required:false, options:[] },
  { id:'q_avail',    label:'Availability (days/times)',          type:'text',     required:false, options:[] },
  { id:'q_whynow',   label:'Why are you starting now?',          type:'textarea', required:false, options:[] },
  { id:'q_outcomes', label:'Desired outcomes',                   type:'textarea', required:false, options:[] },
  { id:'q_other',    label:'Anything else we should know?',      type:'textarea', required:false, options:[] },
];

var loadedQuestions = [];
var loadedBucket = '';

async function loadForm() {
  try {
    var res = await fetch(SUPABASE_URL + '/rest/v1/trainer_settings?user_id=eq.' + TRAINER_ID + '&select=gym_name,form_title,form_description,logo_url,questions,default_bucket', {
      headers: { 'apikey': SUPABASE_KEY, 'Authorization': 'Bearer ' + SUPABASE_KEY }
    });
    var rows = await res.json();
    var s = rows && rows[0] ? rows[0] : {};

    // Apply branding
    if (s.form_title) {
      document.getElementById('form-title').textContent = s.form_title;
      document.title = s.form_title;
    }
    if (s.form_description) document.getElementById('form-desc').textContent = s.form_description;
    if (s.logo_url) {
      document.getElementById('header-img').src = s.logo_url;
      document.getElementById('header-img').style.objectFit = 'contain';
      document.getElementById('header-img').style.background = '#111';
    }

    loadedBucket = s.default_bucket || '';
    loadedQuestions = (s.questions && s.questions.length > 0) ? s.questions : FALLBACK_QUESTIONS;
  } catch(e) {
    loadedQuestions = FALLBACK_QUESTIONS;
  }
  renderFields();
}

function renderFields() {
  var container = document.getElementById('dynamic-fields');
  container.innerHTML = loadedQuestions.map(function(q) {
    var req = q.required ? '<span class="req">*</span>' : '';
    var field = '';

    if (q.type === 'textarea') {
      field = '<textarea id="' + q.id + '" name="' + q.id + '"' + (q.required ? ' required' : '') + '></textarea>';
    } else if (q.type === 'select') {
      var opts = '<option value="">Choose</option>' + (q.options||[]).map(function(o) {
        return '<option value="' + o + '">' + o + '</option>';
      }).join('');
      field = '<select id="' + q.id + '" name="' + q.id + '"' + (q.required ? ' required' : '') + '>' + opts + '</select>';
    } else if (q.type === 'multiselect') {
      field = '<div>' + (q.options||[]).map(function(o) {
        return '<label class="opt"><input type="checkbox" name="' + q.id + '" value="' + o + '"> ' + o + '</label>';
      }).join('') + '</div>';
    } else {
      field = '<input type="' + q.type + '" id="' + q.id + '" name="' + q.id + '"' + (q.required ? ' required' : '') + '>';
    }

    return '<div class="field"><label>' + q.label + req + '</label>' + field + '</div>';
  }).join('');
}

function submitForm() {
  var btn = document.getElementById('submit-btn');
  var fields = {};

  loadedQuestions.forEach(function(q) {
    if (q.type === 'multiselect') {
      var checked = Array.from(document.querySelectorAll('input[name="' + q.id + '"]:checked')).map(function(c){ return c.value; });
      fields[q.id] = checked.join(', ');
    } else {
      var el = document.getElementById(q.id);
      fields[q.id] = el ? el.value : '';
    }
  });

  // Validate required
  var missing = loadedQuestions.filter(function(q) { return q.required && !fields[q.id]; });
  if (missing.length > 0) {
    alert('Please fill in: ' + missing.map(function(q){ return q.label; }).join(', '));
    return;
  }

  var lead = {
    user_id: TRAINER_ID,
    name:    fields['q_name']  || '',
    phone:   fields['q_phone'] || '',
    email:   fields['q_email'] || '',
    status:  'New',
    data: JSON.stringify(Object.assign({}, fields, {
      source: 'Intake Form',
      bucket: loadedBucket,
      submittedAt: new Date().toISOString()
    }))
  };

  btn.disabled = true;
  btn.textContent = 'Submitting...';

  fetch(SUPABASE_URL + '/rest/v1/leads', {
    method: 'POST',
    headers: {
      'apikey': SUPABASE_KEY,
      'Authorization': 'Bearer ' + SUPABASE_KEY,
      'Content-Type': 'application/json',
      'Prefer': 'return=minimal'
    },
    body: JSON.stringify(lead)
  }).then(function(resp) {
    if (resp.ok || resp.status === 201) {
      document.getElementById('form-wrap').innerHTML = '<div class="success"><div class="success-icon">✅</div><h2>You\'re all set!</h2><p>We\'ll be in touch with you shortly.</p></div>';
    } else {
      btn.disabled = false;
      btn.textContent = 'Submit & Get Started';
      alert('Something went wrong. Please try again.');
    }
  }).catch(function(e) {
    btn.disabled = false;
    btn.textContent = 'Submit & Get Started';
    alert('Error: ' + e.message);
  });
}

loadForm();
</script>"""

html = html[:old_script_start] + new_script + html[old_script_end:]
open(path, 'w').write(html)
print('DONE - intake.html patched successfully')
