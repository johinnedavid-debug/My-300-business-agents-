"""
PNG Agent OS — Task Definitions
Pre-built task templates for both PNG businesses
"""

from crewai import Task
from agents.agent_definitions import *


# ═════════════════════════════════════════════════════════════
# SHARED UTILITY — Task with retry logic
# ═════════════════════════════════════════════════════════════

def make_task(description: str, agent, expected_output: str,
              context: list = None) -> Task:
    """Factory: create a Task with standard retry and QA wrapper"""
    full_description = f"""
{description}

EXECUTION RULES (follow strictly):
1. Think step-by-step before acting
2. If you hit an error or dead end, try a different approach (max 3 attempts)
3. Never return incomplete or placeholder output
4. Always verify your output against the expected output spec below
5. If you truly cannot complete the task, escalate with a specific explanation
   of what blocked you and what you tried

PAPUA NEW GUINEA CONTEXT:
- Primary currency: PGK (Papua New Guinea Kina)
- Primary social platform: Facebook
- Payment systems: BSP Bank, Kina Bank, mobile money
- Connectivity: many users have limited bandwidth — optimize for this
- Culture: warmth, community, and cultural pride are core values
    """
    return Task(
        description=full_description,
        agent=agent,
        expected_output=expected_output,
        context=context or []
    )


# ═════════════════════════════════════════════════════════════
# TOURISM PLATFORM TASKS
# ═════════════════════════════════════════════════════════════

def task_tourism_market_analysis(agents: dict) -> Task:
    return make_task(
        description="""
        Conduct a comprehensive market analysis for the PNG Souvenir & Tourism
        Digital Platform. Research:
        
        1. How many tourists visit PNG annually and what they buy
        2. Existing souvenir/artisan platforms in PNG (online and physical)
        3. What authentic PNG products tourists most want (bilum, masks, jewelry,
           tapa cloth, kundu drums, etc.)
        4. Price points tourists expect vs. what artisans charge
        5. Top 3 competitor weaknesses we can exploit
        6. Recommended launch focus: which product categories to start with
        7. Digital penetration: how many PNG artisans are online-ready?
        """,
        agent=agents["tier4"]["researcher"],
        expected_output="""
        A structured market analysis report containing:
        - Tourism visitor statistics (annual numbers, spend data)
        - Competitor matrix (name, products, pricing, weaknesses)
        - Top 5 product categories to prioritize at launch with reasoning
        - Recommended price range per category (PGK and USD)
        - Digital readiness assessment of PNG artisan community
        - 3 biggest market opportunities with specific action recommendations
        All data cited with sources. Length: 600-900 words.
        """
    )

def task_tourism_artisan_outreach_email(agents: dict) -> Task:
    return make_task(
        description="""
        Draft an outreach email to invite PNG artisans to join the 
        PNG Souvenir & Tourism Platform. The email must:
        
        - Address a traditional bilum weaver or wood carver in PNG
        - Explain the platform in simple, clear language (no tech jargon)
        - Highlight what's in it for them: reach tourists, earn more income,
          keep their cultural crafts alive
        - Explain the process: list products → tourists discover → you get paid
        - Include simple onboarding steps
        - Warm, respectful PNG tone — this person may receive this in Tok Pisin
          communities so clarity is essential
        - Include a clear call-to-action
        """,
        agent=agents["tier5"]["email_agent"],
        expected_output="""
        A complete email with:
        - Subject line (under 60 chars)
        - Greeting
        - Body (4-6 short paragraphs, plain language)
        - Call-to-action with specific next step
        - Professional sign-off
        Ready to send — no placeholders.
        """
    )

def task_tourism_product_descriptions(agents: dict) -> Task:
    return make_task(
        description="""
        Write product descriptions for 5 signature PNG souvenir categories
        for the tourism platform. Categories:
        
        1. Handwoven Bilum Bag (traditional string bag)
        2. Sepik River Wood Carving (ancestral spirit mask)
        3. Tapa Cloth Wall Art (bark cloth, traditional patterns)
        4. Kundu Drum (traditional hourglass drum)
        5. Shell Jewelry (traditional Pacific adornment)
        
        Each description must:
        - Be 120-180 words
        - Tell the cultural story behind the item
        - Appeal to international tourists (English, accessible)
        - Include care/shipping note at the end
        - Make the buyer feel they are getting a piece of genuine PNG
        """,
        agent=agents["tier5"]["content_writer"],
        expected_output="""
        5 complete product descriptions, each clearly labeled:
        PRODUCT 1: [Name]
        [Description 120-180 words]
        [Care & Shipping note]
        
        ...repeated for all 5 products.
        All descriptions publication-ready. No placeholders.
        """
    )

def task_tourism_launch_campaign(agents: dict) -> Task:
    return make_task(
        description="""
        Create a 30-day social media launch campaign plan for the
        PNG Souvenir & Tourism Platform. The campaign must:
        
        - Cover Facebook (primary) + Instagram + TikTok
        - Week 1: Teaser — build anticipation ("Something special is coming...")
        - Week 2: Launch — announce platform, feature first artisans
        - Week 3: Social proof — artisan stories, first customer testimonials
        - Week 4: Momentum — deals, featured products, community building
        
        For each week provide:
        - Campaign theme and messaging angle
        - 3 sample post captions (per platform)
        - Content types (video, photo, carousel, etc.)
        - Hashtag strategy
        - Engagement tactics (polls, questions, live sessions)
        
        Budget assumption: organic only (no paid ads initially)
        """,
        agent=agents["tier3"]["social_mgr"],
        expected_output="""
        A complete 30-day campaign plan organized by week.
        For each week:
        - Theme (1 sentence)
        - Platform breakdown (Facebook / Instagram / TikTok)
        - 3 sample captions per platform (labeled, ready to post)
        - Content types to produce
        - Hashtag list (10-15 relevant PNG + tourism tags)
        - One engagement tactic
        Total: structured, actionable, ready to execute immediately.
        """
    )

def task_tourism_financial_projection(agents: dict) -> Task:
    return make_task(
        description="""
        Build a 12-month financial projection for the PNG Tourism Platform.
        
        Assumptions to model (create 3 scenarios):
        
        CONSERVATIVE:
        - Month 1: 20 products listed, 5 sales @ avg PGK 150
        - Growth: 8% monthly
        - Operating costs: PGK 2,000/month (hosting, marketing, misc)
        
        BASE CASE:
        - Month 1: 50 products listed, 15 sales @ avg PGK 200
        - Growth: 15% monthly  
        - Operating costs: PGK 3,500/month
        
        OPTIMISTIC:
        - Month 1: 100 products listed, 40 sales @ avg PGK 250
        - Growth: 25% monthly
        - Operating costs: PGK 5,000/month
        
        Platform commission: 15% of each sale
        Include: monthly revenue, costs, profit, and cumulative totals.
        Convert final year totals to AUD and USD.
        """,
        agent=agents["tier4"]["finance_model"],
        expected_output="""
        Three scenario tables (Conservative / Base / Optimistic) each showing:
        - Month-by-month: GMV (Gross Merchandise Value), Platform Revenue (15%),
          Operating Costs, Net Profit/Loss
        - 12-month totals in PGK, AUD, USD
        - Break-even month for each scenario
        - Key insight: which scenario David should plan for and why
        Format: clean tables, easy to read. No financial jargon.
        """
    )


# ═════════════════════════════════════════════════════════════
# FASHION VENTURE TASKS
# ═════════════════════════════════════════════════════════════

def task_fashion_china_suppliers(agents: dict) -> Task:
    return make_task(
        description="""
        Research industrial weaving and knitting machinery suppliers in China
        for David's PNG Meri Blouse & Bilum Fashion venture. Research:
        
        1. Top Chinese manufacturers of:
           - Flat knitting machines (for Meri Blouse fabric)
           - Rapier weaving looms (for bilum-style fabric)
           - Computer-controlled embroidery machines (for traditional patterns)
        
        2. For each machine type find:
           - Top 3 manufacturers (name, city, website if available)
           - Price range (USD)
           - MOQ (Minimum Order Quantity)
           - Lead time
           - Power specifications (must include 240V/50Hz option for PNG)
        
        3. Key trade shows David could visit:
           - China International Textile Machinery exhibition dates
           - Canton Fair textile section
        
        4. Recommended regions to visit in China (Guangzhou, Hangzhou, etc.)
        
        5. Import considerations: PNG customs duty on industrial machinery
        """,
        agent=agents["tier3"]["china_sourcing"],
        expected_output="""
        A sourcing report containing:
        - Machine type breakdown (3 types) with top 3 suppliers each
        - Price ranges in USD
        - Power/voltage specifications for PNG compatibility
        - Trade show calendar (next 12 months)
        - Recommended China travel itinerary for David (which cities, in what order)
        - PNG import duty estimate for industrial machinery
        - Red flags to watch for when dealing with Chinese machinery suppliers
        Format: practical, actionable, ready to use for trip planning.
        """
    )

def task_fashion_brand_identity(agents: dict) -> Task:
    return make_task(
        description="""
        Develop a complete brand identity brief for David's PNG fashion venture.
        The brand sells:
        - Custom Meri Blouse (traditional PNG women's dress, modernized)
        - Authentic Bilum bags and accessories
        - Modern Papua New Guinean fashion fusing traditional + contemporary
        
        Target customers:
        - PNG women aged 20-55 (domestic)
        - PNG diaspora worldwide (Australia, NZ, US, UK)
        - International fashion lovers who want authentic Pacific fashion
        
        Develop:
        1. Brand name options (3 options with meanings and rationale)
        2. Brand positioning statement (1 sentence)
        3. Brand personality (5 adjectives + explanation)
        4. Visual direction: colors (inspired by PNG nature/culture), typography mood,
           photography style
        5. Tagline options (3 options)
        6. Brand voice guide (how we write, what we never say)
        7. Key brand story (150 words — the WHY behind this brand)
        """,
        agent=agents["tier4"]["visual_design"],
        expected_output="""
        A complete brand identity brief containing all 7 sections above.
        Brand name options should draw from PNG languages and culture.
        Visual direction should reference specific PNG cultural elements
        (bilum patterns, bird of paradise, tribal geometry, highland colors).
        Brand story should feel personal, authentic, and emotionally compelling.
        Total length: 700-1000 words. Well-structured with clear section headers.
        """
    )

def task_fashion_custom_order_workflow(agents: dict) -> Task:
    return make_task(
        description="""
        Design the complete custom order workflow for the Meri Blouse
        & Bilum fashion business. Map every step from customer inquiry
        to product delivery. Include:
        
        1. Customer Journey:
           - Discovery (how they find the brand)
           - Style selection (fabric, pattern, size customization)
           - Order placement and payment (BSP Bank / Kina Bank / PayPal for diaspora)
           - Production confirmation
           - Progress updates during production
           - Delivery and unboxing experience
        
        2. Internal Production Flow:
           - Order received → Design brief created
           - Fabric/material sourcing check
           - Production assigned (which artisan/machine)
           - Quality control checkpoint
           - Packaging (branded, culturally themed)
           - Shipping label + tracking
        
        3. Timelines: realistic production times per item type
        4. Pricing matrix: base price + customization premiums
        5. Handling difficult situations: delays, quality issues, wrong size
        
        Format as a clear SOP (Standard Operating Procedure) document
        """,
        agent=agents["tier3"]["product_mgr"],
        expected_output="""
        A complete SOP document for custom orders containing:
        - Customer journey map (step-by-step with owner at each step)
        - Internal production flow (step-by-step with time estimates)
        - Realistic production timelines per item type
        - Pricing matrix template (base + customization options)
        - 3 scenario scripts for handling delays, quality issues, sizing errors
        Professional format, practical enough to hand to a new staff member.
        """
    )

def task_fashion_financial_model(agents: dict) -> Task:
    return make_task(
        description="""
        Build a financial model for the PNG Meri Blouse & Bilum fashion venture.
        Include the China machinery investment analysis.
        
        STARTUP COSTS (one-time):
        - Industrial knitting machine: ~USD 15,000-25,000
        - Weaving loom: ~USD 8,000-15,000
        - Embroidery machine: ~USD 3,000-8,000
        - Shipping + import duty + install: ~USD 5,000
        - Initial fabric inventory: ~PGK 10,000
        - Brand + website setup: ~PGK 5,000
        - Working capital reserve: ~PGK 20,000
        
        REVENUE MODEL:
        - Meri Blouse (standard): PGK 250-400 per unit
        - Meri Blouse (custom/premium): PGK 500-900 per unit  
        - Bilum bag (standard): PGK 150-300 per unit
        - Bilum bag (premium artisan): PGK 350-700 per unit
        - Diaspora/export premium: 2x local price in AUD
        
        OPERATING COSTS:
        - Estimated monthly: PGK 8,000-15,000 (staff, utilities, materials)
        
        Build: 24-month projection showing machinery ROI, break-even,
        and path to profitability. 3 scenarios as before.
        """,
        agent=agents["tier4"]["finance_model"],
        expected_output="""
        Complete 24-month financial model with:
        - Startup cost summary (total investment in USD + PGK)
        - 3 scenarios (Conservative/Base/Optimistic)
        - Month-by-month: Units sold, Revenue, COGS, Operating costs, Net profit
        - Machinery ROI analysis: when does the equipment pay for itself?
        - Break-even analysis: month and cumulative units
        - 24-month totals in PGK, AUD, USD
        - One-paragraph recommendation: is this a sound investment? Why?
        Format: clean tables + narrative summary. Practical for bank presentation.
        """
    )

def task_fashion_launch_content(agents: dict) -> Task:
    return make_task(
        description="""
        Write a complete launch content package for the PNG Fashion brand.
        
        Produce:
        1. WEBSITE HERO TEXT
           - Headline (max 8 words, powerful)
           - Subheadline (1-2 sentences)
           - CTA button text
        
        2. ABOUT US PAGE (250 words)
           - Brand story, mission, cultural connection
           - Why Meri Blouse and Bilum deserve a global stage
        
        3. FACEBOOK LAUNCH POST (for brand page)
           - Announcement post (200-300 words)
           - Emotionally compelling, community-first tone
        
        4. INSTAGRAM CAPTION SET (5 captions)
           - For launch week posts
           - Visual descriptions for each (what the image should show)
           - Hashtags included
        
        5. WHATSAPP BROADCAST MESSAGE
           - To send to David's personal network
           - Casual, warm, asking people to check out and share
           - Under 200 words
        
        All content should radiate PNG pride, cultural warmth, and
        the excitement of a PNG brand ready to go global.
        """,
        agent=agents["tier5"]["content_writer"],
        expected_output="""
        5 clearly labeled content sections, all publication-ready:
        1. WEBSITE HERO TEXT (headline + subheadline + CTA)
        2. ABOUT US PAGE (250 words)
        3. FACEBOOK LAUNCH POST (200-300 words)  
        4. INSTAGRAM CAPTIONS (5 captions with image descriptions + hashtags)
        5. WHATSAPP BROADCAST (under 200 words)
        
        No placeholders. Complete, ready-to-use content. PNG cultural pride
        must be evident throughout every single piece.
        """
    )


# ═════════════════════════════════════════════════════════════
# SHARED CROSS-BUSINESS TASKS
# ═════════════════════════════════════════════════════════════

def task_tech_stack_plan(agents: dict, business: str) -> Task:
    return make_task(
        description=f"""
        Create the complete technical architecture plan for the
        {business} platform. Based on David's existing stack:
        Next.js 14, Node.js, PostgreSQL, Prisma ORM, TypeScript, Vercel.
        
        Design:
        1. Database schema (key tables and relationships)
        2. API routes needed (RESTful endpoints list)
        3. Authentication system (JWT with refresh tokens)
        4. Payment integration plan (BSP Bank + Kina Bank + PayPal for diaspora)
        5. PWA/offline strategy (for PNG's low-connectivity users)
        6. File storage (product images — recommend Cloudinary or S3)
        7. Email system (for order confirmations, artisan notifications)
        8. Deployment pipeline (Vercel + Railway for backend)
        9. Environment variables needed (list all, with descriptions)
        10. Phase 1 MVP scope: minimum features to launch in 30 days
        """,
        agent=agents["tier4"]["tech_dev"],
        expected_output=f"""
        Complete technical architecture document for {business} containing:
        - Database schema (table names, key fields, relationships)
        - API endpoint list (method + path + description)
        - Auth flow diagram (text description)
        - Payment integration steps for each provider
        - PWA implementation checklist
        - Complete environment variables list
        - MVP feature list (what's IN and OUT for launch)
        - Estimated development time for solo developer
        Format: clear sections, code snippets where helpful.
        David is a beginner-level developer — explain any complex concepts simply.
        """
    )

def task_legal_business_setup(agents: dict) -> Task:
    return make_task(
        description="""
        Research and outline the complete legal business setup process
        for registering and operating both:
        1. PNG Souvenir & Tourism Platform (digital marketplace)
        2. PNG Meri Blouse & Bilum Fashion (manufacturing + retail + export)
        
        Cover:
        1. Business registration with IPA (Investment Promotion Authority)
           - Process, costs, timeline, documents needed
        2. Tax registration with IRC
           - GST obligations (threshold), income tax, PAYE if hiring staff
        3. Business banking
           - BSP vs Kina Bank business account requirements
           - Merchant account for online payments
        4. Import licenses (for China machinery)
        5. Export permits (for selling fashion internationally)
        6. Intellectual property: protecting PNG cultural designs
        7. E-commerce regulations in PNG
        8. Recommended business structure (sole trader vs. limited company)
        """,
        agent=agents["tier2"]["legal"],
        expected_output="""
        A practical legal setup guide containing:
        - Recommended business structure with reasoning
        - Step-by-step IPA registration process (with costs in PGK)
        - Tax obligations checklist (GST, income tax, PAYE)
        - Banking setup guide (which bank + account type to open first)
        - Import/export permit requirements
        - IP protection options for PNG cultural designs
        - Timeline: how long does full setup take?
        - Total estimated setup cost in PGK
        - One critical warning: the most common legal mistake PNG startups make
        Written in plain English — practical, actionable, not legal jargon.
        DISCLAIMER: Research only. Consult a PNG lawyer for binding advice.
        """
    )


# ═════════════════════════════════════════════════════════════
# MASTER ORCHESTRATION — Run all startup tasks
# ═════════════════════════════════════════════════════════════

def get_tourism_startup_tasks(agents: dict) -> list:
    """All tasks needed to kick-start the tourism platform"""
    return [
        task_tourism_market_analysis(agents),
        task_tourism_financial_projection(agents),
        task_tourism_product_descriptions(agents),
        task_tourism_artisan_outreach_email(agents),
        task_tourism_launch_campaign(agents),
        task_tech_stack_plan(agents, "PNG Souvenir & Tourism Platform"),
        task_legal_business_setup(agents),
    ]

def get_fashion_startup_tasks(agents: dict) -> list:
    """All tasks needed to kick-start the fashion venture"""
    return [
        task_fashion_china_suppliers(agents),
        task_fashion_financial_model(agents),
        task_fashion_brand_identity(agents),
        task_fashion_custom_order_workflow(agents),
        task_fashion_launch_content(agents),
        task_tech_stack_plan(agents, "PNG Meri Blouse & Bilum Fashion Website"),
        task_legal_business_setup(agents),
    ]
