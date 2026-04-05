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
            if (svc.calc_type === 'carpet') state.activeCalcType = 'carpet';
            else if (svc.calc_type === 'curtains') state.activeCalcType = 'curtains';
            else if (svc.calc_type === 'furniture') state.activeCalcType = 'furniture';
            else state.activeCalcType = 'default';
        }
        // Hide main tabs if they exist
        var tabsEl = document.getElementById('calc-main-tabs');
        if (tabsEl) tabsEl.style.display = 'none';

        // Handle services.html containers
        var fw = document.getElementById('calc-furniture-wrapper');
        var cw = document.getElementById('calc-carpet-wrapper');
        var cuw = document.getElementById('calc-curtains-wrapper');
        if (fw) fw.style.display = state.activeCalcType === 'furniture' ? '' : 'none';
        if (cw) cw.style.display = state.activeCalcType === 'carpet' ? '' : 'none';
        if (cuw) cuw.style.display = state.activeCalcType === 'curtains' ? '' : 'none';

        // Handle service_detail.html sections
        var dp = document.getElementById('carpet-params');
        var cp = document.getElementById('curtain-params');
        var dopt = document.getElementById('default-options');
        if (dp) dp.style.display = state.activeCalcType === 'carpet' ? '' : 'none';
        if (cp) cp.style.display = state.activeCalcType === 'curtains' ? '' : 'none';
        if (dopt) dopt.style.display = state.activeCalcType === 'furniture' ? '' : 'none';
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
            var key = qaBtn.dataset.qaKey;
            var d = parseInt(qaBtn.dataset.qaDelta);
            if (key === 'hairM') {
                state.hairM = Math.max(1, state.hairM + d);
                var el1 = document.getElementById('hair-m');
                var el2 = document.getElementById('carpet-hair-m');
                if (el1) el1.textContent = state.hairM;
                if (el2) el2.textContent = state.hairM;
                recalc();
            }
            if (key === 'boxQ') {
                state.boxQ = Math.max(1, state.boxQ + d);
                var el1 = document.getElementById('box-q');
                var el2 = document.getElementById('carpet-box-q');
                if (el1) el1.textContent = state.boxQ;
                if (el2) el2.textContent = state.boxQ;
                recalc();
            }
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
            if (homePanel) homePanel.classList.toggle('active', tab === 'home');
            if (bizPanel)  bizPanel.classList.toggle('active', tab === 'business');
            // Reset cart for items not in this panel to avoid ghost values
            recalc();
            return;
        }


        // 5. Dirt level
        var dirtBtn = e.target.closest('.dirt-btn');
        if (dirtBtn) {
            state.dirtMult = parseFloat(dirtBtn.dataset.dirt) + 1;
            document.querySelectorAll('.dirt-btn').forEach(function(b) {
                b.classList.toggle('active', b.dataset.dirt === dirtBtn.dataset.dirt);
            });
            recalc();
            return;
        }

        // 6. Global Options (Hair, Box, Night, Faraway)
        var optCard = e.target.closest('.opt-card');
        if (optCard) {
            var optId = optCard.dataset.optId;
            var isCarpetTab = !!optCard.closest('#calc-carpet-wrapper');
            var prefix = isCarpetTab ? 'carpet-' : 'furn-';

            if (optId === 'hair') {
                var cb = document.getElementById(prefix + 'hair');
                // Sync the other checkbox too
                var otherCb = document.getElementById((isCarpetTab ? 'furn-' : 'carpet-') + 'hair');
                if (cb) { 
                    cb.checked = !cb.checked; 
                    if (otherCb) otherCb.checked = cb.checked;
                    // Update classes for BOTH cards if they exist
                    document.querySelectorAll('.opt-card[data-opt-id="hair"]').forEach(function(c) {
                        c.classList.toggle('on', cb.checked);
                    });
                }
                // Show/hide adjusters in BOTH tabs
                var adj1 = document.getElementById('hair-adj');
                var adj2 = document.getElementById('carpet-hair-adj');
                if (adj1) adj1.classList.toggle('visible', cb && cb.checked);
                if (adj2) adj2.classList.toggle('visible', cb && cb.checked);
                recalc();
            } else if (optId === 'box') {
                var cb = document.getElementById(prefix + 'box');
                var otherCb = document.getElementById((isCarpetTab ? 'furn-' : 'carpet-') + 'box');
                if (cb) { 
                    cb.checked = !cb.checked; 
                    if (otherCb) otherCb.checked = cb.checked;
                    document.querySelectorAll('.opt-card[data-opt-id="box"]').forEach(function(c) {
                        c.classList.toggle('on', cb.checked);
                    });
                }
                var adj1 = document.getElementById('box-adj');
                var adj2 = document.getElementById('carpet-box-adj');
                if (adj1) adj1.classList.toggle('visible', cb && cb.checked);
                if (adj2) adj2.classList.toggle('visible', cb && cb.checked);
                recalc();
            } else if (optId === 'night') {
                var cb = document.getElementById(prefix + 'night');
                var otherCb = document.getElementById((isCarpetTab ? 'furn-' : 'carpet-') + 'night');
                if (cb) { 
                    cb.checked = !cb.checked; 
                    if (otherCb) otherCb.checked = cb.checked;
                    document.querySelectorAll('.opt-card[data-opt-id="night"]').forEach(function(c) {
                        c.classList.toggle('on', cb.checked);
                    });
                    recalc(); 
                }
            } else if (optId === 'faraway') {
                var cb = document.getElementById(prefix + 'faraway');
                var otherCb = document.getElementById((isCarpetTab ? 'furn-' : 'carpet-') + 'faraway');
                if (cb) { 
                    cb.checked = !cb.checked; 
                    if (otherCb) otherCb.checked = cb.checked;
                    document.querySelectorAll('.opt-card[data-opt-id="faraway"]').forEach(function(c) {
                        c.classList.toggle('on', cb.checked);
                    });
                    recalc(); 
                }
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

    document.querySelectorAll('input[name="carpet-mode"]').forEach(function(r) {
        r.addEventListener('change', function() {
            state.carpetMode = this.value;
            document.querySelectorAll('.carpet-mode-btn').forEach(function(btn) {
                btn.classList.toggle('active', btn.dataset.mode === state.carpetMode);
            });
            var desc = document.getElementById('carpet-mode-desc');
            if (desc) {
                desc.innerHTML = state.carpetMode === 'general' ?
                    '<b style="color:#28C460;">Американская технология (IICRC S100)</b> Капитальная чистка.' :
                    '<b style="color:#d9534f;">Эконом (Экспресс)</b> Быстрая поверхностная обработка.';
            }
            recalc();
        });
    });

    document.querySelectorAll('input[name="carpet-material"]').forEach(function(r) {
        r.addEventListener('change', function() {
            state.carpetMaterial = this.value;
            document.querySelectorAll('.carpet-material-btn').forEach(function(btn) {
                btn.classList.toggle('active', btn.dataset.material === state.carpetMaterial);
            });
            var desc = document.getElementById('carpet-material-desc');
            if (desc) {
                desc.textContent = state.carpetMaterial === 'synthetic' ?
                    'Стандартные офисные и домашние покрытия.' :
                    'Деликатные покрытия (шерсть, шёлк). +50% к стоимости.';
            }
            recalc();
        });
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
            var sel = document.getElementById('curtain-type');
            var w = wInput ? parseF(wInput.value) : 0;
            var h = hInput ? parseF(hInput.value) : 0;
            if (w <= 0 || h <= 0 || !sel) return;

            var coeff = parseF(sel.value, 0.6);
            var typeName = sel.options[sel.selectedIndex].text.split(' (')[0];
            var weight = w * h * coeff;

            state.curtainWindows.push({ w: w, h: h, weight: weight, type: typeName, coeff: coeff });
            if (wInput) wInput.value = '';
            if (hInput) hInput.value = '';

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
            state.curtainRoman = this.checked;
            var qty = document.getElementById('curtain-roman-qty');
            if (qty) qty.style.display = state.curtainRoman ? 'flex' : 'none';
            if (!state.curtainRoman) {
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

        // If on single service page with default service, use its base price
        if (isSingleService && SERVICES.length === 1) {
            var svc = SERVICES[0];
            grandBase = parseFloat(svc.base_price) || 0;
            det.push({n: svc.name, v: Math.round(grandBase), cls: 'pos'});
            // For single service, check its cart quantity if exists, else 1
            var c = state.cart[svc.id];
            totalQty = (c && c.q) ? c.q : 1;
        } else {
            // Full furniture catalog mode — фильтруем по uphTarget
            if (state.uphTarget === 'business') {
                // Только бизнес-позиции
                var bizFlat = [].concat(CAT.bizChairs, CAT.bizSofas, CAT.bizConf, CAT.bizLounge, CAT.bizPanels);
                bizFlat.forEach(function(item) {
                    var c = state.cart[item.id];
                    if (!c || !c.q) return;
                    var lineBase = item.p * state.uphMult * state.dirtMult * c.q;
                    grandBase += lineBase;
                    var qty = c.q > 1 ? ' ×' + c.q : '';
                    det.push({n: c.n + qty, v: Math.round(lineBase), cls: 'pos'});
                });
            } else {
                // Домашние позиции (home)
                allFlat.forEach(function(item) {
                    var c = state.cart[item.id];
                    if (!c || !c.q) return;
                    var lineBase = item.p * state.uphMult * state.dirtMult * c.q;
                    grandBase += lineBase;
                    var qty = c.q > 1 ? ' ×' + c.q : '';
                    det.push({n: c.n + qty, v: Math.round(lineBase), cls: 'pos'});
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
                });
            }
        }


        if (grandBase === 0) {
            det.push({n: 'Введите параметры для расчёта...', v: 0, cls: 'empty'});
            renderSummary(det, 0);
            return;
        }


        if (state.uphMult > 1) det.push({n: 'Кожа/экокожа (+50%)', v: 0, cls: 'add'});
        if (state.dirtMult > 1) {
            var lbl = state.dirtMult === 1.2 ? 'Сильные загрязнения (+20%)' : 'После ремонта (+50%)';
            det.push({n: lbl, v: 0, cls: 'add'});
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
        if (hairCb && hairCb.checked) { var cost = 5000 * state.hairM; extras += cost; det.push({n: 'Шерсть (' + state.hairM + ' пог.м)', v: Math.round(cost), cls: 'add'}); }
        var boxCb = document.getElementById('furn-box');
        if (boxCb && boxCb.checked) { var cost = 1000 * state.boxQ; extras += cost; det.push({n: 'Ящики (' + state.boxQ + ' шт)', v: Math.round(cost), cls: 'add'}); }
        var nightCb = document.getElementById('furn-night');
        if (nightCb && nightCb.checked) { extras += 5000; det.push({n: 'После 21:00', v: 5000, cls: 'add'}); }
        var farCb = document.getElementById('furn-faraway');
        if (farCb && farCb.checked) { det.push({n: 'Выезд за 10 км', v: 0, cls: 'warn'}); }

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

        if (state.isNewClient) {
            var disc = total * 0.05;
            total -= disc;
            det.push({n: '🎁 Скидка 5% (первый заказ)', v: -Math.round(disc), cls: 'disc'});
        }

        if (state.isCombo) {
            det.push({n: '🔄 Доп. заказ (скидка 15% на мебель)', v: 0, cls: 'warn'});
        }

        renderSummary(det, total);
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
        
        if (state.carpetMode === 'eco') {
            det.push({n: 'Режим Эконом (−40%)', v: 0, cls: 'add'});
        }

        // --- GLOBAL OPTIONS FOR CARPET ---
        var extras = 0;
        var hairCb = document.getElementById('carpet-hair');
        if (hairCb && hairCb.checked) { 
            var cost = 5000 * state.hairM; 
            extras += cost; 
            det.push({n: 'Шерсть (' + state.hairM + ' пог.м)', v: Math.round(cost), cls: 'add'}); 
        }
        var boxCb = document.getElementById('carpet-box');
        if (boxCb && boxCb.checked) { 
            var cost = 1000 * state.boxQ; 
            extras += cost; 
            det.push({n: 'Ящики (' + state.boxQ + ' шт)', v: Math.round(cost), cls: 'add'}); 
        }
        var nightCb = document.getElementById('carpet-night');
        if (nightCb && nightCb.checked) { 
            extras += 5000; 
            det.push({n: 'Работа после 21:00', v: 5000, cls: 'add'}); 
        }
        var farCb = document.getElementById('carpet-faraway');
        if (farCb && farCb.checked) { 
            det.push({n: 'Выезд за 10 км', v: 0, cls: 'warn'}); 
        }
        total += extras;

        total = applyOptionsAndDiscounts(total, det, area, 0, 1);
        renderSummary(det, total);
    }

    // ═══════════════════════════════════════════════════════════════
    // CALC CURTAINS
    // ═══════════════════════════════════════════════════════════════
    function getCoeff(name) {
        var found = COEFFS.find(function(c) { return c.name === name; });
        return found ? parseFloat(found.coefficient) : 0.6;
    }

    function calcCurtains() {
        var wgt = 0, area = 0;

        if (state.curtainMode === 'weight') {
            wgt = state.curtainWeight;
            area = wgt * 1.5;
        } else {
            state.curtainWindows.forEach(function(item) {
                wgt += item.weight;
                area += item.w * item.h;
            });
        }

        if (wgt <= 0 && state.curtainWindows.length === 0 && !state.curtainRoman) {
            renderSummary([{n: 'Введите вес или добавьте окна...', v: 0, cls: 'empty'}], 0);
            return;
        }

        var det = [];
        var pricePerKg = 3600;
        var curtainSvc = null;
        for (var id in servicesMap) {
            if (servicesMap[id].calc_type === 'curtains') { curtainSvc = servicesMap[id]; break; }
        }
        if (curtainSvc) pricePerKg = parseFloat(curtainSvc.base_price) || 0;

        var total = wgt * pricePerKg;
        if (wgt > 0) {
            det.push({n: 'Химчистка (' + wgt.toFixed(1) + ' кг × ' + pricePerKg.toLocaleString('ru-RU') + ' ₸/кг)', v: Math.round(total), cls: 'pos'});
        }

        if (state.curtainRoman) { var c = state.romanQty * 3000; total += c; det.push({n: 'Монтаж римских (' + state.romanQty + ' шт)', v: Math.round(c), cls: 'add'}); }

        // Custom Curtains Addons
        if (state.curtainRemoval) {
            var c = wgt * 400;
            total += c;
            det.push({n: 'Снятие штор (+' + Math.round(c).toLocaleString('ru-RU') + ' ₸)', v: Math.round(c), cls: 'add'});
        }
        if (state.curtainHanging) {
            var c = wgt * 600;
            total += c;
            det.push({n: 'Навеска и стяжка (+' + Math.round(c).toLocaleString('ru-RU') + ' ₸)', v: Math.round(c), cls: 'add'});
        }
        if (state.curtainIroning) {
            var c = area * 500;
            // Does NOT affect price per user request
            det.push({n: 'Глажка / Отпаривание (+' + Math.round(c).toLocaleString('ru-RU') + ' ₸)', v: 0, cls: 'warn'});
        }

        total = applyOptionsAndDiscounts(total, det, area, wgt, state.curtainWindows.length);
        renderSummary(det, total);
    }

    // ═══════════════════════════════════════════════════════════════
    // RENDER SUMMARY
    // ═══════════════════════════════════════════════════════════════
    function renderSummary(det, total) {
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
            var svcName = '';
            if (state.activeCalcType === 'furniture') svcName = 'Химчистка мебели';
            else if (state.activeCalcType === 'carpet') svcName = 'Химчистка ковролина';
            else if (state.activeCalcType === 'curtains') svcName = 'Химчистка штор';
            else svcName = service_id ? 'Заказ услуги' : 'Химчистка';
            orderBtn.dataset.serviceName = svcName;
            orderBtn.dataset.options = det.filter(function(d) { return d.cls !== 'sep' && d.cls !== 'empty'; }).map(function(d) { 
                return d.n + (d.v !== 0 ? ': ' + fmt(d.v) : ''); 
            }).join('\n');
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
        
        total = applyOptionsAndDiscounts(total, det, 0, 0, 1);
        renderSummary(det, total);
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
    renderFurniture();
    initAccordion();
    bindOptionCheckboxes();
    recalc();
});
