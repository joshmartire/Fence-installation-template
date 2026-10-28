# -*- coding: utf-8 -*-
# Fence services. Each entry becomes a service page (500-600 words of main content together with its
# COSTS entry and FAQs) plus one page per city in content_cities.py.
#
# Tokens: {biz} = business name, {phone} = phone number, {locates} = the utility locate service from
# site.config.json ("locate_service"), [[slug|anchor text]] = link to another service (or [[contact|...]],
# [[estimate|...]], [[area:windsor|...]]). Links to services the client does not offer become plain text
# and are listed in _build/removed-service-mentions.txt for rewording.
#
# "cities" holds one short paragraph per city slug. It must be genuinely about that town, not a
# find-and-replace of the city name.
#
# Facts used in the copy (Ontario, checked October 2026): utility locates must be requested before digging
# and are free through Ontario One Call; Ontario's Line Fences Act sets out a process for boundary fence
# disputes between neighbours; each municipality has its own fence and pool enclosure by-laws (see
# content_cities.py). Essex County soils are mostly heavy clay, which holds water and heaves when it freezes.
# Re-check these if the template is used outside Ontario.

SERVICES = [
# ------------------------------------------------------------------ FENCE TYPES
{
"slug": "wood-fences",
"name": "Wood Fences",
"cat": "fences",
"icon": "wood",
"short": "Cedar and pressure-treated wood fences, from classic dog-ear privacy to board-on-board and shadowbox, built on posts set to last.",
"title": "Wood Fence Installation | Cedar & Pressure-Treated",
"desc": "Cedar and pressure-treated wood fence installation: privacy, board-on-board, shadowbox and picket styles on properly set posts, with a written quote.",
"h1": "Wood Fences",
"lead": "Real wood, built right. Cedar or pressure-treated pickets on posts that are set deep, drained and plumb, so the fence still stands straight in ten years.",
"body": """
<p>A wood fence is still the most popular way to close in a backyard, and for good reason: it's warm, private, easy to repair and can be built in almost any style. What separates a wood fence that lasts from one that leans after three winters isn't the pickets, though. It's the posts. {biz} builds wood fences from the ground up, starting with what's under the grass.</p>
<h2>What's included</h2>
<ul>
<li><strong>Layout and locates</strong> — we confirm the line with you, request free utility locates through {locates} and mark every post before a shovel goes in.</li>
<li><strong>Posts set for our soil</strong> — holes dug below frost, gravel at the base for drainage, and concrete shaped so frost has nothing to grab.</li>
<li><strong>Rails and framing</strong> — top, middle and bottom rails fastened with exterior-rated screws or ring-shank nails, not staples.</li>
<li><strong>Your choice of style</strong> — dog-ear privacy, board-on-board, shadowbox, picket or horizontal, in cedar or pressure-treated lumber.</li>
<li><strong>Gates that close</strong> — framed and braced so they don't sag, with heavy hinges and a latch that lines up.</li>
<li><strong>Clean-up</strong> — dirt, offcuts and the old fence (if we're replacing one) hauled away.</li>
</ul>
<h2>How the job runs</h2>
<ol>
<li><strong>Site visit.</strong> We walk the line, talk about style and height, and check grade changes, trees and gates.</li>
<li><strong>Written quote.</strong> Material, height, length, gates, removal and any extras listed separately.</li>
<li><strong>Posts first.</strong> Posts are set and the concrete is given time to cure before the fence is hung.</li>
<li><strong>Build and walk-through.</strong> Rails, pickets, gates and caps go on, and we check every gate with you.</li>
</ol>
<h2>Cedar or pressure-treated?</h2>
<p>Cedar is lighter, more stable and naturally resists rot, and it weathers to a soft grey if you leave it alone. Pressure-treated lumber costs less and is very durable in the ground, but it moves more as it dries. Either way, a [[fence-staining|stain and seal]] once it has dried out adds years. Comparing materials? Price wood against [[vinyl-fences|vinyl]] in the [[estimate|instant fence estimate]].</p>
""",
"faqs": [
("How long does a wood fence last?", "A well-built cedar or pressure-treated fence typically lasts 15 to 20 years, and longer with regular staining. Posts are usually what fails first, which is why we put the most care into setting them."),
("Which side of the fence faces out?", "Traditionally the finished side faces the neighbour and the street, but it's your choice. Board-on-board and shadowbox styles look finished from both sides."),
("When can I stain a new wood fence?", "New lumber needs to dry first. Pressure-treated wood often needs a few months; kiln-dried cedar can be stained sooner. We'll tell you when yours is ready."),
("Can you build a wood fence in winter?", "Yes, as long as the ground can be dug. Frozen topsoil slows the digging, and concrete needs protection from freezing while it cures, so winter jobs can take a little longer. Spring and fall are the most popular seasons, so booking early helps."),
],
"related": ["privacy-fences", "fence-staining", "custom-gates"],
"cities": {
"windsor": "Many Windsor backyards back onto a public alley, which means two jobs in one: a privacy fence along the side lot lines and a gated section on the alley side for garage or trash access. Windsor's by-law allows taller fences along an alley than in the front yard, and we build the alley gate with a frame and hardware that can handle daily use.",
"lasalle": "In LaSalle's subdivisions, most wood fences sit on a shared lot line with two or three neighbours, and many lots have a rear-yard drainage swale running along the back. We set posts so the fence doesn't block that swale and leave a consistent gap at the bottom of the pickets so water can move through.",
"tecumseh": "Closer to Lake St. Clair, a six-foot solid wood fence catches a lot of wind. On exposed Tecumseh lots we tighten the post spacing, use heavier posts at gates and corners, or suggest a board-on-board or shadowbox style that lets some wind through while still blocking the view."
},
},
{
"slug": "vinyl-fences",
"name": "Vinyl Fences",
"cat": "fences",
"icon": "vinyl",
"short": "Low-maintenance vinyl privacy, semi-privacy and picket fences that never need paint, installed straight and level on a solid post layout.",
"title": "Vinyl Fence Installation | Privacy & Picket",
"desc": "Vinyl fence installation: privacy, semi-privacy, lattice-top and picket styles that never need paint, installed level with properly set posts.",
"h1": "Vinyl Fences",
"lead": "No paint, no stain, no splinters. Vinyl fences look clean for years with nothing more than a rinse, as long as they're installed level and true.",
"body": """
<p>Vinyl (PVC) fencing is built for people who would rather enjoy their yard than maintain it. It doesn't rot, it doesn't need painting and a hose takes care of most dirt. The catch is that vinyl is a precise system: posts have to be set at exact spacing, plumb and at the right height, or the panels won't sit properly. {biz} installs vinyl fences the way the manufacturer intends, so they look as sharp in year ten as on day one.</p>
<h2>What's included</h2>
<ul>
<li><strong>Exact post layout</strong> — panel widths are fixed, so we measure and string the line before digging, then adjust spacing at corners and ends.</li>
<li><strong>Posts set in concrete</strong> — with aluminum stiffeners in gate and end posts where the system calls for them.</li>
<li><strong>Panels and rails</strong> — privacy, semi-privacy, lattice-top, picket or horizontal styles in white, tan, grey or woodgrain finishes.</li>
<li><strong>Stepping on slopes</strong> — panels stepped evenly down a grade, or racked where the style allows.</li>
<li><strong>Gates</strong> — vinyl gates reinforced with metal framing and fitted with self-closing hinges where you need them.</li>
<li><strong>Caps and clean-up</strong> — post caps fastened, debris removed and the job site left tidy.</li>
</ul>
<h2>How the job runs</h2>
<ol>
<li><strong>Site visit.</strong> We measure, check the grade and talk through styles, colours and gate locations.</li>
<li><strong>Written quote.</strong> Panels, posts, gates, hardware and removal listed separately.</li>
<li><strong>Layout and posts.</strong> Locates confirmed, the line strung and posts set to height.</li>
<li><strong>Panels and gates.</strong> Rails and panels installed, gates hung and adjusted, caps on.</li>
</ol>
<h2>Is vinyl right for you?</h2>
<p>Vinyl suits privacy fences, pool areas and anyone who doesn't want weekend maintenance. It costs more up front than [[wood-fences|wood]], but there's no staining over its life. For a natural look without the upkeep, compare it with [[composite-fences|composite]]. See both side by side in the [[estimate|instant fence estimate]].</p>
""",
"faqs": [
("Does vinyl fencing crack in the cold?", "Quality vinyl is formulated for Canadian winters. It gets stiffer in deep cold, so the main risk is a hard impact, like a snowblower or a thrown chunk of ice, rather than the temperature itself."),
("How do I clean a vinyl fence?", "A garden hose handles most dirt. For green or grey film, a soft brush with mild soap and water works. Avoid pressure washers at close range and harsh solvents."),
("Can a vinyl fence go on a slope?", "Yes. Most vinyl panels are stepped down the slope in even increments. Some picket and semi-privacy styles can be racked to follow the grade."),
("Will a vinyl fence turn yellow?", "Quality vinyl contains UV inhibitors that keep it from yellowing or chalking in the sun. Cheap, thin vinyl is more likely to discolour, which is one reason we tell you the brand and profile thickness in every quote."),
],
"related": ["privacy-fences", "pool-fences", "composite-fences"],
"cities": {
"windsor": "Vinyl has become a favourite in Windsor's newer east-end and south-end neighbourhoods, where homeowners want a crisp privacy fence that matches vinyl siding and doesn't need staining. In older areas with narrow side yards, we plan the panel layout around the house and any gas meter or downspout so the last panel isn't an awkward sliver.",
"lasalle": "LaSalle's backyard pools make vinyl a common choice for pool enclosures. Vinyl privacy panels have no footholds on the outside, and paired with self-closing, self-latching gates they suit the Town's pool enclosure permit requirements, which we confirm before the job starts.",
"tecumseh": "On wind-exposed Tecumseh lots near the lake, solid vinyl panels take a lot of load. We use the manufacturer's reinforced posts and stiffeners where recommended, and suggest semi-privacy styles with small gaps where full privacy isn't essential."
},
},
{
"slug": "ornamental-fences",
"name": "Ornamental Fences",
"cat": "fences",
"icon": "ornamental",
"short": "Aluminum and steel ornamental fences with clean pickets and finials, for front yards, pools and properties that want security without hiding the view.",
"title": "Ornamental Aluminum & Steel Fence Installation",
"desc": "Ornamental aluminum and steel fence installation for front yards, pools and properties: powder-coated pickets, finials and matching gates.",
"h1": "Ornamental Fences",
"lead": "The look of wrought iron without the rust. Powder-coated aluminum and steel fences that define your property, protect your pool and keep the view open.",
"body": """
<p>Ornamental fencing does something wood and vinyl can't: it marks a boundary and adds security while keeping sightlines open. That makes it the go-to choice for front yards, corner lots, pool enclosures and homes with something worth looking at. {biz} installs powder-coated aluminum and steel ornamental fences that look like classic wrought iron but don't need sanding and repainting every few years.</p>
<h2>What's included</h2>
<ul>
<li><strong>Aluminum or steel</strong> — aluminum for rust-free, low-maintenance residential fencing; steel where extra strength or security is needed.</li>
<li><strong>Styles and tops</strong> — flat-top, spear-top, staggered pickets, rings and scrolls, in black, bronze or white.</li>
<li><strong>Pool-ready spacing</strong> — narrow picket spacing and heights that suit pool enclosure rules, with no horizontal footholds on the outside.</li>
<li><strong>Racked on slopes</strong> — panels racked to follow the grade smoothly instead of stair-stepping.</li>
<li><strong>Matching gates</strong> — single walk gates and double drive gates, with self-closing hinges and magnetic latches available.</li>
<li><strong>Posts in concrete</strong> — set plumb, at the exact panel width, with caps fastened.</li>
</ul>
<h2>How the job runs</h2>
<ol>
<li><strong>Site visit.</strong> We measure the run, check slopes and talk through style, height and gates.</li>
<li><strong>Written quote.</strong> Panels, posts, gates and hardware itemized, with lead time for the material.</li>
<li><strong>Posts and panels.</strong> Locates confirmed, posts set at panel spacing and panels attached as the line goes.</li>
<li><strong>Gates and finish.</strong> Gates hung and adjusted to swing and latch properly, caps and finials checked.</li>
</ol>
<h2>Where ornamental fences make sense</h2>
<p>Front yards and corner lots are often limited to lower fences, and many municipalities allow open designs closer to corners because they don't block drivers' sightlines. Because it's strong, open and easy to keep clean, ornamental fencing is also a popular [[pool-fences|pool fence]] and pairs well with [[custom-gates|custom driveway gates]]. Price it out in the [[estimate|instant fence estimate]].</p>
""",
"faqs": [
("Is aluminum fencing strong enough?", "For most homes, yes. Residential aluminum is strong enough for yards, pools and pets. Commercial-grade aluminum or steel is used where extra strength or security is needed."),
("Will an aluminum fence rust?", "No. Aluminum doesn't rust. Steel ornamental fencing is galvanized and powder-coated to resist rust, and any scratches should be touched up."),
("Can my dog get through an ornamental fence?", "Small dogs may fit between standard pickets. Puppy-picket panels add extra pickets along the bottom to close those gaps."),
("Can an ornamental fence follow a slope?", "Yes. Aluminum panels can be racked so the rails run parallel to the ground while the pickets stay vertical, which looks much cleaner than stepping on a gentle slope. On steeper grades, panels are stepped instead, and we show you how it will look before ordering."),
],
"related": ["pool-fences", "custom-gates", "commercial-fences"],
"cities": {
"windsor": "Windsor's older homes in Walkerville and along the riverfront often call for a front-yard fence with some character. Black aluminum with spear or flat tops suits brick houses, and because Windsor limits front-yard fences to a lower height and keeps corner sightlines clear, an open picket design is often the most practical way to enclose a front yard.",
"lasalle": "In LaSalle, ornamental aluminum is a common choice around pools and along rear lot lines that face parks, trails or water, where homeowners want a secure enclosure without losing the view. We confirm pool spacing and gate hardware against the Town's pool enclosure requirements before ordering.",
"tecumseh": "Ornamental fencing works well for Tecumseh homes on larger lots and near the water, where an open design lets wind pass straight through. On the rural side of town, we also use it to frame front yards and driveway entrances on properties that use farm fence elsewhere."
},
},
{
"slug": "chain-link-fences",
"name": "Chain Link Fences",
"cat": "fences",
"icon": "chainlink",
"short": "Galvanized and black vinyl-coated chain link for yards, dogs, side yards and commercial lots: strong, affordable and quick to install.",
"title": "Chain Link Fence Installation | Galvanized & Black",
"desc": "Chain link fence installation: galvanized and black vinyl-coated fencing for yards, dog runs and commercial properties, with gates and privacy slats.",
"h1": "Chain Link Fences",
"lead": "The hardest-working fence there is. Galvanized or black vinyl-coated chain link, stretched tight on a proper frame so it stays that way.",
"body": """
<p>Chain link is the most cost-effective way to fence a large area, and it's nearly indestructible when it's installed properly. The difference between a tight, straight chain link fence and a saggy one comes down to the frame: solid terminal posts, a properly braced top rail and fabric stretched with the right tension. {biz} builds chain link fences for backyards, dog runs, side yards and commercial lots.</p>
<h2>What's included</h2>
<ul>
<li><strong>Terminal and line posts</strong> — heavier posts at ends, corners and gates, line posts at even spacing, all set in concrete.</li>
<li><strong>Top rail and bracing</strong> — top rail through loop caps, with bottom tension wire to keep the fabric from being pushed out.</li>
<li><strong>Fabric stretched tight</strong> — galvanized or black vinyl-coated mesh, pulled with a stretcher bar and fastened with tension bands.</li>
<li><strong>Heights from 4 to 8 feet</strong> — residential heights for yards and dogs, taller heights for commercial and security fencing.</li>
<li><strong>Privacy options</strong> — slats woven into the mesh for screening without replacing the fence.</li>
<li><strong>Gates</strong> — walk gates, double drive gates and rolling gates, with latches that can take a padlock.</li>
</ul>
<h2>How the job runs</h2>
<ol>
<li><strong>Site visit.</strong> We measure the run, mark gates and check for grade changes and obstacles.</li>
<li><strong>Written quote.</strong> Height, fabric type, gates, slats and removal listed separately.</li>
<li><strong>Posts and frame.</strong> Locates confirmed, posts set and cured, top rail and fittings installed.</li>
<li><strong>Fabric and gates.</strong> Mesh stretched and tied, gates hung and latches adjusted.</li>
</ol>
<h2>Galvanized or black?</h2>
<p>Galvanized chain link is the most affordable option and lasts for decades. Black vinyl-coated chain link costs more but disappears into the landscape and looks far better from the house. For larger properties, see [[farm-fences|farm and rural fencing]] and [[commercial-fences|commercial fencing]], or price a run in the [[estimate|instant fence estimate]].</p>
""",
"faqs": [
("Is chain link good for dogs?", "Yes. It's strong and hard to chew through. For diggers, we can add a bottom tension wire close to the ground or bury a strip of mesh along the line."),
("Can I add privacy to a chain link fence?", "Yes. Privacy slats woven into the mesh block most of the view. They add wind load, so we check that the posts and spacing can handle it."),
("How long does chain link last?", "Galvanized chain link commonly lasts 20 years or more. Black vinyl-coated fabric adds another layer of protection against rust."),
("Can chain link go on a slope or uneven ground?", "Yes. Chain link fabric follows the grade naturally, and posts are set to keep the top rail smooth while the bottom stays close to the ground. On uneven ground, we trim or fill under the fence so pets can't squeeze underneath."),
],
"related": ["commercial-fences", "farm-fences", "custom-gates"],
"cities": {
"windsor": "Chain link is everywhere in Windsor's older neighbourhoods, and much of it is 40 or 50 years old: rusted fabric, missing top rail and posts heaved by decades of frost. We replace it with new galvanized or black vinyl-coated fence, often reusing the same line, and add privacy slats for homeowners who want a little screening from the alley.",
"lasalle": "LaSalle homeowners usually choose black vinyl-coated chain link for side yards, dog runs and fences along open space, where it blends into the landscape far better than galvanized. On lots with drainage easements, we keep posts clear of the swale so water keeps moving.",
"tecumseh": "From commercial lots in the Oldcastle industrial area to dog runs on rural Tecumseh properties, chain link covers a lot of ground here. On longer rural runs we use heavier terminal posts and bracing so the fabric stays tight across wide-open spans."
},
},
{
"slug": "composite-fences",
"name": "Composite Fences",
"cat": "fences",
"icon": "composite",
"short": "Composite and modern horizontal fences that look like wood without rotting, warping or needing stain, on aluminum or steel posts.",
"title": "Composite & Horizontal Fence Installation",
"desc": "Composite and modern horizontal fence installation: the look of wood without the rot, warping or staining, built on aluminum or steel posts.",
"h1": "Composite Fences",
"lead": "Wood grain without the wood problems. Composite boards in clean horizontal lines that won't rot, warp or need a stain, built on a metal frame.",
"body": """
<p>Composite fencing combines wood fibres and plastic into boards that look like real wood and hold their colour, without splintering, rotting or warping. Paired with aluminum or steel posts, it gives you a modern horizontal fence that stays straight and needs almost no upkeep. {biz} installs composite fence systems for homeowners who want a fence that looks sharp for years and don't want to maintain it.</p>
<h2>What's included</h2>
<ul>
<li><strong>Metal posts</strong> — aluminum or steel posts set in concrete, so the frame never rots or twists.</li>
<li><strong>Composite boards</strong> — capped composite boards that resist fading and staining, in a range of wood tones and greys.</li>
<li><strong>Horizontal or vertical</strong> — modern horizontal boards, vertical privacy boards or mixed designs with metal accents.</li>
<li><strong>Clean finishing</strong> — top caps and trim that hide board ends and fasteners for a finished look on both sides.</li>
<li><strong>Matching gates</strong> — framed gates in the same boards, with hardware sized for the extra weight.</li>
<li><strong>Precise layout</strong> — board lengths are fixed, so post spacing is planned around them to avoid waste and awkward cuts.</li>
</ul>
<h2>How the job runs</h2>
<ol>
<li><strong>Site visit and samples.</strong> We measure, check the grade and bring colour samples to see against your house.</li>
<li><strong>Written quote.</strong> Boards, posts, trim, gates and removal itemized, with material lead time.</li>
<li><strong>Posts.</strong> Locates confirmed, posts set to exact spacing and height.</li>
<li><strong>Boards and trim.</strong> Boards stacked and secured, caps and trim installed, gates hung and adjusted.</li>
</ol>
<h2>Composite vs. wood vs. vinyl</h2>
<p>Composite costs more up front than [[wood-fences|wood]] and most [[vinyl-fences|vinyl]], but it has the most natural look of the low-maintenance options and holds up well to sun and moisture. It's a strong choice for [[privacy-fences|privacy fences]] around patios and pools. Compare all three in the [[estimate|instant fence estimate]].</p>
""",
"faqs": [
("Does composite fencing fade?", "Capped composite boards resist fading much better than wood, though all materials soften slightly in colour over the first months in the sun. They don't need stain to stay that way."),
("Is composite fencing heavy?", "Yes, it's heavier than wood. That's why we use metal posts and set them deep, and why gates are framed and hung on heavier hardware."),
("Can composite fence go on a slope?", "Horizontal composite fences are stepped down the slope section by section, which suits the clean, level lines of the style."),
("How long does a composite fence last?", "Capped composite boards on metal posts commonly last 25 years or more. Because nothing in the frame can rot, the fence stays straight, and the boards only need an occasional rinse to look close to new."),
],
"related": ["privacy-fences", "vinyl-fences", "custom-gates"],
"cities": {
"windsor": "Windsor homeowners renovating older houses often want a modern horizontal fence to go with a new deck or patio. In tight backyards close to the neighbours, we plan board heights and post spacing so the fence reads as one clean line, and make sure it stays within the city's height limit for side and rear yards.",
"lasalle": "Composite is popular in LaSalle's newer custom-home neighbourhoods, where homeowners want a fence that matches a composite deck and won't need staining. Metal posts set in our wet clay soil are a big advantage here, because they don't rot at the ground line the way wood posts can.",
"tecumseh": "In Tecumseh, composite fences often go up around patios and pools on larger lots. Horizontal boards with small gaps let some wind pass through on exposed lots near the lake, and metal posts handle the extra load better than wood."
},
},
# ------------------------------------------------------------------ PROJECTS
{
"slug": "privacy-fences",
"name": "Privacy Fences",
"cat": "projects",
"icon": "privacy",
"short": "Full-height privacy fences in wood, vinyl and composite, built to block the view, cut the noise and stand up to wind.",
"title": "Privacy Fence Installation | Wood, Vinyl & Composite",
"desc": "Privacy fence installation in wood, vinyl and composite: solid, board-on-board and lattice-top designs built to the allowed height and to handle wind.",
"h1": "Privacy Fences",
"lead": "Your backyard, not the neighbourhood's. Full-height privacy fences that block the view and the wind, built to the height your town allows.",
"body": """
<p>A privacy fence turns a backyard into a room. It blocks the view from neighbours and the street, softens traffic noise, keeps kids and pets in and gives you somewhere to relax without an audience. Because a solid fence acts like a sail in the wind, it has to be built stronger than an open fence. {biz} designs privacy fences around how much privacy you want, what your by-law allows and how exposed your yard is.</p>
<h2>What's included</h2>
<ul>
<li><strong>Height planning</strong> — the tallest height your municipality allows in each part of the yard, with lower sections where the rules require them.</li>
<li><strong>Material choice</strong> — [[wood-fences|wood]], [[vinyl-fences|vinyl]] or [[composite-fences|composite]], compared side by side.</li>
<li><strong>Privacy level</strong> — fully solid, board-on-board, shadowbox or lattice-top designs, depending on how much light and air you want through.</li>
<li><strong>Wind-ready posts</strong> — tighter spacing and deeper footings on exposed lots, heavier posts at gates and corners.</li>
<li><strong>Grade handling</strong> — stepped sections and gap control at the bottom so the fence looks level and drainage still works.</li>
<li><strong>Gates and access</strong> — walk gates for the side yard and wider gates for equipment or a trailer.</li>
</ul>
<h2>How the job runs</h2>
<ol>
<li><strong>Site visit.</strong> We look at sightlines from your patio and windows, slopes, trees and where gates belong.</li>
<li><strong>Written quote.</strong> Material, height, length, gates and removal listed separately.</li>
<li><strong>Posts and frame.</strong> Locates confirmed, posts set and the frame built.</li>
<li><strong>Infill and gates.</strong> Pickets, panels or boards installed, gates hung and adjusted.</li>
</ol>
<h2>Talk to the neighbours first</h2>
<p>Most privacy fences sit on or near a property line, so it's worth talking with your neighbours before work starts, about the line, the style and which side faces them. If the line is in doubt, a survey settles it. Ontario's Line Fences Act also sets out a process when neighbours can't agree on a shared boundary fence. For a quick number, try the [[estimate|instant fence estimate]].</p>
""",
"faqs": [
("How tall can a privacy fence be?", "It depends on your municipality and where the fence is on your lot. Rear and side yards usually allow around six to seven feet, while front yards are limited to about four. We confirm the current rules for your address."),
("Do I need my neighbour's permission?", "If the fence is entirely on your property, you generally don't need permission, but it's good practice to talk first. Shared boundary fences are a conversation, and the Line Fences Act covers disputes."),
("What's the most private fence style?", "A solid privacy fence or board-on-board design blocks the view completely. Shadowbox and lattice-top styles trade a little privacy for more airflow and light."),
("How do I keep a privacy fence from blowing over?", "Set posts deep, below frost, in concrete, and use heavier posts at gates, corners and ends. On very exposed lots, closer post spacing or a design with small gaps between boards lets some wind through and takes load off the posts."),
],
"related": ["wood-fences", "vinyl-fences", "composite-fences"],
"cities": {
"windsor": "Windsor lots are often narrow, with houses close together and rear alleys behind them, so a privacy fence makes a big difference. The city allows taller fences in side and rear yards, and taller still where a yard backs onto an alley or public walkway, while front yards and corner sightlines are kept low. We plan each section's height around those rules.",
"lasalle": "LaSalle's subdivision backyards back directly onto each other, and a privacy fence is usually the first project after a new home closes. We help neighbours coordinate shared sections and keep the bottom of the fence above rear-yard drainage swales so it doesn't trap water.",
"tecumseh": "Tecumseh's fence by-law allows fences up to about 1.9 metres in rear and side yards and requires a fence permit, which we help you arrange. On lake-exposed lots, we strengthen the post layout for wind or recommend designs that let some air through."
},
},
{
"slug": "pool-fences",
"name": "Pool Fences",
"cat": "projects",
"icon": "pool",
"short": "Pool enclosures in aluminum, vinyl, glass-look and wood, with self-closing, self-latching gates built to local pool enclosure rules.",
"title": "Pool Fence & Pool Enclosure Installation",
"desc": "Pool fence and pool enclosure installation: aluminum, vinyl and wood enclosures with self-closing, self-latching gates, built to local pool by-laws.",
"h1": "Pool Fences",
"lead": "A pool fence has one job that matters more than looks: keeping small children out. We build enclosures that meet the rules and still look good.",
"body": """
<p>Pool fences are the one kind of fence where the rules are strict and for good reason. Most Ontario municipalities require a pool enclosure permit, a minimum height, limited gaps and footholds, and gates that close and latch by themselves. {biz} builds pool enclosures that meet your municipality's requirements, and we coordinate the details with your pool installer so the permit and inspection go smoothly.</p>
<h2>What's included</h2>
<ul>
<li><strong>Permit-ready layout</strong> — a site plan showing the pool, the enclosure and the gates, for your pool enclosure permit application.</li>
<li><strong>Compliant heights and gaps</strong> — fence height, picket spacing and ground clearance built to the local by-law.</li>
<li><strong>No climbable footholds</strong> — rails on the pool side or designs without horizontal footholds on the outside.</li>
<li><strong>Self-closing, self-latching gates</strong> — hinges and latches that close and lock every time, with latches mounted out of a child's reach.</li>
<li><strong>Material options</strong> — [[ornamental-fences|ornamental aluminum]], [[vinyl-fences|vinyl]], [[wood-fences|wood]] or a combination.</li>
<li><strong>Inspection-ready finish</strong> — everything checked against the permit before the town's inspection.</li>
</ul>
<h2>How the job runs</h2>
<ol>
<li><strong>Site visit.</strong> We measure around the pool, check the house walls and doors that form part of the enclosure, and plan gate locations.</li>
<li><strong>Written quote and site plan.</strong> Materials, gates, hardware and the drawing for your permit.</li>
<li><strong>Build.</strong> Locates confirmed, posts set, panels installed and gates hung.</li>
<li><strong>Gate test.</strong> Every gate is tested to close and latch from any position before we leave.</li>
</ol>
<h2>Timing with your pool build</h2>
<p>Pools usually can't be filled until the enclosure has passed inspection, so the fence often sets the schedule. We work with your pool installer on access for equipment, then close the enclosure as soon as the heavy work is done. Need a temporary fence during construction? Ask us. For the rest of the yard, see [[privacy-fences|privacy fences]] and [[custom-gates|gates]].</p>
""",
"faqs": [
("Do I need a permit for a pool fence?", "In most Ontario municipalities, yes. A pool enclosure permit is usually required before the pool is built or filled, followed by an inspection. We prepare the site plan and confirm the current rules for your address."),
("Can my house wall be part of the pool enclosure?", "Often, yes, but doors and windows that open onto the pool area may need alarms, self-closing hardware or other measures. Rules vary by municipality, and we check them before building."),
("What makes a gate pool-compliant?", "It must close and latch by itself from any open position, with the latch mounted high or on the pool side where small children can't reach it. Many by-laws also require gates to swing away from the pool."),
("How tall does a pool fence need to be?", "It depends on your municipality. Many Ontario towns require at least four feet, and some ask for more. Gaps under and between pickets are also limited. We check the current by-law for your address before designing the enclosure."),
],
"related": ["ornamental-fences", "vinyl-fences", "custom-gates"],
"cities": {
"windsor": "Windsor regulates pool enclosures under a separate by-law from its general fence rules, and a pool enclosure permit is needed before the pool goes in. Many Windsor backyards are tight, so the enclosure often uses the house wall or a detached garage as one side, and we plan doors, windows and gates around that.",
"lasalle": "In LaSalle, a regular fence doesn't need a permit, but a swimming pool does, and the application includes a site plan and your fence enclosure details. We prepare the drawing, build the enclosure to the Town's requirements and coordinate with your pool installer on timing.",
"tecumseh": "Tecumseh requires pool fences to be at least four feet high, not climbable and fitted with spring-loaded, self-latching gates on the pool side, and fences need a permit and a final inspection. We handle the layout and build so the inspection goes smoothly."
},
},
{
"slug": "farm-fences",
"name": "Farm & Rural Fences",
"cat": "projects",
"icon": "farm",
"short": "Post-and-rail, split rail, field fence and livestock fencing for rural properties, acreages and hobby farms, with gates for equipment.",
"title": "Farm & Rural Fence Installation | Post & Rail",
"desc": "Farm and rural fence installation: post-and-rail, split rail, field fence and livestock fencing for acreages and hobby farms, with equipment gates.",
"h1": "Farm & Rural Fences",
"lead": "Long runs, open ground and animals that lean on everything. Rural fences built with braced corners and posts that stay put.",
"body": """
<p>Rural fencing is a different job from a backyard fence. The runs are long, the ground changes, and the fence has to hold livestock, mark a boundary or keep deer out of a garden for decades with little attention. Most of a rural fence's strength is in its corners and ends: if the bracing is right, the line stays tight. {biz} builds rural fences for acreages, hobby farms and country homes.</p>
<h2>What's included</h2>
<ul>
<li><strong>Post-and-rail and split rail</strong> — classic wood rail fences for frontages, driveways and paddocks.</li>
<li><strong>Field and woven wire fence</strong> — for sheep, goats, dogs and general livestock, stretched tight between braced ends.</li>
<li><strong>Horse fencing</strong> — rail, board or no-climb wire designs that are easy for horses to see and safe if they lean on it.</li>
<li><strong>Braced corners and ends</strong> — H-braces or angle braces at corners, ends and gates so the wire never loosens.</li>
<li><strong>Equipment gates</strong> — wide farm gates for tractors and trailers, hung on posts that won't sag.</li>
<li><strong>Clearing the line</strong> — removal of old rusted wire and rotten posts along the existing fence line.</li>
</ul>
<h2>How the job runs</h2>
<ol>
<li><strong>Walk the line.</strong> We walk the property with you, note grade changes, wet areas and gate locations.</li>
<li><strong>Written quote.</strong> Post type, spacing, fence material, bracing, gates and removal listed separately.</li>
<li><strong>Posts and bracing.</strong> Locates confirmed, corner and end assemblies built first, then line posts.</li>
<li><strong>Wire or rails.</strong> Wire stretched and fastened, or rails installed, and gates hung.</li>
</ol>
<h2>Fence for the animal, not the catalogue</h2>
<p>Horses, goats, cattle and dogs each test a fence differently, so we choose height, wire spacing and post spacing for what the fence actually needs to hold. For areas around the house, [[chain-link-fences|chain link]] and [[wood-fences|wood fences]] work alongside farm fence. Need a wide entrance? See [[custom-gates|gates]].</p>
""",
"faqs": [
("How far apart are farm fence posts?", "It depends on the fence type and the animals. Woven wire is commonly built with posts every 3 to 5 metres, and rail fences match the rail length. Corners and gates get braced assemblies."),
("Can you remove an old farm fence?", "Yes. We pull old wire and posts along the line before building the new fence, and haul away the scrap."),
("Do rural properties need utility locates?", "Yes. Buried lines run to rural homes and along roads too, so locates are requested before any digging, wherever the property is."),
("What fence keeps deer out of a garden?", "Deer can clear most fences under about eight feet, so a tall woven wire or mesh fence on sturdy posts is the usual choice around gardens and orchards. Shorter fences can work when combined with a second offset fence, depending on the property."),
],
"related": ["chain-link-fences", "custom-gates", "fence-removal"],
"cities": {
"windsor": "Windsor is mostly urban, but larger lots on the city's edges and properties near the airport and the south end still use post-and-rail and wire fencing. For these, we often combine a decorative rail fence along the road with practical wire fence around the back of the property.",
"lasalle": "LaSalle still has larger lots and acreages away from its subdivisions, where post-and-rail along the frontage and woven wire around gardens and animal areas are common. Wet clay ground is the main challenge here, so we plan braces and gate posts for soft spring conditions.",
"tecumseh": "South of the town centre, much of Tecumseh is farmland and country properties in the former Sandwich South township. That's where we build long runs of field fence, horse fencing and post-and-rail, with braced corners and wide gates sized for tractors and trailers."
},
},
{
"slug": "commercial-fences",
"name": "Commercial Fences",
"cat": "projects",
"icon": "commercial",
"short": "Commercial and industrial fencing for businesses, yards and facilities: chain link, ornamental steel, security toppings and gates.",
"title": "Commercial Fence Installation | Security & Yards",
"desc": "Commercial fence installation for businesses and industrial yards: heavy chain link, ornamental steel, security toppings, slats and access gates.",
"h1": "Commercial Fences",
"lead": "Fences that secure the yard, control who comes and goes and look professional from the road, installed with minimal disruption to your business.",
"body": """
<p>Commercial fencing has to do more than mark a line. It secures equipment and inventory, controls vehicle and foot traffic, screens storage areas and creates a professional first impression. It also has to meet municipal rules for height, sightlines and security toppings. {biz} installs commercial fencing for businesses, industrial yards, property managers and institutions.</p>
<h2>What's included</h2>
<ul>
<li><strong>Heavy chain link</strong> — commercial-weight posts, fabric and fittings at heights up to 8 feet and more where permitted.</li>
<li><strong>Ornamental steel</strong> — for storefronts, offices and multi-unit properties that need security with a finished look.</li>
<li><strong>Security toppings</strong> — barbed wire arms where by-laws allow it, and other options that don't need special approval.</li>
<li><strong>Screening</strong> — privacy slats or screen fabric for storage yards and equipment areas.</li>
<li><strong>Access control</strong> — swing gates, rolling cantilever gates and pedestrian gates, ready for locks or access systems.</li>
<li><strong>Work around your hours</strong> — scheduling and staging planned to keep your business running.</li>
</ul>
<h2>How the job runs</h2>
<ol>
<li><strong>Site review.</strong> We walk the property, note traffic patterns, gates, grade and any by-law limits.</li>
<li><strong>Written proposal.</strong> Materials, heights, gates, toppings and schedule laid out for approval.</li>
<li><strong>Posts and framework.</strong> Locates confirmed, posts set and framework installed in stages.</li>
<li><strong>Fabric, gates and hand-over.</strong> Fence completed, gates adjusted and keys or hardware handed over.</li>
</ol>
<h2>Know the rules before you order</h2>
<p>Commercial fences often face stricter rules than residential ones, including maximum heights, setbacks from driveways and limits on barbed or razor wire. We check the by-law for your property before finalizing the design, and flag anything that needs a permit or approval so it doesn't hold up the schedule. For the fence itself, see [[chain-link-fences|chain link]] and [[ornamental-fences|ornamental fencing]], and for vehicle access, [[custom-gates|gates]].</p>
""",
"faqs": [
("Can a commercial fence have barbed wire?", "Often, but with conditions. Many by-laws allow barbed wire only on non-residential properties and only above a minimum height. We confirm what's allowed for your property."),
("Can you work while our business is open?", "Yes. We stage the work in sections and plan around deliveries and customer hours so the site stays secure and usable."),
("Do you install automatic gates?", "We install swing and rolling gates built to accept gate operators. Electrical connections are made by a licensed electrician."),
("How tall can a commercial fence be?", "Each municipality sets its own limit for non-residential fences, and rules often differ near roads, driveways and corners. Taller security fencing may need approval. We check the by-law for your property and design the fence to fit it before anything is ordered. If you manage several properties, we can plan the work across all of them so fencing, gates and hardware match from site to site."),
],
"related": ["chain-link-fences", "ornamental-fences", "custom-gates"],
"cities": {
"windsor": "Windsor's industrial areas and commercial corridors need fencing that handles trucks, storage and security. The city sets a maximum height for non-residential fences, limits barbed wire to fences above a minimum height and requires a setback from driveways and lanes, which we design around from the start.",
"lasalle": "LaSalle's commercial work is mostly retail plazas, offices, service businesses and multi-unit properties, where ornamental steel and black chain link give a clean, secure look. We schedule installation around customer traffic so entrances stay open.",
"tecumseh": "The Oldcastle industrial area in Tecumseh is home to manufacturers, trucking yards and contractors that need heavy chain link, rolling gates and screening for outdoor storage. We plan the fence line around truck turning paths and gate access."
},
},
# ------------------------------------------------------------------ GATES, REPAIR & CARE
{
"slug": "custom-gates",
"name": "Custom Gates",
"cat": "care",
"icon": "gate",
"short": "Walk gates, double driveway gates and rolling gates in wood, vinyl, aluminum and steel, framed so they swing true and latch every time.",
"title": "Custom Fence & Driveway Gate Installation",
"desc": "Custom gate installation: walk gates, double driveway gates and rolling gates in wood, vinyl, aluminum and steel, framed so they never sag.",
"h1": "Custom Gates",
"lead": "The gate is the part of a fence you use every day. We build gates that swing true, latch every time and don't drag on the ground in two years.",
"body": """
<p>Most fence complaints are really gate complaints: a gate that sags, drags, won't latch or slams in the wind. A gate is a moving part hanging off one post, so it needs a stiff frame, the right hinges and a post set to carry the weight. {biz} builds gates as part of new fences and adds or replaces gates on existing ones.</p>
<h2>What's included</h2>
<ul>
<li><strong>Walk gates</strong> — single gates for side yards and backyards, matched to your fence style.</li>
<li><strong>Double driveway gates</strong> — wide double gates for vehicles, trailers and boats, with drop rods to hold them open or closed.</li>
<li><strong>Rolling and cantilever gates</strong> — for wide openings and commercial properties where swing gates won't fit.</li>
<li><strong>Frames that don't sag</strong> — steel frames, diagonal bracing or anti-sag kits depending on the material.</li>
<li><strong>Heavy-duty hardware</strong> — hinges sized to the gate's weight, latches that line up, and self-closing and lockable options.</li>
<li><strong>Gate posts set deeper</strong> — larger footings for gate posts, because they carry the most load on the fence.</li>
</ul>
<h2>How the job runs</h2>
<ol>
<li><strong>Measure the opening.</strong> We check the width, the grade under the swing and the condition of existing posts.</li>
<li><strong>Written quote.</strong> Gate size, material, frame, hardware and any new posts listed separately.</li>
<li><strong>Build and hang.</strong> New posts set if needed, gate built and hung.</li>
<li><strong>Adjust.</strong> Swing, clearance and latch adjusted until the gate closes cleanly.</li>
</ol>
<h2>Plan the swing</h2>
<p>A gate that swings uphill will hit the ground. We check the slope under every gate, choose which way it opens and leave the right clearance. If the gate leads into a pool area, it must close and latch by itself every time, so see [[pool-fences|pool fences]] for those rules. A gate that already sags can often be fixed, see [[fence-repair|fence repair]].</p>
""",
"faqs": [
("Why do gates sag?", "Usually because the frame isn't braced, the hinges are too light or the gate post has shifted. We fix the cause, not just the latch."),
("How wide should a driveway gate be?", "Wide enough for the largest vehicle or trailer you'll bring through, plus room to spare. Double gates are common for openings over about four feet."),
("Can you add a gate to my existing fence?", "Usually, yes. We cut in a new opening, add properly set gate posts and build a gate to match the fence as closely as the material allows."),
("Can a gate be made self-closing?", "Yes. Spring hinges or a gate closer pull the gate shut, and a gravity or magnetic latch catches it. Self-closing, self-latching gates are required around pools and are a smart choice anywhere pets or kids are in the yard."),
],
"related": ["fence-repair", "pool-fences", "wood-fences"],
"cities": {
"windsor": "In Windsor, the most-used gate on many properties is the one onto the rear alley, opened for garbage day, the garage and deliveries. We build alley gates with steel-framed or braced construction and hardware that can handle daily use, and double gates where a vehicle needs to pass.",
"lasalle": "LaSalle homeowners often need a wide side-yard gate for lawn equipment, a pool installer's machine or a trailer. We size the opening for the biggest thing that will come through and keep gates clear of the drainage swales common along the sides of subdivision lots.",
"tecumseh": "On rural Tecumseh properties, gates are about equipment: tractors, trailers and boats. We build wide farm and driveway gates on large posts with deeper footings, so a long gate doesn't drop at the latch end after a few seasons."
},
},
{
"slug": "fence-repair",
"name": "Fence Repair",
"cat": "care",
"icon": "repair",
"short": "Repairs for leaning posts, broken pickets, storm damage and sagging gates, so a fence with good bones doesn't have to be replaced.",
"title": "Fence Repair | Posts, Panels, Gates & Storm Damage",
"desc": "Fence repair for leaning or broken posts, damaged pickets and panels, storm damage and sagging gates, priced in writing before work starts.",
"h1": "Fence Repair",
"lead": "Leaning post, missing pickets, a gate that won't latch or a section the wind took down. We fix what's broken and tell you honestly if it's time to replace.",
"body": """
<p>A fence rarely fails all at once. One post rots at the ground line or heaves in the frost, the section beside it starts to lean, and then a windstorm finishes the job. Catching it early usually means a repair instead of a new fence. {biz} repairs wood, vinyl, chain link and ornamental fences, and we'll tell you straight when a fence has reached the point where repair money is wasted.</p>
<h2>What's included</h2>
<ul>
<li><strong>Post replacement</strong> — broken, rotted or heaved posts pulled and reset in fresh concrete, often without removing the whole section.</li>
<li><strong>Leaning sections</strong> — straightened and re-secured, with the cause fixed so they don't lean again.</li>
<li><strong>Pickets, boards and panels</strong> — replaced and matched as closely as the material allows.</li>
<li><strong>Gate repair</strong> — re-hung, re-braced or fitted with new hinges and latches so they swing and latch properly.</li>
<li><strong>Storm and impact damage</strong> — sections knocked down by wind, falling branches or vehicles rebuilt.</li>
<li><strong>Chain link repair</strong> — bent top rail, loose fabric and broken ties restored to tension.</li>
</ul>
<h2>How the job runs</h2>
<ol>
<li><strong>Inspection.</strong> We look at the damage and check the posts on either side, which are often the real problem.</li>
<li><strong>Written price.</strong> Repair or replace options, priced before any work starts.</li>
<li><strong>Repair.</strong> Posts reset, sections rebuilt and hardware replaced.</li>
<li><strong>Check.</strong> Line, gates and latches checked before we leave.</li>
</ol>
<h2>Repair or replace?</h2>
<p>If most posts are solid, repair almost always makes sense. If posts are failing along the whole line or the fence is near the end of its life, a [[wood-fences|new wood fence]] or [[vinyl-fences|vinyl fence]] may cost less over time. Wood that is sound but grey can be revived with [[fence-staining|staining]]. Storm damage? Photos help with insurance claims, so take them before cleaning up.</p>
""",
"faqs": [
("Can you replace one fence post?", "Yes. Replacing a single broken or heaved post is one of the most common repairs, and the panels on either side can usually be reattached."),
("Can you match my old fence?", "We match style and size as closely as possible. New wood will look brighter until it weathers or is stained, and some discontinued vinyl styles can't be matched exactly."),
("Is fence damage covered by insurance?", "Sometimes, for sudden events like storms or falling trees. Check with your insurer. We provide a written repair price you can submit."),
("How quickly can you fix storm damage?", "We prioritize fences that are down after a storm, especially where pets, pools or security are involved. If a full repair needs materials, we can often secure the opening temporarily first and come back to finish the job properly."),
],
"related": ["custom-gates", "fence-staining", "fence-removal"],
"cities": {
"windsor": "Windsor's mature trees are beautiful until a limb comes down on the fence, and many older fences in the city have posts that have been rotting quietly at the ground line for years. Storm calls after summer thunderstorms are common here, and we start by checking the posts on either side of the damage.",
"lasalle": "Many LaSalle fences went up at the same time as the subdivisions around them, and their original posts are now reaching the age where they rot or heave in the clay. Shared fences between neighbours are common, so we provide a clear written price that both owners can look at.",
"tecumseh": "Wind off Lake St. Clair is the leading cause of fence damage in north Tecumseh, while rural properties see more damage from frost heave and equipment. We rebuild fallen sections and reset heaved posts with drainage gravel and concrete shaped to resist frost."
},
},
{
"slug": "fence-staining",
"name": "Fence Staining & Sealing",
"cat": "care",
"icon": "stain",
"short": "Cleaning, brightening, staining and sealing for wood fences, to bring back grey wood and protect it from sun and moisture.",
"title": "Fence Staining & Sealing | Wood Fence Protection",
"desc": "Wood fence staining and sealing: cleaning, brightening and penetrating stain to protect new or weathered fences from sun, moisture and grey fading.",
"h1": "Fence Staining & Sealing",
"lead": "Grey, dry or blotchy wood can look new again. We clean, prep and stain wood fences so they're protected from the sun and water for years.",
"body": """
<p>Wood fences go grey because the sun breaks down the surface fibres, and they crack and rot because water gets in. A quality stain blocks both. Staining is the most effective thing you can do to make a wood fence last, and it transforms the look of the whole yard. {biz} stains and seals new and existing wood fences, with the prep work that makes the stain last.</p>
<h2>What's included</h2>
<ul>
<li><strong>Inspection first</strong> — we check for loose boards, popped fasteners and soft spots that should be fixed before staining.</li>
<li><strong>Cleaning</strong> — dirt, mildew and grey surface fibres removed with a wood cleaner and a careful low-pressure wash.</li>
<li><strong>Brightening</strong> — a brightener to restore the wood's colour and open the grain so the stain soaks in.</li>
<li><strong>Penetrating stain</strong> — semi-transparent or solid stain applied to both sides or your side only, in the colour you choose.</li>
<li><strong>Protecting your yard</strong> — plants, patios, siding and neighbouring surfaces covered or masked.</li>
<li><strong>Clean finish</strong> — drips and overspray cleaned up and the work area left tidy.</li>
</ul>
<h2>How the job runs</h2>
<ol>
<li><strong>Look and colour.</strong> We check the fence, show you stain colours and agree on which sides get stained.</li>
<li><strong>Written quote.</strong> Prep, repairs, stain type and sides listed separately.</li>
<li><strong>Clean and dry.</strong> The fence is cleaned and brightened, then left to dry thoroughly.</li>
<li><strong>Stain.</strong> Stain applied in suitable weather, back-brushed where needed for even coverage.</li>
</ol>
<h2>When to stain</h2>
<p>New pressure-treated wood usually needs a few months to dry; new cedar can often be stained sooner. After that, plan on a fresh coat every two to four years depending on sun exposure and stain type. Spring and early fall, with dry days and mild temperatures, are ideal, because stain needs dry wood and a day or two without rain to cure properly. Building new? See [[wood-fences|wood fences]], or if boards are already failing, [[fence-repair|fence repair]].</p>
""",
"faqs": [
("Semi-transparent or solid stain?", "Semi-transparent shows the wood grain and is easier to refresh. Solid stain hides more weathering and lasts longer between coats, but looks more like paint."),
("Do you stain the neighbour's side?", "Only with permission. We usually stain your side, or both sides when the neighbour agrees, which protects the wood better."),
("Can you stain a vinyl or composite fence?", "No. Those materials don't need or accept stain. Cleaning is all they need."),
("How long does fence stain last?", "Semi-transparent stain usually lasts about two to three years on surfaces that get a lot of sun, and solid stain somewhat longer. Shaded sides of the fence last longer than sunny ones. When water stops beading on the wood, it's time for a fresh coat."),
],
"related": ["wood-fences", "fence-repair", "privacy-fences"],
"cities": {
"windsor": "Windsor gets some of the hottest, sunniest summers in Ontario, which is hard on south- and west-facing fences. Many Windsor wood fences are a few years old and already grey, and a proper clean, brighten and stain brings them back before the surface starts to crack.",
"lasalle": "In LaSalle neighbourhoods where fences went up together, staining is often a shared project: one neighbour stains their side, or both agree on one colour. We coordinate access and colour choices so the fence looks consistent from both yards.",
"tecumseh": "Fences near the lake in Tecumseh deal with damp air and mildew, while fences on open lots to the south take full sun all day. We adjust the cleaning and stain choice for each, and plan the work around Tecumseh's windier days."
},
},
{
"slug": "fence-removal",
"name": "Fence Removal",
"cat": "care",
"icon": "removal",
"short": "Old fence tear-out and haul-away, including posts and concrete footings, as a separate job or before a new fence goes in.",
"title": "Old Fence Removal & Haul-Away",
"desc": "Old fence removal and haul-away: wood, vinyl, chain link and wire fences taken down, posts and concrete footings pulled, and debris disposed of.",
"h1": "Fence Removal",
"lead": "Old fence down, posts out, concrete gone and the mess hauled away, as its own job or the first day of your new fence.",
"body": """
<p>Taking out an old fence sounds simple until you get to the posts. Concrete footings, rusted chain link and rotted wood that crumbles in your hands make removal hard, heavy work. {biz} removes old fences cleanly, either as a standalone job or as part of installing a new one, and hauls everything away.</p>
<h2>What's included</h2>
<ul>
<li><strong>All fence types</strong> — wood, vinyl, chain link, wire and ornamental fences taken down section by section.</li>
<li><strong>Posts and footings</strong> — posts pulled and concrete footings removed, or cut below grade where removal isn't practical.</li>
<li><strong>Holes filled</strong> — post holes backfilled and tamped so they don't become trip hazards.</li>
<li><strong>Haul-away and disposal</strong> — wood, concrete and metal removed and disposed of or recycled where possible.</li>
<li><strong>Shared fences handled carefully</strong> — we coordinate with you on fences shared with neighbours before anything comes down.</li>
<li><strong>Clean site</strong> — nails, ties and debris picked up from the yard.</li>
</ul>
<h2>How the job runs</h2>
<ol>
<li><strong>Look at the fence.</strong> We check the length, material and footings, and how close the fence is to gardens and buildings.</li>
<li><strong>Written price.</strong> Removal, footing removal and disposal listed clearly.</li>
<li><strong>Tear-out.</strong> Fence taken down, posts and footings removed.</li>
<li><strong>Clean-up.</strong> Holes backfilled and everything hauled away.</li>
</ol>
<h2>Removing and replacing together</h2>
<p>When a new fence is going up on the same line, removal is usually done the same day the new post holes are dug, so the yard is never open for long. Pets in the yard? We plan the schedule so the gap is as short as possible. See [[wood-fences|wood]], [[vinyl-fences|vinyl]] and [[chain-link-fences|chain link fences]], or include removal in the [[estimate|instant fence estimate]].</p>
""",
"faqs": [
("Do you remove the concrete footings?", "Yes, in most cases. Where a footing is very large or close to a building, we may cut the post below grade and leave the concrete, and we'll tell you before we do."),
("Can you remove a fence without replacing it?", "Yes. Fence removal is available as a standalone service."),
("What happens to the old fence?", "Wood, concrete and metal are hauled away and disposed of, with metal recycled where possible."),
("How long does fence removal take?", "Most residential fences come down in a day, even with concrete footings. Long rural lines, heavily overgrown fence rows and very large footings can take longer. When removal is followed by a new fence, we plan both so the yard is open for as little time as possible. If you only need part of a fence removed, such as one damaged section or a run being moved for a new driveway, we take down just that part and leave the remaining posts solid."),
],
"related": ["fence-repair", "wood-fences", "chain-link-fences"],
"cities": {
"windsor": "In Windsor, fence removal often means old chain link and wood fences that have been patched for decades, sometimes with several generations of posts along the same line. Alley access makes hauling easier on many properties, and we plan the work so your yard is closed in again quickly.",
"lasalle": "LaSalle removals are usually original subdivision fences being replaced, often on a shared line. We coordinate with both neighbours, remove the old fence and set the new posts in the same visit where possible.",
"tecumseh": "On rural Tecumseh properties, fence removal can mean long lines of rusted wire, old cedar posts and fence rows overgrown with brush. We clear the line so new fencing can go up straight, and haul away the scrap."
},
},
]
