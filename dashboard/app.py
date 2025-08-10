import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import json
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from event_bus import event_bus, EventType
from mcp_protocol import mcp_protocol, TaskType, TaskStatus
from agents.sales_genie import generate_listing
from agents.logibot import LogiBot
from agents.buybot import BuyBot

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Agentic-Ecom Dashboard"

# Initialize agents
logibot = LogiBot()
buybot = BuyBot()

def create_metrics_card(title, value, color="primary"):
    """Create a metric card component"""
    return dbc.Card(
        dbc.CardBody([
            html.H4(title, className="card-title"),
            html.H2(value, className=f"text-{color}")
        ]),
        className="mb-3"
    )

def create_agent_status_card(agent_name, status="active"):
    """Create an agent status card"""
    status_color = "success" if status == "active" else "danger"
    return dbc.Card(
        dbc.CardBody([
            html.H5(agent_name, className="card-title"),
            html.Span(status, className=f"badge bg-{status_color}")
        ]),
        className="mb-3"
    )

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Agentic-Ecom Dashboard", className="text-center mb-4"), width=12)
    ]),
    
    # System Overview
    dbc.Row([
        dbc.Col(html.H3("System Overview", className="mb-3"), width=12)
    ]),
    
    dbc.Row([
        dbc.Col(create_agent_status_card("SalesGenie", "active"), width=3),
        dbc.Col(create_agent_status_card("LogiBot", "active"), width=3),
        dbc.Col(create_agent_status_card("BuyBot", "active"), width=3),
        dbc.Col(create_agent_status_card("System", "active"), width=3)
    ]),
    
    # Metrics Row
    dbc.Row([
        dbc.Col(create_metrics_card("Total Products", "0", "info"), width=3),
        dbc.Col(create_metrics_card("Active Orders", "0", "success"), width=3),
        dbc.Col(create_metrics_card("Support Tickets", "0", "warning"), width=3),
        dbc.Col(create_metrics_card("Success Rate", "0%", "primary"), width=3)
    ]),
    
    # Charts Row
    dbc.Row([
        dbc.Col([
            html.H4("Task Completion Over Time"),
            dcc.Graph(id="task-completion-chart")
        ], width=6),
        dbc.Col([
            html.H4("Agent Activity"),
            dcc.Graph(id="agent-activity-chart")
        ], width=6)
    ], className="mb-4"),
    
    # Task Management
    dbc.Row([
        dbc.Col([
            html.H3("Task Management", className="mb-3"),
            dbc.Button("Refresh Tasks", id="refresh-tasks-btn", color="primary", className="mb-3"),
            html.Div(id="task-list")
        ], width=12)
    ]),
    
    # Event Log
    dbc.Row([
        dbc.Col([
            html.H3("Recent Events", className="mb-3"),
            dbc.Button("Refresh Events", id="refresh-events-btn", color="secondary", className="mb-3"),
            html.Div(id="event-log")
        ], width=12)
    ]),
    
    # Manual Controls
    dbc.Row([
        dbc.Col([
            html.H3("Manual Controls", className="mb-3"),
            dbc.Button("Emergency Stop", id="emergency-stop-btn", color="danger", className="me-2"),
            dbc.Button("Resume System", id="resume-system-btn", color="success", className="me-2"),
            dbc.Button("Generate Test Product", id="test-product-btn", color="info")
        ], width=12)
    ]),
    
    # Hidden divs for storing data
    html.Div(id="task-data", style={"display": "none"}),
    html.Div(id="event-data", style={"display": "none"}),
    
    # Interval component for auto-refresh
    dcc.Interval(
        id="interval-component",
        interval=30*1000,  # 30 seconds
        n_intervals=0
    )
], fluid=True)

@app.callback(
    Output("task-completion-chart", "figure"),
    Input("interval-component", "n_intervals")
)
def update_task_completion_chart(n):
    """Update task completion chart"""
    # Get task statistics
    stats = mcp_protocol.get_task_statistics()
    
    # Create sample data (replace with real data)
    dates = pd.date_range(start=datetime.now() - timedelta(days=7), end=datetime.now(), freq='D')
    completed = [stats['completed_tasks']] * len(dates)
    failed = [stats['failed_tasks']] * len(dates)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=completed, mode='lines+markers', name='Completed', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=dates, y=failed, mode='lines+markers', name='Failed', line=dict(color='red')))
    
    fig.update_layout(
        title="Task Completion Trends",
        xaxis_title="Date",
        yaxis_title="Number of Tasks",
        height=400
    )
    
    return fig

@app.callback(
    Output("agent-activity-chart", "figure"),
    Input("interval-component", "n_intervals")
)
def update_agent_activity_chart(n):
    """Update agent activity chart"""
    # Get events by agent
    agents = ["sales_genie", "logibot", "buybot"]
    activity_counts = []
    
    for agent in agents:
        events = event_bus.get_events_by_source(agent, limit=100)
        activity_counts.append(len(events))
    
    fig = px.bar(
        x=agents,
        y=activity_counts,
        title="Agent Activity (Last 100 Events)",
        labels={"x": "Agent", "y": "Event Count"}
    )
    
    fig.update_layout(height=400)
    return fig

@app.callback(
    Output("task-list", "children"),
    Input("refresh-tasks-btn", "n_clicks"),
    Input("interval-component", "n_intervals")
)
def update_task_list(n_clicks, n_intervals):
    """Update task list"""
    tasks = list(mcp_protocol.tasks.values())
    
    if not tasks:
        return html.P("No tasks found", className="text-muted")
    
    task_cards = []
    for task in tasks[-10:]:  # Show last 10 tasks
        status_color = {
            TaskStatus.PENDING: "warning",
            TaskStatus.IN_PROGRESS: "info",
            TaskStatus.COMPLETED: "success",
            TaskStatus.FAILED: "danger",
            TaskStatus.CANCELLED: "secondary"
        }.get(task.status, "secondary")
        
        card = dbc.Card([
            dbc.CardBody([
                html.H6(f"Task {task.id[:8]}...", className="card-title"),
                html.P(f"Type: {task.type.value}"),
                html.P(f"From: {task.source_agent} → To: {task.target_agent}"),
                html.P(f"Status: {task.status.value}"),
                html.P(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}"),
                html.Span(task.status.value, className=f"badge bg-{status_color}")
            ])
        ], className="mb-2")
        
        task_cards.append(card)
    
    return task_cards

@app.callback(
    Output("event-log", "children"),
    Input("refresh-events-btn", "n_clicks"),
    Input("interval-component", "n_intervals")
)
def update_event_log(n_clicks, n_intervals):
    """Update event log"""
    events = event_bus.event_history
    
    if not events:
        return html.P("No events found", className="text-muted")
    
    event_items = []
    for event in events[-20:]:  # Show last 20 events
        item = html.Div([
            html.Small(f"{event.timestamp.strftime('%H:%M:%S')} - {event.source}: {event.type.value}"),
            html.Br(),
            html.Small(f"Data: {str(event.data)[:100]}...", className="text-muted")
        ], className="border-bottom pb-2 mb-2")
        
        event_items.append(item)
    
    return event_items

@app.callback(
    Output("emergency-stop-btn", "children"),
    Input("emergency-stop-btn", "n_clicks")
)
def emergency_stop(n_clicks):
    """Emergency stop functionality"""
    if n_clicks:
        # Create status.lock file
        with open("status.lock", "w") as f:
            f.write("Emergency stop activated")
        
        # Publish emergency stop event
        event_bus.publish_simple(
            EventType.KILL_SWITCH_ENGAGED,
            "dashboard",
            {"reason": "Manual emergency stop"}
        )
        
        return "System Stopped"
    
    return "Emergency Stop"

@app.callback(
    Output("resume-system-btn", "children"),
    Input("resume-system-btn", "n_clicks")
)
def resume_system(n_clicks):
    """Resume system functionality"""
    if n_clicks:
        # Remove status.lock file
        if os.path.exists("status.lock"):
            os.remove("status.lock")
        
        return "System Resumed"
    
    return "Resume System"

@app.callback(
    Output("test-product-btn", "children"),
    Input("test-product-btn", "n_clicks")
)
def generate_test_product(n_clicks):
    """Generate a test product"""
    if n_clicks:
        test_product = {
            "name": "Test Product",
            "category": "electronics",
            "price": 29.99,
            "retail_price": 49.99,
            "tags": ["test", "electronics"],
            "rating": 4.5
        }
        
        try:
            listing = generate_listing(test_product)
            if listing:
                event_bus.publish_simple(
                    EventType.LISTING_GENERATED,
                    "dashboard",
                    {"product_name": test_product["name"], "listing": listing}
                )
                return "Test Product Generated"
        except Exception as e:
            return f"Error: {str(e)}"
    
    return "Generate Test Product"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050) 