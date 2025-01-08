# DAGofThought

This project is an implementation and expansion of an interesting approach to structured reasoning using DAGs (Directed Acyclic Graphs), originally proposed by [@mrsiipa](https://x.com/mrsiipa/status/1876253176963493889) and initially implemented by [Maharshi Pandya](https://gist.github.com/Maharshi-Pandya/4aeccbe1dbaa7f89c182bd65d2764203).

## Overview

DAG of Thought provides a framework for breaking down complex reasoning tasks into manageable, interconnected components using a DAG structure. The project includes tools for:

- Creating structured reasoning processes
- Visualizing thought patterns as Mermaid diagrams
- Processing and analyzing responses
- Managing guard rails for controlled reasoning
- Integrating with language models for automated reasoning

## Example
### Input
```python
TASK = "Design an optimized CUDA kernel implementation for softmax that maximizes throughput while maintaining numerical stability"

GUARDRAILS = [
    GuardRail(
        name="Numerical Stability",
        description="Must maintain numerical stability (handling overflow/underflow)"
    ),
    GuardRail(
        name="Memory Usage",
        description="Maximum shared memory usage of 48KB per block"
    ),
    GuardRail(
        name="Batch Handling",
        description="Must handle variable batch sizes efficiently"
    ),
    GuardRail(
        name="Performance",
        description="Must outperform naive implementation by at least 100x"
    ),
    GuardRail(
        name="Dependencies",
        description="Cannot use external CUDA libraries (only basic CUDA primitives)"
    )
]
```

### Output
### Findings Summary
In revisiting and extending our exploration, we see that:
- Numerical stability hinges on a robust max-subtraction method, possibly refined with warp-level primitives to reduce overhead
- A single-pass approach can reduce global memory traffic, but requires careful synchronization and design of warp-level reductions
- Multi-pass segmented approaches may be necessary for extremely large dimensions, keeping shared memory usage within 48KB per block
- Efficiently coordinating thread blocks for variable batch sizes ensures each batch dimension is handled independently, respecting memory boundaries and delivering high throughput
- These advanced optimizations, if implemented carefully with attention to kernel launch configuration, warp synchronization, and shared memory utilization, further boost performance beyond the initial two-pass approach while still meeting the constraints of numerical stability, memory usage, and dependency limitations

### Remaining Questions
1. Is there a practical upper bound on dimension size where multi-pass segmented softmax is more advantageous than a single-pass approach?
2. Could mixed precision (e.g., FP16 for intermediate exponentials) maintain stability while improving throughput further?

### Conclusion Status
- Is conclusion premature? No
- Reason: conclusion NOT premature

### Reasoning Process Visualization
![Reasoning Process](https://www.mermaidchart.com/raw/25009061-0102-4ca5-9c01-e643b15a1862?theme=light&version=v0.1&format=svg)


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

2. Copy the environment file and add your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

3. Install dependencies:
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