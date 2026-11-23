(function () {
  var WA = '601143010078';
  var PRICES = { kalendar: 35, combo: 47, clicker: 17 };
  var NAMES = { kalendar: 'Kalendar Meja', combo: 'Combo (Kalendar + Clicker)', clicker: 'Clicker' };
  var form = document.getElementById('orderForm');
  var totalEl = document.getElementById('total');
  var errEl = document.getElementById('err');

  function rm(n) { return 'RM' + n.toFixed(2); }
  function qtyInput(pkg) { return form.querySelector('.qty-row[data-pkg="' + pkg + '"] input'); }

  function items() {
    return Object.keys(PRICES).map(function (k) {
      return { key: k, qty: parseInt(qtyInput(k).value, 10) || 0 };
    }).filter(function (i) { return i.qty > 0; });
  }
  function total() {
    return items().reduce(function (s, i) { return s + i.qty * PRICES[i.key]; }, 0);
  }
  function refresh() { totalEl.textContent = rm(total()); }

  form.querySelectorAll('.stepper').forEach(function (st) {
    var input = st.querySelector('input');
    st.querySelector('.plus').addEventListener('click', function () { input.value = Math.min(99, (+input.value || 0) + 1); refresh(); });
    st.querySelector('.minus').addEventListener('click', function () { input.value = Math.max(0, (+input.value || 0) - 1); refresh(); });
  });

  // Butang "Pilih" pada kad harga
  document.querySelectorAll('.pick').forEach(function (b) {
    b.addEventListener('click', function () {
      var pkg = b.getAttribute('data-pkg');
      Object.keys(PRICES).forEach(function (k) { qtyInput(k).value = k === pkg ? 1 : 0; });
      refresh();
      document.getElementById('tempah').scrollIntoView();
      setTimeout(function () { form.elements.nama.focus({ preventScroll: true }); }, 400);
    });
  });

  // Validasi selepas blur, kosongkan ralat bila dibetulkan
  form.querySelectorAll('[required]').forEach(function (el) {
    el.addEventListener('blur', function () { el.classList.toggle('invalid', !el.value.trim()); });
    el.addEventListener('input', function () { if (el.value.trim()) el.classList.remove('invalid'); });
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    errEl.textContent = '';
    var list = items();
    if (!list.length) { errEl.textContent = 'Sila pilih sekurang-kurangnya 1 item.'; return; }
    var missing = Array.prototype.filter.call(form.querySelectorAll('[required]'), function (el) {
      var bad = !el.value.trim(); el.classList.toggle('invalid', bad); return bad;
    });
    if (missing.length) { errEl.textContent = 'Sila lengkapkan maklumat yang bertanda merah.'; missing[0].focus(); return; }
    var f = form.elements;
    if (!/^\d{5}$/.test(f.poskod.value.trim())) { f.poskod.classList.add('invalid'); errEl.textContent = 'Poskod perlu 5 digit.'; f.poskod.focus(); return; }

    var lines = [
      'Assalamualaikum, saya nak tempah *Kalendar Meja Wanita Cantik 2027* 🌺',
      '',
      '*Tempahan:*'
    ];
    list.forEach(function (i) { lines.push('• ' + NAMES[i.key] + ' x' + i.qty + ' = ' + rm(i.qty * PRICES[i.key])); });
    lines.push('*Jumlah: ' + rm(total()) + '* (+ kos pos)', '',
      '*Nama:* ' + f.nama.value.trim(),
      '*Telefon:* ' + f.telefon.value.trim(),
      '*Alamat:* ' + f.alamat.value.trim() + ', ' + f.poskod.value.trim() + ' ' + f.negeri.value);
    if (f.catatan.value.trim()) lines.push('*Catatan:* ' + f.catatan.value.trim());

    window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
  });

  refresh();
})();
