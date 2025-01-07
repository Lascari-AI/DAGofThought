---
authors:
- fjooord
categories:
- Prompt Engineering
comments: true
date: 2024-12-13
description: Learn how to improve LLM outputs by breaking reasoning into multiple structured steps, with real examples using the Instructor library.
draft: false
slug: structured-reasoning
tags:
- prompt engineering
- chain of thought prompting
- structured output
---

# The Secret to Better LLM Outputs: Multiple Structured Reasoning Steps

Traditional chain-of-thought prompting is leaving performance on the table. 

While working on a recent client project, we A/B tested different prompting approaches. 

Breaking LLM reasoning into multiple structured steps was preferred 80% of the time over traditional methods.

Instead of one meandering thought stream, we can greatly boost reliability now get precise by using a tightly controlled response model

- Analyze the example structure
- Analyze the example style
- Generate the output based on the previous steps

I'll show you exactly how to implement this approach using the [Instructor library](https://python.useinstructor.com/){:target="_blank"}, with real examples you can use today.

<!-- more -->

## Why Single Chain-of-Thought Falls Short

Consider this simple response model:
```python
class ReportSectionResponse(BaseModel):
    chain_of_thought: str = Field(
        description="Think step by step about how to generate a psychological assessment report"
    )
    report_section: str = Field(
        description="Generate report section based on the chain of thought"
    )
```
This gives you one long stream of consciousness - like trying to write, edit, and proofread all at once. 

The results? Inconsistent quality and hard-to-debug outputs.

## Multiple Structured Reasoning: A Better Way
Instead of one tangled thought process, we split the reasoning into discrete, specialized steps - like having multiple experts analyze the problem:

```python
class ReportSectionResponse(BaseModel):
    structure_analysis: str = Field(
        description="A medium length analysis of the structure of the provided examples"
    )
    style_analysis: str = Field(
        description="A detailed analysis of the writing style of the provided examples"
    )
    report_section: str = Field(
        description="A report section based on the structure and style analysis"
    )
```

The magic happens in how we structure these fields:

- Clear, descriptive names (example_structure_analysis vs step1)
- Specific field descriptions that act as targeted mini-prompts
- Sequential steps that build on each other's analysis

This structured approach means:

- Each step has one clear job
- You can validate outputs at each stage
- Debugging becomes much easier
- Quality improves dramatically

## See It In Action
Let's look at a real psychological assessment example to see how this structured approach transforms our outputs.

We start with the example:

```markdown
PIIPERSON1's language skills were assessed using the WISC-V and BASC. 
His performance on the WISC-V Verbal Comprehension Index (VCI) resulted in a composite score at the 30th percentile, indicating his language comprehension and verbal processing are average for his age group.
The BASC Functional Communication scale was used to evaluate how PIIPERSON1's communication skills are viewed in different environments. His mother reported his functional communication at home as average, with a T score of 59. 
His current (second-grade) teacher also rated his communication skills as average in the classroom with a T score of 49. 
His first-grade teacher, however, had concerns, noting his abilities as at-risk with a T score of 39. 
Below Average scores on the Functional Communication scale indicate that the student demonstrates poor expressive and receptive communication skills and/or may have difficulty seeking out and finding information on their own.
```

Watch how our structured reasoning unfolds:

### Step 1: Structure Analysis

The model first breaks down the example's organization:

```
The example report section is structured into two main paragraphs
The first paragraph discusses the results from the BASC, focusing on how the child's communication skills are perceived in different environments by different raters
It provides specific T scores and qualitative descriptions from both the mother and teachers, comparing these ratings across different contexts and time periods
The second paragraph shifts focus to the child's performance on the WISC-V, specifically the Verbal Comprehension Index, and provides a percentile score to contextualize the child's abilities relative to peers
The paragraph ends with a brief interpretation of what the scores indicate about the child's language comprehension and verbal processing skills 
```

### Step 2: Style Analysis
Next, it analyzes the writing patterns and tone:

```
The style of the example report is formal and clinical, using specific psychological terminology and test names
It provides quantitative data (percentile and T scores) alongside qualitative descriptors (eg, 'average', 'at-risk') to give a comprehensive view of the child's abilities
The language is precise, with a focus on clarity and objectivity
The report uses acronyms for test names (eg, WISC-V, BASC) and provides a balanced view by discussing both strengths and areas of concern
The sentences are structured to first present the data and then interpret it in the context of the child's overall abilities
```

### Step 3: Generated Output
Finally, it produces new content that matches both structure and style:

```
PIIPERSON1's language skills were evaluated using the BASC-3 and Vineland-3
Her mother reported her functional communication at home as average, with a T score of 48, while her current teacher rated her communication skills as average in the classroom with a T score of 54
These scores suggest that PIIPERSON1's communication abilities are perceived consistently across different environments as average, indicating no significant concerns in expressive or receptive communication skills
```

## Why This Works So Well
This isn't just theoretical - we're seeing consistently better results because:

- Each step has one clear job (analyze structure, analyze style, generate content)
- The model builds understanding progressively
- We can catch issues at any step
- The final output combines insights from all previous analysis


The beauty of this approach? 

It works for **any complex task** - from software architecture to business strategy to scientific research.

---

Want to share your results or get help? Drop a comment below or find me on [Twitter](https://x.com/intent/follow?screen_name=FJ000RD){:target="_blank"}. 

I'd love to see what you build with this!

<div style="text-align: center; justify-content: center; align-items: flex-end; display: flex; gap: 1rem;">
    <a href="https://x.com/intent/follow?screen_name=FJ000RD" class="md-button md-button--primary" target="_blank">
    Follow Me on 

    <span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"></path></svg></span>
  </a>
  <a href="https://fjooord.kit.com/b68056d614" class="md-button md-button--secondary" target="_blank">Subscribe to My Newsletter</a>
</div>