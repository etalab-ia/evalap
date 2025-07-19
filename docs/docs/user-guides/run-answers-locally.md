---
sidebar_position: 4
---

# Run Answers Locally with vLLM

This guide walks you through the process of generating model answers locally using GPU-enabled machines and then submitting experiments to Evalap.
We provide two utility scripts to help accomplish this:
- `run_answers.py`: Generate model responses for an Evalap dataset
- `run_expe.py`: Create or update experiment sets in Evalap

## Prerequisites

- Access to a machine with GPU capabilities
- SSH access configured with your public key (if needed)
- Python environment with virtual environment support
- Sufficient disk space for model downloads
- [vLLM](https://docs.vllm.ai/) installed

## Step 1: Connect to GPU Machine (if needed)

Connect to your GPU-enabled VM or machine using SSH:

```bash
# Add your SSH key to the agent
ssh-add ~/.ssh/your_key

# Connect to the machine
ssh user@gpu-machine-address
```

## Step 2: Check Available Disk Space

Before downloading models, ensure you have sufficient disk space:

```bash
# Check disk usage
df -Th

# If needed, clean up old model cache
# Models are stored in ~/.cache/huggingface/hub/ by default
rm -rf ~/.cache/huggingface/hub/old_models/
```

⚠️ **Note**: Large language models can require significant disk space (10-100GB per model). Plan accordingly.

## Step 3: Launch Model with vLLM

Start the model server using vLLM. Here's an example with Gemma-3:

```bash
vllm serve google/gemma-3-27b-it \
  --gpu-memory-utilization 1 \
  --tensor-parallel-size 1 \
  --max-model-len 32768 \
  --port 9191
```

### Common vLLM Parameters:
- `--gpu-memory-utilization`: Fraction of GPU memory to use (0-1)
- `--tensor-parallel-size`: Number of GPUs for tensor parallelism
- `--max-model-len`: Maximum sequence length
- `--port`: Port for the API server

## Step 4: Install Evalap Framework

Clone and install the Evalap repository:

```bash
# Clone the repository
git clone https://github.com/etalab/evalap.git
cd evalap

# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ./
```

This installation provides access to the command-line tools located in the `evalap/scripts/` directory.

## Step 5: Generate Answers

Use the `run_answers.py` script to generate responses from your model:

```bash
# Set your API keys
export EVALAP_API_KEY="your-evalap-token"
export OPENAI_API_KEY="your-openai-key"  # Optional, if not using --auth-token

# View available options
python -m evalap.scripts.run_answers.run_answers --help

# Example: Generate answers for MFS questions with Gemma-3
python -m evalap.scripts.run_answers.run_answers \
  --run-name gemma-3-27b_mfs \
  --base-url http://localhost:9191/v1 \
  --model google/gemma-3-27b-it \
  --dataset MFS_questions_v01 \
  --repeat 4 \
  --max-workers 8
```

### Key Parameters:
- `--run-name`: Unique identifier for this generation run
- `--base-url`: URL of the vLLM server (e.g., http://localhost:9191/v1)
- `--model`: Model name/identifier
- `--dataset`: Name of the Evalap dataset to use
- `--repeat`: Number of times to run the dataset (default: 1)
- `--max-workers`: Maximum concurrent requests (default: 8)
- `--system-prompt`: Optional system prompt to prepend to queries
- `--sampling-params`: Optional JSON string with sampling parameters (e.g., `'{"temperature": 0.7, "max_tokens": 1024}'`)

The script will:
1. Download the specified dataset from Evalap
2. Generate responses for each query in the dataset
3. Save results to `results/{run_name}__{repetition}.json`
4. Save model details to `results/{run_name}__details.json`

## Step 6: Create and Run Experiments

Use `run_expe.py` to create experiment sets and submit them to Evalap:

```bash
# View available options
python -m evalap.scripts.run_expe.run_expe --help

# Create a new experiment
python -m evalap.scripts.run_expe.run_expe \
  --run-name gemma-3-27b_mfs \
  --expe-name "Gemma-3 27B MFS Evaluation"

# Update an existing experiment set
python -m evalap.scripts.run_expe.run_expe \
  --run-name gemma-3-27b_mfs \
  --expset existing-experiment-id
```

### Key Parameters:
- `--run-name`: Name of the model generation to load (must match files in `results/` directory)
- `--expe-name`: Display name for the experiment set (optional, defaults to run-name)
- `--expset`: Existing experiment set ID to update (optional)

The script will:
1. Load all result files matching `results/{run_name}*.json`
2. Create an experiment set with metrics: answer_relevancy, judge_exactness, judge_notator, output_length, generation_time
3. Submit the experiment set to Evalap for evaluation

## Complete Example Workflow

```bash
# 1. Start vLLM server
vllm serve google/gemma-3-27b-it --gpu-memory-utilization 0.9 --port 9191

# 2. Generate answers (in another terminal)
python -m evalap.scripts.run_answers.run_answers \
  --run-name gemma3_test \
  --base-url http://localhost:9191/v1 \
  --model google/gemma-3-27b-it \
  --dataset MFS_questions_v01 \
  --repeat 3

# 3. Submit experiment to Evalap
python -m evalap.scripts.run_expe.run_expe \
  --run-name gemma3_test \
  --expe-name "Gemma-3 Test Run"
```

## Best Practices

1. **Resource Management**: Monitor GPU memory usage and adjust `--gpu-memory-utilization` accordingly
2. **Concurrent Requests**: Adjust `--max-workers` based on your model's capacity and dataset size
3. **Experiment Tracking**: Use meaningful experiment names and maintain metadata for reproducibility
4. **Multiple Runs**: Use `--repeat` to generate multiple runs for statistical significance
5. **API Keys**: Store your API keys in environment variables for security

## Troubleshooting

### Common Issues:

**Out of Memory Error**
```bash
# Reduce memory utilization
--gpu-memory-utilization 0.8
```

**Connection Refused**
```bash
# Check if vLLM server is running
curl http://localhost:9191/v1/models
```

**Slow Generation**
```bash
# Adjust batch size and parallelism
--tensor-parallel-size 2  # If multiple GPUs available
```

**Missing Results Files**
```bash
# Check that result files were generated
ls results/{run_name}*.json
```

**API Authentication Issues**
```bash
# Ensure API keys are set
echo $EVALAP_API_KEY
echo $OPENAI_API_KEY
```
