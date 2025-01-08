# DAGofThought

This project is an implementation and expansion of an interesting approach to structured reasoning using DAGs (Directed Acyclic Graphs), originally proposed by [@mrsiipa](https://x.com/mrsiipa/status/1876253176963493889) and initially implemented by [Maharshi Pandya](https://gist.github.com/Maharshi-Pandya/4aeccbe1dbaa7f89c182bd65d2764203).

## Overview

DAG of Thought provides a framework for breaking down complex reasoning tasks into manageable, interconnected components using a DAG structure. The project includes tools for:

- Creating structured reasoning processes
- Visualizing thought patterns as Mermaid diagrams
- Processing and analyzing responses
- Managing guard rails for controlled reasoning
- Integrating with language models for automated reasoning

## Project Structure

```
DAGofThought/
├── utils/
│   ├── build_mermaid_diagram.py    # Diagram generation utilities
│   └── make_gpt_pro_prompt.py      # Prompt construction tools
├── models/
│   ├── input_models.py             # Input data structures
│   └── output_models.py            # Output data structures
├── prompts/
│   ├── in_depth_thinking_system_prompt.md      # System prompt template
│   └── format_structured_reasoning_user_prompt.py   # User prompt formatter
├── data/
│   └── outputs/                    # Generated outputs directory
├── Notebooks/
│   ├── 0_generate_thought_dag.ipynb    # DAG generation workflow
│   └── 1_process_responses_for_report.ipynb    # Response analysis
```

## Core Components

### Foundation Observations (FO)
- Basic building blocks of the reasoning process
- Groups related atomic steps
- Provides foundation for higher-level thoughts

### Atomic Steps (AS)
- Individual units of reasoning
- Must flow logically from previous steps
- Can represent either progress or dead ends

### Thoughts (TH)
- Complete reasoning units built on foundation observations
- Can include multiple atomic steps
- May reference guard rails and previous thoughts

### Guard Rails
- Constraints and guidance for the reasoning process
- Help maintain focus and relevance
- Can be customized for specific domains

## Key Features

### Mermaid Diagram Generation
The project can generate visual representations of reasoning processes using Mermaid diagrams, showing:
- Relationships between thoughts
- Foundation observation hierarchies
- Step-by-step reasoning flows

### Structured Output
All reasoning processes are structured as JSON objects with:
- Clear hierarchies
- Traceable relationships
- Standardized formats

### Guard Rail System
Implements a flexible guard rail system that:
- Enforces constraints
- Guides reasoning paths
- Maintains relevance to goals

## Usage

### Basic Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/DAGofThought.git
cd DAGofThought
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running Experiments

1. Configure your task and guard rails in `0_generate_thought_dag.ipynb`
2. Generate thought DAGs:
```python
response = generate_structured_reasoning(TASK, GUARDRAILS, GuardRailEnum)
```

3. Visualize results:
```python
diagram_text = build_mermaid_diagram(response.model_dump())
```

### Processing Results

Use `1_process_responses_for_report.ipynb` to:
- Analyze generated responses
- Create summary reports
- Export visualizations

## Customization

### Adding Guard Rails

1. Define new guard rails in your experiment:
```python
GUARDRAILS = [
    GuardRail(
        name="Custom Rule",
        description="Your constraint description"
    ),
    # Add more as needed
]
```

2. Create corresponding enum entries:
```python
GuardRailEnum = Enum('GuardRailEnum', {
    name.upper().replace(' ', '_'): name 
    for guardrail in GUARDRAILS 
    for name in [guardrail.name]
})
```

## Advanced Features

### GPT Pro Integration
The project includes special handling for GPT Pro:
- Custom prompt formatting
- Response processing
- Timeout handling

### Response Analysis
Built-in tools for:
- Processing multiple responses
- Generating summary reports
- Creating comparative analyses

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Attribution

This project is based on:
- Original concept by [@mrsiipa](https://x.com/mrsiipa/status/1876253176963493889)
- Initial implementation by [Maharshi Pandya](https://gist.github.com/Maharshi-Pandya/4aeccbe1dbaa7f89c182bd65d2764203)