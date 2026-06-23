// ============== REPORTS TAB ==============
var __REPORTS_SUB = localStorage.getItem('arcascend_reports_sub') || 'leads';
var __REPORTS_FROM = null;
var __REPORTS_TO = null;
var __REPORTS_EVENTS = null;
var __REPORTS_LOADING = false;
var __REPORTS_CHART = null;

var __REPORTS_PRESET = localStorage.getItem('arcascend_reports_preset_active') || localStorage.getItem('arcascend_reports_preset_default') || 'month';

function reportsRangeFromPreset(p) {
  var now = new Date();
  var to = now.toISOString().slice(0,10);
  var from;
  if (p === 'month') {
    from = new Date(now.getFullYear(), now.getMonth(), 1).toISOString().slice(0,10);
  } else if (p === 'quarter') {
    var q = Math.floor(now.getMonth() / 3);
    from = new Date(now.getFullYear(), q*3, 1).toISOString().slice(0,10);
  } else if (p === 'year') {
    from = new Date(now.getFullYear(), 0, 1).toISOString().slice(0,10);
  } else {
    from = to; // 'custom' fallback (will be replaced by inputs)
  }
  return { from: from, to: to };
}

function reportsInitRange() {
  if (__REPORTS_FROM && __REPORTS_TO) return;
  if (__REPORTS_PRESET && __REPORTS_PRESET !== 'custom') {
    var r = reportsRangeFromPreset(__REPORTS_PRESET);
    __REPORTS_FROM = r.from;
    __REPORTS_TO = r.to;
  } else {
    var now = new Date();
    var first = new Date(now.getFullYear(), now.getMonth(), 1);
    __REPORTS_FROM = first.toISOString().slice(0,10);
    __REPORTS_TO = now.toISOString().slice(0,10);
  }
}

function reportsLoadEvents() {
  __REPORTS_LOADING = true;
  var token = localStorage.getItem('arcascend_token');
  var uid = (typeof currentUser !== 'undefined' && currentUser) ? currentUser.id : localStorage.getItem('arcascend_user_id');
  var from = __REPORTS_FROM + 'T00:00:00';
  var to = __REPORTS_TO + 'T23:59:59';
  var url = SUPABASE_URL + '/rest/v1/lead_events?user_id=eq.' + uid
    + '&created_at=gte.' + from + '&created_at=lte.' + to
    + '&select=event_type,lead_name,event_data,created_at&order=created_at.asc&limit=5000';
  return fetch(url, {
    headers: { 'Authorization': 'Bearer ' + token, 'apikey': SUPABASE_KEY }
  }).then(function(r){ return r.ok ? r.json() : []; }).catch(function(){ return []; })
    .then(function(events){
      __REPORTS_EVENTS = events || [];
      __REPORTS_LOADING = false;
      return __REPORTS_EVENTS;
    });
}

function renderReportsTab() {
  reportsInitRange();
  var main = document.getElementById('main');
  if (!main) return;

  var html = '';
  html += '<div style="padding:14px 20px 4px;">';
  html += '<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;">';
  html += '<div style="font-size:20px;font-weight:600;">\ud83d\udcca Reports</div>';
  html += '<div style="display:flex;align-items:center;gap:8px;font-size:13px;">';
  html += '<span style="color:var(--text-muted);">From</span>';
  html += '<input type="date" id="rep-from" value="' + __REPORTS_FROM + '" style="background:var(--panel);color:var(--text);border:1px solid var(--border);border-radius:6px;padding:5px 8px;font-size:13px;">';
  html += '<span style="color:var(--text-muted);">To</span>';
  html += '<input type="date" id="rep-to" value="' + __REPORTS_TO + '" style="background:var(--panel);color:var(--text);border:1px solid var(--border);border-radius:6px;padding:5px 8px;font-size:13px;">';
  html += '<button id="rep-apply" style="background:var(--accent);color:#fff;border:none;border-radius:6px;padding:6px 14px;font-size:13px;font-weight:600;cursor:pointer;">Apply</button>';
  html += '</div></div>';

  // Preset range buttons
  var defaultPreset = localStorage.getItem('arcascend_reports_preset_default') || 'month';
  var presets = [['month','Month'],['quarter','Quarter'],['year','Year'],['custom','Custom']];
  html += '<div style="display:flex;align-items:center;gap:6px;margin-top:10px;flex-wrap:wrap;">';
  presets.forEach(function(p){
    var active = __REPORTS_PRESET === p[0];
    var isDefault = defaultPreset === p[0];
    var bg = active ? 'var(--accent)' : 'var(--panel)';
    var color = active ? '#fff' : 'var(--text)';
    html += '<button class="rep-preset" data-preset="' + p[0] + '" style="background:' + bg + ';color:' + color + ';border:1px solid var(--border);border-radius:6px;padding:5px 12px;font-size:12px;font-weight:600;cursor:pointer;">' + p[1] + (isDefault ? ' \u2605' : '') + '</button>';
  });
  html += '<button id="rep-save-default" title="Save current range as default" style="background:transparent;color:var(--text-muted);border:1px solid var(--border);border-radius:6px;padding:5px 12px;font-size:12px;font-weight:600;cursor:pointer;margin-left:6px;">\u2606 Save as default</button>';
  html += '</div>';

  // Sub-tabs
  html += '<div style="display:flex;gap:4px;margin-top:14px;border-bottom:1px solid var(--border);">';
  ['leads','revenue','conversions','activity'].forEach(function(key){
    var active = __REPORTS_SUB === key;
    var label = key.charAt(0).toUpperCase() + key.slice(1);
    html += '<button class="rep-sub" data-sub="' + key + '" style="background:transparent;border:none;border-bottom:2px solid ' + (active?'var(--accent)':'transparent') + ';color:' + (active?'var(--accent)':'var(--text-muted)') + ';padding:8px 16px;font-size:13px;font-weight:600;cursor:pointer;">' + label + '</button>';
  });
  html += '</div>';
  html += '</div>';
  html += '<div id="rep-body" style="padding:16px 20px 40px;"></div>';
  main.innerHTML = html;

  document.getElementById('rep-apply').addEventListener('click', function(){
    __REPORTS_FROM = document.getElementById('rep-from').value;
    __REPORTS_TO = document.getElementById('rep-to').value;
    __REPORTS_PRESET = 'custom';
    localStorage.setItem('arcascend_reports_preset_active', 'custom');
    __REPORTS_EVENTS = null;
    renderReportsTab();
  });

  document.querySelectorAll('.rep-preset').forEach(function(btn){
    btn.addEventListener('click', function(){
      var p = btn.dataset.preset;
      __REPORTS_PRESET = p;
      localStorage.setItem('arcascend_reports_preset_active', p);
      if (p !== 'custom') {
        var r = reportsRangeFromPreset(p);
        __REPORTS_FROM = r.from;
        __REPORTS_TO = r.to;
      }
      __REPORTS_EVENTS = null;
      renderReportsTab();
    });
  });

  var sd = document.getElementById('rep-save-default');
  if (sd) sd.addEventListener('click', function(){
    localStorage.setItem('arcascend_reports_preset_default', __REPORTS_PRESET);
    sd.innerHTML = '\u2605 Saved as default';
    sd.style.color = 'var(--accent)';
    setTimeout(function(){ renderReportsTab(); }, 700);
  });
  document.querySelectorAll('.rep-sub').forEach(function(btn){
    btn.addEventListener('click', function(){
      __REPORTS_SUB = btn.dataset.sub;
      localStorage.setItem('arcascend_reports_sub', __REPORTS_SUB);
      renderReportsTab();
    });
  });

  var body = document.getElementById('rep-body');
  body.innerHTML = '<div style="color:var(--text-muted);">Loading data...</div>';
  reportsLoadEvents().then(function(){
    if (__REPORTS_SUB === 'leads') renderRepLeads(body);
    else if (__REPORTS_SUB === 'revenue') renderRepRevenue(body);
    else if (__REPORTS_SUB === 'conversions') renderRepConversions(body);
    else if (__REPORTS_SUB === 'activity') renderRepActivity(body);
  });
}

// ===== Helper utilities =====
function repStat(label, value, color) {
  return '<div style="background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:14px;">'
    + '<div style="font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px;">' + label + '</div>'
    + '<div style="font-size:24px;font-weight:700;color:' + (color || 'var(--text)') + ';margin-top:4px;">' + value + '</div>'
    + '</div>';
}

function repStatsGrid(items) {
  return '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;margin-bottom:20px;">'
    + items.map(function(it){ return repStat(it.label, it.value, it.color); }).join('')
    + '</div>';
}

function repCard(title, inner) {
  return '<div style="background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:16px;margin-bottom:14px;">'
    + '<div style="font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;color:var(--text-muted);margin-bottom:10px;">' + title + '</div>'
    + inner + '</div>';
}

function repBetweenRange(iso) {
  var d = new Date(iso);
  var f = new Date(__REPORTS_FROM + 'T00:00:00');
  var t = new Date(__REPORTS_TO + 'T23:59:59');
  return d >= f && d <= t;
}

function repBucketGranularity() {
  if (__REPORTS_PRESET === 'month') return 'week';
  if (__REPORTS_PRESET === 'quarter' || __REPORTS_PRESET === 'year') return 'month';
  // Custom: choose based on span
  var f = new Date(__REPORTS_FROM + 'T00:00:00');
  var t = new Date(__REPORTS_TO + 'T00:00:00');
  var days = Math.round((t - f) / 86400000);
  return days < 31 ? 'week' : 'month';
}

function repDateBuckets() {
  // Returns array of bucket keys (YYYY-MM-DD for week-start or YYYY-MM for month)
  var gran = repBucketGranularity();
  var out = [];
  var d = new Date(__REPORTS_FROM + 'T00:00:00');
  var end = new Date(__REPORTS_TO + 'T00:00:00');
  if (gran === 'week') {
    // Snap d to start of week (Sunday)
    var w = new Date(d); w.setDate(w.getDate() - w.getDay());
    while (w <= end) {
      out.push(w.toISOString().slice(0,10));
      w = new Date(w); w.setDate(w.getDate() + 7);
    }
  } else {
    // Monthly
    var m = new Date(d.getFullYear(), d.getMonth(), 1);
    var endM = new Date(end.getFullYear(), end.getMonth(), 1);
    while (m <= endM) {
      out.push(m.toISOString().slice(0,7));
      m = new Date(m.getFullYear(), m.getMonth()+1, 1);
    }
  }
  return out;
}

function repBucketKeyFor(iso) {
  var gran = repBucketGranularity();
  var d = new Date(iso);
  if (gran === 'week') {
    var w = new Date(d); w.setDate(w.getDate() - w.getDay());
    return w.toISOString().slice(0,10);
  } else {
    return d.toISOString().slice(0,7);
  }
}

function repLoadChartJs(cb) {
  if (window.Chart) { cb(); return; }
  var s = document.createElement('script');
  s.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
  s.onload = cb;
  document.head.appendChild(s);
}

function repDrawLineChart(canvasId, label, labels, data, color) {
  repLoadChartJs(function(){
    var ctx = document.getElementById(canvasId);
    if (!ctx) return;
    if (__REPORTS_CHART) { try { __REPORTS_CHART.destroy(); } catch(_){} }
    __REPORTS_CHART = new Chart(ctx, {
      type: 'line',
      data: { labels: labels, datasets: [{ label: label, data: data, borderColor: color || '#4f9eff', backgroundColor: (color || '#4f9eff') + '33', tension: 0.3, fill: true }] },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#aaa' } } }, scales: { x: { ticks: { color: '#888' }, grid: { color: '#333' } }, y: { ticks: { color: '#888' }, grid: { color: '#333' }, beginAtZero: true } } }
    });
  });
}

function repDrawBarChart(canvasId, label, labels, data, color) {
  repLoadChartJs(function(){
    var ctx = document.getElementById(canvasId);
    if (!ctx) return;
    if (__REPORTS_CHART) { try { __REPORTS_CHART.destroy(); } catch(_){} }
    __REPORTS_CHART = new Chart(ctx, {
      type: 'bar',
      data: { labels: labels, datasets: [{ label: label, data: data, backgroundColor: color || '#4f9eff' }] },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#aaa' } } }, scales: { x: { ticks: { color: '#888' }, grid: { color: '#333' } }, y: { ticks: { color: '#888' }, grid: { color: '#333' }, beginAtZero: true } } }
    });
  });
}

// ===== LEADS sub-tab =====
function renderRepLeads(body) {
  var ev = __REPORTS_EVENTS || [];
  var created = ev.filter(function(e){ return e.event_type === 'lead_created'; });
  var intake = ev.filter(function(e){ return e.event_type === 'form_submitted'; });
  var statusChanges = ev.filter(function(e){ return e.event_type === 'status_changed'; });
  var newActiveEv = ev.filter(function(e){ return e.event_type === 'active_client_marked'; });
  var wonEv = statusChanges.filter(function(e){ var t = (e.event_data && e.event_data.to) || ''; return t.toLowerCase().indexOf('won') >= 0; });
  var lostEv = statusChanges.filter(function(e){ var t = (e.event_data && e.event_data.to) || ''; return t.toLowerCase().indexOf('lost') >= 0; });

  // Status distribution from current LEADS state
  var statusCounts = {};
  (LEADS || []).forEach(function(L){
    var s = (L.status || 'New');
    statusCounts[s] = (statusCounts[s] || 0) + 1;
  });

  // Build bucket maps for all three series
  var buckets = repDateBuckets();
  function newMap() { var m = {}; buckets.forEach(function(b){ m[b] = 0; }); return m; }
  var activeMap = newMap(), wonMap = newMap(), lostMap = newMap();

  // Helper: parse L.date which is stored as 'M/D/YYYY' or 'M/D/YYYY HH:MM:SS'
  function parseLeadDate(s) {
    if (!s) return null;
    if (typeof s !== 'string') return null;
    var d = new Date(s);
    if (!isNaN(d.getTime())) return d.toISOString();
    return null;
  }

  // Track which lead names are already represented by events (so we don't double-count)
  var eventNamesActive = {}, eventNamesWon = {}, eventNamesLost = {};
  newActiveEv.forEach(function(e){
    var k = repBucketKeyFor(e.created_at);
    if (activeMap[k] !== undefined) activeMap[k]++;
    if (e.lead_name) eventNamesActive[e.lead_name] = true;
  });
  wonEv.forEach(function(e){
    var k = repBucketKeyFor(e.created_at);
    if (wonMap[k] !== undefined) wonMap[k]++;
    if (e.lead_name) eventNamesWon[e.lead_name] = true;
  });
  lostEv.forEach(function(e){
    var k = repBucketKeyFor(e.created_at);
    if (lostMap[k] !== undefined) lostMap[k]++;
    if (e.lead_name) eventNamesLost[e.lead_name] = true;
  });

  // Fallback: walk LEADS, bucket by L.date if not already accounted for in events
  (LEADS || []).forEach(function(L){
    var iso = parseLeadDate(L.date);
    if (!iso) return;
    var k = repBucketKeyFor(iso);
    if (activeMap[k] === undefined) return; // outside current range
    var status = (L.status || '').toLowerCase();
    if (L.billing && L.billing.active && !eventNamesActive[L.name]) activeMap[k]++;
    if (status.indexOf('won') >= 0 && !eventNamesWon[L.name]) wonMap[k]++;
    if (status.indexOf('lost') >= 0 && !eventNamesLost[L.name]) lostMap[k]++;
  });

  var html = '';
  html += repStatsGrid([
    { label:'Leads Added', value: created.length, color:'#4f9eff' },
    { label:'Intake Forms', value: intake.length, color:'#a78bfa' },
    { label:'New Active Clients', value: newActiveEv.length, color:'#22c55e' },
    { label:'Closed Won', value: wonEv.length, color:'#22c55e' },
    { label:'Closed Lost', value: lostEv.length, color:'#ef4444' }
  ]);

  html += repCard('Outcomes Over Time', '<div style="height:260px;"><canvas id="rep-chart-leads"></canvas></div>');
  html += repCard('Status Distribution (Current)', '<div>' + Object.keys(statusCounts).map(function(s){
    var pct = Math.round(statusCounts[s] / Math.max(1, (LEADS||[]).length) * 100);
    return '<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;font-size:13px;">'
      + '<div style="width:120px;color:var(--text-muted);">' + s + '</div>'
      + '<div style="flex:1;background:var(--panel2);height:18px;border-radius:4px;overflow:hidden;"><div style="background:var(--accent);height:100%;width:' + pct + '%;"></div></div>'
      + '<div style="width:60px;text-align:right;color:var(--text);">' + statusCounts[s] + ' (' + pct + '%)</div>'
      + '</div>';
  }).join('') + '</div>');

  body.innerHTML = html;

  // Draw multi-line chart
  repLoadChartJs(function(){
    var ctx = document.getElementById('rep-chart-leads');
    if (!ctx) return;
    if (__REPORTS_CHART) { try { __REPORTS_CHART.destroy(); } catch(_){} }
    __REPORTS_CHART = new Chart(ctx, {
      type: 'line',
      data: { labels: buckets, datasets: [
        { label: 'New Active Clients', data: buckets.map(function(b){ return activeMap[b]; }), borderColor: '#22c55e', backgroundColor: '#22c55e22', tension: 0.3, fill: false },
        { label: 'Closed Won', data: buckets.map(function(b){ return wonMap[b]; }), borderColor: '#4f9eff', backgroundColor: '#4f9eff22', tension: 0.3, fill: false },
        { label: 'Closed Lost', data: buckets.map(function(b){ return lostMap[b]; }), borderColor: '#ef4444', backgroundColor: '#ef444422', tension: 0.3, fill: false }
      ]},
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#aaa' } } }, scales: { x: { ticks: { color: '#888' }, grid: { color: '#333' } }, y: { ticks: { color: '#888' }, grid: { color: '#333' }, beginAtZero: true } } }
    });
  });
}

// ===== REVENUE sub-tab =====
function renderRepRevenue(body) {
  var ev = __REPORTS_EVENTS || [];
  var payments = ev.filter(function(e){ return e.event_type === 'payment_marked'; });
  var totalPaid = payments.reduce(function(acc, e){
    var amt = (e.event_data && e.event_data.amount) || 0;
    return acc + (parseFloat(amt) || 0);
  }, 0);

  // Current monthly projection (uses live LEADS billing)
  var activeC = (LEADS || []).filter(function(L){ return L.billing && L.billing.active; });
  var projection = activeC.reduce(function(acc, L){
    var sess = parseFloat(L.billing.sessions) || 0;
    var rate = parseFloat(L.billing.rate) || 0;
    return acc + sess * rate;
  }, 0);
  var paidNow = activeC.filter(function(L){ return L.billing.paid; }).reduce(function(acc, L){
    var sess = parseFloat(L.billing.sessions) || 0;
    var rate = parseFloat(L.billing.rate) || 0;
    return acc + sess * rate;
  }, 0);
  var outstanding = projection - paidNow;

  // YTD payments
  var yStart = new Date(new Date().getFullYear(), 0, 1).toISOString();
  // We only have events from the range; YTD shown is over the active range
  // To do a true YTD we'd need to re-fetch — for now we annotate honestly.

  // Daily revenue series in range
  var buckets = repDateBuckets();
  var revMap = {};
  buckets.forEach(function(d){ revMap[d] = 0; });
  payments.forEach(function(e){
    var k = repBucketKeyFor(e.created_at);
    var amt = parseFloat((e.event_data && e.event_data.amount) || 0) || 0;
    if (revMap[k] !== undefined) revMap[k] += amt;
  });
  var revData = buckets.map(function(d){ return revMap[d]; });

  var html = '';
  html += repStatsGrid([
    { label: currentMonthLabel() + ' Projection', value: '$' + projection.toLocaleString(), color:'#4f9eff' },
    { label: currentMonthLabel() + ' Paid', value: '$' + paidNow.toLocaleString(), color:'#22c55e' },
    { label: 'Outstanding', value: '$' + outstanding.toLocaleString(), color:'#f59e0b' },
    { label: 'Payments Logged (range)', value: '$' + totalPaid.toLocaleString() },
    { label: 'Clients Paid', value: activeC.filter(function(L){return L.billing.paid;}).length + ' / ' + activeC.length }
  ]);
  html += repCard('Revenue Logged Over Time (range)', '<div style="height:260px;"><canvas id="rep-chart-revenue"></canvas></div>');
  body.innerHTML = html;
  repDrawLineChart('rep-chart-revenue', 'Revenue ($)', buckets, revData, '#22c55e');
}

// ===== CONVERSIONS sub-tab =====
function renderRepConversions(body) {
  var ev = __REPORTS_EVENTS || [];
  var statusChanges = ev.filter(function(e){ return e.event_type === 'status_changed'; });
  var consultsDone = ev.filter(function(e){ return e.event_type === 'consultation_completed'; });
  var newActive = ev.filter(function(e){ return e.event_type === 'active_client_marked'; });

  var won = statusChanges.filter(function(e){ var t = (e.event_data && e.event_data.to) || ''; return t.toLowerCase().indexOf('won') >= 0; });
  var lost = statusChanges.filter(function(e){ var t = (e.event_data && e.event_data.to) || ''; return t.toLowerCase().indexOf('lost') >= 0; });
  var closedTotal = won.length + lost.length;
  var winRate = closedTotal ? Math.round(won.length / closedTotal * 100) : 0;

  // Daily won/lost series
  var buckets = repDateBuckets();
  var wonMap = {}, lostMap = {};
  buckets.forEach(function(d){ wonMap[d] = 0; lostMap[d] = 0; });
  won.forEach(function(e){ var k = repBucketKeyFor(e.created_at); if(wonMap[k]!==undefined) wonMap[k]++; });
  lost.forEach(function(e){ var k = repBucketKeyFor(e.created_at); if(lostMap[k]!==undefined) lostMap[k]++; });

  var html = '';
  html += repStatsGrid([
    { label: 'Consultations Completed', value: consultsDone.length, color:'#4f9eff' },
    { label: 'Closed Won', value: won.length, color:'#22c55e' },
    { label: 'Closed Lost', value: lost.length, color:'#ef4444' },
    { label: 'Win Rate', value: winRate + '%', color: winRate >= 50 ? '#22c55e' : '#f59e0b' },
    { label: 'New Active Clients', value: newActive.length }
  ]);
  html += repCard('Closed Won vs Lost (over range)', '<div style="height:260px;"><canvas id="rep-chart-conv"></canvas></div>');
  body.innerHTML = html;
  // Two-series bar chart needs a different draw — simulate by drawing combined bar
  repLoadChartJs(function(){
    var ctx = document.getElementById('rep-chart-conv');
    if (!ctx) return;
    if (__REPORTS_CHART) { try { __REPORTS_CHART.destroy(); } catch(_){} }
    __REPORTS_CHART = new Chart(ctx, {
      type: 'bar',
      data: { labels: buckets, datasets: [
        { label: 'Won', data: buckets.map(function(d){ return wonMap[d]; }), backgroundColor: '#22c55e' },
        { label: 'Lost', data: buckets.map(function(d){ return lostMap[d]; }), backgroundColor: '#ef4444' }
      ]},
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#aaa' } } }, scales: { x: { stacked: false, ticks: { color: '#888' }, grid: { color: '#333' } }, y: { stacked: false, ticks: { color: '#888' }, grid: { color: '#333' }, beginAtZero: true } } }
    });
  });
}

// ===== ACTIVITY sub-tab =====
function renderRepActivity(body) {
  var ev = (__REPORTS_EVENTS || []).slice().reverse(); // newest first
  var emojiFor = {
    lead_created: '\u2728',
    status_changed: '\ud83d\udd04',
    active_client_marked: '\ud83d\udcaa',
    payment_marked: '\ud83d\udcb0',
    form_submitted: '\ud83d\udcdd',
    consultation_completed: '\u2705',
    follow_up_scheduled: '\ud83d\udcc5'
  };
  var byType = {};
  ev.forEach(function(e){ byType[e.event_type] = (byType[e.event_type]||0) + 1; });

  var statHtml = repStatsGrid([
    { label: 'Total Events', value: ev.length, color: '#4f9eff' },
    { label: 'Lead Activity', value: (byType.lead_created||0) + (byType.status_changed||0) },
    { label: 'Payments', value: byType.payment_marked || 0, color: '#22c55e' },
    { label: 'Consultations', value: byType.consultation_completed || 0 }
  ]);

  var listHtml = '<div style="max-height:520px;overflow-y:auto;">';
  ev.slice(0, 300).forEach(function(e){
    var emoji = emojiFor[e.event_type] || '\u2022';
    var when = new Date(e.created_at);
    var pretty = when.toLocaleString();
    var detail = '';
    if (e.event_type === 'status_changed' && e.event_data) {
      detail = ((e.event_data.from || '?') + ' \u2192 ' + (e.event_data.to || '?'));
    } else if (e.event_type === 'payment_marked' && e.event_data && e.event_data.amount) {
      detail = '$' + e.event_data.amount;
    }
    listHtml += '<div style="display:flex;align-items:flex-start;gap:10px;padding:8px 0;border-bottom:1px solid var(--border);">'
      + '<div style="font-size:16px;">' + emoji + '</div>'
      + '<div style="flex:1;">'
        + '<div style="font-size:13px;"><b>' + (e.lead_name || '(no name)') + '</b> \u00b7 ' + e.event_type.replace(/_/g,' ') + (detail ? ' \u2014 ' + detail : '') + '</div>'
        + '<div style="font-size:11px;color:var(--text-muted);margin-top:2px;">' + pretty + '</div>'
      + '</div>'
    + '</div>';
  });
  if (ev.length === 0) listHtml += '<div style="color:var(--text-muted);font-size:13px;padding:20px;text-align:center;">No events in this date range.</div>';
  listHtml += '</div>';

  body.innerHTML = statHtml + repCard('Activity Timeline (' + ev.length + ' events)', listHtml);
}
