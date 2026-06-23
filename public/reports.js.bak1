// ============== REPORTS TAB ==============
var __REPORTS_SUB = localStorage.getItem('arcascend_reports_sub') || 'leads';
var __REPORTS_FROM = null;
var __REPORTS_TO = null;
var __REPORTS_EVENTS = null;
var __REPORTS_LOADING = false;
var __REPORTS_CHART = null;

function reportsInitRange() {
  if (__REPORTS_FROM && __REPORTS_TO) return;
  var now = new Date();
  var first = new Date(now.getFullYear(), now.getMonth(), 1);
  __REPORTS_FROM = first.toISOString().slice(0,10);
  __REPORTS_TO = now.toISOString().slice(0,10);
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
    __REPORTS_EVENTS = null;
    renderReportsTab();
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

function repDateBuckets() {
  // Returns array of YYYY-MM-DD strings from FROM to TO
  var out = [];
  var d = new Date(__REPORTS_FROM + 'T00:00:00');
  var end = new Date(__REPORTS_TO + 'T00:00:00');
  while (d <= end) {
    out.push(d.toISOString().slice(0,10));
    d.setDate(d.getDate() + 1);
  }
  return out;
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

  // Status distribution from current LEADS state (date range doesn't apply meaningfully here)
  var statusCounts = {};
  (LEADS || []).forEach(function(L){
    var s = (L.status || 'New');
    statusCounts[s] = (statusCounts[s] || 0) + 1;
  });

  // Build daily series for "Leads added"
  var buckets = repDateBuckets();
  var seriesMap = {};
  buckets.forEach(function(d){ seriesMap[d] = 0; });
  created.forEach(function(e){
    var d = e.created_at.slice(0,10);
    if (seriesMap[d] !== undefined) seriesMap[d]++;
  });
  var seriesData = buckets.map(function(d){ return seriesMap[d]; });

  var html = '';
  html += repStatsGrid([
    { label:'Leads Added', value: created.length, color:'#4f9eff' },
    { label:'Intake Forms Submitted', value: intake.length, color:'#22c55e' },
    { label:'Status Changes', value: statusChanges.length, color:'#f59e0b' },
    { label:'Total Leads (All Time)', value: (LEADS||[]).length }
  ]);

  html += repCard('Leads Added Over Time', '<div style="height:260px;"><canvas id="rep-chart-leads"></canvas></div>');
  html += repCard('Status Distribution (Current)', '<div>' + Object.keys(statusCounts).map(function(s){
    var pct = Math.round(statusCounts[s] / Math.max(1, (LEADS||[]).length) * 100);
    return '<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;font-size:13px;">'
      + '<div style="width:120px;color:var(--text-muted);">' + s + '</div>'
      + '<div style="flex:1;background:var(--panel2);height:18px;border-radius:4px;overflow:hidden;"><div style="background:var(--accent);height:100%;width:' + pct + '%;"></div></div>'
      + '<div style="width:60px;text-align:right;color:var(--text);">' + statusCounts[s] + ' (' + pct + '%)</div>'
      + '</div>';
  }).join('') + '</div>');

  body.innerHTML = html;
  repDrawLineChart('rep-chart-leads', 'Leads added', buckets, seriesData, '#4f9eff');
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
    var d = e.created_at.slice(0,10);
    var amt = parseFloat((e.event_data && e.event_data.amount) || 0) || 0;
    if (revMap[d] !== undefined) revMap[d] += amt;
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
  won.forEach(function(e){ var d = e.created_at.slice(0,10); if(wonMap[d]!==undefined) wonMap[d]++; });
  lost.forEach(function(e){ var d = e.created_at.slice(0,10); if(lostMap[d]!==undefined) lostMap[d]++; });

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
