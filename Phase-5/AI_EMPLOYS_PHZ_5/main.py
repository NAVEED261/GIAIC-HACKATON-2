"""
Phase-5 AI Employs System - Main Entry Point
Expert AI Agents for Todo Application

@author: Phase-5 AI Employs System
@version: 1.0.0

Usage:
    python main.py                    # Interactive mode
    python main.py --test             # Run all agent tests
    python main.py --query "your query"  # Single query mode
    python main.py --agent kafka      # Test specific agent
"""

import asyncio
import argparse
import json
from typing import Dict, List, Any

from orchestrator import AgentOrchestrator
from base_agent import AgentResult


def print_banner():
    """Print the AI Employs banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   ██████╗ ██╗  ██╗ █████╗ ███████╗███████╗    ███████╗               ║
║   ██╔══██╗██║  ██║██╔══██╗██╔════╝██╔════╝    ██╔════╝               ║
║   ██████╔╝███████║███████║███████╗█████╗      ███████╗               ║
║   ██╔═══╝ ██╔══██║██╔══██║╚════██║██╔══╝      ╚════██║               ║
║   ██║     ██║  ██║██║  ██║███████║███████╗    ███████║               ║
║   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚══════╝               ║
║                                                                       ║
║            AI EMPLOYS SYSTEM - Expert Domain Agents                   ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_agents_summary(orchestrator: AgentOrchestrator):
    """Print summary of all available agents"""
    print("\n" + "=" * 70)
    print("                    AVAILABLE AI EMPLOYS (Agents)")
    print("=" * 70)

    total_tools = 0

    for domain, agent in orchestrator.agents.items():
        tool_count = len(agent.tools)
        total_tools += tool_count
        print(f"\n  {agent.emoji} {agent.name}")
        print(f"     Domain: {domain}")
        print(f"     Description: {agent.description}")
        print(f"     MCP Tools: {tool_count}")

        # List tools
        tools_list = ", ".join(list(agent.tools.keys())[:5])
        if len(agent.tools) > 5:
            tools_list += f"... (+{len(agent.tools) - 5} more)"
        print(f"     Tools: {tools_list}")

    print("\n" + "-" * 70)
    print(f"  Total Agents: {len(orchestrator.agents)}")
    print(f"  Total MCP Tools: {total_tools}")
    print("=" * 70 + "\n")


async def run_single_query(orchestrator: AgentOrchestrator, query: str) -> Dict:
    """Run a single query through the orchestrator"""
    print(f"\n📝 Query: {query}")
    print("-" * 50)

    result = await orchestrator.delegate(query)

    print(f"\n✅ Agent Used: {result.agent}")
    print(f"🔧 Tool: {result.tool}")
    print(f"\n📊 Result:")
    print(json.dumps(result.result, indent=2, default=str))

    return result.result


async def run_interactive_mode(orchestrator: AgentOrchestrator):
    """Run in interactive mode"""
    print("\n🎯 Interactive Mode - Enter queries or commands")
    print("   Type 'help' for available commands")
    print("   Type 'exit' or 'quit' to exit\n")

    while True:
        try:
            query = input("\n🤖 Enter query: ").strip()

            if not query:
                continue

            if query.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break

            if query.lower() == 'help':
                print_help()
                continue

            if query.lower() == 'agents':
                print_agents_summary(orchestrator)
                continue

            if query.lower().startswith('tools '):
                domain = query.split()[1]
                await show_agent_tools(orchestrator, domain)
                continue

            # Process the query
            result = await orchestrator.delegate(query)

            print(f"\n  Agent: {result.agent} | Tool: {result.tool}")
            print(f"\n  Result:")
            print(json.dumps(result.result, indent=2, default=str))

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


def print_help():
    """Print help information"""
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                           HELP - Commands                             ║
╠═══════════════════════════════════════════════════════════════════════╣
║  agents          - Show all available agents                          ║
║  tools <domain>  - Show tools for a specific agent domain             ║
║  help            - Show this help message                             ║
║  exit/quit       - Exit the program                                   ║
╠═══════════════════════════════════════════════════════════════════════╣
║                       Example Queries                                 ║
╠═══════════════════════════════════════════════════════════════════════╣
║  "create kafka topic for tasks"     → KafkaAgent                      ║
║  "check dapr status"                → DaprAgent                       ║
║  "set task priority high"           → FeatureAgent                    ║
║  "create weekly recurring task"     → RecurringAgent                  ║
║  "set reminder for tomorrow"        → ReminderAgent                   ║
║  "deploy to kubernetes"             → K8sDeployAgent                  ║
║  "install helm chart"               → HelmAgent                       ║
║  "start minikube cluster"           → MinikubeAgent                   ║
╚═══════════════════════════════════════════════════════════════════════╝
""")


async def show_agent_tools(orchestrator: AgentOrchestrator, domain: str):
    """Show all tools for a specific agent"""
    agent = orchestrator.get_agent(domain)
    if not agent:
        print(f"\n❌ Agent not found for domain: {domain}")
        print(f"   Available domains: {', '.join(orchestrator.agents.keys())}")
        return

    print(f"\n{agent.emoji} {agent.name} - MCP Tools")
    print("=" * 50)

    for name, tool in agent.tools.items():
        print(f"\n  📦 {name}")
        print(f"     {tool.description}")
        if tool.parameters:
            print(f"     Parameters: {tool.parameters}")


async def run_agent_test(orchestrator: AgentOrchestrator,
                        agent_domain: str = None):
    """Run tests for agents"""
    print("\n🧪 Running Agent Tests")
    print("=" * 50)

    test_queries = {
        "kafka": [
            "list all kafka topics",
            "check kafka health",
            "create topic for task-events"
        ],
        "dapr": [
            "check dapr status",
            "list dapr components",
            "create pubsub component"
        ],
        "feature": [
            "set task priority to high",
            "search for tasks",
            "filter completed tasks"
        ],
        "recurring": [
            "create weekly recurring task",
            "get recurrence patterns",
            "calculate next occurrence"
        ],
        "reminder": [
            "set reminder for task",
            "get upcoming reminders",
            "get overdue tasks"
        ],
        "k8s": [
            "get pods in namespace",
            "get deployments",
            "check rollout status"
        ],
        "helm": [
            "list helm releases",
            "get helm status",
            "search for charts"
        ],
        "minikube": [
            "minikube status",
            "list minikube addons",
            "get minikube ip"
        ]
    }

    if agent_domain:
        if agent_domain not in test_queries:
            print(f"\n❌ Unknown agent domain: {agent_domain}")
            return
        test_queries = {agent_domain: test_queries[agent_domain]}

    passed = 0
    failed = 0

    for domain, queries in test_queries.items():
        print(f"\n📋 Testing {domain.upper()} Agent")
        print("-" * 40)

        for query in queries:
            try:
                result = await orchestrator.delegate(query)
                if result.success:
                    print(f"  ✅ {query}")
                    passed += 1
                else:
                    print(f"  ❌ {query}: {result.result}")
                    failed += 1
            except Exception as e:
                print(f"  ❌ {query}: {e}")
                failed += 1

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    print("=" * 50)


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Phase-5 AI Employs System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                         # Interactive mode
  python main.py --test                  # Run all tests
  python main.py --test --agent kafka    # Test Kafka agent
  python main.py --query "list topics"   # Single query
  python main.py --agents                # List all agents
        """
    )

    parser.add_argument('--test', action='store_true',
                       help='Run agent tests')
    parser.add_argument('--agent', type=str,
                       help='Specific agent domain to test')
    parser.add_argument('--query', '-q', type=str,
                       help='Single query to execute')
    parser.add_argument('--agents', action='store_true',
                       help='List all available agents')
    parser.add_argument('--json', action='store_true',
                       help='Output results as JSON')

    args = parser.parse_args()

    # Print banner
    print_banner()

    # Initialize orchestrator
    print("🔄 Initializing AI Employs System...")
    orchestrator = AgentOrchestrator()
    print(f"✅ Loaded {len(orchestrator.agents)} agents\n")

    # Handle different modes
    if args.agents:
        print_agents_summary(orchestrator)

    elif args.test:
        await run_agent_test(orchestrator, args.agent)

    elif args.query:
        result = await run_single_query(orchestrator, args.query)
        if args.json:
            print(json.dumps(result, indent=2, default=str))

    else:
        # Interactive mode
        print_agents_summary(orchestrator)
        await run_interactive_mode(orchestrator)


if __name__ == "__main__":
    asyncio.run(main())
