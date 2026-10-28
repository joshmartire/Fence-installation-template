# -*- coding: utf-8 -*-
# Copy for the home page and the standalone pages (about, FAQ, thank-you, legal).
# Items in HTML comments marked CLIENT REVIEW must be confirmed with the client before launch.

GENERAL_FAQS = [
("What areas do you serve?", "We build fences in {cities}. If your property is nearby but outside these communities, contact us and we'll let you know whether we can help."),
("How accurate is the instant fence estimate?", "It's a ballpark range based on the material, height, length, gates and extras you choose. The exact line, slopes, tree roots, rock, access and permits can change the final price, which is confirmed in writing after a site visit."),
("How deep do you set fence posts?", "Deep enough to sit below the frost line, on a gravel base for drainage, with concrete shaped so frost can't lift it. In our heavy clay soil that matters more than any other part of the fence."),
("Do I need a permit for a fence?", "It depends on your municipality and the fence. Some towns require a permit for every fence, others only for pool enclosures, and all of them limit heights. We confirm the rules for your address before building."),
("Who finds out where buried utilities are?", "We request utility locates before every job. The service is free, and no digging starts until the gas, hydro, cable and water lines near the fence line are marked."),
("What if I'm not sure where my property line is?", "Your survey or plot plan is the most reliable guide. If the line is in doubt or the fence is close to it, a survey by an Ontario Land Surveyor settles it before anything is built."),
("Which fence material lasts the longest?", "Aluminum, vinyl, composite and chain link all last decades with little upkeep. A well-built wood fence lasts 15 to 20 years or more with regular staining, and its posts are what usually decide that."),
("How long does a fence installation take?", "Most residential fences are built in one to three days once materials are in. Posts are set first and the concrete is given time to cure before the fence is hung."),
("Can you build on a slope?", "Yes. Panels are stepped down the slope in even increments, or racked to follow the ground where the style allows, so the fence looks intentional instead of uneven."),
("What should I check before hiring any fence company?", "Ask how deep posts are set and how they drain, who requests the utility locates, what the warranty covers, and for proof of liability insurance and WSIB coverage where applicable. Get the material, height, length and price in writing."),
("How do I get started?", "Use the instant fence estimate for a ballpark number, call us, or send your details through our quote form. We'll follow up to book a site visit."),
]

def _and(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def home(cfg, cities, services=None, all_offered=True):
    names = [c["name"] for c in cities]
    city_text = _and(names)
    d = {
        "desc": f"Fence company serving {city_text}: wood, vinyl, ornamental, chain link and composite fences, gates, repairs and an instant estimate.",
        "eyebrow": f"Fence Company · {cfg['region_label']}",
        "lead": "Wood, vinyl, ornamental, chain link and composite fences on posts set below frost, priced in writing and built straight. See a ballpark for your fence in about a minute.",
        # CLIENT REVIEW: confirm these badges describe how the client actually works.
        "tags": ["Written, itemized quotes", "Utility locates before every dig", "Posts set below frost"],
        # 3D yard scroll scene at the top of the home page (assets/js/yard.js). "steps" label the build stages in the HUD;
        # "messages" appear one after another while the fence goes up around the yard; "tags" float over the family,
        # the dog, the shed and the pool and flip to "Protected" when the gate latches.
        "yard": {
            "steps": ["Layout & locates", "Posts in", "Pickets on", "Gate & latch", "Protected"],
            "messages": [
                ("Your family.", "Room for the kids to run, without one eye on the street."),
                ("Your pets.", "The dog stays in. Everyone else's stays out."),
                ("Your belongings.", "Bikes, tools and the patio set, behind a line nobody crosses uninvited."),
                ("Your privacy.", "Six feet of cedar between your backyard and the rest of the block."),
            ],
            "final": ("Protected.", "Private. Secure. Yours."),
            "tags": [("family", "Family"), ("pets", "Pets"), ("belongings", "Belongings"), ("privacy", "Privacy")],
        },
        "statement_eyebrow": "It starts underground.",
        "statement": "Anyone can hang pickets. What keeps a fence straight for twenty winters is the part you never see: post depth, drainage, concrete and spacing. That's where we put the most care.",
        "statement_points": [
            ("Posts below frost", "Holes dug past the frost line, gravel at the base and concrete shaped so heaving clay can't lift it."),
            ("Priced in writing", "Material, height, length, gates and removal listed separately, so you can compare quotes properly."),
            ("Locates every time", "Buried gas, hydro, cable and water lines marked before a single hole is dug."),
        ],
        "services_lead": "Every material, every kind of project and the gates, repairs and care that come after. Pick a service to see what's included and what to ask before you hire.",
        # pinned scroll sequence: one entry per fence type in fence_art.TYPES (types the client doesn't offer are dropped)
        "fence_types": [
            ("wood", {"text": "Cedar pickets on rails between posts set in concrete. Warm, private and easy to repair, and it gets better with a stain.",
                      "specs": [("Lifespan", "15–20+ yrs"), ("Upkeep", "Stain every 2–4 yrs"), ("Ideal for", "Privacy")]}),
            ("vinyl", {"text": "Tongue-and-groove panels with a lattice top, slid into routed posts. Never needs paint, stain or sealing.",
                       "specs": [("Lifespan", "20–30 yrs"), ("Upkeep", "Rinse with a hose"), ("Ideal for", "Privacy, pools")]}),
            ("ornamental", {"text": "Powder-coated aluminum pickets with spear tops and rings. Secure and elegant without blocking the view.",
                            "specs": [("Lifespan", "30+ yrs"), ("Upkeep", "Almost none"), ("Ideal for", "Front yards, pools")]}),
            ("chain-link", {"text": "Galvanized mesh woven onto a braced top rail and stretched tight between terminal posts. Tough and affordable.",
                            "specs": [("Lifespan", "20+ yrs"), ("Upkeep", "Almost none"), ("Ideal for", "Dogs, big yards")]}),
            ("composite", {"text": "Horizontal composite boards stacked between aluminum posts. The look of wood without the rot or the stain.",
                           "specs": [("Lifespan", "25+ yrs"), ("Upkeep", "Rinse occasionally"), ("Ideal for", "Modern privacy")]}),
        ],
        # "know the line" band: (icon, title, text). {locates} = the locate service from config.
        "digline": [
            ("pin", "Property line", "Your fence goes on your side of the line. If the line isn't clear, your survey or plot plan settles it before anything is built."),
            ("flag", "Utility locates", "We request free locates through {locates} before every job, so gas, hydro, cable and water lines are marked first."),
            ("shovel", "By-laws &amp; permits", "Heights, corner sightlines and pool enclosures are set by your town. We check the rules for your address and help with permits."),
        ],
        "process": [
            ("Estimate online", "Use the instant estimate for a ballpark, or call us. No pressure either way."),
            ("Site visit", "We walk the line with you, measure, and talk through materials, gates and grade."),
            ("Quote in writing", "Material, height, length, gates and removal, every line item, to review on your own time."),
            ("Build & walk-through", "Locates, posts, concrete, then the fence and gates, finished with a walk-through of every gate."),
        ],
        "why_lead": "A fence is outside for every storm and every freeze. These are the standards every job runs on, so you always know what you're paying for.",
        # CLIENT REVIEW: confirm these working standards with the client.
        "features": [
            ("Straight answers", "If a repair makes sense, we'll say so. If the fence is done, we'll show you why."),
            ("Written, itemized quotes", "Material, labour, gates, removal and extras listed separately, every time."),
            ("Built for our ground", "Posts set below frost with drainage, because Essex County clay heaves and holds water."),
            ("Clean, square installs", "Lines strung, posts plumb, gates adjusted and the site left tidy."),
        ],
        "faqs": [(q.replace("{cities}", city_text), a.replace("{cities}", city_text)) for q, a in GENERAL_FAQS[1:5]],
    }
    if not all_offered and services:
        low = [x["name"].lower() for x in services]
        d["desc"] = f"Fence company serving {city_text}: " + (", ".join(low[:5]) + " and more." if len(low) > 5 else _and(low) + ".")
        if len(d["desc"]) > 158:
            d["desc"] = f"Fence company serving {city_text}: " + ", ".join(low[:3]) + " and more."
        d["services_lead"] = "Pick a service to see what's included, how the work runs and what to ask before you hire."
        d["lead"] = "Fences and gates on posts set below frost, priced in writing and built straight. See a ballpark for your fence in about a minute."
    return d


def simple_pages(cfg, cities, services, city_text, all_offered=True):
    biz = cfg["business_name"]
    offered = {x["slug"]: x for x in services}
    locates = cfg.get("locate_service") or "the local call-before-you-dig service"

    def links(slugs, limit=None):
        out = [f"[[{sl}|{offered[sl]['name'].lower()}]]" for sl in dict.fromkeys(slugs) if sl in offered]
        return out[:limit] if limit else out
    faqs = [(q.replace("{cities}", city_text), a.replace("{cities}", city_text)) for q, a in GENERAL_FAQS]
    est_on = (cfg.get("estimator") or {}).get("enabled", True)

    def about(here):
        work = _and(links([x["slug"] for x in services], 6) or ["fences and gates"])
        return f"""
<!-- CLIENT REVIEW: replace or extend with the client's real story: founding year, owner names, crew, insurance and WSIB status, material suppliers, warranties, memberships and real project photos. Do not add claims that can't be verified. -->
<h2>Who we are</h2>
<p>{biz} is a fence company serving {city_text}. We build for homeowners, farms and businesses, and our work includes {work}.</p>
<p>A fence looks simple from the street, but whether it stays straight comes down to work nobody sees: where the line is, what's buried under it, how deep the posts go and how they drain. That's why we explain what we're building, put our prices in writing and set every post like it has to last.</p>
<h2>How we work</h2>
<ul>
<li><strong>Locates first.</strong> Utility locates are requested through {locates} before any digging, on every job.</li>
<li><strong>Posts that stay put.</strong> Below frost, on gravel, in concrete shaped to resist heaving.</li>
<li><strong>Clear, written quotes.</strong> Material, height, length, gates, removal and anything that isn't included, spelled out.</li>
<li><strong>Respect for your property.</strong> Gardens protected, the site kept tidy and the old fence hauled away.</li>
</ul>
<h2>Where we work</h2>
<p>We work across {city_text}. Each community has its own lots, soil and fence by-law, which we cover on our pages for [[area:{cities[0]['slug']}|{cities[0]['name']}]], [[area:{cities[1]['slug']}|{cities[1]['name']}]] and [[area:{cities[2]['slug']}|{cities[2]['name']}]].</p>
<h2>Before you hire anyone</h2>
<p>Whoever you choose, ask how deep they set posts and how they drain, who requests the utility locates, what the warranty covers, and for proof of liability insurance and WSIB coverage where applicable. Get the material, height, length and price in writing. Good contractors are glad to answer those questions. When you're ready, {"try our [[estimate|instant fence estimate]] or " if est_on else ""}[[contact|request a quote]].</p>
"""

    def faq(here):
        out = '<h2>Frequently asked questions</h2><div class="faq">'
        for q, a in faqs:
            if "instant fence estimate" in q.lower() and not est_on:
                continue
            out += f'<details><summary>{q}<i aria-hidden="true"></i></summary><div class="faq__a"><p>{a}</p></div></details>'
        l = links(["wood-fences", "vinyl-fences", "privacy-fences", "pool-fences"] + [x["slug"] for x in services], 4) or ["our services"]
        out += '</div><h2>Service-specific questions</h2><p>Each service page answers common questions about that type of work. Start with ' + (
            l[0] if len(l) == 1 else ", ".join(l[:-1]) + " or " + l[-1]) + ', or browse [[services|all services]].</p>'
        return out

    def thanks(here):
        return f"""<h2>We've received your request</h2>
<p>Thanks for contacting {biz}. We'll review your details and follow up by phone or email to book a site visit.</p>
<p>If a fence is down after a storm and you need it secured quickly, call us at <a href="tel:{cfg['phone_e164']}">{cfg['phone_display']}</a>.</p>
<p>While you wait, you can browse [[services|our services]] or read our [[faq|frequently asked questions]].</p>"""

    tool_privacy = ""
    if est_on:
        tool_privacy = """<p><strong>Instant fence estimate.</strong> The instant fence estimate runs entirely in your web browser. The choices you make, such as material, height and length, are not sent to us or to anyone else unless you choose to submit the estimate form.</p>"""

    def privacy(here):
        return f"""
<!-- CLIENT REVIEW / LEGAL REVIEW REQUIRED: This is a draft based on the website as built (quote and estimate forms via {cfg['form_provider_name']}, static hosting, estimate calculated in the browser, no analytics or advertising). Confirm actual data handling, retention periods, email provider and any CRM, financing or other tools before publishing. If analytics, advertising pixels, chat or booking tools are added, this policy must be updated. -->
<p><strong>Effective date:</strong> {cfg['policy_effective_date']}</p>
<p>This Privacy Policy explains how {cfg['legal_name']} ("we", "us") collects, uses and protects personal information through this website and when you contact us about fences, gates or related services. We handle personal information in accordance with applicable Canadian privacy law, including the <em>Personal Information Protection and Electronic Documents Act</em> (PIPEDA).</p>
<h2>Information we collect</h2>
<p><strong>Information you give us.</strong> When you submit our quote form or send us an instant estimate, we collect your name, phone number, email address, property location or address, the service you're interested in and any details you choose to share. Estimate submissions also include the material, height, length, gates, extras and the estimated price range shown to you. If you call or email us, we collect the information you provide in that conversation.</p>
{tool_privacy}
<p><strong>Technical information.</strong> When you visit, our hosting provider's servers may automatically log technical information such as your IP address and browser details for security and operational purposes. We do not use this website to collect analytics, and we do not use advertising or tracking cookies.</p>
<h2>How we use your information</h2>
<ul>
<li>To respond to your inquiry and book a site visit.</li>
<li>To prepare quotes, contracts and work schedules, and to request utility locates and any permits for your project.</li>
<li>To communicate with you about your project before, during and after the work.</li>
<li>To handle warranty questions and to meet legal, accounting and tax obligations.</li>
</ul>
<p>We do not sell your personal information, and we do not use it for unrelated marketing without your consent.</p>
<h2>Who we share it with</h2>
<p>Quote and estimate requests submitted through this website are transmitted through {cfg['form_provider_name']}, a third-party form service that delivers submissions to our email. To complete your project, your address and project details may be shared with the utility locate service, your municipality for permits, and suppliers or subcontractors when needed, and with professional advisors or authorities where required by law. Service providers we use may store or process information outside Canada, including in the United States and Europe, where it may be subject to the laws of those jurisdictions.</p>
<h2>How long we keep it</h2>
<p>We keep personal information only as long as needed for the purposes above, including any period required for legal, tax or warranty reasons, and then securely delete or destroy it.</p>
<h2>How we protect it</h2>
<p>We use reasonable administrative, technical and physical safeguards appropriate to the sensitivity of the information. No method of transmission or storage is completely secure, so we cannot promise absolute security. Please don't include sensitive information, such as financial details, in our website forms.</p>
<h2>Your choices and rights</h2>
<p>You may ask to access the personal information we hold about you, ask us to correct it, or withdraw your consent to our use of it, subject to legal and contractual restrictions. To make a request, contact us using the details below. If you're not satisfied with our response, you may contact the Office of the Privacy Commissioner of Canada.</p>
<h2>Cookies</h2>
<p>This website does not set cookies. See our [[cookies|Cookie Policy]] for details on the limited browser storage the site uses.</p>
<h2>Contact us</h2>
<p>Questions about privacy can be sent to <a href="mailto:{cfg['privacy_contact']}">{cfg['privacy_contact']}</a> or by phone at <a href="tel:{cfg['phone_e164']}">{cfg['phone_display']}</a>.</p>
<h2>Changes to this policy</h2>
<p>We may update this policy from time to time. The effective date above shows when it was last changed.</p>
"""

    def terms(here):
        est = """<h2>Instant fence estimates</h2>
<p>The instant fence estimate is an automated ballpark calculated from the options you choose and our general pricing. It is not a quote or an offer. The actual price is confirmed only in a written quote after a site visit, and can differ because of the exact fence line, survey and permit requirements, buried utilities, soil, rock and tree roots, slopes, access and other factors. Any length worked out by the yard measuring helper is an approximation.</p>
""" if est_on else ""
        return f"""
<!-- CLIENT REVIEW / LEGAL REVIEW REQUIRED: Draft website terms. Project-specific terms (payment schedules, deposits, warranties, property line responsibility, cancellations) belong in the client's written contracts, not here. Have the limitation of liability and governing-law sections reviewed by a lawyer. -->
<p><strong>Effective date:</strong> {cfg['policy_effective_date']}</p>
<p>These Terms and Conditions apply to your use of this website, operated by {cfg['legal_name']} ("we", "us"). By using the website, you agree to these terms.</p>
<h2>Use of this website</h2>
<p>You may use this website for lawful purposes, such as learning about our services and contacting us. You agree not to misuse the website, attempt to interfere with its operation, or submit false or misleading information through our forms.</p>
<h2>Information on this website</h2>
<p>Content on this website is general information about fences, gates and related services. It is not legal, surveying or code-compliance advice for your specific property. Property lines, fence and pool enclosure by-laws and permit requirements vary by municipality and change over time, and buried utilities must always be located before digging. While we try to keep information accurate and current, we don't warrant that it is complete or error-free.</p>
{est}<h2>Quotes and project agreements</h2>
<p>Nothing on this website is an offer, quote or contract. Pricing, scope, schedules, payment terms, warranties and cancellation terms for any project are set out only in a written quote or contract provided to you. If there is a conflict between this website and your written contract, the contract applies.</p>
<h2>Intellectual property</h2>
<p>The text, design, graphics and logos on this website belong to us or our licensors. You may view and print pages for personal, non-commercial use, but you may not copy, reproduce or republish website content for commercial purposes without our written permission.</p>
<h2>Third-party links and services</h2>
<p>This website may link to third-party websites or use third-party services, such as our form provider and the utility locate service. We aren't responsible for the content, terms or privacy practices of those third parties.</p>
<h2>Limitation of liability</h2>
<p>To the extent permitted by law, we are not liable for any indirect or consequential loss arising from your use of this website or reliance on its general information or automated estimates. Nothing in these terms limits any rights you have under applicable consumer protection law.</p>
<h2>Governing law</h2>
<p>These terms are governed by the laws of the Province of {cfg['legal_jurisdiction']} and the federal laws of Canada that apply there.</p>
<h2>Changes and contact</h2>
<p>We may update these terms from time to time. Questions can be sent to <a href="mailto:{cfg['email']}">{cfg['email']}</a>. Our [[privacy|Privacy Policy]] explains how we handle personal information.</p>
"""

    def cookies(here):
        return f"""
<!-- CLIENT REVIEW: accurate for the template as built (no cookies, no analytics, no pixels; the instant estimate runs in the browser). If Google Analytics, Meta Pixel, Google Ads tags, chat widgets, financing or booking embeds are added, update this page and add a consent mechanism that blocks non-essential tags until the visitor agrees, where required. -->
<p><strong>Effective date:</strong> {cfg['policy_effective_date']}</p>
<h2>Does this website use cookies?</h2>
<p>No. This website does not set cookies, and it does not use analytics, advertising pixels or other tracking technologies.</p>
<h2>Browser storage we use</h2>
<p>The website uses your browser's <em>session storage</em> to remember that the opening animation has already played during your visit, so it isn't shown again on every page. This stores a single value with no personal information, isn't shared with us or anyone else, and is cleared automatically when you close your browser tab. Because it's needed only to provide the website as you'd expect, it doesn't require consent.</p>
<h2>Third-party services</h2>
<p>When you submit one of our forms, your browser sends it to {cfg['form_provider_name']}, which delivers it to us by email. That service may display its own pages, such as a spam-protection check, and may use cookies on its own domain under its own policies. Our hosting provider may log technical information such as IP addresses for security purposes, as explained in our [[privacy|Privacy Policy]].</p>
<h2>Managing storage</h2>
<p>You can clear or block site data at any time through your browser settings. The website will continue to work, although the opening animation may play again.</p>
<h2>Changes</h2>
<p>If we add tools that use cookies or similar technologies, we will update this policy and, where required, ask for your consent before those tools run.</p>
"""

    return {
        "about": dict(title=f"About {biz}", desc=f"{biz} is a fence company serving {city_text}. Learn how we plan, quote, dig, set posts and build fences that stay straight.", eyebrow="About us", h1="About Us", lead="A fence company built around straight answers, written prices and posts that stay where we put them.", inner=about, active="about"),
        "faq": dict(title="Fence FAQ", desc=f"Answers about fence materials, post depth, permits, utility locates, property lines, slopes and hiring a fence company in {city_text}.", eyebrow="FAQ", h1="Frequently Asked Questions", lead="Straight answers about fences and how we build them, before you commit to anything.", inner=faq, active="faq"),
        "thanks": dict(title="Thank You", desc="Your request has been sent.", eyebrow="Request sent", h1="Thank You", lead="Your details are on their way to us.", inner=thanks, noindex=True, aside=False, cta=False, hero_ctas=False),
        "privacy": dict(title="Privacy Policy", desc=f"How {biz} collects, uses and protects personal information submitted through this website, its forms and the instant fence estimate.", eyebrow="Legal", h1="Privacy Policy", lead="How we collect, use and protect your personal information.", inner=privacy, mark="doc", aside=False, cta=False, hero_ctas=False),
        "terms": dict(title="Terms and Conditions", desc=f"Terms and conditions for using the {biz} website and its instant fence estimate.", eyebrow="Legal", h1="Terms and Conditions", lead="The terms that apply when you use this website.", inner=terms, mark="doc", aside=False, cta=False, hero_ctas=False),
        "cookies": dict(title="Cookie Policy", desc=f"How the {biz} website uses cookies and browser storage.", eyebrow="Legal", h1="Cookie Policy", lead="What this website stores in your browser, and what it doesn't.", inner=cookies, mark="doc", aside=False, cta=False, hero_ctas=False),
    }
