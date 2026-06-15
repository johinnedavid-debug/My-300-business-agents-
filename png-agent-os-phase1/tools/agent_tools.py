"""
PNG Agent OS — Agent Tools
Custom tools that agents use to interact with the real world
"""

from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
import json
import os


# ─────────────────────────────────────────────────────────────
# WEB SEARCH TOOL
# ─────────────────────────────────────────────────────────────

_search = DuckDuckGoSearchRun()

def _web_search(query: str) -> str:
    """Search the web for current information"""
    try:
        result = _search.run(query)
        return f"SEARCH RESULTS for '{query}':\n{result}"
    except Exception as e:
        return f"Search failed: {str(e)}. Try rephrasing the query."

web_search_tool = Tool(
    name="web_search",
    func=_web_search,
    description="""
    Search the internet for current information. Use for:
    - Competitor research and pricing
    - Supplier and manufacturer information
    - Market trends and news
    - PNG business and legal information
    Input: a clear search query string.
    """
)


# ─────────────────────────────────────────────────────────────
# MARKET RESEARCH TOOL
# ─────────────────────────────────────────────────────────────

def _market_research(query: str) -> str:
    """Structured market research combining multiple searches"""
    searches = [
        f"{query} market size",
        f"{query} competitors Papua New Guinea",
        f"{query} customer demographics",
        f"{query} pricing strategy"
    ]
    results = {}
    for s in searches:
        try:
            results[s] = _search.run(s)
        except:
            results[s] = "No results found"
    
    return json.dumps({
        "query": query,
        "market_data": results,
        "status": "completed",
        "note": "Synthesize these results into actionable market insights"
    }, indent=2)

market_research_tool = Tool(
    name="market_research",
    func=_market_research,
    description="""
    Conduct structured market research on a topic or industry.
    Returns data on market size, competitors, demographics, and pricing.
    Input: topic or business area to research (e.g. 'PNG tourism souvenirs')
    """
)


# ─────────────────────────────────────────────────────────────
# CONTENT WRITER TOOL
# ─────────────────────────────────────────────────────────────

def _content_writer(brief: str) -> str:
    """
    Generate content based on a brief.
    In production, this would call the Anthropic API directly for speed.
    """
    # This is a passthrough tool — the agent itself IS the content writer.
    # In production, you'd call a dedicated fast API here.
    return f"""
    CONTENT BRIEF RECEIVED: {brief}
    
    STATUS: Agent will now generate content based on this brief.
    VOICE: Warm, proud, culturally authentic PNG tone.
    PLATFORM: Adapt length and format to specified channel.
    INSTRUCTION: Write complete, publication-ready content only.
    No placeholders. No 'Insert X here' templates.
    """

content_writer_tool = Tool(
    name="content_writer",
    func=_content_writer,
    description="""
    Use this to frame a content writing task before executing it.
    Provide a complete brief including: content type, channel, 
    target audience, key message, tone, and word count.
    Input: detailed content brief as a string.
    """
)


# ─────────────────────────────────────────────────────────────
# FINANCIAL MODELING TOOL
# ─────────────────────────────────────────────────────────────

def _financial_model(parameters: str) -> str:
    """Build basic financial projections"""
    try:
        params = json.loads(parameters)
    except:
        params = {"raw_input": parameters}
    
    # Simple projection model
    monthly_revenue    = params.get("monthly_revenue_pgk", 10000)
    growth_rate        = params.get("monthly_growth_rate", 0.10)
    monthly_costs      = params.get("monthly_costs_pgk", 6000)
    months             = params.get("projection_months", 12)
    
    projections = []
    revenue = monthly_revenue
    for m in range(1, months + 1):
        profit = revenue - monthly_costs
        projections.append({
            "month": m,
            "revenue_pgk": round(revenue, 2),
            "costs_pgk": monthly_costs,
            "profit_pgk": round(profit, 2),
            "profit_aud": round(profit / 3.8, 2),  # approx PGK→AUD
            "profit_usd": round(profit / 4.1, 2),  # approx PGK→USD
        })
        revenue = revenue * (1 + growth_rate)
    
    total_revenue = sum(p["revenue_pgk"] for p in projections)
    total_profit  = sum(p["profit_pgk"]  for p in projections)
    
    return json.dumps({
        "projection_period": f"{months} months",
        "monthly_projections": projections,
        "summary": {
            "total_revenue_pgk": round(total_revenue, 2),
            "total_profit_pgk":  round(total_profit, 2),
            "break_even_month":  next(
                (p["month"] for p in projections if p["profit_pgk"] > 0), "N/A"
            )
        },
        "currency_note": "Conversions approximate. Verify with live rates."
    }, indent=2)

financial_model_tool = Tool(
    name="financial_model",
    func=_financial_model,
    description="""
    Build financial projections for a business scenario.
    Input: JSON string with keys:
      - monthly_revenue_pgk (number)
      - monthly_costs_pgk (number)  
      - monthly_growth_rate (decimal, e.g. 0.10 = 10%)
      - projection_months (integer)
    Returns month-by-month projections in PGK, AUD, and USD.
    """
)


# ─────────────────────────────────────────────────────────────
# COMPETITOR ANALYSIS TOOL
# ─────────────────────────────────────────────────────────────

def _competitor_analysis(business_type: str) -> str:
    """Research competitors for a given business type"""
    queries = [
        f"{business_type} competitors Papua New Guinea",
        f"best {business_type} online PNG",
        f"{business_type} pricing comparison Pacific"
    ]
    results = {}
    for q in queries:
        try:
            results[q] = _search.run(q)
        except:
            results[q] = "No data found"
    
    return json.dumps({
        "business_type": business_type,
        "competitor_research": results,
        "action": "Identify top 3-5 competitors, their pricing, strengths, and gaps we can exploit"
    }, indent=2)

competitor_analysis_tool = Tool(
    name="competitor_analysis",
    func=_competitor_analysis,
    description="""
    Research competitors for a given business type in PNG/Pacific market.
    Input: business type or product category (e.g. 'PNG souvenir online store')
    Returns competitor names, pricing, and market positioning data.
    """
)


# ─────────────────────────────────────────────────────────────
# CUSTOMER INSIGHT TOOL
# ─────────────────────────────────────────────────────────────

def _customer_insight(segment: str) -> str:
    """Research customer segment insights"""
    result = _search.run(f"{segment} buying behavior preferences Papua New Guinea")
    return json.dumps({
        "customer_segment": segment,
        "insights": result,
        "framework": {
            "demographics":  "Age, location, income level, device usage",
            "psychographics": "Values, aspirations, cultural identity",
            "buying_triggers": "What makes them purchase",
            "pain_points":   "What problems they want solved",
            "channels":      "Where they discover and buy products in PNG"
        },
        "action": "Use this data to build a customer persona for targeting"
    }, indent=2)

customer_insight_tool = Tool(
    name="customer_insight",
    func=_customer_insight,
    description="""
    Research buying behavior and preferences of a customer segment.
    Input: customer segment description (e.g. 'PNG women aged 25-45 fashion')
    Returns demographic, psychographic, and behavioral data.
    """
)


# ─────────────────────────────────────────────────────────────
# LOGISTICS TOOL
# ─────────────────────────────────────────────────────────────

def _logistics(route: str) -> str:
    """Research shipping and logistics for a given route"""
    result = _search.run(f"shipping logistics {route} cost time options")
    return json.dumps({
        "route": route,
        "logistics_data": result,
        "png_carriers": [
            "Air Niugini Cargo — domestic + Pacific routes",
            "EMS Post PNG — domestic postal service",
            "DHL Express — international express",
            "Toll Group — bulk freight PNG",
            "Pacific Direct Line — sea freight to Pacific Islands"
        ],
        "china_to_png": {
            "sea_freight": "25-35 days via Brisbane transshipment",
            "air_freight": "5-10 days, significantly more expensive",
            "recommended": "Sea freight for machinery, air for urgent samples"
        },
        "action": "Select best carrier for route, cost, and timeline requirements"
    }, indent=2)

logistics_tool = Tool(
    name="logistics",
    func=_logistics,
    description="""
    Research shipping and logistics options for a given route.
    Input: shipping route (e.g. 'China to Port Moresby PNG machinery')
    Returns carrier options, estimated times, costs, and recommendations.
    """
)


# ─────────────────────────────────────────────────────────────
# LEGAL CHECK TOOL
# ─────────────────────────────────────────────────────────────

def _legal_check(topic: str) -> str:
    """Check legal requirements for a business action in PNG"""
    result = _search.run(f"{topic} legal requirements Papua New Guinea law")
    return json.dumps({
        "topic": topic,
        "legal_research": result,
        "png_key_authorities": {
            "IPA":  "Investment Promotion Authority — business registration",
            "IRC":  "Internal Revenue Commission — taxation",
            "ICCC": "Independent Consumer & Competition Commission — trade",
            "BPNG": "Bank of Papua New Guinea — financial regulations",
            "NCC":  "National Cultural Commission — cultural IP protection"
        },
        "warning": "This is research only. For binding legal advice, consult a PNG-licensed lawyer.",
        "action": "Identify specific compliance requirements and flag any red flags"
    }, indent=2)

legal_check_tool = Tool(
    name="legal_check",
    func=_legal_check,
    description="""
    Research legal and compliance requirements for a business activity in PNG.
    Input: legal topic (e.g. 'importing machinery from China PNG customs duty')
    Returns relevant PNG laws, authorities, and compliance requirements.
    WARNING: Research only — not legal advice.
    """
)


# ─────────────────────────────────────────────────────────────
# SOCIAL MEDIA TOOL
# ─────────────────────────────────────────────────────────────

def _social_media(task: str) -> str:
    """Plan and structure social media content"""
    return json.dumps({
        "task": task,
        "png_social_landscape": {
            "primary_platform": "Facebook (dominant in PNG — 70%+ of social users)",
            "visual_platform":  "Instagram (growing, esp. tourism + fashion)",
            "video_platform":   "TikTok (fast-growing among under-35s in PNG)",
            "messaging":        "WhatsApp + Facebook Messenger (customer service)"
        },
        "content_types": {
            "Facebook":  "Long-form posts, videos, Facebook Shop, community groups",
            "Instagram": "Reels, Stories, Shopping tags, Explore",
            "TikTok":    "30-60 sec videos, behind-the-scenes, cultural content"
        },
        "posting_frequency": {
            "Facebook":  "1-2x per day",
            "Instagram": "5-7 Reels/week + daily Stories",
            "TikTok":    "1-3x per day for algorithm growth"
        },
        "action": "Execute specific social task with platform-appropriate format and tone"
    }, indent=2)

social_media_tool = Tool(
    name="social_media",
    func=_social_media,
    description="""
    Plan and execute social media tasks for PNG businesses.
    Input: specific social media task (e.g. 'write 3 Facebook posts for bilum launch')
    Returns platform strategy, content formats, and posting guidance.
    """
)


# ─────────────────────────────────────────────────────────────
# EMAIL TOOL
# ─────────────────────────────────────────────────────────────

def _email(brief: str) -> str:
    """Draft email communications"""
    return json.dumps({
        "email_brief": brief,
        "email_structure": {
            "subject": "Clear, specific, under 60 characters",
            "greeting": "Professional but warm (PNG culture values warmth)",
            "body": "Purpose → Details → Action required → Timeline",
            "closing": "Professional PNG business sign-off",
            "signature": "Name, Title, Business, Phone, Website"
        },
        "action": "Draft complete email based on this brief. Include subject line.",
        "note": "All emails require human approval before sending unless pre-authorized"
    }, indent=2)

email_tool = Tool(
    name="email",
    func=_email,
    description="""
    Draft email communications for business purposes.
    Input: email brief including recipient type, purpose, and key points
    Returns structured email draft ready for review and sending.
    NOTE: Emails require human approval before sending.
    """
)
