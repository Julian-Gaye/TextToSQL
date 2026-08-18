from src.graph.nodes import node_impossible_sql, node_general_conversation, node_max_attempts_error
from src.graph.edges import edge_relevance
from src.graph.nodes import node_agent_check_relevance
from langgraph.graph import StateGraph, END

from src.state.state import InputState, OutputState, OverallState
from src.graph.nodes import (
    node_agent_generator,
    node_check_syntax,
    node_agent_validator,
    node_execute_sql,
    node_get_schema,
)
from src.graph.edges import edge_syntax, edge_validation

def create_workflow():
    builder = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)
    
    builder.add_node("get_schema", node_get_schema)
    builder.add_node("agent_check_relevance", node_agent_check_relevance)
    builder.add_node("agent_generator", node_agent_generator)
    builder.add_node("check_syntax", node_check_syntax)
    builder.add_node("agent_validator", node_agent_validator)
    builder.add_node("execute_sql", node_execute_sql)
    builder.add_node("general_conversation", node_general_conversation)
    builder.add_node("impossible_sql", node_impossible_sql)
    builder.add_node("max_attempts_error", node_max_attempts_error)

    builder.set_entry_point("get_schema")

    builder.add_edge("get_schema", "agent_check_relevance")
    builder.add_conditional_edges("agent_check_relevance", edge_relevance)
    builder.add_edge("general_conversation", END)
    builder.add_edge("impossible_sql", END)
    builder.add_edge("max_attempts_error", END)
    builder.add_edge("agent_generator", "check_syntax")
    builder.add_conditional_edges("check_syntax", edge_syntax)
    builder.add_conditional_edges("agent_validator", edge_validation)
    builder.add_edge("execute_sql", END)

    graph = builder.compile()
    
    return graph

workflow = create_workflow()