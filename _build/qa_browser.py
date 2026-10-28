#!/usr/bin/env python3
"""Browser QA (headless Chromium via Playwright). Run after build.py and qa.py:

    pip install playwright && python3 -m playwright install chromium
    python3 _build/qa_browser.py [--axe path/to/axe.min.js]

Checks the opening animation (landing on any page, once per session, #hash and reduced-motion skips),
the hero airflow, the pinned "inside the system" sequence, menus, form validation, the instant system
estimate end to end (prices recalculated here from site.config.json and compared with what the page shows),
the repair-or-replace check, console errors and horizontal overflow on phones.
With --axe, runs axe-core (WCAG 2.1 A/AA) on key pages. Exits non-zero on failures."""
import asyncio, functools, http.server, socketserver, threading, json, os, sys
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "site.config.json")))
E = CFG.get("estimator") or {}
AXE = sys.argv[sys.argv.index("--axe") + 1] if "--axe" in sys.argv else None
res = []
def rec(ok, msg, extra=""): res.append(("PASS" if ok else "FAIL", msg + (f"  [{extra}]" if extra and not ok else "")))

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def handle(self):
        try: super().handle()
        except (ConnectionResetError, BrokenPipeError): pass
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.ThreadingTCPServer(("127.0.0.1", 8822), functools.partial(Q, directory=ROOT))
threading.Thread(target=srv.serve_forever, daemon=True).start()
B = "http://127.0.0.1:8822"
OFFERED = CFG.get("services") or []
SVC_PAGE = f"/services/{OFFERED[0]}/" if OFFERED else "/services/"
SVC_CITY = f"/services/{OFFERED[0]}/windsor/" if OFFERED and os.path.exists(os.path.join(ROOT, f"services/{OFFERED[0]}/windsor")) else None

def by(lst, i): return next(x for x in lst if x["id"] == i)
def expected(mat, height=None, length=None, terrain=None, walk=0, dbl=0, addons=(), removal=False):
    m = by(E["materials"], mat)
    h = by(E["heights"], height or m.get("default_height") or m["heights"][-1])
    t = by(E["terrain"], terrain or E.get("default_terrain", "flat"))
    L = length or E["length"]["default"]
    per = sum(by(E["addons"], a).get("per_ft", 0) for a in addons)
    flat = sum(by(E["addons"], a).get("flat", 0) for a in addons)
    mid = (m["per_ft"] * h["mult"] * t["mult"] + (E.get("removal_per_ft", 0) if removal else 0) + per) * L + walk * m["walk_gate"] + dbl * m["double_gate"] + flat
    mid = max(E.get("minimum_job", 0), mid)
    pct = E.get("range_pct", 12) / 100; r = E.get("round_to", 50)
    rnd = lambda n: int(round(n / r) * r)
    lo, hi = rnd(mid * (1 - pct)), rnd(mid * (1 + pct))
    lo = max(lo, rnd(E.get("minimum_job", 0)))
    return f"${lo:,}", f"${hi:,}"

async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch()
        errors = []
        async def page(w=1440, h=900, reduced=False, seen=True):
            ctx = await br.new_context(viewport={"width": w, "height": h}, reduced_motion="reduce" if reduced else "no-preference")
            if seen: await ctx.add_init_script("try{sessionStorage.setItem('fn-intro','1')}catch(e){}")
            pg = await ctx.new_page()
            pg.on("pageerror", lambda e: errors.append(str(e)))
            pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            return ctx, pg

        # ---- opening animation
        if CFG.get("intro", True):
            land = SVC_PAGE if CFG.get("intro_scope", "all") == "all" else "/"
            ctx, pg = await page(seen=False)
            await pg.goto(B + land, wait_until="commit"); await pg.wait_for_timeout(700)
            showing = await pg.evaluate("!!document.querySelector('.intro') && !document.documentElement.classList.contains('no-intro')")
            reading = await pg.evaluate("document.querySelectorAll('.intro .ig-pk').length + document.querySelectorAll('.intro .ip').length")
            await pg.wait_for_timeout(4800)
            gone = await pg.evaluate("!document.querySelector('.intro') && document.documentElement.classList.contains('is-ready')")
            rec(showing and gone, f"Opening animation plays when landing on {land} and clears itself", f"showing={showing} gone={gone}")
            rec(reading == 23, "Intro builds the gates: 3 posts and 20 pickets", f"parts={reading}")
            await pg.goto(B + "/about/", wait_until="commit"); await pg.wait_for_timeout(300)
            rec(await pg.evaluate("document.documentElement.classList.contains('no-intro')"), "Intro does not replay on the next page in the same session")
            await ctx.close()
            ctx, pg = await page(seen=False)
            await pg.goto(B + "/#faq-title", wait_until="commit"); await pg.wait_for_timeout(300)
            rec(await pg.evaluate("document.documentElement.classList.contains('no-intro')"), "Intro skipped when the URL has a #hash")
            await ctx.close()
            ctx, pg = await page(seen=False, reduced=True)
            await pg.goto(B + "/"); await pg.wait_for_timeout(300)
            rec(await pg.evaluate("document.documentElement.classList.contains('no-intro')"), "Intro skipped for reduced motion")
            await ctx.close()
            ctx, pg = await page(seen=False)
            await pg.goto(B + "/", wait_until="commit"); await pg.wait_for_timeout(500)
            await pg.mouse.click(10, 500); await pg.wait_for_timeout(2400)
            rec(await pg.evaluate("!document.querySelector('.intro')"), "A click skips the intro")
            await ctx.close()

        # ---- home: hero fence + sequence + CLS
        ctx, pg = await page()
        await pg.goto(B + "/"); await pg.wait_for_timeout(3200)
        if CFG.get("hero_fx", True):
            # fallback hero (no WebGL / no three.js): block three.js and check the normal hero with its SVG fence line
            fctx, fpg = await page()
            await fpg.route("**/three.min.js*", lambda r: r.abort())
            await fpg.goto(B + "/"); await fpg.wait_for_timeout(5000)
            hf = await fpg.evaluate("(()=>{const p=[...document.querySelectorAll('.hero-fence .hp')];return [p.length,p.filter(e=>e.getBoundingClientRect().height>0).length,document.documentElement.classList.contains('yard-off'),getComputedStyle(document.querySelector('.yard')).position, document.querySelector('.yard').offsetHeight < innerHeight*1.5]})()")
            rec(hf[0] > 100 and hf[1] == hf[0] and hf[2] and hf[4], "Without WebGL/three.js: normal hero (not pinned) with the SVG fence line drawn and every picket risen", f"{hf}")
            await fctx.close()
            errors[:] = [e for e in errors if "ERR_FAILED" not in e]   # the blocked three.js request above is deliberate
        if CFG.get("yard_scene", True):
            live = await pg.evaluate("document.documentElement.classList.contains('yard-live') && document.querySelector('.yard__pin') && getComputedStyle(document.querySelector('.yard__pin')).position==='sticky'")
            await pg.evaluate("window.__yardSeek(0.5)"); await pg.wait_for_timeout(300)
            mid = await pg.evaluate("[parseInt(document.querySelector('.yard__ft b').textContent,10), !!document.querySelector('.ymsg.is-on')]")
            await pg.evaluate("window.__yardSeek(0.99)"); await pg.wait_for_timeout(1200)
            end = await pg.evaluate("[document.querySelector('.yard__ft b').textContent, document.querySelector('[data-yard]').classList.contains('is-end'), document.querySelectorAll('.ytag.is-safe').length, getComputedStyle(document.querySelector('.yard .hero__est')).opacity]")
            rec(live and 0 < mid[0] < 256 and mid[1] and end[0] == "256" and end[1] and end[2] == 4 and end[3] == "1",
                "3D yard scene: pinned, fence builds around the yard (footage climbs to 256 ft), messages show, all 4 tags flip to Protected, estimate card appears at the end", f"live={live} mid={mid} end={end}")
            await pg.evaluate("window.__yardSeek(0); window.scrollTo(0,0)"); await pg.wait_for_timeout(300)
        cls = await pg.evaluate("""new Promise(r=>{let v=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)v+=e.value}).observe({type:'layout-shift',buffered:true});setTimeout(()=>r(v),300)})""")
        rec(cls < 0.1, f"Home page layout shift (CLS) {cls:.3f} < 0.1")
        n = await pg.evaluate("document.querySelectorAll('.sequence__stage > .fence-card').length")
        top = await pg.evaluate("document.querySelector('.sequence').getBoundingClientRect().top+scrollY"); span = await pg.evaluate("document.querySelector('.sequence').offsetHeight-innerHeight")
        okall, notes = True, []
        for i in range(n):
            await pg.evaluate(f"window.scrollTo(0,{top + span * (i + 0.03) / n})"); await pg.wait_for_timeout(250)
            early = await pg.evaluate("(()=>{const c=document.querySelector('.fence-card.is-current');const p=c.querySelector('.f-post');return [c.dataset.fence, parseFloat(getComputedStyle(p).opacity), document.querySelector('.sequence__step.is-active h3').textContent]})()")
            await pg.evaluate(f"window.scrollTo(0,{top + span * (i + 0.92) / n})"); await pg.wait_for_timeout(250)
            late = await pg.evaluate("(()=>{const c=document.querySelector('.fence-card.is-current');const parts=[...c.querySelectorAll('.f-post,.f-drop,.f-panel,.f-board,.f-cap')];return [c.dataset.fence, parts.every(e=>parseFloat(getComputedStyle(e).opacity)>0.97), document.querySelector('.sequence__phase').textContent]})()")
            good = early[0] == late[0] and early[1] < 0.5 and late[1]
            okall = okall and good
            if not good: notes.append(f"{i}: early={early} late={late}")
        rec(n == len([x for x in OFFERED if x in ("wood-fences","vinyl-fences","ornamental-fences","chain-link-fences","composite-fences")]) and okall,
            f"Pinned sequence builds all {n} fence types from empty holes to finished fence as you scroll", "; ".join(notes[:3]))
        await pg.evaluate(f"window.scrollTo(0,{top + span})"); await pg.wait_for_timeout(300)
        rec(await pg.evaluate("document.querySelector('.sequence__phase').textContent==='Built' && document.querySelector('.sequence__pct').textContent==='100%'"), "Sequence ends on the last fence fully built (Built, 100%)")
        # desktop menu
        await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(400)
        await pg.click(".nav__item[data-dropdown] button"); await pg.wait_for_timeout(500)
        rec(await pg.evaluate("document.querySelector('.nav__item[data-dropdown]').classList.contains('is-open') && document.querySelector('#mega-services').getBoundingClientRect().right <= innerWidth"), "Services dropdown opens and stays inside the window")
        await pg.keyboard.press("Escape"); await pg.wait_for_timeout(200)
        rec(await pg.evaluate("!document.querySelector('.nav__item.is-open')"), "Escape closes the dropdown")
        if E.get("enabled", True):
            await pg.evaluate("document.querySelector('.pick:nth-child(2) input').checked=true"); await pg.click(".picker__go"); await pg.wait_for_load_state(); await pg.wait_for_timeout(400)
            chosen = await pg.evaluate("(document.querySelector('#est-form input[name=material]:checked')||{}).value")
            rec("fence-estimate" in pg.url and chosen == E["materials"][1]["id"], "Hero material picker opens the estimate with that material selected", f"url={pg.url} chosen={chosen}")
        await ctx.close()

        # ---- reduced motion: sequence shows every fence built, no pinning
        ctx, pg = await page(reduced=True)
        await pg.goto(B + "/"); await pg.wait_for_timeout(500)
        st = await pg.evaluate("(()=>{const s=document.querySelector('.sequence');const cards=[...s.querySelectorAll('.fence-card')];return [getComputedStyle(s.querySelector('.sequence__sticky')).position, cards.every(c=>getComputedStyle(c).opacity==='1' && parseFloat(getComputedStyle(c.querySelector('.f-post')).opacity)>0.99)]})()")
        rec(st[0] != "sticky" and st[1], "Reduced motion: no pinning, every fence shown fully built", str(st))
        await ctx.close()

        # ---- estimator maths
        if E.get("enabled", True):
            ctx, pg = await page()
            await pg.goto(B + "/fence-estimate/"); await pg.wait_for_timeout(400)
            async def shown():
                return [await pg.text_content("#est-low"), await pg.text_content("#est-high")]
            got = await shown(); exp = expected(E["default_material"])
            rec(got == list(exp), f"Default estimate matches config ({exp[0]} – {exp[1]})", f"got {got}")
            allok, bad, cnt = True, [], 0
            for m in E["materials"]:
                await pg.check(f'#est-form input[name=material][value="{m["id"]}"]', force=True)
                for hh in m["heights"]:
                    for t in E["terrain"]:
                        for L in (40, 150, 420):
                            await pg.check(f'#est-form input[name=height][value="{hh}"]', force=True)
                            await pg.check(f'#est-form input[name=terrain][value="{t["id"]}"]', force=True)
                            await pg.fill("#est-len", str(L)); await pg.dispatch_event("#est-len", "change")
                            g = await shown(); x = expected(m["id"], hh, L, t["id"]); cnt += 1
                            if g != list(x): allok = False; bad.append(f'{m["id"]}/{hh}/{t["id"]}/{L}: {g} vs {x}')
            rec(allok, f"Every material × height × ground × length combination matches the config ({cnt} checked)", "; ".join(bad[:3]))
            m0 = E["materials"][0]
            await pg.check(f'#est-form input[name=material][value="{m0["id"]}"]', force=True)
            await pg.check('#est-form input[name=terrain][value="flat"]', force=True)
            await pg.check(f'#est-form input[name=height][value="{m0["heights"][-1]}"]', force=True)
            await pg.fill("#est-len", "150"); await pg.dispatch_event("#est-len", "change")
            await pg.click('#est-walk ~ .stepper__b'); await pg.click('#est-double ~ .stepper__b'); await pg.click('#est-double ~ .stepper__b')
            await pg.check("#est-removal", force=True)
            ids = [a["id"] for a in E.get("addons", []) if m0["id"] in a.get("materials", [m0["id"]])]
            for a in ids: await pg.check(f'#est-form input[name=addon][value="{a}"]', force=True)
            rec(await shown() == list(expected(m0["id"], m0["heights"][-1], 150, "flat", 1, 2, ids, True)), "Gates, old fence removal and extras are added to the estimate", f"{await shown()}")
            other = next((x for x in E["materials"] if x["id"] != m0["id"]), None)
            if other:
                await pg.check(f'#est-form input[name=material][value="{other["id"]}"]', force=True)
                hidden_ok = await pg.evaluate("ids=>[...document.querySelectorAll('#est-addons .chk')].every(l=>{const a=l.dataset.addon;const m=l.dataset.materials.split(' ');return l.hidden===!m.includes(document.querySelector('input[name=material]:checked').value)})", ids)
                rec(hidden_ok, "Extras that don't apply to the chosen material are hidden")
                pv = await pg.evaluate("(document.querySelector('.est-preview .fence-card.is-sel')||{}).dataset?.fence")
                rec(pv == other["id"], "Fence preview switches to the chosen material", f"preview={pv}")
            await pg.click("#est-measure summary"); await pg.fill("#m-w", "50"); await pg.fill("#m-d", "110"); await pg.wait_for_timeout(100)
            await pg.click("#m-use"); await pg.wait_for_timeout(100)
            rec(await pg.input_value("#est-len") == "270", "Measure my yard: 50 × 110 ft yard, back and both sides = 270 ft", await pg.input_value("#est-len"))
            await pg.click("#est-lead-open"); await pg.wait_for_timeout(500)
            fields = await pg.evaluate("Object.fromEntries([...document.querySelectorAll('#est-lead input[type=hidden]')].map(i=>[i.name,i.value]))")
            rec(not await pg.evaluate("document.getElementById('est-lead').hidden") and fields.get("Material") and fields.get("Length") == "270 ft" and "$" in fields.get("Estimate shown", ""), "Lead form opens with the material, length, gates, extras and estimate filled in", json.dumps(fields))
            await pg.click("#est-lead button[type=submit]"); await pg.wait_for_timeout(200)
            rec(await pg.evaluate("document.querySelector('#est-lead .form__status').classList.contains('is-visible') && document.activeElement.id==='lead-name'"), "Empty estimate form shows errors and focuses the first field")
            await ctx.close()
            ctx, pg = await page(390, 844)
            await pg.goto(B + "/fence-estimate/"); await pg.wait_for_timeout(300)
            await pg.evaluate("document.querySelector('.len').scrollIntoView()"); await pg.wait_for_timeout(800)
            rec(await pg.evaluate("document.getElementById('est-live').classList.contains('is-visible') && document.getElementById('est-live-v').textContent.includes('$')"), "Phones: live price bar shows while the result card is off screen")
            await ctx.close()

        # ---- contact form validation
        ctx, pg = await page()
        await pg.goto(B + "/contact/"); await pg.click(".form button[type=submit]"); await pg.wait_for_timeout(200)
        rec(await pg.evaluate("document.querySelector('.form .form__status').classList.contains('is-visible') && document.querySelectorAll('.form [aria-invalid=true]').length>=5"), "Contact form: empty submit shows errors on required fields")
        await pg.fill("#email", "not-an-email"); await pg.click(".form button[type=submit]")
        rec("valid email" in (await pg.text_content("#email-error")), "Contact form: invalid email message")
        await ctx.close()

        # ---- phones: menu, overflow, call bar
        ctx, pg = await page(390, 844)
        over = []
        pages = ["/", "/fence-estimate/", SVC_PAGE, "/services/", "/service-areas/", "/service-areas/windsor/", "/contact/", "/faq/", "/about/", "/privacy-policy.html", "/404.html"] + ([SVC_CITY] if SVC_CITY else [])
        for u in pages:
            await pg.goto(B + u); await pg.wait_for_timeout(250)
            if await pg.evaluate("document.documentElement.scrollWidth > innerWidth + 1"): over.append(u)
        rec(not over, f"No horizontal scrolling at 390px on {len(pages)} key pages", ", ".join(over))
        await pg.goto(B + "/"); await pg.click(".burger"); await pg.wait_for_timeout(800)
        rec(await pg.evaluate("document.getElementById('mobile-nav').classList.contains('is-open') && document.querySelector('.burger').getAttribute('aria-expanded')==='true'"), "Mobile menu opens from the burger button")
        await pg.keyboard.press("Escape"); await pg.wait_for_timeout(300)
        await pg.evaluate("window.scrollTo(0,1400)"); await pg.wait_for_timeout(600)
        rec(await pg.evaluate("document.querySelector('.callbar').classList.contains('is-visible')"), "Mobile call bar appears after scrolling")
        await ctx.close()

        # ---- axe
        if AXE:
            src = open(AXE).read()
            ctx, pg = await page()
            for u in ["/", "/fence-estimate/", SVC_PAGE, "/contact/", "/service-areas/windsor/"]:
                await pg.goto(B + u); await pg.wait_for_timeout(1500); await pg.add_script_tag(content=src)
                v = await pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa','wcag21a','wcag21aa']}).then(r=>r.violations.map(v=>v.id+' ('+v.nodes.length+')'))")
                rec(not v, f"axe WCAG 2.1 AA on {u}: {len(v)} violations", ", ".join(v))
            await ctx.close()

        rec(not errors, f"No JavaScript errors in the console ({len(errors)})", " | ".join(errors[:4]))
        await br.close()
    for s, m in res: print(s, m)
    f = sum(1 for s, _ in res if s == "FAIL")
    print(f"\n{len(res) - f} passed, {f} failed")
    sys.exit(1 if f else 0)

asyncio.run(main())
