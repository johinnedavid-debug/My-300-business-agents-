"""
PNG Agent OS — Main Orchestrator
Entry point: run this file to activate your 300-agent business swarm
"""

import os
import sys
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from crewai import Crew, Process
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

from agents.agent_definitions import build_tourism_crew, build_fashion_crew
from tasks.task_definitions import (
    get_tourism_startup_tasks,
    get_fashion_startup_tasks
)

load_dotenv()
console = Console()


# ─────────────────────────────────────────────────────────────
# STARTUP BANNER
# ─────────────────────────────────────────────────────────────

def print_banner():
    console.print(Panel.fit(
        """
[bold cyan]  ██████╗ ███╗   ██╗ ██████╗      █████╗  ██████╗ ███████╗
  ██╔══██╗████╗  ██║██╔════╝     ██╔══██╗██╔════╝ ██╔════╝
  ██████╔╝██╔██╗ ██║██║  ███╗    ███████║██║  ███╗█████╗  
  ██╔═══╝ ██║╚██╗██║██║   ██║    ██╔══██║██║   ██║██╔══╝  
  ██║     ██║ ╚████║╚██████╔╝    ██║  ██║╚██████╔╝███████╗
  ╚═╝     ╚═╝  ╚═══╝ ╚═════╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝[/bold cyan]
                                                             
  [bold white]300-Agent Business Intelligence System[/bold white]
  [dim]Papua New Guinea | Tourism + Fashion + Education[/dim]
        """,
        title="[bold cyan]AGENT OS v1.0[/bold cyan]",
        border_style="cyan"
    ))


# ─────────────────────────────────────────────────────────────
# SYSTEM STATUS CHECK
# ─────────────────────────────────────────────────────────────

def check_system_status():
    console.print("\n[bold]System Status Check[/bold]")
    checks = {
        "Anthropic API Key":    bool(os.getenv("ANTHROPIC_API_KEY")),
        "OpenAI API Key":       bool(os.getenv("OPENAI_API_KEY")),
        "Business Config":      bool(os.getenv("ACTIVE_BUSINESS")),
        "Target Market":        bool(os.getenv("TARGET_MARKET")),
    }
    
    table = Table(show_header=False, border_style="dim")
    table.add_column("Check", style="dim")
    table.add_column("Status")
    
    all_ok = True
    for check, status in checks.items():
        icon = "[green]✓[/green]" if status else "[red]✗[/red]"
        table.add_row(check, icon)
        if not status and check in ["Anthropic API Key"]:
            all_ok = False
    
    console.print(table)
    
    if not all_ok:
        console.print("\n[red]ERROR: Required API keys missing.[/red]")
        console.print("Copy [cyan].env.example[/cyan] to [cyan].env[/cyan] and add your keys.")
        sys.exit(1)
    
    console.print("[green]All systems operational.[/green]\n")
    return True


# ─────────────────────────────────────────────────────────────
# CREW BUILDER
# ─────────────────────────────────────────────────────────────

def build_crew(business: str, agents: dict, tasks: list) -> Crew:
    """Assemble a CrewAI Crew from agent and task definitions"""
    
    # Flatten agents into a list for CrewAI
    all_agents = []
    for tier in agents.values():
        for agent in tier.values():
            all_agents.append(agent)
    
    return Crew(
        agents=all_agents,
        tasks=tasks,
        process=Process.hierarchical,        # Tier 1 delegates down
        manager_agent=agents["tier1"]["commander"],
        verbose=2,
        memory=True,
        embedder={
            "provider": "openai",
            "config": {"model": "text-embedding-3-small"}
        },
        output_log_file=f"logs/{business}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )


# ─────────────────────────────────────────────────────────────
# RESULT FORMATTER
# ─────────────────────────────────────────────────────────────

def save_results(business: str, results: dict):
    """Save agent outputs to organized files"""
    os.makedirs(f"outputs/{business}", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    output_file = f"outputs/{business}/results_{timestamp}.json"
    with open(output_file, "w") as f:
        json.dump({
            "business":   business,
            "timestamp":  timestamp,
            "results":    results
        }, f, indent=2, default=str)
    
    console.print(f"\n[green]Results saved to:[/green] [cyan]{output_file}[/cyan]")
    return output_file


# ─────────────────────────────────────────────────────────────
# RUN A SINGLE BUSINESS
# ─────────────────────────────────────────────────────────────

def run_business(business_name: str):
    console.print(Panel(
        f"[bold white]Activating Agent Swarm[/bold white]\n"
        f"[cyan]Business:[/cyan] {business_name}\n"
        f"[cyan]Mode:[/cyan] Hierarchical 5-Tier Execution\n"
        f"[cyan]Started:[/cyan] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        border_style="cyan"
    ))
    
    start_time = time.time()
    
    if "Tourism" in business_name or "tourism" in business_name.lower():
        agents = build_tourism_crew()
        tasks  = get_tourism_startup_tasks(agents)
        key    = "tourism"
    else:
        agents = build_fashion_crew()
        tasks  = get_fashion_startup_tasks(agents)
        key    = "fashion"
    
    console.print(f"\n[dim]Agents loaded:[/dim] [cyan]{sum(len(t.values()) for t in agents.values())}[/cyan]")
    console.print(f"[dim]Tasks queued:[/dim]  [cyan]{len(tasks)}[/cyan]\n")
    
    crew = build_crew(key, agents, tasks)
    
    console.print("[bold yellow]► Swarm activating. Agent communication started...[/bold yellow]\n")
    
    try:
        result = crew.kickoff()
        
        elapsed = time.time() - start_time
        console.print(f"\n[green]✓ Mission complete![/green] ({elapsed:.1f}s)")
        
        # Save outputs
        save_results(key, {"final_output": str(result)})
        
        console.print(Panel(
            str(result)[:2000] + ("..." if len(str(result)) > 2000 else ""),
            title=f"[bold green]Agent Output — {business_name}[/bold green]",
            border_style="green"
        ))
        
        return result
        
    except Exception as e:
        console.print(f"\n[red]Error during execution: {str(e)}[/red]")
        console.print("[yellow]Check logs/ directory for detailed trace.[/yellow]")
        raise


# ─────────────────────────────────────────────────────────────
# INTERACTIVE COMMAND MODE
# ─────────────────────────────────────────────────────────────

def interactive_mode():
    """Allow David to type a goal and have the swarm execute it"""
    console.print("\n[bold cyan]INTERACTIVE MODE[/bold cyan]")
    console.print("Type a business goal and the agent swarm will execute it.")
    console.print("Type [bold]'exit'[/bold] to quit.\n")
    
    while True:
        goal = console.input("[bold cyan]David → Swarm:[/bold cyan] ").strip()
        
        if goal.lower() in ['exit', 'quit', 'q']:
            console.print("[dim]Swarm standing by. Goodbye.[/dim]")
            break
        
        if not goal:
            continue
        
        # Detect which business this goal relates to
        tourism_keywords = ["tourism", "souvenir", "artisan", "tourist", "bilum sale", "marketplace"]
        fashion_keywords = ["fashion", "meri blouse", "bilum", "clothing", "china", "machine", "sewing"]
        
        if any(k in goal.lower() for k in tourism_keywords):
            business = "PNG Souvenir & Tourism Platform"
        elif any(k in goal.lower() for k in fashion_keywords):
            business = "PNG Meri Blouse & Bilum Fashion Venture"
        else:
            business = "PNG Enterprises (Tourism + Fashion)"
        
        console.print(f"\n[dim]Routing to:[/dim] [cyan]{business}[/cyan]")
        console.print("[dim]Activating agent swarm...[/dim]\n")
        
        if "Tourism" in business or "tourism" in business.lower():
            agents = build_tourism_crew()
        else:
            agents = build_fashion_crew()
        
        # Create a custom task for the user's goal
        from crewai import Task
        custom_task = Task(
            description=f"""
            The business owner (David) has given this goal:
            
            "{goal}"
            
            Analyze this goal and execute it completely. Break it into
            sub-tasks if needed, delegate to the right specialists, and
            return a comprehensive, actionable result. Never return
            vague advice — give specific, executable outputs.
            
            Business context: {business}
            Location: Papua New Guinea
            Owner: David (entrepreneur, developer, PNG cultural ambassador)
            """,
            agent=agents["tier1"]["commander"],
            expected_output="""
            A complete, actionable response to the goal including:
            - What was done / what was analyzed
            - Specific outputs (content, plans, data, recommendations)
            - Clear next steps for David to take
            - Any risks or considerations flagged
            """
        )
        
        all_agents = [a for tier in agents.values() for a in tier.values()]
        crew = Crew(
            agents=all_agents,
            tasks=[custom_task],
            process=Process.hierarchical,
            manager_agent=agents["tier1"]["commander"],
            verbose=1,
            memory=True
        )
        
        try:
            result = crew.kickoff()
            console.print(Panel(
                str(result),
                title="[bold green]Swarm Output[/bold green]",
                border_style="green"
            ))
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")


# ─────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────

def main():
    print_banner()
    check_system_status()
    
    console.print("[bold]Select mode:[/bold]")
    console.print("  [cyan]1[/cyan] — Run Tourism Platform startup tasks")
    console.print("  [cyan]2[/cyan] — Run Fashion Venture startup tasks")
    console.print("  [cyan]3[/cyan] — Run BOTH businesses (sequential)")
    console.print("  [cyan]4[/cyan] — Interactive mode (type your own goals)")
    
    choice = console.input("\n[bold cyan]Enter choice (1-4):[/bold cyan] ").strip()
    
    os.makedirs("logs", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    
    if choice == "1":
        run_business("PNG Souvenir & Tourism Platform")
    
    elif choice == "2":
        run_business("PNG Meri Blouse & Bilum Fashion Venture")
    
    elif choice == "3":
        console.print("\n[bold yellow]Running BOTH businesses sequentially...[/bold yellow]")
        run_business("PNG Souvenir & Tourism Platform")
        console.print("\n[bold yellow]Switching to Fashion Venture...[/bold yellow]\n")
        run_business("PNG Meri Blouse & Bilum Fashion Venture")
    
    elif choice == "4":
        interactive_mode()
    
    else:
        console.print("[red]Invalid choice. Run again.[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
