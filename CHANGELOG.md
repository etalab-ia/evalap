# Changelog

All notable changes to this project will be documented in this file.


## [0.3.1] - 2025-04-02

### 🚀 Features

- [API] Support Anthropic, Openai, Mistral and Albert providers for judge models `judge_model parameter in experiments` (models are fetch from the openaai api v1/models endpoints
- [SCRIPTS] ADD convenient scripts to run experiment from an isolated machine (like cortex, [see the tutorial](https://tchap.gouv.fr/#/room/!GeUSclgFhhSSkwiExz:agent.dinum.tchap.gouv.fr/$BoFMFX0xNyz0FFIIaFUzdIxyshhulBWPYZxP1q9Zm5s?via=agent.dinum.tchap.gouv.fr)

### 🔧 Improvements
- [UI] Add an orpan special experiment group at the bottom of the experiments list.
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

- Added Docker and Streamlit configuration files.
- Fix supervisord path to deploy.
