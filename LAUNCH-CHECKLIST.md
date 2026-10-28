# Launch Checklist, Test Report & Technical Notes

Template build: October 27, 2026. Sample business "Stakeline Fence Co." with placeholder contact details and **sample estimate pricing**. Not ready to index until the client items below are done and `demo_mode` is `false`.

## 1. Test report

### Passed (verified by running tests, not by reading code)

**Static QA** (`python3 _build/qa.py`, output in `_build/qa-latest.txt`): 32 passed, 0 warnings, 0 failed.
- 67 pages; 0 broken internal links or assets; 0 orphan pages.
- 65 indexable pages: unique titles and descriptions, titles ≤ 65 characters, descriptions ≤ 160, one H1 per page, no duplicate IDs, every form field labelled, every image has alt text.
- Canonical and `og:url` match the file path on every page. `sitemap.xml` is valid with 65 URLs, exactly matching the indexable inventory. `robots.txt` points to it.
- JSON-LD parses everywhere: HomeAndConstructionBusiness ×1, WebSite ×1, Service ×52, BreadcrumbList ×65, ItemList ×1, ContactPage ×1, WebApplication ×1.
- All 13 service pages have 500–600 words of main content. The 39 city pages have 358–430 words each, and the highest overlap between any two city pages is 39%.
- Contrast ≥ 4.5:1 on all key colour pairs. No template tokens or placeholder text. No "best / #1 / guarantee / years of experience / star rating" claims. Legal links in every footer. Demo banner on every page.
- Opening animation is on exactly the 65 indexable pages, never the 404 or thank-you page. The estimate page carries the config prices; the home picker submits to it. The scroll sequence has one complete fence build per offered fence type.
- Removing services was tested (composite, staining and farm removed): their pages, links, menu items, the composite fence in the scroll sequence, the composite estimate material and the stain extra disappear, and the sentences that mention them are listed for rewording.

**Browser QA** (`python3 _build/qa_browser.py --axe axe.min.js`, headless Chromium at 1440×900 and 390×844, output in `_build/qa-browser-latest.txt`): 34 passed, 0 failed.
- Opening animation plays when landing on a service page, builds the gates (3 posts, 20 pickets), swings them open, clears itself and doesn't replay on the next page. Skipped for a `#hash` and reduced motion; a click skips it.
- Hero fence line draws and every picket rises. Home page CLS under 0.01.
- **Scroll sequence:** for each of the 5 fence types, the posts are not yet in at the start of its slot and every post, picket/panel/board and cap is fully in place by the end; the sequence finishes on "Built, 100%". With reduced motion there's no pinning and all five fences show fully built.
- Services dropdown opens inside the window and Escape closes it. Mobile menu and mobile call bar work.
- **Instant estimate:** all 126 material × height × ground × length combinations match prices recalculated from `site.config.json`; gates, removal and extras add correctly; extras that don't apply to a material are hidden; the preview switches material; "measure my yard" gives 270 ft for a 50 × 110 ft yard fenced on three sides; the lead form opens with every choice filled in; empty submit is blocked; the live price bar shows on phones.
- Contact form blocks empty submissions and flags invalid email.
- No horizontal scrolling at 390 px on 12 key pages. No JavaScript errors.
- axe-core (WCAG 2.1 A/AA): 0 violations on home, estimate, a service page, contact and a city hub.

### Not tested yet (needs the deployed site or client accounts)
- Form delivery: needs the client's email in `form_endpoint` and FormSubmit activation.
- Live domain, HTTPS, PageSpeed Insights / Core Web Vitals in the field, Rich Results Test, real iOS Safari and Android devices, Search Console.

### Requires client input
| Item | Where |
|---|---|
| Business name, legal name, phone, email, domain, hours | `site.config.json` |
| Public address or service-area business | `address` |
| **Real installed price per foot for each material, gate prices, height and ground multipliers, removal, extras, minimum job** | `estimator` |
| Materials and heights they actually install | `estimator.materials` + `services` |
| Form recipient + FormSubmit activation | `form_endpoint` |
| Google Business Profile and social URLs | `site.config.json` |
| Confirm hero badges and working standards are true (locates every job, posts below frost, written quotes) | `_build/pages.py` (`tags`, `features`, `statement_points`) |
| Lifespan and upkeep figures in the scroll sequence match what they tell customers | `pages.py` → `fence_types` |
| Real About story, insurance and WSIB, warranties, suppliers | `pages.py` → `about` |
| Real job photos | `photos` in config |
| Legal review of Privacy, Terms, Cookie drafts | `pages.py` |

## 2. Manual launch tasks
1. Fill in config, set real estimate pricing, set `"demo_mode": false`, run `build.py`, `qa.py`, `qa_browser.py`. All must pass.
2. **Hosting (Cloudflare Pages, like the other demos):** connect the repo, no build command, output `/`. Add the custom domain in Pages and the DNS records Cloudflare shows. `_headers` noindexes only `*.pages.dev`.
3. Submit a test quote and a test estimate, confirm the FormSubmit activation email, and submit again.
4. Search Console: verify the domain and submit `https://CLIENTDOMAIN/sitemap.xml`.
5. Rich Results Test and PageSpeed Insights (mobile) on home, a service page and the estimate page.
6. Make sure the Google Business Profile name, phone and service areas match the site.
7. If analytics, ad pixels, chat, financing or booking widgets are added: update the Privacy and Cookie policies and add consent blocking where required.

## 3. Instant estimate: how prices are calculated
`(per_ft × height mult × terrain mult + removal_per_ft (if ticked) + per-foot extras) × length + walk gates × walk_gate + double gates × double_gate + flat extras` → never below `minimum_job`, shown as ± `range_pct`, rounded to `round_to`. Heights a material doesn't come in are hidden; extras only show for the materials they list, and disappear with their `service`.

## 4. By-laws, locates and property lines (Ontario)
City pages state each town's fence and pool enclosure rules as published in October 2026: Windsor (Fence By-law 170-2012 heights for front, side/rear and alley fences, corner sight triangle; separate pool enclosure by-law and permit), LaSalle (no permit for a standard fence; pool enclosure permit required; relief process), Tecumseh (fence permit and final inspection; 1.9 m rear/side, 1.22 m front; pool fence rules). Copy says locates are requested before every dig through the `locate_service` in config (Ontario One Call), mentions Ontario's Line Fences Act for boundary disputes and Ontario Land Surveyors for unclear lines. **Re-check the by-law details before launch**, and rewrite them if the template is used elsewhere (`content_cities.py`, `content_services.py`, `pages.py`).

## 5. SEO and technical summary
- `lang="en-CA"`, unique title and description, canonical, Open Graph and Twitter card on every page; favicon set and 1200×630 share image generated in the brand colours.
- Schema: one `HomeAndConstructionBusiness` (`/#business`) on home; `Service` on service and city pages; `BreadcrumbList` matching visible breadcrumbs; `WebSite`, `ItemList`, `ContactPage`, `WebApplication` (estimate). No reviews, ratings, prices or FAQ markup.
- Internal linking: mega menu and footer link every service; each service links its 3 city pages and related services; city pages cross-link and link the hub; the estimate is linked from the nav, footer, hero, asides, CTAs and city pages.
- Performance: no images or video anywhere in the template (every drawing is inline SVG built at compile time), self-hosted fonts, one ~79 KB stylesheet, 17 KB of deferred site JS and 10 KB more on the estimate page. The scroll sequence updates one CSS variable per frame.
- Privacy: no cookies, no analytics, no third-party requests; one sessionStorage flag for the intro.

## 6. URL structure and redirects
Directory-style URLs with trailing slashes; legal pages use `.html`. If a page is renamed after launch, add a Cloudflare redirect rule.

## 7. Page inventory
Full list with canonical URLs: `_build/page-inventory.json`. Home 1, estimate 1, services hub 1, services 13, service × city 39, areas hub 1, city hubs 3, about/FAQ/contact 3, legal 3, thank-you 1 (noindex), 404 1.
