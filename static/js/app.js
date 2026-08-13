// PrecisionCalc frontend logic
(() => {
  const form = document.getElementById('calc-form');
  const numberInput = document.getElementById('number');
  const divisorInput = document.getElementById('divisor');
  const precisionInput = document.getElementById('precision');
  const resultFlow = document.getElementById('result-flow');
  const resetBtn = document.getElementById('reset-btn');

  // Navigation
  const navLinks = document.querySelectorAll('.nav-link');
  const panels = document.querySelectorAll('.panel');
  navLinks.forEach(btn => btn.addEventListener('click', () => openSection(btn.dataset.section)));

  function openSection(id){
    panels.forEach(p=>p.id===id?p.classList.remove('hidden'):p.classList.add('hidden'));
    navLinks.forEach(n=>n.dataset.section===id? n.classList.add('active'): n.classList.remove('active'));
  }

  // Mobile drawer
  const mobileBtn = document.getElementById('mobile-menu-btn');
  const drawer = document.getElementById('mobile-drawer');
  const closeDrawer = document.getElementById('close-drawer');
  const drawerLinks = document.querySelectorAll('.drawer-link');

  mobileBtn.addEventListener('click', ()=>{drawer.setAttribute('aria-hidden','false'); mobileBtn.setAttribute('aria-expanded','true');});
  closeDrawer.addEventListener('click', closeMobile);
  drawer.addEventListener('click', (e)=>{ if(e.target===drawer) closeMobile(); });
  drawerLinks.forEach(b=>b.addEventListener('click',(e)=>{openSection(b.dataset.section); closeMobile();}));
  function closeMobile(){drawer.setAttribute('aria-hidden','true'); mobileBtn.setAttribute('aria-expanded','false');}

  // Theme & Font
  const themeSelect = document.getElementById('theme-select');
  const themeSelect2 = document.getElementById('theme-select-2');
  const fontSelect = document.getElementById('font-select');
  const fontSelect2 = document.getElementById('font-select-2');

  function applyTheme(theme){
    document.documentElement.setAttribute('data-theme', theme === 'dark' ? 'dark' : 'light');
    themeSelect.value = theme; if(themeSelect2) themeSelect2.value = theme;
    localStorage.setItem('precisioncalc_theme', theme);
  }
  function applyFont(font){
    document.body.style.fontFamily = font;
    fontSelect.value = font; if(fontSelect2) fontSelect2.value = font;
    localStorage.setItem('precisioncalc_font', font);
  }

  themeSelect.addEventListener('change', ()=>applyTheme(themeSelect.value));
  if(themeSelect2) themeSelect2.addEventListener('change', ()=>applyTheme(themeSelect2.value));
  fontSelect.addEventListener('change', ()=>applyFont(fontSelect.value));
  if(fontSelect2) fontSelect2.addEventListener('change', ()=>applyFont(fontSelect2.value));

  // Restore preferences
  const savedTheme = localStorage.getItem('precisioncalc_theme') || 'light';
  const savedFont = localStorage.getItem('precisioncalc_font') || 'Inter, system-ui';
  applyTheme(savedTheme);
  applyFont(savedFont);

  // History
  function loadHistory(){
    try{ return JSON.parse(localStorage.getItem('precisioncalc_history')||'[]'); }catch(e){return []}
  }
  function saveHistory(arr){ localStorage.setItem('precisioncalc_history', JSON.stringify(arr)); renderHistory(); }
  const historyList = document.getElementById('history-list');

  function renderHistory(){
    const h = loadHistory();
    historyList.innerHTML = '';
    if(h.length===0){ historyList.innerHTML = '<div class="muted-small">No history yet.</div>'; return }
    h.slice().reverse().forEach((item, idx)=>{
      const div = document.createElement('div'); div.className='history-item card';
      div.innerHTML = `
        <div>
          <div><strong>${item.original} ÷ ${item.divisor} → ${item.display_result}</strong></div>
          <div class="muted-small">${new Date(item.timestamp).toLocaleString()}</div>
        </div>
        <div>
          <button class="btn ghost" data-i='${idx}'>Delete</button>
        </div>`;
      const btn = div.querySelector('button'); btn.addEventListener('click', ()=>{ removeHistoryAt(idx); });
      historyList.appendChild(div);
    });
  }

  function addToHistory(item){ const h=loadHistory(); h.push(item); saveHistory(h); }
  function removeHistoryAt(indexFromEnd){ const h=loadHistory(); const i = h.length - 1 - indexFromEnd; if(i>=0){ h.splice(i,1); saveHistory(h); } }
  document.getElementById('clear-history').addEventListener('click', ()=>{ if(confirm('Clear all history?')){ saveHistory([]); } });

  renderHistory();

  // Validation helpers
  function showError(el, msg){ el.textContent = msg; }
  function clearErrors(){ showError(document.getElementById('number-error'),''); showError(document.getElementById('divisor-error'),''); }

  form.addEventListener('submit', async (e)=>{
    e.preventDefault(); clearErrors(); resultFlow.classList.add('hidden');
    const num = numberInput.value.trim(); const div = divisorInput.value.trim(); const precision = parseInt(precisionInput.value,10)||0;
    let hasError=false;
    if(num===''){ showError(document.getElementById('number-error'),'Please enter a valid number.'); hasError=true }
    if(div===''|| isNaN(Number(div))){ showError(document.getElementById('divisor-error'),'Please enter a valid divisor.'); hasError=true }
    if(Number(div)===0){ showError(document.getElementById('divisor-error'),'Divisor cannot be zero.'); hasError=true }
    if(hasError) return;

    // Submit to backend
    try{
      const resp = await fetch('/api/calculate', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({number:num,divisor:div,precision:precision})});
      const data = await resp.json();
      if(!resp.ok){ alert(data.error || 'Calculation error'); return }
      showResultFlow(data);
      addToHistory(data);
    }catch(err){ alert('Network error: '+err.message) }
  });

  resetBtn.addEventListener('click', ()=>{ form.reset(); resultFlow.classList.add('hidden'); clearErrors(); });

  function showResultFlow(data){
    resultFlow.innerHTML = '';
    const steps = [
      {label:'Original Number', value:data.original},
      {label:'Division', value:`${data.original} ÷ ${data.divisor}`},
      {label:'Exact Result', value:data.exact_result},
      {label:'Displayed Result', value:data.display_result},
      {label:'Reverse Using Displayed Value', value:`${data.display_result} × ${data.divisor} = ${data.reverse_result_from_display}`},
      {label:'Precision Difference', value:`${data.precision_difference}`},
      {label:'Exact Recovery', value:`${data.exact_result} × ${data.divisor} = ${data.recovered_result}`}
    ];
    steps.forEach(s=>{
      const node = document.createElement('div'); node.className='step card';
      node.innerHTML = `<div class="label">${s.label}</div><div class="value">${s.value}</div>`;
      resultFlow.appendChild(node);
    });
    resultFlow.classList.remove('hidden');
  }

})();
