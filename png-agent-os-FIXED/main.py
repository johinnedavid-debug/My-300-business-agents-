"""
PNG Agent OS — Main Entry Point (Phase 1, Windows Compatible)
"""

import os
import sys
import json
from datetime import datetime

# Load env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── CHECK API KEY ──────────────────────────────────────────
api_key = os.getenv("ANTHROPIC_API_KEY", "")
if not api_key or api_key == "your_anthropic_api_key_here":
    print("\n" + "="*55)
    print("  PNG AGENT OS — SETUP REQUIRED")
    print("="*55)
    print("\n  Your ANTHROPIC_API_KEY is not set.")
    print("  Open your .env file and replace:")
    print("  ANTHROPIC_API_KEY=your_anthropic_api_key_here")
    print("  with your real key from console.anthropic.com\n")
    sys.exit(1)

# ── BANNER ────────────────────────────────────────────────
def print_banner():
    print("\n" + "="*55)
    print("  PNG AGENT OS v1.0")
    print("  300-Agent Business Intelligence System")
    print("  Papua New Guinea | Tourism + Fashion")
    print("="*55)
    print(f"  API Key: {api_key[:12]}...{api_key[-4:]} ✓")
    print(f"  Time:    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*55 + "\n")

# ── IMPORT CREWAI ─────────────────────────────────────────
try:
    from crewai import Crew, Process, Agent, Task
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    print("[WARNING] crewai not fully installed. Running in DEMO mode.")

# ── DEMO MODE (if crewai not available) ───────────────────
def run_demo_mode(goal: str, business: str):
    """
    Simulates agent swarm output using direct Anthropic API calls.
    Works even without crewai installed.
    """
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        print(f"\n{'='*55}")
        print(f"  SUPREME COMMANDER — Analyzing goal...")
        print(f"{'='*55}")

        # Tier 1 — Commander decomposes goal
        commander_prompt = f"""
You are the Supreme Commander AI agent for a PNG business OS.
Business: {business}
Owner: David (entrepreneur in Papua New Guinea)

Goal received: "{goal}"

You are running a 5-tier agent swarm:
- Tier 1 (You): Supreme Commander — decompose and delegate
- Tier 2: Department Chiefs (Marketing, Finance, Tech, Operations, Sales, Legal, CX, Innovation, Supply Chain)
- Tier 3: Division Managers
- Tier 4: Specialist Agents  
- Tier 5: Execution Agents

Step 1: Decompose this goal into 3-5 strategic initiatives.
Step 2: Assign each to the right department chief.
Step 3: For each initiative, show what the specialist agents will produce.

Be specific to Papua New Guinea context:
- Primary social platform: Facebook
- Payments: BSP Bank, Kina Bank
- Currency: PGK (Papua New Guinea Kina)
- Cultural values: community, warmth, PNG pride

Produce a complete, actionable output as if all agents have executed their tasks.
"""
        print("\n[TIER 1] Supreme Commander thinking...\n")
        
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            messages=[{"role": "user", "content": commander_prompt}]
        )
        
        result = response.content[0].text
        print(result)

        # Save output
        os.makedirs("outputs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"outputs/result_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"GOAL: {goal}\n")
            f.write(f"BUSINESS: {business}\n")
            f.write(f"TIME: {timestamp}\n")
            f.write("="*55 + "\n")
            f.write(result)
        
        print(f"\n{'='*55}")
        print(f"  Output saved to: {filename}")
        print(f"{'='*55}\n")

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        print("Check your ANTHROPIC_API_KEY in .env file")


# ── MAIN MENU ─────────────────────────────────────────────
def main():
    print_banner()

    print("  Select mode:")
    print("  1 — Tourism Platform tasks")
    print("  2 — Fashion Venture tasks")
    print("  3 — Both businesses")
    print("  4 — Interactive (type your own goal)")
    print()

    choice = input("  Enter choice (1-4): ").strip()

    os.makedirs("outputs", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    if choice == "1":
        goal = "Analyze the PNG souvenir and tourism platform market, identify top product categories, find artisan suppliers, and create a 30-day launch plan"
        business = "PNG Souvenir & Tourism Platform"
        run_demo_mode(goal, business)

    elif choice == "2":
        goal = "Research China machinery suppliers for industrial knitting and weaving, build financial projections for the Meri Blouse and Bilum fashion venture, and create brand identity options"
        business = "PNG Meri Blouse & Bilum Fashion Venture"
        run_demo_mode(goal, business)

    elif choice == "3":
        print("\n  Running Tourism Platform first...\n")
        run_demo_mode(
            "Analyze PNG tourism market and create launch strategy",
            "PNG Souvenir & Tourism Platform"
        )
        print("\n  Now running Fashion Venture...\n")
        run_demo_mode(
            "Research China machinery and build PNG fashion brand",
            "PNG Meri Blouse & Bilum Fashion Venture"
        )

    elif choice == "4":
        print("\n  INTERACTIVE MODE")
        print("  Type your business goal. The agent swarm will execute it.")
        print("  Type 'exit' to quit.\n")

        businesses = {
            "1": "PNG Souvenir & Tourism Platform",
            "2": "PNG Meri Blouse & Bilum Fashion Venture",
            "3": "Both PNG Businesses"
        }

        print("  Which business?")
        print("  1 — Tourism Platform")
        print("  2 — Fashion Venture")
        print("  3 — Both")
        biz_choice = input("\n  Choose (1-3): ").strip()
        business = businesses.get(biz_choice, "PNG Businesses")

        while True:
            print()
            goal = input("  David → Swarm: ").strip()
            if goal.lower() in ['exit', 'quit', 'q']:
                print("\n  Swarm standing by. Goodbye.\n")
                break
            if goal:
                run_demo_mode(goal, business)
    else:
        print("\n  Invalid choice. Please run again and enter 1, 2, 3, or 4.\n")


if __name__ == "__main__":
    main()
