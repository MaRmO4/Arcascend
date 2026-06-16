path = '/Users/marioarcata/Desktop/arcascend/public/index.html'
html = open(path).read()

old_init = """async function formsInit() {
  if (!currentUser) return;
  const link = 'https://arcascend.app/intake.html?trainer=' + currentUser.id;
  document.getElementById('forms-link-input').value = link;
  document.getElementById('forms-open-btn').href = link;
  const qrEl = document.getElementById('forms-qr');
  qrEl.innerHTML = '';
  if (typeof QRCode !== 'undefined') new QRCode(qrEl, { text: link, width:100, height:100, colorDark:'#000', colorLight:'#fff', correctLevel: QRCode.CorrectLevel.M });
  const { data } = await supabase.from('trainer_settings').select('*').eq('user_id', currentUser.id).single();
  if (data) {
    formsSettings = data;
    document.getElementById('forms-gym-name').value    = data.gym_name || '';
    document.getElementById('forms-form-title').value  = data.form_title || '';
    document.getElementById('forms-form-desc').value   = data.form_description || '';
    document.getElementById('forms-logo-url').value    = data.logo_url || '';
    document.getElementById('forms-bucket').value      = data.default_bucket || '';
    formsPreviewLogo(data.logo_url);
    formsQuestions = (data.questions && data.questions.length > 0) ? data.questions : JSON.parse(JSON.stringify(INTAKE_DEFAULT_QUESTIONS));
  } else {
    formsQuestions = JSON.parse(JSON.stringify(INTAKE_DEFAULT_QUESTIONS));
  }
  formsRenderQuestions();
  document.getElementById('forms-logo-url').addEventListener('input', function(e) { formsPreviewLogo(e.target.value); });
}"""

new_init = """async function formsInit() {
  if (!currentUser) return;
  var link = 'https://arcascend.app/intake.html?trainer=' + currentUser.id;
  document.getElementById('forms-link-input').value = link;
  document.getElementById('forms-open-btn').href = link;
  var qrEl = document.getElementById('forms-qr');
  qrEl.innerHTML = '';
  if (typeof QRCode !== 'undefined') new QRCode(qrEl, { text: link, width:100, height:100, colorDark:'#000', colorLight:'#fff', correctLevel: QRCode.CorrectLevel.M });
  var token = localStorage.getItem('arcascend_token');
  try {
    var res = await fetch(SUPABASE_URL + '/rest/v1/trainer_settings?user_id=eq.' + currentUser.id + '&select=*', {
      headers: { 'Authorization': 'Bearer ' + token, 'apikey': SUPABASE_KEY }
    });
    var rows = await res.json();
    var data = rows && rows[0] ? rows[0] : null;
    if (data) {
      formsSettings = data;
      document.getElementById('forms-gym-name').value   = data.gym_name || '';
      document.getElementById('forms-form-title').value = data.form_title || '';
      document.getElementById('forms-form-desc').value  = data.form_description || '';
      document.getElementById('forms-logo-url').value   = data.logo_url || '';
      document.getElementById('forms-bucket').value     = data.default_bucket || '';
      formsPreviewLogo(data.logo_url);
      formsQuestions = (data.questions && data.questions.length > 0) ? data.questions : JSON.parse(JSON.stringify(INTAKE_DEFAULT_QUESTIONS));
    } else {
      formsQuestions = JSON.parse(JSON.stringify(INTAKE_DEFAULT_QUESTIONS));
    }
  } catch(e) { formsQuestions = JSON.parse(JSON.stringify(INTAKE_DEFAULT_QUESTIONS)); }
  formsRenderQuestions();
  document.getElementById('forms-logo-url').addEventListener('input', function(e) { formsPreviewLogo(e.target.value); });
}"""

old_save = """async function formsSaveSettings() {
  if (!currentUser) return;
  const statusEl = document.getElementById('forms-save-status');
  statusEl.textContent = 'Saving...';
  const { error } = await supabase.from('trainer_settings').upsert({
    user_id: currentUser.id,
    gym_name: document.getElementById('forms-gym-name').value.trim(),
    form_title: document.getElementById('forms-form-title').value.trim(),
    form_description: document.getElementById('forms-form-desc').value.trim(),
    logo_url: document.getElementById('forms-logo-url').value.trim(),
    default_bucket: document.getElementById('forms-bucket').value.trim() || null,
    questions: formsQuestions,
  }, { onConflict: 'user_id' });
  if (error) { statusEl.textContent = 'Error: ' + error.message; }
  else { statusEl.textContent = 'Saved!'; setTimeout(function(){ statusEl.textContent = ''; }, 2500); }
}"""

new_save = """async function formsSaveSettings() {
  if (!currentUser) return;
  var statusEl = document.getElementById('forms-save-status');
  statusEl.textContent = 'Saving...';
  var token = localStorage.getItem('arcascend_token');
  var payload = {
    user_id: currentUser.id,
    gym_name: document.getElementById('forms-gym-name').value.trim(),
    form_title: document.getElementById('forms-form-title').value.trim(),
    form_description: document.getElementById('forms-form-desc').value.trim(),
    logo_url: document.getElementById('forms-logo-url').value.trim(),
    default_bucket: document.getElementById('forms-bucket').value.trim() || null,
    questions: formsQuestions,
  };
  try {
    var res = await fetch(SUPABASE_URL + '/rest/v1/trainer_settings', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + token,
        'apikey': SUPABASE_KEY,
        'Content-Type': 'application/json',
        'Prefer': 'resolution=merge-duplicates'
      },
      body: JSON.stringify(payload)
    });
    if (res.ok || res.status === 201 || res.status === 204) {
      statusEl.textContent = 'Saved!';
      setTimeout(function(){ statusEl.textContent = ''; }, 2500);
    } else {
      var err = await res.text();
      statusEl.textContent = 'Error: ' + err;
    }
  } catch(e) {
    statusEl.textContent = 'Error: ' + e.message;
  }
}"""

if old_init in html:
    html = html.replace(old_init, new_init)
    print('Replaced formsInit')
else:
    print('ERROR: formsInit not found - may need manual check')

if old_save in html:
    html = html.replace(old_save, new_save)
    print('Replaced formsSaveSettings')
else:
    print('ERROR: formsSaveSettings not found - may need manual check')

open(path, 'w').write(html)
print('Done')
