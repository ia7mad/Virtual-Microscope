const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const html = fs.readFileSync(path.join(__dirname, '../index.html'), 'utf8');
const script = html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];

function harness(baseURI = 'https://ia7mad.github.io/Virtual-Microscope/') {
    const timers = new Map();
    let id = 0;
    const head = { scripts: [], appendChild(script) { this.scripts.push(script); } };
    const context = {
        URL, console, window: {},
        document: { baseURI, head, createElement: () => ({ remove() { this.removed = true; } }) },
        setTimeout(fn) { const key = ++id; timers.set(key, fn); return key; },
        clearTimeout(key) { timers.delete(key); }
    };
    const prefix = script.slice(0, script.indexOf("document.addEventListener('DOMContentLoaded'"));
    vm.runInNewContext(prefix + '\nthis.media = MicroscopeMedia;', context);
    context.tick = () => { const callbacks = [...timers.values()]; timers.clear(); callbacks.forEach(fn => fn()); };
    context.timers = timers;
    return context;
}
const legacy = 'https://ddaxqnhubrctawppwwzc.supabase.co/storage/v1/object/public/microscope-media/specimens/';

test('all eight default slides use existing local images', () => {
    const defaults = [...html.matchAll(/imgUrl: '([^']+)'/g)].map(m => m[1]);
    assert.equal(defaults.length, 8);
    for (const image of defaults) {
        assert.ok(image.startsWith('assets/'), image);
        assert.ok(fs.existsSync(path.join(__dirname, '..', image)), image);
    }
    assert.ok(!/<script[^>]+src=/.test(html), 'No parser-blocking SDK dependency');
    new vm.Script(script);
});

test('old cloud URLs migrate to the exact bundled images, including clinical cases', () => {
    const { media } = harness();
    const images = fs.readdirSync(path.join(__dirname, '../assets')).filter(p => p.endsWith('.png'));
    images.push(...fs.readdirSync(path.join(__dirname, '../assets/cases')).map(p => 'cases/' + p));
    assert.equal(images.length, 13);
    for (const image of images) {
        assert.equal(media.localUrl(legacy + image + '?t=123#preview'), 'assets/' + image);
    }
    assert.equal(media.localUrl('assets/blood_smear.png'), 'assets/blood_smear.png');
    assert.equal(harness('file:///demo/index.html').media.localUrl(legacy + images[0]), 'assets/' + images[0]);
});

test('custom uploads and unrelated specimens keep their identity', () => {
    const { media } = harness();
    for (const url of [legacy + 'unknown.png', legacy.replace('/specimens/', '/uploads/') + 'blood_smear.png',
        'https://example.org/blood_smear.png', 'data:image/png;base64,abc', 'blob:https://example.org/id']) {
        assert.equal(media.localUrl(url), url);
    }
});

test('legacy cache metadata is retained; malformed rows cannot break boot', () => {
    const { media } = harness();
    const cache = [{ id: 'blood', imgUrl: legacy + 'blood_smear.png', name: { ar: 'Blood' },
        notes: 'keep me', markers: [null, {}, { top: '1%', left: '2%', label: { en: 'Cell' } }] }, null, {},
        { id: 'empty', imgUrl: '' }];
    const normalized = media.normalizeSamples(cache);
    assert.equal(normalized.length, 1);
    assert.equal(normalized[0].imgUrl, 'assets/blood_smear.png');
    assert.equal(normalized[0].name.en, 'Blood');
    assert.equal(normalized[0].notes, 'keep me');
    assert.equal(normalized[0].markers.length, 1);
    assert.equal(normalized[0].markers[0].label.ar, 'Cell');
    assert.equal(cache[0].imgUrl, legacy + 'blood_smear.png', 'Input is not mutated');
    assert.equal(media.normalizeSamples({}).length, 0);
});

test('successful image load clears its deadline', () => {
    const h = harness();
    const img = { naturalWidth: 1024 };
    let ready = 0;
    h.media.loadImage(img, legacy + 'blood_smear.png', { ready: () => ready++ });
    assert.equal(img.src, 'assets/blood_smear.png');
    img.onload();
    assert.equal(ready, 1);
    assert.equal(h.timers.size, 0);
});

test('transient failure retries once with cache bypass, then reports failure', () => {
    const h = harness();
    const img = {};
    let failures = 0;
    h.media.loadImage(img, 'assets/blood_smear.png', { failed: () => failures++ });
    img.onerror();
    assert.match(img.src, /\/Virtual-Microscope\/assets\/blood_smear.png\?_microscope_retry=/);
    img.onerror();
    assert.equal(failures, 1);
    assert.equal(h.timers.size, 0);
    assert.equal(img.onerror, null);
});

test('stalled downloads have a bounded deadline', () => {
    const h = harness();
    let failed = false;
    h.media.loadImage({}, 'assets/blood_smear.png', { failed: () => failed = true });
    h.tick();
    assert.equal(failed, false);
    h.tick();
    assert.equal(failed, true);
    assert.equal(h.timers.size, 0);
});

test('changing slides cancels timers and ignores old load/error callbacks', () => {
    const h = harness();
    const img = { naturalWidth: 1024 };
    let oldCallbacks = 0, newCallbacks = 0;
    h.media.loadImage(img, 'first.png', { ready: () => oldCallbacks++, failed: () => oldCallbacks++ });
    const staleLoad = img.onload, staleError = img.onerror;
    h.media.loadImage(img, 'second.png', { ready: () => newCallbacks++ });
    staleLoad(); staleError();
    assert.equal(oldCallbacks, 0);
    assert.equal(h.timers.size, 1);
    img.onload();
    assert.equal(newCallbacks, 1);
    assert.equal(h.timers.size, 0);
});

test('data and blob URLs do not get invalid cache-busting query strings', () => {
    const h = harness();
    const img = {};
    let failures = 0;
    h.media.loadImage(img, 'data:image/png;base64,invalid', { failed: () => failures++ });
    img.onerror();
    assert.equal(failures, 1);
    assert.equal(img.src, 'data:image/png;base64,invalid');
});

test('optional SDK timeout/error resolves without blocking local boot', async () => {
    const h = harness();
    const promise = h.connectOptionalBackend();
    assert.equal(h.document.head.scripts[0].async, true);
    h.tick();
    assert.equal(await promise, null);
    assert.equal(h.document.head.scripts[0].removed, true);
    const errorPromise = h.connectOptionalBackend();
    h.document.head.scripts[1].onerror();
    assert.equal(await errorPromise, null);
    assert.equal(h.timers.size, 0);
});

test('optional SDK still connects when available', async () => {
    const h = harness();
    const client = { connected: true };
    h.window.supabase = { createClient: () => client };
    const promise = h.connectOptionalBackend();
    h.document.head.scripts[0].onload();
    assert.equal(await promise, client);
    assert.equal(h.timers.size, 0);
});
