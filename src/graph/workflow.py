from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

from src.state.state import SqlState
from src.graph.nodes import (
    node_agent_generator,
    node_check_syntax,
    node_agent_validator,
    node_execute_sql,
)
from src.graph.edges import edge_syntax, edge_validation
from src.tools.get_schema import get_schema

def create_workflow():
    builder = StateGraph(SqlState)
    
    builder.add_node("agent_generator", node_agent_generator)
    builder.add_node("tools", ToolNode([get_schema]))
    builder.add_node("check_syntax", node_check_syntax)
    builder.add_node("agent_validator", node_agent_validator)
    builder.add_node("execute_sql", node_execute_sql)
    
    builder.set_entry_point("agent_generator")
    
    builder.add_conditional_edges(
        "agent_generator",
        tools_condition,
        {"tools": "tools", "__end__": "check_syntax"}
    )
    builder.add_edge("tools", "agent_generator")
    
    builder.add_conditional_edges("check_syntax", edge_syntax)
    builder.add_conditional_edges("agent_validator", edge_validation)
    builder.add_edge("execute_sql", END)
    
    return builder.compile()

workflow = create_workflow()