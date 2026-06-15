"""
PNG Agent OS — Agent Tools (Fixed for latest LangChain)
"""

import json
import os

try:
    from langchain_core.tools import Tool
except ImportError:
    try:
        from langchain.tools import Tool
    except ImportError:
        # Fallback: define a simple Tool class
        class Tool:
            def __init__(self, name, func, description):
                self.name = name
                self.func = func
                self.description = description
            def run(self, query):
                return self.func(query)

# Web search — try multiple backends
def _web_search(query: str) -> str:
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
        search = DuckDuckGoSearchRun()
        result = search.run(query)
        return f"SEARCH RESULTS for '{query}':\n{result}"
    except Exception:
        try:
            import urllib.request, urllib.parse
            url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                return f"Search completed for: {query}"
        except Exception as e:
            return f"Search attempted for '{query}'. Result: Unable to connect. Try manually searching this term."

web_search_tool = Tool(
    name="web_search",
    func=_web_search,
    description="Search the internet for current information about PNG markets, suppliers, competitors."
)


def _market_research(query: str) -> str:
    results = {}
    for suffix in ["market size", "competitors Papua New Guinea", "customer demographics", "pricing"]:
        results[suffix] = _web_search(f"{query} {suffix}")
    return json.dumps({"query": query, "research": results}, indent=2)

market_research_tool = Tool(
    name="market_research",
    func=_market_research,
    description="Structured market research on PNG business topics. Input: topic or business area."
)


def _content_writer(brief: str) -> str:
    return json.dumps({
        "brief": brief,
        "instruction": "Write complete, publication-ready content. PNG cultural pride tone. No placeholders.",
        "voice": "Warm, proud, authentic Papua New Guinean",
        "status": "ready_to_write"
    }, indent=2)

content_writer_tool = Tool(
    name="content_writer",
    func=_content_writer,
    description="Frame a content writing task. Input: detailed brief with content type, channel, audience, tone."
)


def _financial_model(parameters: str) -> str:
    try:
        params = json.loads(parameters)
    except Exception:
        params = {}

    monthly_revenue = params.get("monthly_revenue_pgk", 10000)
    growth_rate     = params.get("monthly_growth_rate", 0.10)
    monthly_costs   = params.get("monthly_costs_pgk", 6000)
    months          = params.get("projection_months", 12)

    projections = []
    revenue = monthly_revenue
    for m in range(1, months + 1):
        profit = revenue - monthly_costs
        projections.append({
            "month": m,
            "revenue_pgk": round(revenue, 2),
            "costs_pgk": monthly_costs,
            "profit_pgk": round(profit, 2),
            "profit_aud": round(profit / 3.8, 2),
            "profit_usd": round(profit / 4.1, 2),
        })
        revenue = revenue * (1 + growth_rate)

    total_revenue = sum(p["revenue_pgk"] for p in projections)
    total_profit  = sum(p["profit_pgk"]  for p in projections)

    return json.dumps({
        "projections": projections,
        "summary": {
            "total_revenue_pgk": round(total_revenue, 2),
            "total_profit_pgk":  round(total_profit, 2),
            "break_even_month":  next((p["month"] for p in projections if p["profit_pgk"] > 0), "N/A")
        }
    }, indent=2)

financial_model_tool = Tool(
    name="financial_model",
    func=_financial_model,
    description="Build PNG business financial projections in PGK/AUD/USD. Input: JSON with revenue, costs, growth rate, months."
)


def _competitor_analysis(business_type: str) -> str:
    result = _web_search(f"{business_type} competitors Papua New Guinea online")
    return json.dumps({"business_type": business_type, "competitor_data": result}, indent=2)

competitor_analysis_tool = Tool(
    name="competitor_analysis",
    func=_competitor_analysis,
    description="Research PNG market competitors. Input: business type or product category."
)


def _customer_insight(segment: str) -> str:
    result = _web_search(f"{segment} buying behavior Papua New Guinea")
    return json.dumps({
        "segment": segment,
        "insights": result,
        "png_context": {
            "primary_social": "Facebook dominates PNG",
            "payment": "BSP Bank, Kina Bank, mobile money",
            "connectivity": "Variable — optimize for low bandwidth"
        }
    }, indent=2)

customer_insight_tool = Tool(
    name="customer_insight",
    func=_customer_insight,
    description="Research PNG customer segment behaviors. Input: customer segment description."
)


def _logistics(route: str) -> str:
    return json.dumps({
        "route": route,
        "png_carriers": [
            "Air Niugini Cargo — domestic + Pacific",
            "EMS Post PNG — domestic postal",
            "DHL Express — international",
            "Toll Group — bulk freight PNG",
            "Pacific Direct Line — sea freight Pacific"
        ],
        "china_to_png": {
            "sea_freight": "25-35 days via Brisbane",
            "air_freight": "5-10 days, more expensive",
            "recommended": "Sea freight for machinery, air for samples"
        }
    }, indent=2)

logistics_tool = Tool(
    name="logistics",
    func=_logistics,
    description="PNG shipping and logistics options. Input: route description."
)


def _legal_check(topic: str) -> str:
    result = _web_search(f"{topic} legal requirements Papua New Guinea")
    return json.dumps({
        "topic": topic,
        "research": result,
        "png_authorities": {
            "IPA":  "Investment Promotion Authority — business registration",
            "IRC":  "Internal Revenue Commission — tax",
            "BPNG": "Bank of PNG — financial regulations"
        },
        "disclaimer": "Research only. Consult a PNG-licensed lawyer for binding advice."
    }, indent=2)

legal_check_tool = Tool(
    name="legal_check",
    func=_legal_check,
    description="PNG legal and compliance research. Input: legal topic."
)


def _social_media(task: str) -> str:
    return json.dumps({
        "task": task,
        "png_platforms": {
            "primary": "Facebook (70%+ of PNG social users)",
            "visual":  "Instagram (tourism + fashion)",
            "video":   "TikTok (under-35s, fast growing)"
        },
        "posting_frequency": {
            "Facebook":  "1-2x per day",
            "Instagram": "5-7 Reels/week",
            "TikTok":    "1-3x per day"
        }
    }, indent=2)

social_media_tool = Tool(
    name="social_media",
    func=_social_media,
    description="PNG social media planning. Input: specific social task."
)


def _email(brief: str) -> str:
    return json.dumps({
        "brief": brief,
        "structure": {
            "subject": "Clear, under 60 chars",
            "greeting": "Professional but warm (PNG culture values warmth)",
            "body": "Purpose → Details → Action → Timeline",
            "closing": "Professional PNG sign-off"
        },
        "note": "All emails require human approval before sending"
    }, indent=2)

email_tool = Tool(
    name="email",
    func=_email,
    description="Draft business emails for PNG context. Input: email brief."
)
