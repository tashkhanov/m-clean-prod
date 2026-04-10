/**
 * M-CLEAN Calculator v8 — Clean icons, null-safe, qa-btn fixed
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Calculator v8 loaded');

    // ═══════════════════════════════════════════════════════════════
    // LOAD DATA
    // ═══════════════════════════════════════════════════════════════
    var servicesEl = document.getElementById('services-data');
    var optionsEl = document.getElementById('all-options-data');
    var coeffsEl = document.getElementById('curtain-coeffs-data');
    var minOrderEl = document.getElementById('min-order-data');

    function parseF(val, def) {
        if (!val) return def || 0;
        var s = String(val).replace(',', '.');
        var n = parseFloat(s);
        return isNaN(n) ? (def || 0) : n;
    }

    if (!servicesEl) { console.error('No services-data'); return; }

    var SERVICES_RAW = JSON.parse(servicesEl.textContent);
    // services-data can be array (services.html) or single object (service_detail.html)
    var SERVICES = Array.isArray(SERVICES_RAW) ? SERVICES_RAW : [SERVICES_RAW];
    var OPTIONS_RAW = optionsEl ? JSON.parse(optionsEl.textContent) : [];
    var OPTIONS = Array.isArray(OPTIONS_RAW) ? OPTIONS_RAW : [];
    var COEFFS = coeffsEl ? JSON.parse(coeffsEl.textContent) : [];
    var MIN_ORDER = minOrderEl ? parseInt(JSON.parse(minOrderEl.textContent)) : 7000;

    console.log('Calculator loaded. SERVICES:', SERVICES.length, 'OPTIONS:', OPTIONS.length, 'COEFFS:', COEFFS.length);

    var servicesMap = {};
    SERVICES.forEach(function(s) { servicesMap[s.id] = s; });

    // ═══════════════════════════════════════════════════════════════
    // CLIENT FURNITURE CATALOG (Premium SVG Icons)
    // ═══════════════════════════════════════════════════════════════
    var CAT = {
        sofas: [
            {id:'s1',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 9V6a2 2 0 00-2-2H6a2 2 0 00-2 2v3"/><path d="M2 11v5a2 2 0 002 2h16a2 2 0 002-2v-5a2 2 0 00-4 0v2H6v-2a2 2 0 00-4 0z"/><path d="M4 18v2M20 18v2"/></svg>',n:'2-местный диван',d:'100–150 см',p:13000},
            {id:'s2',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 9V6a2 2 0 00-2-2H6a2 2 0 00-2 2v3"/><path d="M2 11v5a2 2 0 002 2h16a2 2 0 002-2v-5a2 2 0 00-4 0v2H6v-2a2 2 0 00-4 0z"/><path d="M4 18v2M20 18v2"/></svg>',n:'3-местный диван',d:'150–200 см',p:17000},
            {id:'s3',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 9V6a2 2 0 00-2-2H6a2 2 0 00-2 2v3"/><path d="M2 11v5a2 2 0 002 2h16a2 2 0 002-2v-5a2 2 0 00-4 0v2H6v-2a2 2 0 00-4 0z"/><path d="M4 18v2M20 18v2"/></svg>',n:'4-местный диван',d:'200–250 см',p:20000},
            {id:'s4',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 9V6a2 2 0 00-2-2H6a2 2 0 00-2 2v3"/><path d="M2 11v5a2 2 0 002 2h16a2 2 0 002-2v-5a2 2 0 00-4 0v2H6v-2a2 2 0 00-4 0z"/><path d="M4 18v2M20 18v2"/></svg>',n:'Угловой (2+угол)',d:'~200×150 см',p:22000},
            {id:'s5',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 9V6a2 2 0 00-2-2H6a2 2 0 00-2 2v3"/><path d="M2 11v5a2 2 0 002 2h16a2 2 0 002-2v-5a2 2 0 00-4 0v2H6v-2a2 2 0 00-4 0z"/><path d="M4 18v2M20 18v2"/></svg>',n:'Угловой (3+угол)',d:'~250×180 см',p:25000},
            {id:'s6',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 9V6a2 2 0 00-2-2H6a2 2 0 00-2 2v3"/><path d="M2 11v5a2 2 0 002 2h16a2 2 0 002-2v-5a2 2 0 00-4 0v2H6v-2a2 2 0 00-4 0z"/><path d="M4 18v2M20 18v2"/></svg>',n:'Угловой (4+угол)',d:'~300×200 см',p:30000},
            {id:'s7',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 9V6a2 2 0 00-2-2H6a2 2 0 00-2 2v3"/><path d="M2 11v5a2 2 0 002 2h16a2 2 0 002-2v-5a2 2 0 00-4 0v2H6v-2a2 2 0 00-4 0z"/><path d="M4 18v2M20 18v2"/></svg>',n:'П-образный (6 мест)',d:'300–400 см',p:35000},
            {id:'s8',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 4v16"/><path d="M2 8h18a2 2 0 012 2v10"/><path d="M2 17h20"/><path d="M6 8v9"/></svg>',n:'Спальное место дивана',d:'любой механизм',p:7000},
        ],
        chairs: [
            {id:'c1',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 9V6a2 2 0 00-2-2H7a2 2 0 00-2 2v3"/><path d="M3 11v5a2 2 0 002 2h14a2 2 0 002-2v-5a2 2 0 00-4 0H7a2 2 0 00-4 0z"/></svg>',n:'Кресло стандартное',d:'50–70 см',p:7500},
            {id:'c2',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 9V6a2 2 0 00-2-2H7a2 2 0 00-2 2v3"/><path d="M3 11v5a2 2 0 002 2h14a2 2 0 002-2v-5a2 2 0 00-4 0H7a2 2 0 00-4 0z"/></svg>',n:'Кресло большое (лаунж)',d:'70–100 см',p:10000},
            {id:'c3',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 9V6a2 2 0 00-2-2H7a2 2 0 00-2 2v3"/><path d="M3 11v5a2 2 0 002 2h14a2 2 0 002-2v-5a2 2 0 00-4 0H7a2 2 0 00-4 0z"/></svg>',n:'Кресло реклайнер',d:'80–100 см',p:12000},
            {id:'c4',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 9V6a2 2 0 00-2-2H7a2 2 0 00-2 2v3"/><path d="M3 11v5a2 2 0 002 2h14a2 2 0 002-2v-5a2 2 0 00-4 0H7a2 2 0 00-4 0z"/></svg>',n:'Кухонный уголок',p:12000},
            {id:'c5',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 9V6a2 2 0 00-2-2H7a2 2 0 00-2 2v3"/><path d="M3 11v5a2 2 0 002 2h14a2 2 0 002-2v-5a2 2 0 00-4 0H7a2 2 0 00-4 0z"/></svg>',n:'Стул (мягкая спинка)',p:3000},
            {id:'c6',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 9V6a2 2 0 00-2-2H7a2 2 0 00-2 2v3"/><path d="M3 11v5a2 2 0 002 2h14a2 2 0 002-2v-5a2 2 0 00-4 0H7a2 2 0 00-4 0z"/></svg>',n:'Стул (без спинки)',p:2500},
        ],
        beds: [
            {id:'b1',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 4v16"/><path d="M2 8h18a2 2 0 012 2v10"/><path d="M2 17h20"/><path d="M6 8v9"/></svg>',n:'Кровать (изголовье + царги)',d:'90–200 см',p:15000},
            {id:'b2',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 4v16"/><path d="M2 8h18a2 2 0 012 2v10"/><path d="M2 17h20"/><path d="M6 8v9"/></svg>',n:'Изголовье отдельно',d:'90–200 см',p:8000},
        ],
        misc: [
            {id:'p1',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.5 10.5a3.5 3.5 0 01-3.5 3.5H7a3.5 3.5 0 01-3.5-3.5 3.5 3.5 0 013.5-3.5h10a3.5 3.5 0 013.5 3.5z"/></svg>',n:'Подушка маленькая',d:'40×30 см',p:1500},
            {id:'p2',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.5 10.5a3.5 3.5 0 01-3.5 3.5H7a3.5 3.5 0 01-3.5-3.5 3.5 3.5 0 013.5-3.5h10a3.5 3.5 0 013.5 3.5z"/></svg>',n:'Подушка средняя',d:'60×40 см',p:2000},
            {id:'p3',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.5 10.5a3.5 3.5 0 01-3.5 3.5H7a3.5 3.5 0 01-3.5-3.5 3.5 3.5 0 013.5-3.5h10a3.5 3.5 0 013.5 3.5z"/></svg>',n:'Подушка большая',d:'70×50 см',p:2500},
        ],
        mattress: [
            {id:'m1',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="6" width="20" height="12" rx="2"/><path d="M6 6V4M18 6V4M2 12h20"/></svg>',n:'Матрас детский',d:'60×120 см',p:5000},
            {id:'m2',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="6" width="20" height="12" rx="2"/><path d="M6 6V4M18 6V4M2 12h20"/></svg>',n:'Матрас односпальный',d:'90×190 см',p:7500},
            {id:'m3',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="6" width="20" height="12" rx="2"/><path d="M6 6V4M18 6V4M2 12h20"/></svg>',n:'Матрас полутораспальный',d:'120×190 см',p:12500},
            {id:'m4',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="6" width="20" height="12" rx="2"/><path d="M6 6V4M18 6V4M2 12h20"/></svg>',n:'Матрас двуспальный',d:'190×190 см',p:15000},
        ],
        // ── БИЗНЕС-КАТЕГОРИИ (фронтенд-хардкод) ──
        bizChairs: [
            {id:'o1',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 9V6a2 2 0 00-2-2H7a2 2 0 00-2 2v3"/><path d="M3 11v5a2 2 0 002 2h14a2 2 0 002-2v-5a2 2 0 00-4 0H7a2 2 0 00-4 0z"/></svg>',n:'Офисный стул (ткань)',p:2500},
            {id:'o2',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 9V6a2 2 0 00-2-2H7a2 2 0 00-2 2v3"/><path d="M3 11v5a2 2 0 002 2h14a2 2 0 002-2v-5a2 2 0 00-4 0H7a2 2 0 00-4 0z"/></svg>',n:'Офисный стул (кожа/экокожа)',p:2000},
            {id:'o3',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 9V6a2 2 0 00-2-2H7a2 2 0 00-2 2v3"/><path d="M3 11v5a2 2 0 002 2h14a2 2 0 002-2v-5a2 2 0 00-4 0H7a2 2 0 00-4 0z"/></svg>',n:'Офисное кресло (стандарт)',p:3500},
            {id:'o4',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 9V6a2 2 0 00-2-2H7a2 2 0 00-2 2v3"/><path d="M3 11v5a2 2 0 002 2h14a2 2 0 002-2v-5a2 2 0 00-4 0H7a2 2 0 00-4 0z"/></svg>',n:'Кресло руководителя',p:6000},
        ],
        bizSofas: [
            {id:'os1',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 9V6a2 2 0 00-2-2H6a2 2 0 00-2 2v3"/><path d="M2 11v5a2 2 0 002 2h16a2 2 0 002-2v-5a2 2 0 00-4 0v2H6v-2a2 2 0 00-4 0z"/><path d="M4 18v2M20 18v2"/></svg>',n:'Диван 2-местный',p:12000},
            {id:'os2',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 9V6a2 2 0 00-2-2H6a2 2 0 00-2 2v3"/><path d="M2 11v5a2 2 0 002 2h16a2 2 0 002-2v-5a2 2 0 00-4 0v2H6v-2a2 2 0 00-4 0z"/><path d="M4 18v2M20 18v2"/></svg>',n:'Диван 3-местный',p:17000},
            {id:'os3',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 9V6a2 2 0 00-2-2H6a2 2 0 00-2 2v3"/><path d="M2 11v5a2 2 0 002 2h16a2 2 0 002-2v-5a2 2 0 00-4 0v2H6v-2a2 2 0 00-4 0z"/><path d="M4 18v2M20 18v2"/></svg>',n:'Угловой диван',p:25000},
        ],
        bizConf: [
            {id:'cf1',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 9V6a2 2 0 00-2-2H7a2 2 0 00-2 2v3"/><path d="M3 11v5a2 2 0 002 2h14a2 2 0 002-2v-5a2 2 0 00-4 0H7a2 2 0 00-4 0z"/></svg>',n:'Конференц-кресло',p:4000},
            {id:'cf2',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 9V6a2 2 0 00-2-2H7a2 2 0 00-2 2v3"/><path d="M3 11v5a2 2 0 002 2h14a2 2 0 002-2v-5a2 2 0 00-4 0H7a2 2 0 00-4 0z"/></svg>',n:'Мягкий стул (переговорная)',p:3000},
        ],
        bizLounge: [
            {id:'lz1',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.5 10.5a3.5 3.5 0 01-3.5 3.5H7a3.5 3.5 0 01-3.5-3.5 3.5 3.5 0 013.5-3.5h10a3.5 3.5 0 013.5 3.5z"/></svg>',n:'Пуф',p:3500},
            {id:'lz2',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2"/></svg>',n:'Банкетка',p:6000},
        ],
        bizPanels: [
            {id:'wp1',e:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/></svg>',n:'Мягкая стеновая панель',d:'за 1 м²',p:3000},
        ],
    };


    // ═══════════════════════════════════════════════════════════════
    // STATE
    // ═══════════════════════════════════════════════════════════════
    var state = {
        activeCalcType: 'furniture',
        uphTarget: 'home',       // 'home' | 'business'
        cart: {},
        itemAddons: {},
        matState: {},
        uphMult: 1,
        dirtMult: 1,
        hairM: 1,
        boxQ: 1,
        carpetArea: 0,
        carpetMode: 'general',
        carpetMaterial: 'synthetic',
        curtainMode: 'weight',
        curtainWeight: 0,
        curtainWindows: [],
        curtainRoman: false,
        romanQty: 1,
        curtainRemoval: false,
        curtainHanging: false,
        curtainIroning: false,
        selectedOptions: [],
        isNewClient: false,
        isCombo: false
    };


    var fmt = function(n) { return Math.round(n).toLocaleString('ru-RU') + ' ₸'; };

    var isSingleService = document.getElementById('single-service-calc');
    var BASE_PRICE = 0;
    if (isSingleService) {
        var svcId = parseInt(isSingleService.dataset.serviceId) || 0;
        var svc = servicesMap[svcId];
        if (svc) {
            BASE_PRICE = svc.base_price || svc.price || 0;
            console.log('Single Service Mode: ' + svc.name + ' (' + BASE_PRICE + ' ₸)');
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // MAIN TABS (only on services.html)
    // ═══════════════════════════════════════════════════════════════
    var mainTabs = document.querySelectorAll('.calc-main-tab');
    if (mainTabs.length > 0) {
        mainTabs.forEach(function(tab) {
            tab.addEventListener('click', function() {
                mainTabs.forEach(function(t) { t.classList.remove('active'); });
                this.classList.add('active');

                var type = this.dataset.calcType;
                state.activeCalcType = type;

                var fw = document.getElementById('calc-furniture-wrapper');
                var cw = document.getElementById('calc-carpet-wrapper');
                var cuw = document.getElementById('calc-curtains-wrapper');
                if (fw) fw.style.display = type === 'furniture' ? '' : 'none';
                if (cw) cw.style.display = type === 'carpet' ? '' : 'none';
                if (cuw) cuw.style.display = type === 'curtains' ? '' : 'none';

                recalc();
            });
        });
    }

    if (isSingleService) {
        var svcId = parseInt(isSingleService.dataset.serviceId) || 0;
        var svc = servicesMap[svcId];
        if (svc) {
            BASE_PRICE = svc.base_price || svc.price || 0;
            
            // 1. Client Type (Home/Business)
            if (isSingleService.dataset.defaultClient) {
                state.uphTarget = isSingleService.dataset.defaultClient;
            } else if (svc.default_client_type) {
                state.uphTarget = svc.default_client_type;
            }
            
            // 2. Material (Fabric/Leather)
            var defMat = isSingleService.dataset.defaultMaterial || svc.default_material || 'fabric';
            state.uphMult = (defMat === 'leather') ? 1.5 : 1;

            // 3. activeCalcType - CRITICAL: separating furniture from default
            if (svc.calc_type === 'carpet') state.activeCalcType = 'carpet';
            else if (svc.calc_type === 'curtains') state.activeCalcType = 'curtains';
            else if (svc.calc_type === 'furniture') state.activeCalcType = 'furniture';
            else state.activeCalcType = 'default';

            // Sync UI Tabs (Home/Business)
            document.querySelectorAll('.tab-btn').forEach(function(b) {
                b.classList.toggle('active', b.dataset.tab === state.uphTarget);
            });
            var fh = document.getElementById('furn-home');
            var fb = document.getElementById('furn-business');
            if (fh && fb) {
                fh.style.display = (state.uphTarget === 'home') ? 'block' : 'none';
                fb.style.display = (state.uphTarget === 'business') ? 'block' : 'none';
            }

            // Sync Material Buttons
            document.querySelectorAll('.uph-btn').forEach(function(b) {
                var btnVal = b.dataset.upholstery || b.dataset.uph;
                b.classList.toggle('active', btnVal === defMat);
            });

            // Sync Leather Note
            var leatherNote = document.getElementById('leather-note');
            if (leatherNote) leatherNote.style.display = (state.uphMult > 1) ? 'block' : 'none';

            // Hide main tabs on detail page
            var tabsEl = document.getElementById('calc-main-tabs');
            if (tabsEl) tabsEl.style.display = 'none';

            // Handle main containers display
            var fw_wrap = document.getElementById('calc-furniture-wrapper');
            var cw_wrap = document.getElementById('calc-carpet-wrapper');
            var cuw_wrap = document.getElementById('calc-curtains-wrapper');
            if (fw_wrap) fw_wrap.style.display = (state.activeCalcType === 'furniture' || state.activeCalcType === 'default') ? '' : 'none';
            if (cw_wrap) cw_wrap.style.display = (state.activeCalcType === 'carpet') ? '' : 'none';
            if (cuw_wrap) cuw_wrap.style.display = (state.activeCalcType === 'curtains') ? '' : 'none';

            // Selective visibility within furniture/default wrapper
            if (fw_wrap) {
                var mseg = fw_wrap.querySelector('.master-seg');
                var furn = fw_wrap.querySelector('.furniture-wrapper');
                
                // Show master-seg (home/business tabs) for furniture type only
                if (mseg) mseg.style.display = (state.activeCalcType === 'furniture') ? '' : 'none';
                // Show furniture catalog for BOTH 'furniture' and 'default' types
                if (furn) furn.style.display = (state.activeCalcType === 'furniture' || state.activeCalcType === 'default') ? '' : 'none';
            }
            
            recalc();
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // FURNITURE RENDERING
    // ═══════════════════════════════════════════════════════════════
    function renderItems(list, cid) {
        var el = document.getElementById(cid);
        if (!el) return;
        el.innerHTML = list.map(function(item) {
            var dispP = Math.round(item.p * state.uphMult);
            return '<div id="irow-' + item.id + '">' +
                '<div class="item-row">' +
                    '<span class="item-ico">' + item.e + '</span>' +
                    '<div class="item-info"><b>' + item.n + '</b>' + (item.d ? '<span>' + item.d + '</span>' : '') + '</div>' +
                    '<div class="item-price" id="ip-' + item.id + '">' + dispP.toLocaleString('ru-RU') + ' ₸' + (state.uphMult > 1 ? '<span class="lp">кожа +50%</span>' : '') + '</div>' +
                    '<div class="counter">' +
                        '<button class="cbtn" data-action="minus" data-item-id="' + item.id + '">−</button>' +
                        '<span class="cqty" id="q-' + item.id + '">0</span>' +
                        '<button class="cbtn p" data-action="plus" data-item-id="' + item.id + '">+</button>' +
                    '</div>' +
                '</div>' +
                '<div id="addons-' + item.id + '" style="display:none;padding:0 8px 10px;">' +
                    '<div class="item-addons">' +
                        '<div class="addon-chip" data-addon="drying" data-item-id="' + item.id + '"><span class="aci"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/></svg></span>Сушка<span class="addon-price">авто</span></div>' +
                        '<div class="addon-chip" data-addon="odor" data-item-id="' + item.id + '"><span class="aci"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg></span>Запах<span class="addon-price">+20%</span></div>' +
                        '<div class="addon-chip" data-addon="stain" data-item-id="' + item.id + '"><span class="aci"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg></span>Пятна<span class="addon-price">+15%</span></div>' +
                    '</div>' +
                '</div>' +
            '</div>';
        }).join('');
    }

    function renderMattresses() {
        var el = document.getElementById('cat-mattress');
        if (!el) return;
        el.innerHTML = CAT.mattress.map(function(m) {
            if (!state.matState[m.id]) state.matState[m.id] = {sides: 1};
            var dispP = Math.round(m.p * state.uphMult);
            var disp2 = Math.round(m.p * 2 * 0.95 * state.uphMult);
            return '<div class="mat-row" id="matrow-' + m.id + '">' +
                '<div class="mat-top">' +
                    '<span class="item-ico">' + m.e + '</span>' +
                    '<div class="mat-info"><b>' + m.n + '</b>' + (m.d ? '<span>' + m.d + '</span>' : '') + '</div>' +
                    '<div class="mat-price" id="mp-' + m.id + '">' + dispP.toLocaleString('ru-RU') + ' ₸/ст.' + (state.uphMult > 1 ? '<span class="lp">кожа +50%</span>' : '') + '</div>' +
                    '<div class="counter">' +
                        '<button class="cbtn" data-action="minus" data-mat-id="' + m.id + '">−</button>' +
                        '<span class="cqty" id="q-' + m.id + '">0</span>' +
                        '<button class="cbtn p" data-action="plus" data-mat-id="' + m.id + '">+</button>' +
                    '</div>' +
                '</div>' +
                '<div id="mat-details-' + m.id + '" style="display:none">' +
                    '<div class="sides-tog" style="margin-top:10px">' +
                        '<div class="side-btn active" id="side1-' + m.id + '" data-sides="1" data-mat-id="' + m.id + '">1 сторона — ' + dispP.toLocaleString('ru-RU') + ' ₸</div>' +
                        '<div class="side-btn" id="side2-' + m.id + '" data-sides="2" data-mat-id="' + m.id + '">2 стороны — ' + disp2.toLocaleString('ru-RU') + ' ₸ (−5%)</div>' +
                    '</div>' +
                    '<div class="item-addons" style="margin-top:8px">' +
                        '<div class="addon-chip" data-addon="drying" data-mat-id="' + m.id + '"><span class="aci"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/></svg></span>Сушка<span class="addon-price">авто</span></div>' +
                        '<div class="addon-chip" data-addon="odor" data-mat-id="' + m.id + '"><span class="aci"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg></span>Запах<span class="addon-price">7000/ст</span></div>' +
                        '<div class="addon-chip" data-addon="whiten" data-mat-id="' + m.id + '"><span class="aci"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/></svg></span>Отбеливание<span class="addon-price">10000/ст</span></div>' +
                    '</div>' +
                '</div>' +
            '</div>';
        }).join('');
    }

    function renderFurniture() {
        renderItems(CAT.sofas, 'cat-sofas');
        renderItems(CAT.chairs, 'cat-chairs');
        renderItems(CAT.beds, 'cat-beds');
        renderItems(CAT.misc, 'cat-misc');
        renderMattresses();
        // Бизнес-категории
        renderItems(CAT.bizChairs, 'cat-biz-chairs');
        renderItems(CAT.bizSofas, 'cat-biz-sofas');
        renderItems(CAT.bizConf, 'cat-biz-conf');
        renderItems(CAT.bizLounge, 'cat-biz-lounge');
        renderItems(CAT.bizPanels, 'cat-biz-panels');
    }


    function refreshPrices() {
        var allItems = [].concat(CAT.sofas, CAT.chairs, CAT.beds, CAT.misc,
                                  CAT.bizChairs, CAT.bizSofas, CAT.bizConf, CAT.bizLounge, CAT.bizPanels);
        allItems.forEach(function(item) {
            var el = document.getElementById('ip-' + item.id);
            if (!el) return;
            var dispP = Math.round(item.p * state.uphMult);
            el.innerHTML = dispP.toLocaleString('ru-RU') + ' ₸' + (state.uphMult > 1 ? '<span class="lp">кожа +50%</span>' : '');
        });
        CAT.mattress.forEach(function(m) {
            var el = document.getElementById('mp-' + m.id);
            if (!el) return;
            var dispP = Math.round(m.p * state.uphMult);
            var disp2 = Math.round(m.p * 2 * 0.95 * state.uphMult);
            el.innerHTML = dispP.toLocaleString('ru-RU') + ' ₸/ст.' + (state.uphMult > 1 ? '<span class="lp">кожа +50%</span>' : '');
            var s1 = document.getElementById('side1-' + m.id);
            var s2 = document.getElementById('side2-' + m.id);
            if (s1) s1.textContent = '1 сторона — ' + dispP.toLocaleString('ru-RU') + ' ₸';
            if (s2) s2.textContent = '2 стороны — ' + disp2.toLocaleString('ru-RU') + ' ₸ (−5%)';
        });
    }


    // ═══════════════════════════════════════════════════════════════
    // FURNITURE INTERACTIONS
    // ═══════════════════════════════════════════════════════════════
    function bump(id) {
        var el = document.getElementById('q-' + id);
        if (!el) return;
        el.textContent = (state.cart[id] || {q: 0}).q;
        el.classList.remove('bmp'); void el.offsetWidth; el.classList.add('bmp');
    }

    function chg(id, d, baseP, name, emoji) {
        if (!state.cart[id]) state.cart[id] = {q: 0, p: baseP, n: name, e: emoji};
        if (!state.itemAddons[id]) state.itemAddons[id] = {drying: false, odor: false, stain: false};
        state.cart[id].q = Math.max(0, state.cart[id].q + d);
        bump(id);
        var adPanel = document.getElementById('addons-' + id);
        if (adPanel) adPanel.style.display = state.cart[id].q > 0 ? 'block' : 'none';
        recalc();
    }

    function chgMat(id, d, baseP, name, emoji) {
        if (!state.cart[id]) state.cart[id] = {q: 0, p: baseP, n: name, e: emoji, isMat: true};
        if (!state.itemAddons[id]) state.itemAddons[id] = {drying: false, odor: false, whiten: false};
        if (!state.matState[id]) state.matState[id] = {sides: 1};
        state.cart[id].q = Math.max(0, state.cart[id].q + d);
        bump(id);
        var row = document.getElementById('matrow-' + id);
        if (row) row.classList.toggle('active-mat', state.cart[id].q > 0);
        var det = document.getElementById('mat-details-' + id);
        if (det) det.style.display = state.cart[id].q > 0 ? 'block' : 'none';
        recalc();
    }

    function setSides(id, sides) {
        if (!state.matState[id]) state.matState[id] = {sides: 1};
        state.matState[id].sides = sides;
        var s1 = document.getElementById('side1-' + id);
        var s2 = document.getElementById('side2-' + id);
        if (s1) s1.classList.toggle('active', sides === 1);
        if (s2) s2.classList.toggle('active', sides === 2);
        recalc();
    }

    function togAddon(itemId, key) {
        if (!state.itemAddons[itemId]) state.itemAddons[itemId] = {};
        state.itemAddons[itemId][key] = !state.itemAddons[itemId][key];
        var chip = document.querySelector('[data-addon="' + key + '"][data-item-id="' + itemId + '"]') ||
                   document.querySelector('[data-addon="' + key + '"][data-mat-id="' + itemId + '"]');
        if (chip) chip.classList.toggle('on', state.itemAddons[itemId][key]);
        recalc();
    }

    function dryingCost(base) {
        var pct = base >= 200000 ? 0.20 : base >= 100000 ? 0.25 : base >= 50000 ? 0.25 : 0.30;
        return Math.max(5000, base * pct);
    }

    // ═══════════════════════════════════════════════════════════════
    // ACCORDION (direct binding on render)
    // ═══════════════════════════════════════════════════════════════
    function initAccordion() {
        document.querySelectorAll('.accordion-header').forEach(function(header) {
            header.onclick = function() {
                var item = this.closest('.accordion-item');
                if (!item) return;
                var isActive = item.classList.contains('active');
                document.querySelectorAll('.accordion-item').forEach(function(ai) {
                    ai.classList.remove('active');
                });
                if (!isActive) item.classList.add('active');
            };
        });
    }

    // ═══════════════════════════════════════════════════════════════
    // GLOBAL EVENT DELEGATION (Fixes all dynamic buttons)
    // ═══════════════════════════════════════════════════════════════
    document.addEventListener('click', function(e) {
        // 0. Quantity Adjusters for Hair/Boxes (+/-) — MUST be first!
        var qaBtn = e.target.closest('.qa-btn');
        if (qaBtn) {
            e.preventDefault();
            e.stopPropagation();
            var action = qaBtn.dataset.action;
            var param = qaBtn.dataset.param;
            if (param === 'hair') {
                if (action === 'plus') state.hairM++;
                else if (action === 'minus' && state.hairM > 1) state.hairM--;
                var hairSelectors = '#hair-val, #carpet-hair-val, #curtain-hair-val';
                document.querySelectorAll(hairSelectors).forEach(function(el) { el.textContent = state.hairM; });
            } else if (param === 'box') {
                if (action === 'plus') state.boxQ++;
                else if (action === 'minus' && state.boxQ > 0) state.boxQ--;
                var boxSelectors = '#box-val, #carpet-box-val, #curtain-box-val';
                document.querySelectorAll(boxSelectors).forEach(function(el) { el.textContent = state.boxQ; });
            } else if (param === 'roman') {
                if (action === 'plus') state.romanQty++;
                else if (action === 'minus' && state.romanQty > 1) state.romanQty--;
                var romanSelectors = '#roman-qty-val, #curtain-roman-val';
                document.querySelectorAll(romanSelectors).forEach(function(el) { el.textContent = state.romanQty; });
            }
            recalc();
            return;
        }

        // 1. Furniture +/- buttons
        var btn = e.target.closest('.cbtn');
        if (btn) {
            var action = btn.dataset.action;
            var itemId = btn.dataset.itemId || btn.dataset.matId;
            if (!itemId) return;

            if (btn.dataset.matId) {
                var matItem = CAT.mattress.find(function(m) { return m.id === itemId; });
                if (matItem) chgMat(itemId, action === 'plus' ? 1 : -1, matItem.p, matItem.n, matItem.e);
            } else {
                var allItems = [].concat(CAT.sofas, CAT.chairs, CAT.beds, CAT.misc, 
                                          CAT.bizChairs, CAT.bizSofas, CAT.bizConf, CAT.bizLounge, CAT.bizPanels);
                var item = allItems.find(function(i) { return i.id === itemId; });
                if (item) chg(itemId, action === 'plus' ? 1 : -1, item.p, item.n, item.e);
            }
            return;
        }

        // 2. Mattress sides toggle
        var sideBtn = e.target.closest('.side-btn');
        if (sideBtn) {
            setSides(sideBtn.dataset.matId, parseInt(sideBtn.dataset.sides));
            return;
        }

        // 3. Item Addons (drying, odor, stain)
        var addonChip = e.target.closest('.addon-chip');
        if (addonChip) {
            togAddon(addonChip.dataset.itemId || addonChip.dataset.matId, addonChip.dataset.addon);
            return;
        }

        // 4. Upholstery type (Fabric/Leather)
        var uphBtn = e.target.closest('.uph-btn');
        if (uphBtn) {
            var val = uphBtn.dataset.uph;
            state.uphMult = val === 'leather' ? 1.5 : 1;
            document.querySelectorAll('.uph-btn').forEach(function(b) {
                b.classList.toggle('active', b.dataset.uph === val);
            });
            var note = document.getElementById('leather-note');
            if (note) note.classList.toggle('visible', val === 'leather');
            refreshPrices();
            recalc();
            return;
        }

        // 4b. Home/Business tab
        var tabBtn = e.target.closest('.tab-btn');
        if (tabBtn) {
            var tab = tabBtn.dataset.tab;
            if (!tab) return;
            state.uphTarget = tab;
            document.querySelectorAll('.tab-btn').forEach(function(b) {
                b.classList.toggle('active', b.dataset.tab === tab);
            });
            var homePanel = document.getElementById('furn-home');
            var bizPanel  = document.getElementById('furn-business');
            // Must use 'block' explicitly to override CSS .furn-panel { display:none }
            if (homePanel) homePanel.style.display = tab === 'home' ? 'block' : 'none';
            if (bizPanel)  bizPanel.style.display  = tab === 'business' ? 'block' : 'none';
            recalc();
            return;
        }


        // 5. Dirt level
        var dirtBtn = e.target.closest('.dirt-btn');
        if (dirtBtn) {
            var val = dirtBtn.dataset.coeff; // "0", "0.2", "0.5"
            state.dirtMult = parseFloat(val) + 1;
            document.querySelectorAll('.dirt-btn').forEach(function(b) {
                b.classList.toggle('active', b.dataset.coeff === val);
            });
            recalc();
            return;
        }

        // 5a. General Counter Buttons (+ / -)
        var qaBtn = e.target.closest('.qa-btn');
        if (qaBtn) {
            var action = qaBtn.dataset.action;
            var param = qaBtn.dataset.param; // 'hair' or 'box'
            
            if (param === 'hair') {
                if (action === 'plus') state.hairM++;
                else if (action === 'minus' && state.hairM > 1) state.hairM--;
                var valEl = document.getElementById('hair-val');
                if (valEl) valEl.textContent = state.hairM;
            } else if (param === 'box') {
                if (action === 'plus') state.boxQ++;
                else if (action === 'minus' && state.boxQ > 0) state.boxQ--;
                var valEl = document.getElementById('box-val');
                if (valEl) valEl.textContent = state.boxQ;
            }
            recalc();
            return;
        }

        // 6. Global Options (Hair, Box, Night, Faraway)
        var optCard = e.target.closest('.opt-card');
        if (optCard) {
            e.preventDefault();
            e.stopPropagation();
            var optId = optCard.dataset.optId;
            var isCarpetTab = !!optCard.closest('#calc-carpet-wrapper');
            var prefix = isCarpetTab ? 'carpet-' : 'furn-';

            function toggleOpt(cbId, otherCbId, adjId1, adjId2) {
                var cb = document.getElementById(cbId);
                if (!cb) return;
                cb.checked = !cb.checked;
                var isOn = cb.checked;
                var otherCb = document.getElementById(otherCbId);
                if (otherCb) otherCb.checked = isOn;
                document.querySelectorAll('.opt-card[data-opt-id="' + optId + '"]').forEach(function(c) {
                    c.classList.toggle('on', isOn);
                });
                if (adjId1) { var a = document.getElementById(adjId1); if (a) a.classList.toggle('visible', isOn); }
                if (adjId2) { var a = document.getElementById(adjId2); if (a) a.classList.toggle('visible', isOn); }
            }

            if (optId === 'hair') {
                toggleOpt(prefix + 'hair', (isCarpetTab ? 'furn-' : 'carpet-') + 'hair', 'hair-adj', 'carpet-hair-adj');
                recalc();
            } else if (optId === 'box') {
                toggleOpt(prefix + 'box', (isCarpetTab ? 'furn-' : 'carpet-') + 'box', 'box-adj', 'carpet-box-adj');
                recalc();
            } else if (optId === 'night') {
                toggleOpt(prefix + 'night', (isCarpetTab ? 'furn-' : 'carpet-') + 'night', null, null);
                recalc();
            } else if (optId === 'faraway') {
                toggleOpt(prefix + 'faraway', (isCarpetTab ? 'furn-' : 'carpet-') + 'faraway', null, null);
                recalc();
            }
            return;
        }
    });

    // ═══════════════════════════════════════════════════════════════
    // CARPET BINDINGS
    // ═══════════════════════════════════════════════════════════════
    var carpetAreaEl = document.getElementById('carpet-area');
    if (carpetAreaEl) {
        carpetAreaEl.addEventListener('input', function() {
            state.carpetArea = parseFloat(this.value) || 0;
            recalc();
        });
    }

    document.querySelectorAll('.carpet-mode-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var mode = this.dataset.mode;
            var radio = document.getElementById('mode-' + mode);
            if (radio) {
                radio.checked = true;
                state.carpetMode = mode;
                document.querySelectorAll('.carpet-mode-btn').forEach(function(b) {
                    b.classList.toggle('active', b.dataset.mode === mode);
                });
                var desc = document.getElementById('carpet-mode-desc');
                if (desc) {
                    desc.innerHTML = mode === 'general' ?
                        '<b style="color:#28C460;">Генеральная (IICRC S100)</b> — капитальная чистка с полным циклом удаления грязи.' :
                        '<b style="color:#64748b;">Эконом (Экспресс)</b> — поверхностная чистка. Подходит для регулярного ухода.';
                }
                recalc();
            }
        });
    });

    document.querySelectorAll('.carpet-material-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var mat = this.dataset.material;
            var radio = document.getElementById('mat-' + mat);
            if (radio) {
                radio.checked = true;
                state.carpetMaterial = mat;
                document.querySelectorAll('.carpet-material-btn').forEach(function(b) {
                    b.classList.toggle('active', b.dataset.material === mat);
                });
                var desc = document.getElementById('carpet-material-desc');
                if (desc) {
                    desc.textContent = mat === 'synthetic' ?
                        'Стандартные синтетические покрытия (полиамид, акрил, полиэстер).' :
                        'Деликатные покрытия (шерсть, шёлк, вискоза). Требуют щадящих составов. +50% к цене.';
                }
                recalc();
            }
        });
    });

    // (opt-card click is handled by the main document listener above)

    document.querySelectorAll('.carpet-addon').forEach(function(cb) {
        cb.addEventListener('change', recalc);
    });

    // --- GENERAL PARAMETER CHECKBOXES: toggle counter panels ---
    var genParamIds = [
        {cbId: 'furn-hair', panelId: 'hair-adj'},
        {cbId: 'furn-box', panelId: 'box-adj'},
        {cbId: 'carpet-hair', panelId: 'carpet-hair-adj'},
        {cbId: 'carpet-box', panelId: 'carpet-box-adj'},
        {cbId: 'curtain-hair', panelId: 'curtain-hair-adj'},
        {cbId: 'curtain-box', panelId: 'curtain-box-adj'},
        {cbId: 'curtain-roman-mount', panelId: 'curtain-roman-adj'}
    ];
    genParamIds.forEach(function(item) {
        var cb = document.getElementById(item.cbId);
        if (cb) {
            cb.addEventListener('change', function() {
                var panel = document.getElementById(item.panelId);
                if (panel) panel.style.display = this.checked ? 'flex' : 'none';
                recalc();
            });
        }
    });
    // Night and faraway — just recalc
    ['furn-night', 'furn-faraway', 'carpet-night', 'carpet-faraway', 'curtain-night', 'curtain-faraway'].forEach(function(id) {
        var cb = document.getElementById(id);
        if (cb) cb.addEventListener('change', recalc);
    });

    // ═══════════════════════════════════════════════════════════════
    // CURTAIN BINDINGS
    // ═══════════════════════════════════════════════════════════════
    document.querySelectorAll('input[name="curtain-mode"]').forEach(function(r) {
        r.addEventListener('change', function() {
            state.curtainMode = this.value;
            // Clear irrelevant state when switching modes
            if (state.curtainMode === 'weight') {
                state.curtainWindows = [];
            } else {
                state.curtainWeight = 0;
                var curtainWeightEl = document.getElementById('curtain-weight');
                if (curtainWeightEl) curtainWeightEl.value = '';
            }
            document.querySelectorAll('.curtain-mode-btn').forEach(function(btn) {
                btn.classList.toggle('active', btn.dataset.mode === state.curtainMode);
            });
            var wMode = document.getElementById('curtain-weight-mode');
            var wWin = document.getElementById('curtain-windows-mode');
            if (wMode) wMode.style.display = state.curtainMode === 'weight' ? '' : 'none';
            if (wWin) wWin.style.display = state.curtainMode === 'windows' ? '' : 'none';
            recalc();
        });
    });

    var curtainWeightEl = document.getElementById('curtain-weight');
    if (curtainWeightEl) {
        curtainWeightEl.addEventListener('input', function() {
            state.curtainWeight = parseFloat(this.value) || 0;
            recalc();
        });
    }

    var addBtn = document.getElementById('add-window-btn');
    if (addBtn) {
        addBtn.addEventListener('click', function() {
            var wInput = document.getElementById('curtain-w');
            var hInput = document.getElementById('curtain-h');
            var sel1 = document.getElementById('curtain-type');
            var sel2 = document.getElementById('curtain-fabric-select');
            
            var sel = sel1 || sel2;
            if (!sel) return;
            
            var w = wInput ? parseF(wInput.value) : 0;
            var h = hInput ? parseF(hInput.value) : 0;
            if (w <= 0 || h <= 0) return;

            var coeff, typeName, price_per_kg = null;
            if (sel2 && COEFFS) { // if using fabric-select mode
                var fIdx = sel.value;
                if (fIdx === "") return;
                var fabric = COEFFS[fIdx];
                if (!fabric) return;
                coeff = fabric.coefficient;
                typeName = fabric.name;
                price_per_kg = fabric.price_per_kg || null;
            } else { // if using curtain-type mode
                coeff = parseF(sel.value, 0.6);
                typeName = sel.options[sel.selectedIndex].text.split(' (')[0];
            }

            var weight = w * h * coeff;
            
            state.curtainWindows.push({
                id: Date.now(),
                w: w, 
                h: h, 
                weight: weight, 
                fabric: typeName,
                type: typeName, 
                coeff: coeff,
                price_per_kg: price_per_kg
            });
            
            if (wInput) wInput.value = '';
            if (hInput) hInput.value = '';
            if (sel2) sel.selectedIndex = 0;

            renderWindows();
            recalc();
        });
    }

    function renderWindows() {
        var list = document.getElementById('window-list');
        if (!list) return;
        if (state.curtainWindows.length === 0) { list.innerHTML = ''; return; }
        list.innerHTML = state.curtainWindows.map(function(item, i) {
            return '<div style="display:flex;justify-content:space-between;padding:8px;background:#fff;border-radius:8px;margin-bottom:6px;font-size:13px;">' +
                '<span>' + item.type + ' (' + item.w + '×' + item.h + 'м = ' + item.weight.toFixed(1) + ' кг)</span>' +
                '<span onclick="window._removeWindow(' + i + ')" style="color:red;cursor:pointer;font-weight:bold;">✕</span>' +
                '</div>';
        }).join('');
    }

    window._removeWindow = function(i) {
        state.curtainWindows.splice(i, 1);
        renderWindows();
        recalc();
    };

    function bindCurtainToggle(id, stateKey) {
        var el = document.getElementById(id);
        if (el) {
            el.addEventListener('change', function() {
                state[stateKey] = this.checked;
                recalc();
            });
        }
    }
    bindCurtainToggle('curtain-removal', 'curtainRemoval');
    bindCurtainToggle('curtain-hanging', 'curtainHanging');
    bindCurtainToggle('curtain-ironing', 'curtainIroning');

    var romanEl = document.getElementById('curtain-roman');
    if (romanEl) {
        romanEl.addEventListener('change', function() {
            // Sync BOTH state keys — curtainRoman (display) and curtainRomanMount (calc)
            state.curtainRoman = this.checked;
            state.curtainRomanMount = this.checked;
            var qty = document.getElementById('curtain-roman-qty');
            if (qty) qty.style.display = state.curtainRomanMount ? 'flex' : 'none';
            if (!state.curtainRomanMount) {
                state.romanQty = 1;
                var val = document.getElementById('roman-val');
                if (val) val.textContent = '1';
            }
            recalc();
        });
    }

    var romanMinus = document.getElementById('roman-minus');
    var romanPlus = document.getElementById('roman-plus');
    if (romanMinus) {
        romanMinus.addEventListener('click', function() {
            state.romanQty = Math.max(1, state.romanQty - 1);
            var val = document.getElementById('roman-val');
            if (val) val.textContent = state.romanQty;
            recalc();
        });
    }
    if (romanPlus) {
        romanPlus.addEventListener('click', function() {
            state.romanQty++;
            var val = document.getElementById('roman-val');
            if (val) val.textContent = state.romanQty;
            recalc();
        });
    }

    // ═══════════════════════════════════════════════════════════════
    // DB OPTIONS CHECKBOXES (Direct binding)
    // ═══════════════════════════════════════════════════════════════
    function bindOptionCheckboxes() {
        document.querySelectorAll('input[name="calc-option"]').forEach(function(cb) {
            cb.addEventListener('change', function() {
                var id = parseInt(this.value);
                if (this.checked) {
                    if (state.selectedOptions.indexOf(id) === -1) state.selectedOptions.push(id);
                } else {
                    state.selectedOptions = state.selectedOptions.filter(function(x) { return x !== id; });
                }
                console.log('Option', id, 'checked:', this.checked, 'selected:', state.selectedOptions);
                recalc();
            });
        });
    }

    // ═══════════════════════════════════════════════════════════════
    // DISCOUNTS
    // ═══════════════════════════════════════════════════════════════
    var newClientEl = document.getElementById('calc-new-client');
    if (newClientEl) {
        newClientEl.addEventListener('change', function() {
            state.isNewClient = this.checked;
            recalc();
        });
    }
    var comboEl = document.getElementById('calc-combo-order');
    if (comboEl) {
        comboEl.addEventListener('change', function() {
            state.isCombo = this.checked;
            recalc();
        });
    }

    var mobileFloatBar = document.getElementById('mobile-float-bar');
    if (mobileFloatBar) {
        mobileFloatBar.addEventListener('click', function() {
            var target = document.getElementById('sticky-total');
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    }

    // ═══════════════════════════════════════════════════════════════
    // CALCULATION ENGINE
    // ═══════════════════════════════════════════════════════════════
    function getCarpetPricePerM2(area) {
        var carpetSvc = null;
        for (var id in servicesMap) {
            if (servicesMap[id].calc_type === 'carpet') { 
                carpetSvc = servicesMap[id]; 
                break; 
            }
        }

        var basePrice = 2000; // Default fallback
        if (carpetSvc) {
            basePrice = parseFloat(carpetSvc.base_price) || 2000;
            var rules = carpetSvc.price_rules;
            
            // Support both rules.tiers (object) and rules (array) structures
            var tiersArray = null;
            if (rules && rules.tiers && Array.isArray(rules.tiers)) {
                tiersArray = rules.tiers;
            } else if (Array.isArray(rules)) {
                tiersArray = rules;
            }
            if (!tiersArray || tiersArray.length === 0) {
                tiersArray = [
                    { max_area: 25, price: 2000 },
                    { max_area: 50, price: 1750 },
                    { max_area: 100, price: 1500 },
                    { max_area: null, price: 1250 }
                ];
            }

            if (tiersArray && tiersArray.length > 0) {
                // Sort by max_area to ensure correct tier matching
                var sortedTiers = tiersArray.slice().sort(function(a, b) {
                    return (parseFloat(a.max_area) || 999999) - (parseFloat(b.max_area) || 999999);
                });
                
                var found = false;
                for (var i = 0; i < sortedTiers.length; i++) {
                    var maxA = parseFloat(sortedTiers[i].max_area) || 999999;
                    if (area <= maxA) {
                        basePrice = parseFloat(sortedTiers[i].price);
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    basePrice = parseFloat(sortedTiers[sortedTiers.length - 1].price);
                }
            }
        }

        var finalBase = basePrice;
        if (state.carpetMode === 'eco') {
            finalBase = finalBase * 0.6; // Task 2: 40% discount
        }
        
        console.log('DEBUG CALC CARPET:', {
            area: area,
            foundSvc: !!carpetSvc,
            basePrice: basePrice,
            mode: state.carpetMode,
            finalPricePerM2: finalBase
        });

        return finalBase;
    }

    function calcOptionCost(opt, total, area, weight, qty) {
        var price = parseFloat(opt.price) || 0;
        var unit = opt.calc_unit || 'fixed';
        switch (unit) {
            case 'percentage': return total * (price / 100);
            case 'per_kg': return weight * price;
            case 'per_m2': return area * price;
            case 'per_item': return qty * price;
            default: return price;
        }
    }

    function applyOptionsAndDiscounts(total, det, area, weight, qty) {
        state.selectedOptions.forEach(function(id) {
            var opt = OPTIONS.find(function(o) { return o.id === id; });
            if (!opt) return;
            var price = parseFloat(opt.price) || 0;
            var cost = calcOptionCost(opt, total, area, weight, qty);
            total += cost;
            var label = opt.name;
            if (opt.calc_unit === 'percentage') label += ' (' + price + '%)';
            else if (opt.calc_unit === 'per_kg') label += ' (' + weight.toFixed(1) + ' кг)';
            else if (opt.calc_unit === 'per_m2') label += ' (' + area.toFixed(1) + ' м²)';
            det.push({n: label, v: Math.round(cost), cls: 'add'});
        });

        if (state.isNewClient) {
            var d = total * 0.05;
            total -= d;
            det.push({n: 'Скидка 5% (первый заказ)', v: -Math.round(d), cls: 'disc'});
        }
        if (state.isCombo) {
            det.push({n: 'Доп. заказ (−15% на мебель): пользователь хочет доп. заказ со скидкой 15%', v: 0, cls: 'warn'});
        }

        return total;
    }

    // ═══════════════════════════════════════════════════════════════
    // CALC FURNITURE (or default single-service)
    // ═══════════════════════════════════════════════════════════════
    function calcFurniture() {
        var det = [];
        var grandBase = 0;
        var totalQty = 0;
        var allFlat = [].concat(CAT.sofas, CAT.chairs, CAT.beds, CAT.misc);

        // Robust Qty sum for Furniture (Home + Business + Mattresses)
        var totalQty = 0;
        
        // Final Price Calculation logic
        // If on single service page, check if any items are selected in catalog
        var hasCatalogItems = false;
        for (var id in state.cart) { if (state.cart[id] && state.cart[id].q > 0) hasCatalogItems = true; }

        if (isSingleService && SERVICES.length === 1 && !hasCatalogItems) {
            // Case 1: Simple service page, nothing from catalog selected yet
            var svc = SERVICES[0];
            var base = parseFloat(svc.base_price) || 0;
            grandBase = base * state.uphMult * state.dirtMult;
            det.push({n: svc.name, v: Math.round(grandBase), cls: 'pos'});
            totalQty = 1;
        } else {
            // Case 2: Either main services page OR catalog items are selected on detail page
            if (state.uphTarget === 'business') {
                var bizFlat = [].concat(CAT.bizChairs, CAT.bizSofas, CAT.bizConf, CAT.bizLounge, CAT.bizPanels);
                bizFlat.forEach(function(item) {
                    var c = state.cart[item.id];
                    if (!c || !c.q) return;
                    var lineBase = item.p * state.uphMult * state.dirtMult * c.q;
                    grandBase += lineBase;
                    var qty = c.q > 1 ? ' ×' + c.q : '';
                    det.push({n: c.n + qty, v: Math.round(lineBase), cls: 'pos'});
                    totalQty += c.q;
                });
            } else {
                allFlat.forEach(function(item) {
                    var c = state.cart[item.id];
                    if (!c || !c.q) return;
                    var lineBase = item.p * state.uphMult * state.dirtMult * c.q;
                    grandBase += lineBase;
                    var qty = c.q > 1 ? ' ×' + c.q : '';
                    det.push({n: c.n + qty, v: Math.round(lineBase), cls: 'pos'});
                    totalQty += c.q;
                });

                CAT.mattress.forEach(function(m) {
                     var c = state.cart[m.id];
                    if (!c || !c.q) return;
                    var st = state.matState[m.id] || {sides: 1};
                    var sides = st.sides || 1;
                    var lineBase = sides === 2 ? m.p * 2 * 0.95 * state.uphMult * state.dirtMult * c.q : m.p * state.uphMult * state.dirtMult * c.q;
                    grandBase += lineBase;
                    var qty = c.q > 1 ? ' ×' + c.q : '';
                    var sidesLabel = sides === 2 ? ' (2 ст.)' : ' (1 ст.)';
                    det.push({n: c.n + sidesLabel + qty, v: Math.round(lineBase), cls: 'pos'});
                    totalQty += c.q;
                });
            }
        }


        if (grandBase === 0) {
            det.push({n: 'Введите параметры для расчёта...', v: 0, cls: 'empty'});
            renderSummary(det, 0);
            return;
        }


        if (state.uphMult > 1) det.push({n: 'Материал: Кожа/экокожа (+50%)', v: 0, cls: 'add'});
        if (state.dirtMult > 1) {
            var dirtSurcharge = grandBase - (grandBase / state.dirtMult);
            var lbl = state.dirtMult <= 1.25 ? 'Сильные загрязнения (+20%)' : 'Сложные загрязнения (+50%)';
            det.push({n: lbl, v: Math.round(dirtSurcharge), cls: 'add'});
        }

        var extras = 0;

        var addonItems = state.uphTarget === 'business' 
            ? [].concat(CAT.bizChairs, CAT.bizSofas, CAT.bizConf, CAT.bizLounge, CAT.bizPanels)
            : allFlat;

        addonItems.forEach(function(item) {
            var c = state.cart[item.id];
            var ad = state.itemAddons[item.id];
            if (!c || !c.q || !ad) return;
            var lineBase = item.p * state.uphMult * state.dirtMult * c.q;
            if (ad.drying) { var cost = dryingCost(lineBase); extras += cost; det.push({n: 'Сушка: ' + c.n, v: Math.round(cost), cls: 'add'}); }
            if (ad.odor) { var cost = Math.max(2000, lineBase * 0.20); extras += cost; det.push({n: 'Удаление запахов: ' + c.n, v: Math.round(cost), cls: 'add'}); }
            if (ad.stain) { var cost = Math.max(1000, lineBase * 0.15); extras += cost; det.push({n: 'Пятна: ' + c.n, v: Math.round(cost), cls: 'add'}); }
        });


        CAT.mattress.forEach(function(m) {
            var c = state.cart[m.id];
            var ad = state.itemAddons[m.id];
            if (!c || !c.q || !ad) return;
            var st = state.matState[m.id] || {sides: 1};
            var sides = st.sides || 1;
            var lineBase = (sides === 2 ? m.p * 2 * 0.95 : m.p) * state.uphMult * state.dirtMult * c.q;
            if (ad.drying) { var cost = dryingCost(lineBase); extras += cost; det.push({n: 'Сушка: ' + c.n, v: Math.round(cost), cls: 'add'}); }
            if (ad.odor) { var cost = 7000 * sides * c.q; extras += cost; det.push({n: 'Удаление запахов: ' + c.n, v: Math.round(cost), cls: 'add'}); }
            if (ad.whiten) { var cost = 10000 * sides * c.q; extras += cost; det.push({n: 'Отбеливание: ' + c.n, v: Math.round(cost), cls: 'add'}); }
        });


        var hairCb = document.getElementById('furn-hair');
        if (hairCb && hairCb.checked) {
            var cost = 5000 * state.hairM;
            extras += cost;
            det.push({n: 'Шерсть животных (' + state.hairM + ' пог.м)', v: Math.round(cost), cls: 'add'});
        }
        var boxCb = document.getElementById('furn-box');
        if (boxCb && boxCb.checked) {
            var cost = 1000 * state.boxQ;
            extras += cost;
            det.push({n: 'Чистка ящиков (' + state.boxQ + ' шт)', v: Math.round(cost), cls: 'add'});
        }
        var nightCb = document.getElementById('furn-night');
        if (nightCb && nightCb.checked) {
            extras += 5000;
            det.push({n: 'Работа после 21:00', v: 5000, cls: 'add'});
        }
        var farCb = document.getElementById('furn-faraway');
        if (farCb && farCb.checked) {
            det.push({n: 'Выезд за 10 км', v: 0, cls: 'warn'});
        }

        // Robust Qty sum for Furniture (Home + Business + Mattresses)
        var totalQty = 0;
        if (isSingleService && SERVICES.length === 1) {
            var c = state.cart[SERVICES[0].id];
            totalQty = (c && c.q) ? c.q : 1;
        } else {
            for (var id in state.cart) {
                var c = state.cart[id];
                if (c && c.q > 0) {
                    totalQty += c.q;
                }
            }
        }

        var total = grandBase + extras;
        det.push({n: 'sep', v: 0, cls: 'sep'});

        total = applyOptionsAndDiscounts(total, det, 0, 0, totalQty);
        
        var discountInfo = [];
        if (state.isNewClient) discountInfo.push('Скидка 5% (первый заказ)');
        if (state.isCombo) discountInfo.push('Доп. заказ (скидка 15% на мебель)');

        renderSummary(det, total, discountInfo.join(', '));
    }

    // ═══════════════════════════════════════════════════════════════
    // CALC CARPET
    // ═══════════════════════════════════════════════════════════════
    function calcCarpet() {
        if (state.carpetArea <= 0) {
            renderSummary([{n: 'Введите площадь ковролина...', v: 0, cls: 'empty'}], 0);
            return;
        }
        var det = [];
        var area = state.carpetArea;
        var pricePerM2 = getCarpetPricePerM2(area);
        var total = area * pricePerM2;
        
        det.push({
            n: area + ' м² × ' + Math.round(pricePerM2).toLocaleString('ru-RU') + ' ₸/м²', 
            v: Math.round(total), 
            cls: 'pos'
        });

        // Task 3: Natural Material Markup (+50%)
        if (state.carpetMaterial === 'natural') {
            var naturalMarkup = total * 0.5;
            total += naturalMarkup;
            det.push({
                n: 'Натуральный ворс (+50%): +' + fmt(naturalMarkup), 
                v: Math.round(naturalMarkup), 
                cls: 'add'
            });
        }

        if (state.dirtMult > 1) {
            var dc = total * (state.dirtMult - 1);
            total += dc;
            var lbl = state.dirtMult <= 1.25 ? 'Сильные загрязнения (+20%)' : 'Сложные загрязнения (+50%)';
            det.push({n: lbl, v: Math.round(dc), cls: 'add'});
        }
        
        if (state.carpetMode === 'eco') {
            det.push({n: 'Режим Эконом (−40%)', v: 0, cls: 'add'});
        }

        // --- CARPET SPECIFIC ADDONS (use data-price from HTML) ---
        var carpetAddons = document.querySelectorAll('.carpet-addon:checked');
        carpetAddons.forEach(function(cb) {
            var cost = parseFloat(cb.dataset.price) || 0;
            var name = cb.closest('.calc-option').querySelector('.calc-option__name').textContent;
            if (cost > 0) {
                total += cost;
                det.push({n: name, v: Math.round(cost), cls: 'add'});
            }
        });

        // --- GENERAL PARAMETERS ---
        var extras = 0;
        var pfx = (typeof isSingleService !== 'undefined' && isSingleService) ? 'furn-' : 'carpet-';
        var hairCb = document.getElementById(pfx + 'hair');
        if (hairCb && hairCb.checked) {
            var cost = 5000 * state.hairM;
            extras += cost;
            det.push({n: 'Шерсть животных (' + state.hairM + ' пог.м)', v: Math.round(cost), cls: 'add'});
        }
        var boxCb = document.getElementById(pfx + 'box');
        if (boxCb && boxCb.checked) {
            var cost = 1000 * state.boxQ;
            extras += cost;
            det.push({n: 'Чистка ящиков (' + state.boxQ + ' шт)', v: Math.round(cost), cls: 'add'});
        }
        var nightCb = document.getElementById(pfx + 'night');
        if (nightCb && nightCb.checked) {
            extras += 5000;
            det.push({n: 'Работа после 21:00', v: 5000, cls: 'add'});
        }
        var farCb = document.getElementById(pfx + 'faraway');
        if (farCb && farCb.checked) {
            det.push({n: 'Выезд за 10 км', v: 0, cls: 'warn'});
        }
        total += extras;

        total = applyOptionsAndDiscounts(total, det, area, 0, 1);

        var discountInfo = [];
        if (state.isNewClient) discountInfo.push('Скидка 5% (первый заказ)');
        if (state.isCombo) discountInfo.push('Доп. заказ (скидка 15% на мебель)');

        renderSummary(det, total, discountInfo.join(', '));
    }

    // ═══════════════════════════════════════════════════════════════
    // CALC CURTAINS
    // ═══════════════════════════════════════════════════════════════
    function getCoeff(name) {
        var found = COEFFS.find(function(c) { return c.name === name; });
        return found ? parseFloat(found.coefficient) : 0.6;
    }

    function calcCurtains() {
        var wgt = 0, area = 0, romanCount = 0;

        if (state.curtainMode === 'weight') {
            wgt = state.curtainWeight;
            area = wgt * 1.5; // Roughly estimate for area-based addons if weight-only
        } else {
            state.curtainWindows.forEach(function(item) {
                var itemArea = item.w * item.h;
                wgt += itemArea * (item.coeff || 0.6);
                area += itemArea;
                if (item.fabric && item.fabric.toLowerCase().indexOf('римская') !== -1) {
                    romanCount++;
                }
            });
        }

        if (wgt <= 0 && state.curtainWindows.length === 0) {
            renderSummary([{n: 'Введите параметры...', v: 0, cls: 'empty'}], 0);
            return;
        }

        // Calculate price: in windows mode use per-window price_per_kg if available
        var det = [];
        var pricePerKg = 3600;
        var curtainSvc = null;
        for (var id in servicesMap) {
            if (servicesMap[id].calc_type === 'curtains') { curtainSvc = servicesMap[id]; break; }
        }
        if (curtainSvc) pricePerKg = parseFloat(curtainSvc.base_price) || 0;

        var total = 0;
        if (state.curtainMode === 'weight') {
            total = wgt * pricePerKg;
            if (wgt > 0) {
                det.push({n: 'Химчистка штор (' + wgt.toFixed(1) + ' кг × ' + Math.round(pricePerKg).toLocaleString('ru-RU') + ' ₸/кг)', v: Math.round(total), cls: 'pos'});
            }
        } else {
            // Windows mode: calculate per-window with possible price_per_kg override
            state.curtainWindows.forEach(function(win) {
                var winArea = win.w * win.h;
                var winWeight = winArea * (win.coeff || 0.6);
                var winPrice = (win.price_per_kg != null) ? win.price_per_kg : pricePerKg;
                var winCost = winWeight * winPrice;
                total += winCost;
                var priceNote = (win.price_per_kg != null) ? Math.round(win.price_per_kg).toLocaleString('ru-RU') + ' ₸/кг' : Math.round(pricePerKg).toLocaleString('ru-RU') + ' ₸/кг';
                det.push({n: win.fabric + ' ' + win.w + '×' + win.h + 'м (~' + winWeight.toFixed(1) + ' кг, ' + priceNote + ')', v: Math.round(winCost), cls: 'pos'});
            });
        }

        // Addons logic (Match Photo Prices)
        if (state.curtainRemoval) {
            var c = wgt * 400; // +400 ₸/кг
            total += c;
            det.push({n: 'Снятие штор', v: Math.round(c), cls: 'add'});
        }
        if (state.curtainHanging) {
            var c = wgt * 600; // +600 ₸/кг
            total += c;
            det.push({n: 'Навеска и стяжка', v: Math.round(c), cls: 'add'});
        }
        if (state.curtainIroning) {
            var c = area * 500; // +500 ₸/м²
            total += c;
            det.push({n: 'Глажка / Отпаривание', v: Math.round(c), cls: 'add'});
        }
        if (state.curtainRomanMount) {
            var c = state.romanQty * 3000; // 3000 ₸/шт
            total += c;
            det.push({n: 'Монтаж Римских (' + state.romanQty + ' шт)', v: Math.round(c), cls: 'add'});
        }

        // --- GENERAL PARAMETERS ---
        var extras = 0;
        var pfx = (typeof isSingleService !== 'undefined' && isSingleService) ? 'furn-' : 'curtain-';
        var hairCb = document.getElementById(pfx + 'hair');
        if (hairCb && hairCb.checked) {
            var cost = 5000 * state.hairM;
            extras += cost;
            det.push({n: 'Шерсть животных (' + state.hairM + ' пог.м)', v: Math.round(cost), cls: 'add'});
        }
        var boxCb = document.getElementById(pfx + 'box');
        if (boxCb && boxCb.checked) {
            var cost = 1000 * state.boxQ;
            extras += cost;
            det.push({n: 'Чистка ящиков (' + state.boxQ + ' шт)', v: Math.round(cost), cls: 'add'});
        }
        var nightCb = document.getElementById(pfx + 'night');
        if (nightCb && nightCb.checked) {
            extras += 5000;
            det.push({n: 'Работа после 21:00', v: 5000, cls: 'add'});
        }
        var farCb = document.getElementById(pfx + 'faraway');
        if (farCb && farCb.checked) {
            det.push({n: 'Выезд за 10 км', v: 0, cls: 'warn'});
        }
        total += extras;

        total = applyOptionsAndDiscounts(total, det, area, wgt, state.curtainWindows.length);
        
        var discountInfo = [];
        if (state.isNewClient) discountInfo.push('Скидка 5% (первый заказ)');
        if (state.isCombo) discountInfo.push('Доп. заказ (скидка 15% на мебель)');

        renderSummary(det, total, discountInfo.join(', '));
    }

    // ═══════════════════════════════════════════════════════════════
    // RENDER SUMMARY
    // ═══════════════════════════════════════════════════════════════
    function renderSummary(det, total, discountInfo) {
        var orderLines = document.getElementById('order-lines');
        var totalVal = document.getElementById('total-val');
        var minNote = document.getElementById('min-note');

        if (!orderLines || !totalVal) return;

        var orderBtn = document.getElementById('calc-order');
        var waBtn = document.getElementById('calc-whatsapp-btn');

        if (det.length === 0 || (det.length === 1 && det[0].cls === 'empty')) {
            orderLines.innerHTML = '<div class="empty-msg">Выберите позиции для расчёта...</div>';
            totalVal.textContent = '0 ₸';
            if (minNote) minNote.style.display = 'none';
            // Disable all buttons
            if (orderBtn) {
                orderBtn.textContent = 'Выберите услугу';
                orderBtn.disabled = true;
                orderBtn.classList.add('btn--disabled');
                orderBtn.dataset.totalPrice = '';
                orderBtn.dataset.serviceName = '';
                orderBtn.dataset.options = '';
            }
            if (waBtn) {
                waBtn.disabled = true;
                waBtn.classList.add('btn--disabled');
            }
            return;
        }

        var html = '';
        det.forEach(function(d) {
            if (d.cls === 'sep') { html += '<div class="sep"></div>'; return; }
            var cls = d.cls || 'pos';
            var valHtml = '';
            if (d.v === 0 && cls === 'warn') valHtml = '<span class="lv warn">уточним</span>';
            else if (d.v === 0) valHtml = '<span class="lv add">учтено</span>';
            else if (cls === 'pos') valHtml = '<span class="lv pos">' + fmt(d.v) + '</span>';
            else if (cls === 'add') valHtml = '<span class="lv add">+' + fmt(d.v) + '</span>';
            else if (cls === 'disc') valHtml = '<span class="lv disc">−' + fmt(Math.abs(d.v)) + '</span>';
            html += '<div class="ol"><span class="ln">' + d.n + '</span>' + valHtml + '</div>';
        });

        orderLines.innerHTML = html;

        var fin = total;
        if (total > 0 && total < MIN_ORDER) {
            fin = MIN_ORDER;
            if (minNote) { minNote.style.display = 'block'; minNote.textContent = '* Применён минимальный заказ — ' + MIN_ORDER.toLocaleString('ru-RU') + ' ₸'; }
        } else {
            if (minNote) minNote.style.display = 'none';
        }

        totalVal.textContent = fmt(fin);

        var orderBtn = document.getElementById('calc-order');
        if (orderBtn) {
            if (fin > 0) {
                orderBtn.textContent = 'Заказать за ' + fmt(fin);
                orderBtn.disabled = false;
                orderBtn.classList.remove('btn--disabled');
            } else {
                orderBtn.textContent = 'Выберите услугу';
                orderBtn.disabled = true;
                orderBtn.classList.add('btn--disabled');
            }
            orderBtn.dataset.totalPrice = fmt(fin);
            var svcId = (typeof isSingleService !== 'undefined' && isSingleService) ? parseInt(isSingleService.dataset.serviceId) : null;
            svcName = svcId ? 'Заказ услуги' : 'Химчистка';
            orderBtn.dataset.serviceName = svcName;
            orderBtn.dataset.options = det.filter(function(d) { return d.cls !== 'sep' && d.cls !== 'empty'; }).map(function(d) { 
                return d.n + (d.v !== 0 ? ': ' + fmt(d.v) : ''); 
            }).join('\n');
            orderBtn.dataset.discountInfo = discountInfo || '';
        }

        var waBtn = document.getElementById('calc-whatsapp-btn');
        if (waBtn) {
            if (fin > 0) {
                waBtn.disabled = false;
                waBtn.classList.remove('btn--disabled');
            } else {
                waBtn.disabled = true;
                waBtn.classList.add('btn--disabled');
            }
        }

        // Update mobile floating bar
        var floatBar = document.getElementById('mobile-float-bar');
        var floatTotal = document.getElementById('mfb-total');
        if (floatBar && floatTotal) {
            var staticTotalBox = document.querySelector('.total-box');
            var isStaticVisible = false;
            if (staticTotalBox) {
                var rect = staticTotalBox.getBoundingClientRect();
                isStaticVisible = (rect.top >= 0 && rect.bottom <= window.innerHeight);
            }

            if (fin > 0 && !isStaticVisible) {
                floatTotal.textContent = fmt(fin);
                floatBar.classList.add('active');
            } else {
                floatBar.classList.remove('active');
            }
        }
    }

    function calcDefault() {
        var det = [];
        var total = BASE_PRICE;
        det.push({n: 'Базовая стоимость', v: Math.round(total), cls: 'pos'});
        
        if (state.dirtMult > 1) {
            var dc = total * (state.dirtMult - 1);
            total += dc;
            det.push({n: 'Степень загрязнения (+' + Math.round((state.dirtMult - 1) * 100) + '%)', v: Math.round(dc), cls: 'add'});
        }

        var extras = 0;
        var hairCb = document.getElementById('furn-hair');
        if (hairCb && hairCb.checked) {
            var cost = 5000 * state.hairM;
            extras += cost;
            det.push({n: 'Шерсть животных (' + state.hairM + ' пог.м)', v: Math.round(cost), cls: 'add'});
        }
        var boxCb = document.getElementById('furn-box');
        if (boxCb && boxCb.checked) {
            var cost = 1000 * state.boxQ;
            extras += cost;
            det.push({n: 'Чистка ящиков (' + state.boxQ + ' шт)', v: Math.round(cost), cls: 'add'});
        }
        var nightCb = document.getElementById('furn-night');
        if (nightCb && nightCb.checked) {
            extras += 5000;
            det.push({n: 'Работа после 21:00', v: 5000, cls: 'add'});
        }
        var farCb = document.getElementById('furn-faraway');
        if (farCb && farCb.checked) {
            det.push({n: 'Выезд за 10 км', v: 0, cls: 'warn'});
        }
        total += extras;

        total = applyOptionsAndDiscounts(total, det, 0, 0, 1);

        var discountInfo = [];
        if (state.isNewClient) discountInfo.push('Скидка 5% (первый заказ)');
        if (state.isCombo) discountInfo.push('Доп. заказ (скидка 15% на мебель)');

        renderSummary(det, total, discountInfo.join(', '));
    }

    function recalc() {
        if (state.activeCalcType === 'furniture') calcFurniture();
        else if (state.activeCalcType === 'carpet') calcCarpet();
        else if (state.activeCalcType === 'curtains') calcCurtains();
        else calcDefault();
    }

    window.addEventListener('scroll', recalc);

    // ═══════════════════════════════════════════════════════════════
    // WHATSAPP
    // ═══════════════════════════════════════════════════════════════
    var waBtn = document.getElementById('calc-whatsapp-btn');
    if (waBtn) {
        waBtn.addEventListener('click', function() {
            var svcName = '';
            if (state.activeCalcType === 'furniture') svcName = 'Химчистка мебели';
            else if (state.activeCalcType === 'carpet') svcName = 'Химчистка ковролина';
            else if (state.activeCalcType === 'curtains') svcName = 'Химчистка штор';

            var totalEl = document.getElementById('total-val');
            var total = totalEl ? totalEl.textContent : '0 ₸';
            var orderBtn = document.getElementById('calc-order');
            var detailsText = orderBtn ? orderBtn.dataset.options : '';

            var msg = '🔥 Расчет с сайта M-Clean:\n\n';
            msg += '🛠 Услуга: ' + svcName + '\n';
            if (detailsText) msg += '\n📊 Детализация:\n' + detailsText + '\n';
            msg += '\n💰 ИТОГО: ' + total;

            var phone = document.querySelector('[data-whatsapp-phone]')?.dataset.whatsappPhone || '77075288004';
            window.open('https://wa.me/' + phone + '?text=' + encodeURIComponent(msg), '_blank');
        });
    }

    // ═══════════════════════════════════════════════════════════════
    // INIT
    // ═══════════════════════════════════════════════════════════════
    // --- Curtains dynamic setup ---
    var cWeightInp = document.getElementById('curtain-weight');
    if (cWeightInp) {
        cWeightInp.addEventListener('input', function() {
            state.curtainWeight = parseF(this.value, 0);
            recalc();
        });
    }

    var cModeBtns = document.querySelectorAll('.curtain-mode-btn');
    if (cModeBtns.length > 0) {
        cModeBtns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                cModeBtns.forEach(function(b) { b.classList.remove('active'); });
                this.classList.add('active');
                state.curtainMode = this.dataset.mode;
                
                var wm = document.getElementById('curtain-weight-mode');
                var winm = document.getElementById('curtain-windows-mode');
                if (wm) wm.style.display = state.curtainMode === 'weight' ? '' : 'none';
                if (winm) winm.style.display = state.curtainMode === 'windows' ? '' : 'none';
                
                recalc();
            });
        });
    }

    var cFabricSelect = document.getElementById('curtain-fabric-select');
    if (cFabricSelect && COEFFS) {
        COEFFS.forEach(function(c, idx) {
            var opt = document.createElement('option');
            opt.value = idx;
            var priceStr = c.price_per_kg ? ' — ' + Math.round(c.price_per_kg).toLocaleString('ru-RU') + ' ₸/кг' : '';
            opt.textContent = c.name + ' (' + c.coefficient + ' кг/м²' + priceStr + ')';
            cFabricSelect.appendChild(opt);
        });
    }

    // Replaced duplicate add-window-btn logic with the unified one above

    function renderWindows() {
        var list = document.getElementById('window-list');
        if (!list) return;
        if (state.curtainWindows.length === 0) { list.innerHTML = ''; return; }
        
        list.innerHTML = state.curtainWindows.map(function(win) {
            return '<div class="window-item" style="display:flex; justify-content:space-between; align-items:center; background:var(--color-bg-alt); padding:8px 12px; border-radius:8px; margin-bottom:6px; font-size:12px; font-weight:600;">' +
                   '<div style="display:flex; flex-direction:column; gap:2px;">' +
                   '<span>Окно ' + win.w + '×' + win.h + ' м</span>' +
                   '<span style="font-size:10px; color:#64748b; font-weight:500;">' + win.fabric + '</span>' +
                   '</div>' +
                   '<button type="button" class="del-win" data-id="' + win.id + '" style="background:none; border:none; color:#d9534f; cursor:pointer; padding:4px;">' +
                   '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>' +
                   '</button>' +
                   '</div>';
        }).join('');
        
        list.querySelectorAll('.del-win').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var id = parseInt(this.dataset.id);
                state.curtainWindows = state.curtainWindows.filter(function(w) { return w.id !== id; });
                renderWindows();
                recalc();
            });
        });
    }

    function bindCurtainAddons() {
        var ids = ['curtain-removal', 'curtain-hanging', 'curtain-ironing', 'curtain-roman-mount'];
        ids.forEach(function(id) {
            var cb = document.getElementById(id);
            if (cb) {
                cb.addEventListener('change', function() {
                    var key = id.replace(/-([a-z])/g, function (g) { return g[1].toUpperCase(); });
                    state[key] = this.checked;
                    recalc();
                });
            }
        });
    }
    bindCurtainAddons();

    renderFurniture();
    initAccordion();
    bindOptionCheckboxes();
    recalc();
});
