---
slug: /
id: intro
sidebar_position: 1
sidebar_label: Introduction
---

# Welcome to EvalAP

**EvalAP** (**Eval**uation **A**PI and **P**latform) is a high-level service designed to perform evaluations for Etalab. This project provides an API to evaluate LLM models and an interface to navigate datasets, models, metrics, and experiments.

## What is EvalAP?

Evalap is a comprehensive platform that allows you to:

- Evaluate Large Language Models (LLMs) using standardized metrics
- Navigate through datasets, models, and experiments
- Create and run your own evaluation experiments
- Compare different models and their performances
- Build your own Leaderboards


## Guide Overview

:::info
Currently, the EvalAP webapp (frontend) is a read-only application to visualize the evaluation data. To publish datasets and run experiments you must use the EvalAP API.
:::


<div className="container">
  <div className="row">
    <div className="col col--4">
      <div className="featureCard">
        <h3 className="featureTitle">Getting Started</h3>
        <p className="featureDescription">Learn how to install and set up Evalap on your system.</p>
        <a href="/docs/getting-started/install-from-source">Install from source →</a><br/>
        <a href="/docs/getting-started/install-with-docker">Install with Docker →</a>
      </div>
    </div>
    <div className="col col--4">
      <div className="featureCard">
        <h3 className="featureTitle">User Guides</h3>
        <p className="featureDescription">Discover how to use Evalap for your evaluation needs.</p>
        <a href="/docs/user-guides/add-your-dataset">Add your dataset →</a><br/>
        <a href="/docs/user-guides/create-a-simple-experiment">Create an experiment →</a>
      </div>
    </div>
    <div className="col col--4">
      <div className="featureCard">
        <h3 className="featureTitle">Developer Guide</h3>
        <p className="featureDescription">Extend and customize Evalap for your specific requirements.</p>
        <a href="/docs/developer-guide/adding-a-new-metric">Adding a new metric →</a><br/>
        <a href="/docs/developer-guide/increase-parallel-requests">Increase parallel requests →</a>
      </div>
    </div>
  </div>
  <div className="row" style={{marginTop: '20px'}}>
    <div className="col col--4 col--offset-0">
      <div className="featureCard">
        <h3 className="featureTitle">API Reference</h3>
        <p className="featureDescription">Comprehensive documentation of the Evalap API.</p>
        <a href="/docs/api-reference/index">View API Reference →</a>
      </div>
    </div>
  </div>
</div>

## Contributing

You can open issues for bugs you've found or features you think are missing. You can also submit pull requests to the Evalap repository. To get started, take a look at the CONTRIBUTING.md file in [the repository](https://github.com/etalab-ia/evalap).
