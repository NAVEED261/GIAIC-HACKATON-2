"""
Database Agent - POWERFUL Database Expert with MCP Tools
PostgreSQL, SQLite, migrations, queries, backups

@author: Phase-4 Multi-Agent System
"""

import asyncio
import json
from typing import Dict, Any, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, MCPTool, AgentResult


class DatabaseAgent(BaseAgent):
    """
    POWERFUL Database Expert Agent
    - Self-reasoning for complex queries
    - MCP Tools for all database operations
    - PostgreSQL & SQLite support
    - Migrations, backups, optimization
    """

    KEYWORDS = [
        'database', 'db', 'postgres', 'postgresql', 'sqlite', 'sql',
        'query', 'table', 'migration', 'backup', 'restore', 'schema',
        'index', 'connection', 'pool', 'transaction'
    ]

    def __init__(self, connection_string: str = None):
        super().__init__("Database", "Database operations expert - PostgreSQL, SQLite, migrations, optimization")
        self.connection_string = connection_string
        self._register_mcp_tools()

    def _register_mcp_tools(self):
        """Register all MCP tools for database operations"""

        # Tool: Execute SQL Query
        self.register_tool(MCPTool(
            name="execute_query",
            description="Execute a SQL query and return results",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "SQL query to execute"},
                    "database": {"type": "string", "description": "Database name or connection string"},
                    "params": {"type": "array", "description": "Query parameters"}
                },
                "required": ["query"]
            },
            handler=self._execute_query
        ))

        # Tool: List Tables
        self.register_tool(MCPTool(
            name="list_tables",
            description="List all tables in the database with row counts",
            parameters={
                "type": "object",
                "properties": {
                    "database": {"type": "string"},
                    "schema": {"type": "string", "description": "Schema name (default: public)"}
                }
            },
            handler=self._list_tables
        ))

        # Tool: Describe Table
        self.register_tool(MCPTool(
            name="describe_table",
            description="Get table structure including columns, types, constraints",
            parameters={
                "type": "object",
                "properties": {
                    "table": {"type": "string", "description": "Table name"},
                    "database": {"type": "string"}
                },
                "required": ["table"]
            },
            handler=self._describe_table
        ))

        # Tool: Check Connection
        self.register_tool(MCPTool(
            name="check_connection",
            description="Test database connection and get status",
            parameters={
                "type": "object",
                "properties": {
                    "database": {"type": "string"}
                }
            },
            handler=self._check_connection
        ))

        # Tool: Get Database Stats
        self.register_tool(MCPTool(
            name="get_db_stats",
            description="Get database statistics - size, connections, performance",
            parameters={
                "type": "object",
                "properties": {
                    "database": {"type": "string"}
                }
            },
            handler=self._get_db_stats
        ))

        # Tool: Create Backup
        self.register_tool(MCPTool(
            name="create_backup",
            description="Create a database backup",
            parameters={
                "type": "object",
                "properties": {
                    "database": {"type": "string"},
                    "output_path": {"type": "string", "description": "Backup file path"},
                    "format": {"type": "string", "description": "Backup format (sql, custom, tar)"}
                },
                "required": ["output_path"]
            },
            handler=self._create_backup
        ))

        # Tool: Restore Backup
        self.register_tool(MCPTool(
            name="restore_backup",
            description="Restore database from backup",
            parameters={
                "type": "object",
                "properties": {
                    "backup_path": {"type": "string", "description": "Backup file path"},
                    "database": {"type": "string"},
                    "clean": {"type": "boolean", "description": "Drop existing objects before restore"}
                },
                "required": ["backup_path"]
            },
            handler=self._restore_backup
        ))

        # Tool: Run Migrations
        self.register_tool(MCPTool(
            name="run_migrations",
            description="Run database migrations using Alembic",
            parameters={
                "type": "object",
                "properties": {
                    "direction": {"type": "string", "description": "upgrade or downgrade"},
                    "revision": {"type": "string", "description": "Target revision (head, -1, etc.)"},
                    "migrations_path": {"type": "string"}
                }
            },
            handler=self._run_migrations
        ))

        # Tool: Check Indexes
        self.register_tool(MCPTool(
            name="check_indexes",
            description="Analyze indexes - missing, unused, duplicates",
            parameters={
                "type": "object",
                "properties": {
                    "table": {"type": "string"},
                    "database": {"type": "string"}
                }
            },
            handler=self._check_indexes
        ))

        # Tool: Vacuum/Optimize
        self.register_tool(MCPTool(
            name="optimize_database",
            description="Vacuum and analyze tables for optimization",
            parameters={
                "type": "object",
                "properties": {
                    "table": {"type": "string", "description": "Specific table or all"},
                    "full": {"type": "boolean", "description": "Full vacuum (locks table)"},
                    "analyze": {"type": "boolean", "description": "Update statistics"}
                }
            },
            handler=self._optimize_database
        ))

        # Tool: Show Active Queries
        self.register_tool(MCPTool(
            name="show_active_queries",
            description="Show currently running queries",
            parameters={
                "type": "object",
                "properties": {
                    "database": {"type": "string"},
                    "min_duration": {"type": "integer", "description": "Minimum duration in seconds"}
                }
            },
            handler=self._show_active_queries
        ))

        # Tool: Kill Query
        self.register_tool(MCPTool(
            name="kill_query",
            description="Terminate a running query by PID",
            parameters={
                "type": "object",
                "properties": {
                    "pid": {"type": "integer", "description": "Process ID to terminate"},
                    "force": {"type": "boolean", "description": "Force terminate"}
                },
                "required": ["pid"]
            },
            handler=self._kill_query
        ))

    # ==================== TOOL IMPLEMENTATIONS ====================

    async def _run_cmd(self, cmd: str) -> str:
        """Execute shell command"""
        self.log(f"$ {cmd}", "working")

        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0 and stderr:
            raise Exception(stderr.decode())

        return stdout.decode()

    async def _execute_query(self, query: str, database: str = None, params: List = None, **kwargs) -> Dict:
        db = database or self.connection_string or "postgres"
        self.log(f"Executing query: {query[:80]}...", "working")

        # Use psql for PostgreSQL queries
        safe_query = query.replace("'", "\\'")
        cmd = f'psql "{db}" -c "{safe_query}" --csv'

        try:
            result = await self._run_cmd(cmd)
            lines = result.strip().split('\n')

            if len(lines) > 1:
                headers = lines[0].split(',')
                rows = [dict(zip(headers, line.split(','))) for line in lines[1:]]
                return {"rows": rows, "count": len(rows)}

            return {"result": result, "rows": []}
        except Exception as e:
            return {"error": str(e), "query": query}

    async def _list_tables(self, database: str = None, schema: str = "public", **kwargs) -> List[Dict]:
        db = database or self.connection_string or "postgres"

        query = f"""
        SELECT table_name,
               (SELECT COUNT(*) FROM {schema}."{{table_name}}") as row_count
        FROM information_schema.tables
        WHERE table_schema = '{schema}'
        ORDER BY table_name;
        """

        # Simplified approach
        cmd = f'psql "{db}" -c "SELECT table_name FROM information_schema.tables WHERE table_schema = \'{schema}\';" --csv'

        try:
            result = await self._run_cmd(cmd)
            tables = [t.strip() for t in result.strip().split('\n')[1:] if t.strip()]
            return [{"table": t, "schema": schema} for t in tables]
        except Exception as e:
            return [{"error": str(e)}]

    async def _describe_table(self, table: str, database: str = None, **kwargs) -> Dict:
        db = database or self.connection_string or "postgres"

        cmd = f'psql "{db}" -c "\\d+ {table}"'

        try:
            result = await self._run_cmd(cmd)
            return {"table": table, "description": result}
        except Exception as e:
            return {"error": str(e), "table": table}

    async def _check_connection(self, database: str = None, **kwargs) -> Dict:
        db = database or self.connection_string or "postgres"

        cmd = f'psql "{db}" -c "SELECT version();" --csv'

        try:
            result = await self._run_cmd(cmd)
            return {"connected": True, "version": result.strip().split('\n')[-1]}
        except Exception as e:
            return {"connected": False, "error": str(e)}

    async def _get_db_stats(self, database: str = None, **kwargs) -> Dict:
        db = database or self.connection_string or "postgres"

        stats_query = """
        SELECT
            pg_database.datname as database,
            pg_size_pretty(pg_database_size(pg_database.datname)) as size,
            numbackends as connections
        FROM pg_database
        JOIN pg_stat_database ON pg_database.datname = pg_stat_database.datname;
        """

        cmd = f'psql "{db}" -c "{stats_query}" --csv'

        try:
            result = await self._run_cmd(cmd)
            return {"stats": result}
        except Exception as e:
            return {"error": str(e)}

    async def _create_backup(self, output_path: str, database: str = None, format: str = "custom", **kwargs) -> Dict:
        db = database or self.connection_string or "postgres"

        format_flag = {"sql": "", "custom": "-Fc", "tar": "-Ft"}.get(format, "-Fc")
        cmd = f'pg_dump {format_flag} "{db}" > "{output_path}"'

        try:
            await self._run_cmd(cmd)
            return {"status": "backup_created", "path": output_path, "format": format}
        except Exception as e:
            return {"error": str(e)}

    async def _restore_backup(self, backup_path: str, database: str = None, clean: bool = False, **kwargs) -> Dict:
        db = database or self.connection_string or "postgres"

        clean_flag = "--clean" if clean else ""
        cmd = f'pg_restore {clean_flag} -d "{db}" "{backup_path}"'

        try:
            await self._run_cmd(cmd)
            return {"status": "restored", "backup": backup_path}
        except Exception as e:
            return {"error": str(e)}

    async def _run_migrations(self, direction: str = "upgrade", revision: str = "head", migrations_path: str = None, **kwargs) -> Dict:
        path = migrations_path or "."

        cmd = f'cd {path} && alembic {direction} {revision}'

        try:
            result = await self._run_cmd(cmd)
            return {"status": "migrations_applied", "direction": direction, "revision": revision, "output": result}
        except Exception as e:
            return {"error": str(e)}

    async def _check_indexes(self, table: str = None, database: str = None, **kwargs) -> Dict:
        db = database or self.connection_string or "postgres"

        query = """
        SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
        FROM pg_stat_user_indexes
        ORDER BY idx_scan DESC;
        """

        if table:
            query = f"""
            SELECT indexrelname, idx_scan, idx_tup_read
            FROM pg_stat_user_indexes
            WHERE relname = '{table}';
            """

        cmd = f'psql "{db}" -c "{query}" --csv'

        try:
            result = await self._run_cmd(cmd)
            return {"indexes": result}
        except Exception as e:
            return {"error": str(e)}

    async def _optimize_database(self, table: str = None, full: bool = False, analyze: bool = True, **kwargs) -> Dict:
        target = table or ""
        full_flag = "FULL" if full else ""
        analyze_flag = "ANALYZE" if analyze else ""

        cmd = f'psql -c "VACUUM {full_flag} {analyze_flag} {target};"'

        try:
            result = await self._run_cmd(cmd)
            return {"status": "optimized", "table": target or "all", "full": full, "analyze": analyze}
        except Exception as e:
            return {"error": str(e)}

    async def _show_active_queries(self, database: str = None, min_duration: int = 0, **kwargs) -> List[Dict]:
        db = database or self.connection_string or "postgres"

        query = f"""
        SELECT pid, now() - pg_stat_activity.query_start AS duration, query, state
        FROM pg_stat_activity
        WHERE (now() - pg_stat_activity.query_start) > interval '{min_duration} seconds'
        AND state != 'idle'
        ORDER BY duration DESC;
        """

        cmd = f'psql "{db}" -c "{query}" --csv'

        try:
            result = await self._run_cmd(cmd)
            return {"active_queries": result}
        except Exception as e:
            return {"error": str(e)}

    async def _kill_query(self, pid: int, force: bool = False, **kwargs) -> Dict:
        func = "pg_terminate_backend" if force else "pg_cancel_backend"
        cmd = f'psql -c "SELECT {func}({pid});"'

        try:
            await self._run_cmd(cmd)
            return {"status": "killed", "pid": pid, "force": force}
        except Exception as e:
            return {"error": str(e)}

    # ==================== AGENT INTERFACE ====================

    def can_handle(self, task: str) -> bool:
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in self.KEYWORDS)

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute using self-reasoning and MCP tools"""
        query = task.get("task", "")
        params = task.get("params", {})

        # Use powerful process method with reasoning
        return await self.process(query, params)

    async def execute_direct(self, step: Dict) -> Any:
        """Direct execution for steps without specific tools"""
        query = step.get("query", step.get("action", ""))

        if query:
            return await self._execute_query(query)

        return {"status": "no action taken"}
