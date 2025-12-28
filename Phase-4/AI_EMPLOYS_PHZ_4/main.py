"""
POWERFUL Multi-Agent System - Main Runner
Orchestrator with 15+ Specialized Agents

@author: Phase-4 Multi-Agent System
"""

import asyncio
import sys
import os

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Add agent paths
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all agents
from orchestrator import Orchestrator

# Infrastructure Agents
from infrastructure.docker_agent import DockerAgent
from infrastructure.kubernetes_agent import KubernetesAgent
from infrastructure.helm_agent import HelmAgent
from infrastructure.network_agent import NetworkAgent

# Application Agents
from application.task_agent import TaskAgent
from application.chat_agent import ChatAgent
from application.auth_agent import AuthAgent
from application.database_agent import DatabaseAgent

# DevOps Agents
from devops.cicd_agent import CICDAgent
from devops.monitoring_agent import MonitoringAgent
from devops.security_agent import SecurityAgent
from devops.backup_agent import BackupAgent

# Expert Agents
from expert.architect_agent import ArchitectAgent
from expert.debugger_agent import DebuggerAgent
from expert.optimizer_agent import OptimizerAgent


def print_banner():
    """Print the system banner"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  {Fore.YELLOW}🤖 POWERFUL Multi-Agent System{Fore.CYAN}                                      ║
║  {Fore.WHITE}Phase-4 Todo Application Deployment & Management{Fore.CYAN}                   ║
║                                                                      ║
║  {Fore.GREEN}15+ Specialized Agents with MCP Tools{Fore.CYAN}                              ║
║  {Fore.GREEN}Self-Reasoning • Multi-Step Execution • Error Recovery{Fore.CYAN}             ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def create_orchestrator() -> Orchestrator:
    """Create and configure the orchestrator with all agents"""

    print(f"\n{Fore.YELLOW}🎯 Initializing Orchestrator...{Style.RESET_ALL}")
    orchestrator = Orchestrator()

    # Register Infrastructure Agents
    print(f"{Fore.CYAN}📦 Registering Infrastructure Agents...{Style.RESET_ALL}")
    orchestrator.register_agent(DockerAgent())
    orchestrator.register_agent(KubernetesAgent())
    orchestrator.register_agent(HelmAgent())
    orchestrator.register_agent(NetworkAgent())

    # Register Application Agents
    print(f"{Fore.GREEN}📱 Registering Application Agents...{Style.RESET_ALL}")
    orchestrator.register_agent(TaskAgent())
    orchestrator.register_agent(ChatAgent())
    orchestrator.register_agent(AuthAgent())
    orchestrator.register_agent(DatabaseAgent())

    # Register DevOps Agents
    print(f"{Fore.MAGENTA}🔧 Registering DevOps Agents...{Style.RESET_ALL}")
    orchestrator.register_agent(CICDAgent())
    orchestrator.register_agent(MonitoringAgent())
    orchestrator.register_agent(SecurityAgent())
    orchestrator.register_agent(BackupAgent())

    # Register Expert Agents
    print(f"{Fore.BLUE}🧠 Registering Expert Agents...{Style.RESET_ALL}")
    orchestrator.register_agent(ArchitectAgent())
    orchestrator.register_agent(DebuggerAgent())
    orchestrator.register_agent(OptimizerAgent())

    print(f"\n{Fore.GREEN}✅ All agents registered successfully!{Style.RESET_ALL}")

    return orchestrator


def print_agents(orchestrator: Orchestrator):
    """Print list of available agents"""
    print(f"\n{Fore.YELLOW}📋 Available Agents:{Style.RESET_ALL}")
    print("-" * 60)

    for name, agent in orchestrator.agents.items():
        status = agent.get_status()
        tools_count = status.get("tools_count", 0)
        print(f"  {status['emoji']} {Fore.CYAN}{name:15}{Style.RESET_ALL} │ {status['description'][:35]:35} │ Tools: {tools_count}")

    print("-" * 60)
    print(f"  {Fore.GREEN}Total: {len(orchestrator.agents)} agents{Style.RESET_ALL}")


async def interactive_mode(orchestrator: Orchestrator):
    """Run in interactive mode"""
    print(f"\n{Fore.GREEN}🚀 Interactive Mode{Style.RESET_ALL}")
    print("Type your query or command. Type 'help' for options, 'quit' to exit.\n")

    while True:
        try:
            # Get user input
            query = input(f"{Fore.YELLOW}You: {Style.RESET_ALL}").strip()

            if not query:
                continue

            if query.lower() in ['quit', 'exit', 'q']:
                print(f"\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}")
                break

            if query.lower() == 'help':
                print_help()
                continue

            if query.lower() == 'agents':
                print_agents(orchestrator)
                continue

            if query.lower() == 'status':
                await show_status(orchestrator)
                continue

            # Process the query - Delegate to specialist agent
            print(f"\n{Fore.CYAN}Processing...{Style.RESET_ALL}")
            result = await orchestrator.delegate(query)

            # Print result
            print(f"\n{Fore.GREEN}📤 Result:{Style.RESET_ALL}")
            if hasattr(result, 'to_dict'):
                result_dict = result.to_dict()
                if result_dict.get("success"):
                    print_result(result_dict.get("data", result_dict))
                else:
                    print(f"{Fore.RED}Error: {result_dict.get('error')}{Style.RESET_ALL}")
            elif isinstance(result, dict):
                if result.get("success"):
                    print_result(result.get("data", result))
                else:
                    print(f"{Fore.RED}Error: {result.get('error')}{Style.RESET_ALL}")
            else:
                print(result)

            print()

        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")


def print_help():
    """Print help information"""
    help_text = f"""
{Fore.YELLOW}Available Commands:{Style.RESET_ALL}
  help      - Show this help
  agents    - List all available agents
  status    - Show system status
  quit      - Exit the program

{Fore.YELLOW}Example Queries:{Style.RESET_ALL}
  {Fore.CYAN}Infrastructure:{Style.RESET_ALL}
    "Show me all pods in the todo namespace"
    "Check cluster health"
    "List docker containers"
    "Deploy helm chart"

  {Fore.CYAN}Application:{Style.RESET_ALL}
    "Create a new task: Complete Phase-4"
    "Show all tasks"
    "Login with email test@example.com"

  {Fore.CYAN}DevOps:{Style.RESET_ALL}
    "Run git status"
    "Check monitoring metrics"
    "Run security audit"
    "Create database backup"

  {Fore.CYAN}Expert:{Style.RESET_ALL}
    "Analyze architecture of this project"
    "Debug: pods are crashing"
    "Optimize resource usage"
"""
    print(help_text)


def print_result(data, indent=0):
    """Pretty print result data"""
    prefix = "  " * indent

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                print(f"{prefix}{Fore.CYAN}{key}:{Style.RESET_ALL}")
                print_result(value, indent + 1)
            else:
                print(f"{prefix}{Fore.CYAN}{key}:{Style.RESET_ALL} {value}")
    elif isinstance(data, list):
        for i, item in enumerate(data[:10]):  # Limit to 10 items
            if isinstance(item, (dict, list)):
                print(f"{prefix}[{i}]")
                print_result(item, indent + 1)
            else:
                print(f"{prefix}- {item}")
        if len(data) > 10:
            print(f"{prefix}... and {len(data) - 10} more")
    else:
        print(f"{prefix}{data}")


async def show_status(orchestrator: Orchestrator):
    """Show system status"""
    print(f"\n{Fore.YELLOW}📊 System Status:{Style.RESET_ALL}")
    print("-" * 40)

    for name, agent in orchestrator.agents.items():
        status = agent.get_status()
        working = "🟢" if status.get("is_working") else "⚪"
        print(f"  {working} {status['emoji']} {name}: {status['tools_count']} tools")

    print("-" * 40)


async def run_demo(orchestrator: Orchestrator):
    """Run a demo of the agent system"""
    print(f"\n{Fore.YELLOW}🎬 Running Demo...{Style.RESET_ALL}\n")

    demo_queries = [
        "Check cluster health",
        "Show all pods in todo namespace",
        "Get monitoring metrics for the namespace"
    ]

    for query in demo_queries:
        print(f"\n{Fore.CYAN}Demo Query: {query}{Style.RESET_ALL}")
        print("-" * 50)

        try:
            result = await orchestrator.process(query)

            if isinstance(result, dict) and result.get("success"):
                print(f"{Fore.GREEN}✅ Success{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Result received{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

        await asyncio.sleep(1)


async def main():
    """Main entry point"""
    print_banner()

    # Create orchestrator
    orchestrator = create_orchestrator()

    # Print available agents
    print_agents(orchestrator)

    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo":
            await run_demo(orchestrator)
        else:
            # Process single query via delegation
            query = " ".join(sys.argv[1:])
            print(f"\n{Fore.CYAN}Query: {query}{Style.RESET_ALL}")
            print("-" * 50)
            result = await orchestrator.delegate(query)
            print(f"\n{Fore.GREEN}📤 Result:{Style.RESET_ALL}")
            if hasattr(result, 'to_dict'):
                print_result(result.to_dict().get("data", result.to_dict()))
    else:
        # Interactive mode
        await interactive_mode(orchestrator)


if __name__ == "__main__":
    asyncio.run(main())
