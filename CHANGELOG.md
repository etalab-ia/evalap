# Changelog

All notable changes to this project will be documented in this file.


## [0.4] - 2025-05-21

### 🚀 Features

- Support thinking model in judge
- Add nb_tool_call as ops metrics + add MCP_BRIFGE_URL + format
- Parquet dataset support + ocr metrics + notebook demo
- Add and handle new with_vision and prelude_prompt attribute
- Calculation of the environmental impact of models for the response generation part.
- Creation of two new environmental metrics: energy_consumption and gwp_consumption.

### 🔧 Improvements

- [UI] display of the environmental brick in the OPS pane and experiments_set metric results.

### 🐛 Bug Fixes

- *(runners)* Nb_tool_calls metrics computation
- Improve log level warning.
- *(ui)* Use two point float precision in score table.
- Temporary url for MCP bridge
- Tool activation and rag metrics error handling
- *(ui)* Show dataset name and all model paramsi in expeset overview
- *(mcp)* Allow tool_choice tuning
- *(clients)* Add support for aliases models in v1/models
- *(api)* Judge model must be unique in a set.
- Strip answer + think
- Fix multi-step agent loop generation if max_steps is reached.
- Remove rerun_metric in patch exp + better handle error in patch expset route + fix format
- Disallow model_judge patch for experiment and experiment_set
- Parquet support and schemas
- *(schema)* Rename prompt_system to system_prompt
- Columns_map for ocr marker demo dataset
- Dataset views
- *(tasks)* Empty query

### 💼 Other

- Strip answer + not test on integrer !!!
- *(runner)* Limit deep search steps + tool_choice 'none'.
- Import collections
- *(mcp)* Fix the multi-step loop
- Unbound variables
- Non blocking model sync


## [0.3.1] - 2025-04-02

### 🚀 Features

- [API] Support Anthropic, Openai, Mistral and Albert providers for judge models `judge_model` parameter in experiments (models are fetch from the openai api v1/models endpoints)
- [SCRIPTS] ADD convenient scripts to run experiment from an isolated environment (e.g. like cortex, [see the tutorial](https://tchap.gouv.fr/#/room/!GeUSclgFhhSSkwiExz:agent.dinum.tchap.gouv.fr/$BoFMFX0xNyz0FFIIaFUzdIxyshhulBWPYZxP1q9Zm5s?via=agent.dinum.tchap.gouv.fr) )

### 🔧 Improvements

- [UI] Add a special card for orphan experiments at the bottom of the experiments list.
- [UI] Order the experiment set from the newest first
- [UI] Remove old confusing experiments menu in favor of only the experiment sets menu (renamed simply experiments)


## [0.3] - 2025-03-27

### 🚀 Features

- Added experiment set with cross-validation parameters and demo notebooks.
- Integrated multiple RAG metrics for deep evaluation.
- Supported delete experiment route for admin users.
- Introduced new retry and post routes with UI improvements.
- Added experiments 'finished' and 'failure' ratio in overview.
- Integrated MCP support and multi-step LLM generations with MCP client bridge.
- New tests for an increase code coverage and addressed pydantic warnings.
- Implemented loop limit and tool call step saving.
- Improved sorting and metrics highlighting in the experiment set score table.

### 🐛 Bug Fixes

- Enhanced error handling for missing metric input and baseline demo notebook.
- Removed unnecessary attributes and improved schema validation.
- Fixed various UI bugs and improved experiment view.
- Improved notebook variable names and used public endpoints.
- Enhanced GitHub Actions CI and addressed Alembic issues.
- Corrected schema serialization and computation needs.
- Improved experiment status updates and endpoint terminology.
- Handled unknown model cases and improved dataset visibility.
- Fixed various typos and improved model sorting and ops board status.
- Improved schema validation and error detail return for API.
- Addressed issues with experiment view and retry functionality.

### 🛠️ Code Improvements

- Reorganized code structure (pip ready) and fixed import issues.
- Moved API components to clients and adjusted imports accordingly.

### 🔥 Hotfixes

- Addressed dataset and SQL float compatibility issues.
- Updated configuration files for supervisord and Alembic.

### ⚙️ Operations

- Added Docker and Docusaurus configuration files.
- Fix supervisord path to deploy.
