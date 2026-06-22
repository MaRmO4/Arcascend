// ============== ACTIVE CLIENTS BOARD ==============
var __ACTIVE_VIEW = localStorage.getItem('arcascend_activeview') || 'list';

function sessionsToRow(L) {
  if (L.weeklySessionsOverride) return L.weeklySessionsOverride;
  // Prefer billing.package label since that's what drag now sets
  var pkg = (L.billing && L.billing.package) || '';
  if (pkg.indexOf('5x') === 0) return '5x+';
  if (pkg.indexOf('4x') === 0) return '4x';
  if (pkg.indexOf('3x') === 0) return '3x';
  if (pkg.indexOf('2x') === 0) return '2x';
  if (pkg.indexOf('1x') === 0) return '1x';
  // Fall back to session-count buckets
  var n = parseInt((L.billing && L.billing.sessions) || 0, 10);
  if (n >= 13) return '4x';
  if (n >= 9) return '3x';
  if (n >= 6) return '2x';
  return '1x';
}

function activeIsPaid(L) {
  return !!(L.billing && L.billing.paid);
}

function setActivePaid(L, paid) {
  if (!L.billing) L.billing = {};
  L.billing.paid = !!paid;
  if (paid && typeof logEvent === 'function') {
    logEvent('payment_marked', L.name, { amount: typeof leadTotal === 'function' ? leadTotal(L) : null });
  }
}

function renderActiveClientsBoard() {
  var main = document.getElementById('main');
  if (!main) return;
  var rows = ['1x','2x','3x','4x','5x+'];
  var clients = (typeof activeClients === 'function') ? activeClients() : LEADS.filter(function(L){ return L.billing && L.billing.active; });

  var bucket = {};
  rows.forEach(function(r){ bucket[r] = { Projected:[], Paid:[] }; });
  clients.forEach(function(L){
    var r = sessionsToRow(L);
    if (rows.indexOf(r) < 0) r = '1x';
    var col = activeIsPaid(L) ? 'Paid' : 'Projected';
    bucket[r][col].push(L);
  });

  var html = '';
  html += '<div style="display:flex;align-items:center;justify-content:space-between;padding:14px 20px 4px;">';
  html += '<div style="font-size:18px;font-weight:600;">Active Clients <span style="color:var(--text-muted);font-weight:normal;font-size:13px;">(' + clients.length + ')</span></div>';
  html += '<div style="display:inline-flex;background:var(--panel);border:1px solid var(--border);border-radius:8px;overflow:hidden;">';
  html += '<button id="ac-view-list" style="padding:6px 14px;border:none;background:' + (__ACTIVE_VIEW==='list'?'var(--accent)':'transparent') + ';color:' + (__ACTIVE_VIEW==='list'?'#fff':'var(--text)') + ';font-size:13px;cursor:pointer;">List</button>';
  html += '<button id="ac-view-board" style="padding:6px 14px;border:none;background:' + (__ACTIVE_VIEW==='board'?'var(--accent)':'transparent') + ';color:' + (__ACTIVE_VIEW==='board'?'#fff':'var(--text)') + ';font-size:13px;cursor:pointer;">Board</button>';
  html += '</div></div>';

  if (__ACTIVE_VIEW === 'list') {
    // Inject our List/Board toggle above main, then defer to the existing rich card renderer.
    main.innerHTML = html;
    var listMount = document.createElement('div');
    listMount.id = 'ac-list-mount';
    main.appendChild(listMount);
    if (typeof renderClientsTab === 'function') {
      // renderClientsTab() rewrites #main internals; capture, then prepend our toggle bar back
      var toggleBar = main.firstChild.cloneNode(true);
      renderClientsTab();
      // Re-inject the toggle bar at the top of #main
      if (main.firstChild) {
        main.insertBefore(toggleBar, main.firstChild);
      }
      // Re-wire the buttons in the freshly inserted toggle bar
      wireActiveToggle();
    } else {
      wireActiveToggle();
    }
    return;
  }

  html += '<div style="padding:14px 20px 30px;">';
  html += '<div style="display:grid;grid-template-columns:60px 1fr 1fr;gap:8px;align-items:stretch;">';
  html += '<div></div>';
  html += '<div style="text-align:center;font-size:12px;font-weight:600;color:var(--text-muted);padding:4px;">PROJECTED</div>';
  html += '<div style="text-align:center;font-size:12px;font-weight:600;color:var(--won);padding:4px;">PAID</div>';
  rows.forEach(function(r){
    html += '<div style="display:flex;align-items:center;justify-content:flex-end;font-size:13px;color:var(--text-muted);font-weight:600;padding:0 6px;">' + r + '</div>';
    ['Projected','Paid'].forEach(function(col){
      var list = bucket[r][col];
      html += '<div class="ac-cell" data-row="' + r + '" data-col="' + col + '" style="background:var(--panel);border:1px solid var(--border);border-radius:8px;min-height:50px;padding:6px;">';
      list.forEach(function(L){
        var sess = (L.billing && L.billing.sessions) ? L.billing.sessions : 0;
        var price = (L.billing && L.billing.rate) ? L.billing.rate : 0;
        var subtitle = sess + ' sess' + (price ? ' · $' + (sess*price) : '');
        html += '<div class="ac-card" draggable="true" data-name="' + (L.name||'').replace(/"/g,'&quot;') + '" style="background:var(--panel2);border:1px solid var(--border);border-radius:6px;padding:5px 8px;margin-bottom:4px;cursor:grab;">';
        html += '<div style="font-size:13px;font-weight:600;">' + (L.name||'(no name)') + '</div>';
        html += '<div style="font-size:11px;color:var(--text-muted);margin-top:2px;">' + subtitle + '</div>';
        html += '</div>';
      });
      html += '</div>';
    });
  });
  html += '</div></div>';
  main.innerHTML = html;
  wireActiveToggle();
  wireActiveBoardDnD();
}

function wireActiveToggle(){
  var b1 = document.getElementById('ac-view-list');
  var b2 = document.getElementById('ac-view-board');
  if (b1) b1.addEventListener('click', function(){ __ACTIVE_VIEW='list'; localStorage.setItem('arcascend_activeview','list'); renderActiveClientsBoard(); });
  if (b2) b2.addEventListener('click', function(){ __ACTIVE_VIEW='board'; localStorage.setItem('arcascend_activeview','board'); renderActiveClientsBoard(); });
}

function wireActiveBoardDnD(){
  var dragName = null;
  // Auto-scroll when dragging near top/bottom of viewport
  var __dragScrollTimer = null;
  function handleDragScroll(e){
    var y = e.clientY;
    var vh = window.innerHeight;
    var edge = 80; // px from top/bottom that triggers scroll
    var speed = 0;
    if (y < edge) speed = -Math.max(6, (edge - y) / 4);
    else if (y > vh - edge) speed = Math.max(6, (y - (vh - edge)) / 4);
    if (speed !== 0) window.scrollBy(0, speed);
  }
  document.addEventListener('dragover', handleDragScroll);
  document.querySelectorAll('.ac-card').forEach(function(card){
    card.addEventListener('click', function(){
      if (card.__justDragged) { card.__justDragged = false; return; }
      if (typeof openLead === 'function') openLead(card.dataset.name);
    });
    card.addEventListener('dragstart', function(e){
      dragName = card.dataset.name;
      card.style.opacity = '0.5';
      try { e.dataTransfer.setData('text/plain', dragName); } catch(_){}
    });
    card.addEventListener('dragend', function(){
      card.style.opacity = '1';
      card.__justDragged = true;
      setTimeout(function(){ card.__justDragged = false; }, 300);
    });
  });
  document.querySelectorAll('.ac-cell').forEach(function(cell){
    cell.addEventListener('dragover', function(e){ e.preventDefault(); cell.style.outline = '2px dashed var(--accent)'; });
    cell.addEventListener('dragleave', function(){ cell.style.outline = 'none'; });
    cell.addEventListener('drop', function(e){
      e.preventDefault();
      cell.style.outline = 'none';
      var name = dragName || e.dataTransfer.getData('text/plain');
      if (!name) return;
      var L = LEADS.find(function(x){ return x.name === name; });
      if (!L) return;
      var newRow = cell.dataset.row;
      var newCol = cell.dataset.col;
      // Map row -> package label and default sessions (matches existing PACKAGE dropdown options)
      var ROW_TO_PACKAGE = { '1x':'1x/week', '2x':'2x/week', '3x':'3x/week', '4x':'4x/week', '5x+':'5x+/week' };
      var ROW_TO_SESSIONS = { '1x':4, '2x':8, '3x':12, '4x':16, '5x+':20 };
      if (!L.billing) L.billing = {};
      L.billing.package = ROW_TO_PACKAGE[newRow] || L.billing.package;
      L.billing.sessions = ROW_TO_SESSIONS[newRow] || L.billing.sessions;
      // Clear the override since the row now matches sessions naturally
      delete L.weeklySessionsOverride;
      setActivePaid(L, newCol === 'Paid');
      if (typeof saveState === 'function') saveState();
      renderActiveClientsBoard();
    });
  });
}
