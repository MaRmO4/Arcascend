path = '/Users/marioarcata/Desktop/arcascend/public/index.html'
html = open(path).read()

# 1. Add QRCode.js before </head>
if 'qrcodejs' not in html:
    html = html.replace('</head>', '<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>\n</head>')
    print('Added QRCode.js')

# 2. Add Forms tab button after notes tab
forms_tab = '\n    <div class="tab" data-tab="forms">📋 Forms</div>'
if 'data-tab="forms"' not in html:
    html = html.replace('data-tab="notes"', 'data-tab="notes"', 1)
    # Insert after the full notes tab div
    import re
    html = re.sub(r'(<div class="tab" data-tab="notes">[^<]*(?:<[^>]+>[^<]*)*?</div>)', r'\1' + forms_tab, html, count=1)
    print('Added Forms tab button')

# 3. Add Forms panel before </body>
if 'id="tab-forms"' not in html:
    forms_panel = '''
<div id="tab-forms" class="tab-panel" style="display:none">
  <div style="max-width:720px;margin:0 auto;padding:24px 16px">
    <div style="margin-bottom:28px">
      <h2 style="font-size:20px;font-weight:700;color:var(--text-primary);margin:0 0 6px">Intake Form Settings</h2>
      <p style="color:var(--text-muted);font-size:14px;margin:0">Customize your client intake form and share your unique link.</p>
    </div>
    <div class="card" style="padding:20px;margin-bottom:20px">
      <div style="font-size:13px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:12px">Your Intake Form Link</div>
      <div style="display:flex;gap:8px;align-items:center">
        <input id="forms-link-input" readonly style="flex:1;background:var(--bg-secondary);border:1px solid var(--border);border-radius:8px;padding:10px 12px;color:var(--text-primary);font-size:13px;font-family:monospace" />
        <button id="forms-copy-btn" onclick="formsCopyLink()" style="padding:10px 16px;background:var(--accent);color:#fff;border:none;border-radius:8px;font-size:13px;font-weight:600;cursor:pointer;white-space:nowrap">Copy Link</button>
        <a id="forms-open-btn" href="#" target="_blank" style="padding:10px 14px;background:var(--bg-secondary);border:1px solid var(--border);border-radius:8px;font-size:13px;color:var(--text-primary);text-decoration:none;white-space:nowrap">Open &#x2197;</a>
      </div>
      <div style="margin-top:16px;display:flex;align-items:flex-start;gap:16px">
        <div id="forms-qr" style="background:#fff;padding:8px;border-radius:8px;display:inline-block"></div>
        <div style="font-size:12px;color:var(--text-muted);padding-top:4px;line-height:1.6">Share this QR code in your gym, on social media, or in your bio.<br>It links directly to <em>your</em> intake form.</div>
      </div>
    </div>
    <div class="card" style="padding:20px;margin-bottom:20px">
      <div style="font-size:13px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:16px">Form Branding</div>
      <div style="display:grid;gap:14px">
        <div><label style="font-size:13px;color:var(--text-secondary);display:block;margin-bottom:6px">Gym / Business Name</label><input id="forms-gym-name" placeholder="e.g. Fit Club" style="width:100%;background:var(--bg-secondary);border:1px solid var(--border);border-radius:8px;padding:10px 12px;color:var(--text-primary);font-size:14px;box-sizing:border-box" /></div>
        <div><label style="font-size:13px;color:var(--text-secondary);display:block;margin-bottom:6px">Form Title</label><input id="forms-form-title" placeholder="e.g. Client Intake Form" style="width:100%;background:var(--bg-secondary);border:1px solid var(--border);border-radius:8px;padding:10px 12px;color:var(--text-primary);font-size:14px;box-sizing:border-box" /></div>
        <div><label style="font-size:13px;color:var(--text-secondary);display:block;margin-bottom:6px">Form Description</label><textarea id="forms-form-desc" rows="2" placeholder="e.g. Fill out the form and we will be in touch shortly." style="width:100%;background:var(--bg-secondary);border:1px solid var(--border);border-radius:8px;padding:10px 12px;color:var(--text-primary);font-size:14px;resize:vertical;box-sizing:border-box"></textarea></div>
        <div><label style="font-size:13px;color:var(--text-secondary);display:block;margin-bottom:6px">Logo URL <span style="color:var(--text-muted);font-weight:400">(paste a direct image link)</span></label><input id="forms-logo-url" placeholder="https://your-logo-url.com/logo.png" style="width:100%;background:var(--bg-secondary);border:1px solid var(--border);border-radius:8px;padding:10px 12px;color:var(--text-primary);font-size:14px;box-sizing:border-box" /><div id="forms-logo-preview" style="margin-top:8px;display:none"><img id="forms-logo-img" style="height:60px;object-fit:contain;border-radius:6px;border:1px solid var(--border)" /></div></div>
      </div>
      <div style="margin-top:20px;display:flex;gap:10px;align-items:center">
        <button onclick="formsSaveSettings()" style="padding:10px 20px;background:var(--accent);color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer">Save Settings</button>
        <span id="forms-save-status" style="font-size:13px;color:var(--text-muted)"></span>
      </div>
    </div>
    <div class="card" style="padding:20px;margin-bottom:20px">
      <div style="font-size:13px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px">Bucket Routing</div>
      <p style="font-size:13px;color:var(--text-muted);margin:0 0 14px">New leads from your intake form will be tagged with this bucket. Leave blank for All Leads.</p>
      <input id="forms-bucket" placeholder="e.g. InBody Scan Leads, Free Consult..." style="width:100%;background:var(--bg-secondary);border:1px solid var(--border);border-radius:8px;padding:10px 12px;color:var(--text-primary);font-size:14px;box-sizing:border-box" />
    </div>
    <div class="card" style="padding:20px;margin-bottom:20px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
        <div>
          <div style="font-size:13px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:.05em">Form Questions</div>
          <p style="font-size:13px;color:var(--text-muted);margin:4px 0 0">Drag to reorder. Changes save with the button above.</p>
        </div>
        <button onclick="formsAddQuestion()" style="padding:8px 14px;background:var(--accent);color:#fff;border:none;border-radius:8px;font-size:13px;font-weight:600;cursor:pointer">+ Add Question</button>
      </div>
      <div id="forms-questions-list" style="display:flex;flex-direction:column;gap:10px"></div>
      <div style="margin-top:16px"><button onclick="formsResetQuestions()" style="padding:8px 14px;background:transparent;border:1px solid var(--border);border-radius:8px;font-size:13px;color:var(--text-muted);cursor:pointer">Reset to Defaults</button></div>
    </div>
    <div style="background:var(--bg-secondary);border:1px solid var(--border);border-radius:10px;padding:16px;font-size:13px;color:var(--text-muted);line-height:1.6">
      <strong style="color:var(--text-secondary)">Link Preview (Open Graph)</strong><br>
      When you share your intake form link in iMessage, WhatsApp, or Instagram DMs, it shows a branded card. Your gym name and form title appear automatically once saved.
    </div>
  </div>
</div>'''
    html = html.replace('</body>', forms_panel + '\n</body>')
    print('Added Forms panel HTML')

# 4. Add JS before </script>
if 'formsInit' not in html:
    forms_js = """
const INTAKE_DEFAULT_QUESTIONS = [
  { id:'q_name',     label:'Full Name',                          type:'text',     required:true,  options:[] },
  { id:'q_phone',    label:'Phone Number',                       type:'tel',      required:true,  options:[] },
  { id:'q_email',    label:'Email Address',                      type:'email',    required:true,  options:[] },
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

let formsSettings = {};
let formsQuestions = [];
let formsDragSrc = null;

async function formsInit() {
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
}

function formsPreviewLogo(url) {
  const preview = document.getElementById('forms-logo-preview');
  const img = document.getElementById('forms-logo-img');
  if (url && url.startsWith('http')) { img.src = url; preview.style.display = 'block'; }
  else preview.style.display = 'none';
}

function formsCopyLink() {
  navigator.clipboard.writeText(document.getElementById('forms-link-input').value).then(function() {
    var btn = document.getElementById('forms-copy-btn');
    btn.textContent = 'Copied!';
    setTimeout(function() { btn.textContent = 'Copy Link'; }, 1800);
  });
}

function formsRenderQuestions() {
  const list = document.getElementById('forms-questions-list');
  list.innerHTML = '';
  formsQuestions.forEach(function(q, i) {
    const row = document.createElement('div');
    row.draggable = true;
    row.dataset.idx = i;
    row.style.cssText = 'background:var(--bg-secondary);border:1px solid var(--border);border-radius:10px;padding:14px;display:grid;grid-template-columns:24px 1fr auto;gap:10px;align-items:start;cursor:grab;transition:opacity .15s';
    const typeOpts = ['text','textarea','tel','email','number','select','multiselect'].map(function(t) { return '<option value="'+t+'"'+(q.type===t?' selected':'')+'>'+t+'</option>'; }).join('');
    const showOpts = ['select','multiselect'].indexOf(q.type) > -1;
    row.innerHTML = '<div style="padding-top:2px;color:var(--text-muted);user-select:none;font-size:18px;line-height:1">&#8995;</div>'
      + '<div style="display:flex;flex-direction:column;gap:8px">'
      + '<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">'
      + '<input class="forms-q-label" data-idx="'+i+'" value="'+q.label.replace(/"/g,"&quot;")+'" placeholder="Question label" style="flex:1;min-width:160px;background:var(--bg-primary);border:1px solid var(--border);border-radius:6px;padding:7px 10px;color:var(--text-primary);font-size:13px" />'
      + '<select class="forms-q-type" data-idx="'+i+'" style="background:var(--bg-primary);border:1px solid var(--border);border-radius:6px;padding:7px 8px;color:var(--text-primary);font-size:13px">'+typeOpts+'</select>'
      + '<label style="display:flex;align-items:center;gap:5px;font-size:12px;color:var(--text-muted);white-space:nowrap;cursor:pointer"><input type="checkbox" class="forms-q-required" data-idx="'+i+'" '+(q.required?'checked':'')+' style="accent-color:var(--accent)"> Required</label>'
      + '</div>'
      + '<div class="forms-q-options-wrap" style="display:'+(showOpts?'block':'none')+'">'
      + '<div style="font-size:12px;color:var(--text-muted);margin-bottom:4px">Options (one per line):</div>'
      + '<textarea class="forms-q-options" data-idx="'+i+'" rows="3" style="width:100%;background:var(--bg-primary);border:1px solid var(--border);border-radius:6px;padding:7px 10px;color:var(--text-primary);font-size:12px;resize:vertical;box-sizing:border-box">'+(q.options||[]).join('\\n')+'</textarea>'
      + '</div></div>'
      + '<button onclick="formsDeleteQuestion('+i+')" style="padding:4px 8px;background:transparent;border:1px solid var(--border);border-radius:6px;color:var(--text-muted);font-size:16px;cursor:pointer;line-height:1">x</button>';
    row.querySelector('.forms-q-label').addEventListener('input', function(e) { formsQuestions[+e.target.dataset.idx].label = e.target.value; });
    row.querySelector('.forms-q-type').addEventListener('change', function(e) {
      var idx = +e.target.dataset.idx;
      formsQuestions[idx].type = e.target.value;
      row.querySelector('.forms-q-options-wrap').style.display = ['select','multiselect'].indexOf(e.target.value) > -1 ? 'block' : 'none';
    });
    row.querySelector('.forms-q-required').addEventListener('change', function(e) { formsQuestions[+e.target.dataset.idx].required = e.target.checked; });
    var optTA = row.querySelector('.forms-q-options');
    if (optTA) optTA.addEventListener('input', function(e) { formsQuestions[+e.target.dataset.idx].options = e.target.value.split('\\n').map(function(s){return s.trim();}).filter(Boolean); });
    row.addEventListener('dragstart', function(e) { formsDragSrc=i; e.dataTransfer.effectAllowed='move'; setTimeout(function(){row.style.opacity='0.4';},0); });
    row.addEventListener('dragend', function() { row.style.opacity='1'; formsDragSrc=null; });
    row.addEventListener('dragover', function(e) { e.preventDefault(); e.dataTransfer.dropEffect='move'; });
    row.addEventListener('drop', function(e) { e.preventDefault(); if(formsDragSrc===null||formsDragSrc===i)return; var moved=formsQuestions.splice(formsDragSrc,1)[0]; formsQuestions.splice(i,0,moved); formsRenderQuestions(); });
    list.appendChild(row);
  });
}

function formsAddQuestion() {
  formsQuestions.push({ id:'q_'+Date.now(), label:'', type:'text', required:false, options:[] });
  formsRenderQuestions();
  var last = document.getElementById('forms-questions-list').lastElementChild;
  if (last) last.scrollIntoView({ behavior:'smooth', block:'nearest' });
}

function formsDeleteQuestion(idx) {
  if (formsQuestions.length <= 1) return;
  formsQuestions.splice(idx, 1);
  formsRenderQuestions();
}

function formsResetQuestions() {
  if (!confirm('Reset all questions to defaults?')) return;
  formsQuestions = JSON.parse(JSON.stringify(INTAKE_DEFAULT_QUESTIONS));
  formsRenderQuestions();
}

async function formsSaveSettings() {
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
}
"""
    last_script = html.rfind('</script>')
    html = html[:last_script] + forms_js + '\n</script>' + html[last_script+9:]
    print('Added Forms JS')

# 5. Wire formsInit into tab switcher
if "tab === 'forms'" not in html and 'tab == "forms"' not in html:
    # Find the tab switcher pattern and add forms
    html = html.replace(
        "if (tab === 'sync')",
        "if (tab === 'forms') formsInit();\n  if (tab === 'sync')"
    )
    if "tab === 'forms'" not in html:
        html = html.replace(
            'if (tab == "sync")',
            'if (tab == "forms") formsInit();\n  if (tab == "sync")'
        )
    print('Wired formsInit to tab switcher')

open(path, 'w').write(html)
print('DONE - file written successfully')
