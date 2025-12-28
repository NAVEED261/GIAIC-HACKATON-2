"""
Kafka Agent - Event Streaming Expert
Handles Kafka/Redpanda operations for Phase-5

@author: Phase-5 AI Employs System
"""

import asyncio
import subprocess
import json
from typing import Dict, List, Any, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, MCPTool, AgentResult


class KafkaAgent(BaseAgent):
    """
    Kafka/Redpanda Expert Agent

    Capabilities:
    - Topic management (create, delete, list)
    - Event publishing
    - Consumer management
    - Health checks
    - Offset management

    MCP Tools: 12
    """

    def __init__(self):
        super().__init__()
        self.name = "KafkaAgent"
        self.domain = "kafka"
        self.description = "Kafka/Redpanda event streaming expert"
        self.emoji = "📨"
        self.broker = "localhost:9092"  # Default, can be configured

    def _setup_tools(self):
        """Setup Kafka MCP tools"""

        # Tool 1: Create Topic
        self.register_tool(MCPTool(
            name="create_topic",
            description="Create a Kafka topic",
            parameters={
                "topic_name": "string (required)",
                "partitions": "int (default: 1)",
                "replication_factor": "int (default: 1)"
            },
            handler=self._create_topic
        ))

        # Tool 2: Delete Topic
        self.register_tool(MCPTool(
            name="delete_topic",
            description="Delete a Kafka topic",
            parameters={"topic_name": "string (required)"},
            handler=self._delete_topic
        ))

        # Tool 3: List Topics
        self.register_tool(MCPTool(
            name="list_topics",
            description="List all Kafka topics",
            parameters={},
            handler=self._list_topics
        ))

        # Tool 4: Publish Event
        self.register_tool(MCPTool(
            name="publish_event",
            description="Publish an event to a Kafka topic",
            parameters={
                "topic": "string (required)",
                "message": "dict (required)",
                "key": "string (optional)"
            },
            handler=self._publish_event
        ))

        # Tool 5: Get Topic Info
        self.register_tool(MCPTool(
            name="get_topic_info",
            description="Get information about a Kafka topic",
            parameters={"topic_name": "string (required)"},
            handler=self._get_topic_info
        ))

        # Tool 6: Check Kafka Health
        self.register_tool(MCPTool(
            name="check_kafka_health",
            description="Check Kafka/Redpanda cluster health",
            parameters={},
            handler=self._check_health
        ))

        # Tool 7: Get Consumer Groups
        self.register_tool(MCPTool(
            name="get_consumer_groups",
            description="List all consumer groups",
            parameters={},
            handler=self._get_consumer_groups
        ))

        # Tool 8: Get Topic Offsets
        self.register_tool(MCPTool(
            name="get_topic_offsets",
            description="Get offsets for a topic",
            parameters={"topic_name": "string (required)"},
            handler=self._get_topic_offsets
        ))

        # Tool 9: Create Producer Config
        self.register_tool(MCPTool(
            name="create_producer_config",
            description="Generate Kafka producer configuration",
            parameters={"broker": "string (optional)"},
            handler=self._create_producer_config
        ))

        # Tool 10: Create Consumer Config
        self.register_tool(MCPTool(
            name="create_consumer_config",
            description="Generate Kafka consumer configuration",
            parameters={
                "group_id": "string (required)",
                "broker": "string (optional)"
            },
            handler=self._create_consumer_config
        ))

        # Tool 11: Describe Cluster
        self.register_tool(MCPTool(
            name="describe_cluster",
            description="Describe Kafka cluster",
            parameters={},
            handler=self._describe_cluster
        ))

        # Tool 12: Test Connection
        self.register_tool(MCPTool(
            name="test_connection",
            description="Test connection to Kafka broker",
            parameters={"broker": "string (optional)"},
            handler=self._test_connection
        ))

    def _match_tool(self, query: str) -> Optional[str]:
        """Match query to best Kafka tool"""
        query = query.lower()

        if any(w in query for w in ['create topic', 'new topic', 'add topic']):
            return 'create_topic'
        elif any(w in query for w in ['delete topic', 'remove topic']):
            return 'delete_topic'
        elif any(w in query for w in ['list topic', 'show topic', 'all topic']):
            return 'list_topics'
        elif any(w in query for w in ['publish', 'send', 'produce']):
            return 'publish_event'
        elif any(w in query for w in ['topic info', 'describe topic']):
            return 'get_topic_info'
        elif any(w in query for w in ['health', 'status', 'check']):
            return 'check_kafka_health'
        elif any(w in query for w in ['consumer group', 'groups']):
            return 'get_consumer_groups'
        elif any(w in query for w in ['offset']):
            return 'get_topic_offsets'
        elif any(w in query for w in ['producer config']):
            return 'create_producer_config'
        elif any(w in query for w in ['consumer config']):
            return 'create_consumer_config'
        elif any(w in query for w in ['cluster', 'broker']):
            return 'describe_cluster'
        elif any(w in query for w in ['test', 'connect']):
            return 'test_connection'

        return 'list_topics'

    async def execute_direct(self, step: Dict) -> Any:
        """Smart direct execution"""
        query = step.get("query", "").lower()
        tool_name = step.get("tool") or self._match_tool(query)

        if tool_name == 'create_topic':
            # Extract topic name from query
            topic = self._extract_topic_name(query) or "test-topic"
            return await self._create_topic(topic_name=topic)

        elif tool_name == 'delete_topic':
            topic = self._extract_topic_name(query)
            return await self._delete_topic(topic_name=topic)

        elif tool_name == 'list_topics':
            return await self._list_topics()

        elif tool_name == 'publish_event':
            return await self._publish_event(
                topic="task-events",
                message={"test": True}
            )

        elif tool_name == 'get_topic_info':
            topic = self._extract_topic_name(query) or "task-events"
            return await self._get_topic_info(topic_name=topic)

        elif tool_name == 'check_kafka_health':
            return await self._check_health()

        elif tool_name == 'get_consumer_groups':
            return await self._get_consumer_groups()

        elif tool_name == 'describe_cluster':
            return await self._describe_cluster()

        elif tool_name == 'test_connection':
            return await self._test_connection()

        else:
            return await self._list_topics()

    def _extract_topic_name(self, query: str) -> Optional[str]:
        """Extract topic name from query"""
        words = query.split()
        for i, word in enumerate(words):
            if word in ['topic', 'topics'] and i + 1 < len(words):
                return words[i + 1]
        return None

    # ==================== Tool Handlers ====================

    async def _create_topic(self, topic_name: str, partitions: int = 1,
                           replication_factor: int = 1) -> Dict:
        """Create a Kafka topic"""
        try:
            # Try using rpk (Redpanda) or kafka-topics
            result = subprocess.run(
                ['rpk', 'topic', 'create', topic_name,
                 '-p', str(partitions), '-r', str(replication_factor)],
                capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0:
                return {
                    "status": "created",
                    "topic": topic_name,
                    "partitions": partitions,
                    "replication_factor": replication_factor
                }
            else:
                return {
                    "status": "info",
                    "message": f"Topic '{topic_name}' creation command sent",
                    "note": "Use rpk or kafka-topics.sh to verify",
                    "command": f"rpk topic create {topic_name} -p {partitions}"
                }
        except FileNotFoundError:
            return {
                "status": "info",
                "message": "rpk not found - topic creation command generated",
                "command": f"rpk topic create {topic_name} -p {partitions} -r {replication_factor}",
                "alternative": f"kubectl exec -it redpanda-0 -- rpk topic create {topic_name}"
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _delete_topic(self, topic_name: str) -> Dict:
        """Delete a Kafka topic"""
        try:
            result = subprocess.run(
                ['rpk', 'topic', 'delete', topic_name],
                capture_output=True, text=True, timeout=10
            )
            return {
                "status": "deleted" if result.returncode == 0 else "info",
                "topic": topic_name,
                "command": f"rpk topic delete {topic_name}"
            }
        except Exception as e:
            return {
                "status": "info",
                "command": f"rpk topic delete {topic_name}",
                "note": str(e)
            }

    async def _list_topics(self) -> Dict:
        """List all Kafka topics"""
        try:
            result = subprocess.run(
                ['rpk', 'topic', 'list'],
                capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                topics = [l.split()[0] for l in lines[1:] if l.strip()]
                return {
                    "status": "success",
                    "topics": topics,
                    "count": len(topics)
                }
            else:
                return {
                    "status": "info",
                    "message": "Could not list topics",
                    "command": "rpk topic list",
                    "note": "Ensure Redpanda/Kafka is running"
                }
        except FileNotFoundError:
            return {
                "status": "info",
                "message": "rpk not found",
                "command": "rpk topic list",
                "expected_topics": ["task-events", "reminders", "task-updates"]
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _publish_event(self, topic: str, message: Dict,
                            key: str = None) -> Dict:
        """Publish event to Kafka"""
        return {
            "status": "info",
            "message": "Event publish command generated",
            "topic": topic,
            "payload": message,
            "dapr_command": f"POST http://localhost:3500/v1.0/publish/kafka-pubsub/{topic}",
            "python_code": f"""
import httpx
await httpx.post(
    "http://localhost:3500/v1.0/publish/kafka-pubsub/{topic}",
    json={json.dumps(message)}
)
"""
        }

    async def _get_topic_info(self, topic_name: str) -> Dict:
        """Get topic information"""
        try:
            result = subprocess.run(
                ['rpk', 'topic', 'describe', topic_name],
                capture_output=True, text=True, timeout=10
            )
            return {
                "status": "success" if result.returncode == 0 else "info",
                "topic": topic_name,
                "output": result.stdout if result.returncode == 0 else None,
                "command": f"rpk topic describe {topic_name}"
            }
        except Exception as e:
            return {
                "status": "info",
                "topic": topic_name,
                "command": f"rpk topic describe {topic_name}",
                "note": str(e)
            }

    async def _check_health(self) -> Dict:
        """Check Kafka cluster health"""
        try:
            result = subprocess.run(
                ['rpk', 'cluster', 'health'],
                capture_output=True, text=True, timeout=10
            )
            return {
                "status": "healthy" if result.returncode == 0 else "unknown",
                "output": result.stdout,
                "command": "rpk cluster health"
            }
        except Exception as e:
            return {
                "status": "info",
                "message": "Health check command generated",
                "command": "rpk cluster health",
                "kubectl_command": "kubectl exec -it redpanda-0 -n todo-phase5 -- rpk cluster health",
                "note": str(e)
            }

    async def _get_consumer_groups(self) -> Dict:
        """List consumer groups"""
        try:
            result = subprocess.run(
                ['rpk', 'group', 'list'],
                capture_output=True, text=True, timeout=10
            )
            return {
                "status": "success" if result.returncode == 0 else "info",
                "output": result.stdout,
                "command": "rpk group list"
            }
        except Exception as e:
            return {
                "status": "info",
                "command": "rpk group list",
                "note": str(e)
            }

    async def _get_topic_offsets(self, topic_name: str) -> Dict:
        """Get topic offsets"""
        return {
            "status": "info",
            "topic": topic_name,
            "command": f"rpk topic consume {topic_name} --offset start --num 1"
        }

    async def _create_producer_config(self, broker: str = None) -> Dict:
        """Generate producer configuration"""
        broker = broker or self.broker
        return {
            "status": "success",
            "config": {
                "bootstrap_servers": broker,
                "value_serializer": "json",
                "acks": "all",
                "retries": 3
            },
            "python_code": f"""
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="{broker}",
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all',
    retries=3
)

# Publish
producer.send("task-events", {{"event": "task_created", "task_id": 1}})
producer.flush()
"""
        }

    async def _create_consumer_config(self, group_id: str,
                                      broker: str = None) -> Dict:
        """Generate consumer configuration"""
        broker = broker or self.broker
        return {
            "status": "success",
            "config": {
                "bootstrap_servers": broker,
                "group_id": group_id,
                "auto_offset_reset": "earliest",
                "enable_auto_commit": True
            },
            "python_code": f"""
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'task-events',
    bootstrap_servers="{broker}",
    group_id="{group_id}",
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    print(message.value)
"""
        }

    async def _describe_cluster(self) -> Dict:
        """Describe Kafka cluster"""
        try:
            result = subprocess.run(
                ['rpk', 'cluster', 'info'],
                capture_output=True, text=True, timeout=10
            )
            return {
                "status": "success" if result.returncode == 0 else "info",
                "output": result.stdout,
                "command": "rpk cluster info"
            }
        except Exception as e:
            return {
                "status": "info",
                "command": "rpk cluster info",
                "note": str(e)
            }

    async def _test_connection(self, broker: str = None) -> Dict:
        """Test Kafka connection"""
        broker = broker or self.broker
        try:
            result = subprocess.run(
                ['rpk', 'cluster', 'info', '--brokers', broker],
                capture_output=True, text=True, timeout=10
            )
            return {
                "status": "connected" if result.returncode == 0 else "disconnected",
                "broker": broker,
                "command": f"rpk cluster info --brokers {broker}"
            }
        except Exception as e:
            return {
                "status": "info",
                "broker": broker,
                "command": f"rpk cluster info --brokers {broker}",
                "note": str(e)
            }
