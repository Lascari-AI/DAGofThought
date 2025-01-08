def build_mermaid_diagram(data: dict, is_gpt_pro: bool = False) -> str:
    """
    Build a Mermaid flowchart diagram (top-to-bottom) from the JSON-like structure
    of the InDepthStructuredReasoning model output, accounting for 'previous_step_key' in AtomicSteps.

    :param data: Dictionary matching the structure of the InDepthStructuredReasoning output
    :return: A string containing a Mermaid flowchart in top-to-bottom (TB) orientation.
    """

    # Extract the key parts from the data
    reasoning_process = data["reasoning_process"]
    foundation_observations = reasoning_process["foundation_observations"]
    thoughts = reasoning_process["thoughts"]

    # We'll collect lines in a list, then join them at the end
    mermaid_lines = []
    mermaid_lines.append("flowchart TB\n")

    # We’ll store the created node IDs for atomic steps so we can link them properly
    # The key will be something like "FO_1_AS_1" or "TH_1_AS_21"
    # and we'll store references to easily build connections after creation
    created_nodes = set()

    # ------------------------------------------------------
    # 1) Foundation Observations (FOs)
    # ------------------------------------------------------
    mermaid_lines.append("subgraph Foundation Observations")

    # For storing step connections: (node_from, node_to)
    fo_step_connections = []

    for fo in foundation_observations:
        fo_key = fo["key"]
        fo_name = fo["name"]
        mermaid_lines.append(
            f'    subgraph {fo_key}["{fo_key}: {fo_name}"]\n    direction TB'
        )

        # Each FO has a list of atomic_steps
        for atom_step in fo["atomic_steps"]:
            as_key = atom_step["key"]
            # In the new model, previous_step_key may or may not exist.
            # If it doesn't exist in the dict, we default to "None".
            previous_step_key = atom_step.get("previous_step_key", "None")
            as_content = atom_step["content"]

            # Escape potential newlines
            as_content_escaped = as_content.replace("\n", "\\n")

            # Create a unique ID for this node
            node_id = f"{fo_key}_{as_key}"
            created_nodes.add(node_id)
            mermaid_lines.append(f'        {node_id}["{as_key}: {as_content_escaped}"]')

            # If there's a valid previous step, create a link from previous -> current
            if previous_step_key != "None":
                prev_node_id = f"{fo_key}_{previous_step_key}"
                fo_step_connections.append((prev_node_id, node_id))

        mermaid_lines.append("    end")  # End subgraph for this FO

    mermaid_lines.append("end\n")  # End "Foundation Observations" subgraph

    # ------------------------------------------------------
    # 2) Thoughts (THs)
    # ------------------------------------------------------
    mermaid_lines.append("subgraph Thoughts")

    # For storing step connections within thoughts
    th_step_connections = []

    for th in thoughts:
        th_key = th["key"]
        th_name = th["name"]
        th_backtracked = th["backtracked_from"]
        th_parent = th["parent_thought"]
        th_fo_associations = th["associated_foundation_observations"]
        guard_rails = th["guard_rails_to_consider"]
        thought_process = th["thought_process"]

        # Build a multiline label
        label_lines = [
            f"{th_key}: {th_name}",
            f"(backtracked_from: {th_backtracked})",
            f"(parent_thought: {th_parent})",
            f"Associated FOs: [{', '.join(th_fo_associations)}]",
        ]
        thought_label = "\\n".join(label_lines)

        # Start the subgraph for this Thought
        mermaid_lines.append(f'    subgraph {th_key}["{thought_label}"]')

        # --- Guard Rails ---
        mermaid_lines.append(f'        subgraph GR_{th_key}["Guard Rails"]')
        if len(guard_rails) == 0:
            mermaid_lines.append("            GR_None_1[No guard rails specified]")
        else:
            for i, gr in enumerate(guard_rails, start=1):
                if is_gpt_pro:
                    gr_value = gr.replace("\n", "\\n")
                else:
                    gr_value = gr.name.replace("\n", "\\n")
                mermaid_lines.append(f'            GR_{th_key}_{i}["{gr_value}"]')
        mermaid_lines.append(f"        end")  # End of guard rails subgraph

        # --- Thought Process (Atomic Steps) ---
        mermaid_lines.append(
            f'        subgraph {th_key}_AtomicSteps["Thought Process"]\n    direction TB'
        )
        for atom_step in thought_process:
            as_key = atom_step["key"]
            previous_step_key = atom_step.get("previous_step_key", "None")
            as_content = atom_step["content"]
            as_content_escaped = as_content.replace("\n", "\\n")

            # Unique ID for this step
            node_id = f"{th_key}_{as_key}"
            created_nodes.add(node_id)

            mermaid_lines.append(
                f'            {node_id}["{as_key}: {as_content_escaped}"]'
            )

            # If there's a valid previous step, link them
            if previous_step_key != "None":
                prev_node_id = f"{th_key}_{previous_step_key}"
                th_step_connections.append((prev_node_id, node_id))

        mermaid_lines.append(f"        end")  # End subgraph of thought process

        mermaid_lines.append("    end")  # End subgraph for this Thought

    mermaid_lines.append("end\n")  # End "Thoughts" subgraph

    # ------------------------------------------------------
    # 3) Connect FO -> Thoughts (based on associated_foundation_observations)
    # ------------------------------------------------------
    for th in thoughts:
        th_key = th["key"]
        for fo_key in th["associated_foundation_observations"]:
            mermaid_lines.append(f"{fo_key} --> {th_key}")

    # ------------------------------------------------------
    # 4) Connect parent_thought -> child_thought
    # ------------------------------------------------------
    for th in thoughts:
        th_key = th["key"]
        parent_key = th["parent_thought"]
        if parent_key != "None":
            mermaid_lines.append(f"{parent_key} --> {th_key}")

    # ------------------------------------------------------
    # 5) Connect atomic steps within each FO
    # ------------------------------------------------------
    for prev_node, current_node in fo_step_connections:
        # Only connect if both nodes were created (to avoid missing reference)
        if prev_node in created_nodes and current_node in created_nodes:
            mermaid_lines.append(f"{prev_node} --> {current_node}")

    # ------------------------------------------------------
    # 6) Connect atomic steps within each TH
    # ------------------------------------------------------
    for prev_node, current_node in th_step_connections:
        if prev_node in created_nodes and current_node in created_nodes:
            mermaid_lines.append(f"{prev_node} --> {current_node}")

    # Join all lines
    return "\n".join(mermaid_lines)
