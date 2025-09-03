from langgraph.graph import StateGraph, START, END

from extractor.graph.type import State


def build_graph():
    graph = StateGraph(State)