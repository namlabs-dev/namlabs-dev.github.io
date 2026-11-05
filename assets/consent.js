// Google Analytics with Consent Mode. Visitors in the EEA, UK and Switzerland
// start with analytics cookies denied (Google applies the region rule by IP)
// and see a small banner; everyone else is measured without one. Ads storage
// stays denied everywhere because the site shows no ads.
(function () {
  var ID = 'G-CB1KDFSZJ2';
  var KEY = 'namlabs-consent';
  var EU = ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV',
            'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'IS', 'LI', 'NO', 'GB', 'CH'];
  var ADS = { ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' };

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;

  function extend(a, b) { for (var k in b) a[k] = b[k]; return a; }
  gtag('consent', 'default', extend({ analytics_storage: 'denied', region: EU, wait_for_update: 500 }, ADS));
  gtag('consent', 'default', extend({ analytics_storage: 'granted' }, ADS));

  function load(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function save(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode: ask again next time */ } }

  var saved = load(KEY);
  if (saved === 'granted' || saved === 'denied') gtag('consent', 'update', { analytics_storage: saved });

  gtag('js', new Date());
  gtag('config', ID, { cookie_expires: 34128000 }); // about 13 months
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + ID;
  document.head.appendChild(s);

  var TEXT = {
    en: ['We use Google Analytics cookies to see which pages people visit. Is that OK?', 'Accept', 'Decline', 'Privacy', 'Cookie choice'],
    vi: ['Chúng tôi dùng cookie Google Analytics để biết trang nào được xem nhiều. Bạn đồng ý chứ?', 'Đồng ý', 'Từ chối', 'Quyền riêng tư', 'Lựa chọn cookie'],
    ja: ['どのページが見られているかを知るため、Google アナリティクスの Cookie を使用します。よろしいですか？', '同意する', '拒否する', 'プライバシー', 'Cookie の設定']
  };

  // Styles live here so pages without site.css (the per-game policies) get the
  // same banner. Each colour falls back for pages that lack the site's tokens.
  var CSS =
    '.consent{position:fixed;z-index:50;left:16px;right:16px;bottom:max(16px,env(safe-area-inset-bottom));margin:0 auto;max-width:560px;' +
    'display:flex;flex-wrap:wrap;align-items:center;gap:10px 12px;padding:16px 18px;box-sizing:border-box;' +
    'background:var(--card,#fff);color:var(--text,#13232b);border:1px solid var(--line,#d9e6ea);border-radius:18px;' +
    'box-shadow:var(--shadow,0 12px 32px -12px rgba(0,0,0,.35));font:inherit}' +
    '.consent p{flex:1 1 100%;margin:0;font-size:14px;line-height:1.5}' +
    '.consent a{color:var(--brand,var(--accent,#7c3aed))}' +
    '.consent button{padding:9px 18px;border-radius:14px;font-family:inherit;font-size:15px;font-weight:700;line-height:1.2;cursor:pointer}' +
    '.consent .consent-yes{background:#111;color:#fff;border:0}' +
    '.consent .consent-no{background:var(--bg-2,transparent);color:var(--text,inherit);border:1.5px solid var(--line,#d9e6ea)}' +
    '.consent button:focus-visible{outline:3px solid var(--brand,var(--accent,#7c3aed));outline-offset:3px}' +
    '@media (prefers-color-scheme:dark){.consent .consent-yes{background:#fff;color:#111;border:1.5px solid #111}}';

  // The banner only appears where consent is needed. The time zone is a cheap
  // stand-in for the visitor's region; outside Europe consent is granted anyway.
  function inEurope() {
    try { return /^(Europe\/|Atlantic\/(Reykjavik|Canary|Madeira|Azores|Faroe)$|Asia\/(Nicosia|Famagusta)$|Arctic\/Longyearbyen$)/.test(Intl.DateTimeFormat().resolvedOptions().timeZone); }
    catch (e) { return false; }
  }

  function banner() {
    if (document.querySelector('.consent')) return;
    var opener = document.activeElement;
    var lang = document.documentElement.lang;
    var t = TEXT[lang] || TEXT.en;
    if (!document.getElementById('consent-css')) {
      var st = document.createElement('style');
      st.id = 'consent-css';
      st.textContent = CSS;
      document.head.appendChild(st);
    }
    var box = document.createElement('div');
    box.className = 'consent';
    box.setAttribute('role', 'region');
    box.setAttribute('aria-label', t[4]);
    box.setAttribute('aria-live', 'polite');
    var p = document.createElement('p');
    p.textContent = t[0] + ' ';
    var a = document.createElement('a');
    a.href = (lang === 'en' || !TEXT[lang] ? '/' : '/' + lang + '/') + 'privacy.html';
    a.textContent = t[3];
    p.appendChild(a);
    box.appendChild(p);
    [['granted', t[1], 'consent-yes'], ['denied', t[2], 'consent-no']].forEach(function (b) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = b[2];
      btn.textContent = b[1];
      btn.addEventListener('click', function () {
        save(KEY, b[0]);
        gtag('consent', 'update', { analytics_storage: b[0] });
        box.remove();
        if (opener && opener !== document.body && opener.focus) opener.focus();
      });
      box.appendChild(btn);
    });
    document.body.appendChild(box);
  }

  // The privacy page has a button that reopens the choice.
  window.namlabsConsent = banner;
  function bindChange() {
    var btn = document.getElementById('consent-change');
    if (btn) btn.addEventListener('click', banner);
  }

  function ready() {
    bindChange();
    if (!saved && inEurope()) banner();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready);
  else ready();
})();
