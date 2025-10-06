import schemas
from pydantic import ConfigDict


class ModelCreateIgnoreExtra(schemas.ModelCreate):
    model_config = ConfigDict(extra="ignore")


class DatasetCreateIgnoreExtra(schemas.DatasetCreate):
    model_config = ConfigDict(extra="ignore")


# Create a new model class with the desired config
class ExperimentCreateIgnoreExtra(schemas.ExperimentCreate):
    model_config = ConfigDict(extra="ignore")
    model: ModelCreateIgnoreExtra | None
    judge_model: ModelCreateIgnoreExtra | None
    dataset: str | DatasetCreateIgnoreExtra | None


def experiments_to_gridcv(experiments: list[dict]) -> schemas.GridCV | None:
    """
    Convert a list of experiments to GridCV format by identifying common parameters.

    Args:
        experiments: List of experiment dictionaries

    Returns:
        GridCV object if conversion is possible, None otherwise
    """
    if not experiments:
        return None

    if len(experiments) == 1:
        # Single experiment - no grid search needed
        return None

    # Convert experiments to comparable format
    exp_dicts = []
    for exp in experiments:
        exp_dict = {}
        for key, value in exp.items():
            if isinstance(value, dict):
                exp_dict[key] = value
            else:
                exp_dict[key] = value
        exp_dicts.append(exp_dict)

    # Find common parameters (same across all experiments)
    common_params = {}
    grid_params = {}

    # Get all keys from first experiment
    all_keys = set()
    for exp in exp_dicts:
        all_keys.update(exp.keys())

    for key in all_keys:
        if key in ["name"]:
            continue
        values = []
        for exp in exp_dicts:
            if key in exp:
                values.append(exp[key])
            else:
                values.append(None)

        # Check if all values are the same
        if all(v == values[0] for v in values):
            common_params[key] = values[0]
        else:
            # Collect unique values for grid params
            unique_values = []
            for v in values:
                if v not in unique_values:
                    unique_values.append(v)
            grid_params[key] = unique_values

    # If no varying parameters, return None
    if not grid_params:
        return None

    # Detect repeat value by finding the GCD of counts of each unique value
    repeat = 1
    if grid_params:
        # Count occurrences of each unique value for each parameter
        value_counts = []
        for key in grid_params:
            values = []
            for exp in exp_dicts:
                if key in exp:
                    values.append(exp[key])
                else:
                    values.append(None)

            # Count occurrences of each unique value
            for unique_val in grid_params[key]:
                count = values.count(unique_val)
                value_counts.append(count)

        # Find GCD of all counts
        if value_counts:
            from math import gcd

            repeat = value_counts[0]
            for count in value_counts[1:]:
                repeat = gcd(repeat, count)

    return schemas.GridCV(common_params=common_params, grid_params=grid_params, repeat=repeat)


# Update your conversion code:
def convert_experimentset_to_create(experimentset):
    # Extract parameters
    expset = {
        "name": experimentset.get("name", ""),
        "readme": experimentset.get("readme", ""),
        "experiments": [],
    }

    # Transform full Experiment objects to ExperimentCreate objects
    for exp in experimentset.get("experiments", []):
        # Parse the full Experiment object
        exp = exp.copy()
        exp["experiment_set_id"] = None

        if exp.get("model"):
            exp["model"]["api_key"] = "YOUR_MODEL_API_KEY"

        if exp.get("judge_model"):
            exp["judge_model"]["api_key"] = "YOUR_MODEL_API_KEY"

        exp["metrics"] = [
            schemas.MetricParametrized(name=r["metric_name"], params=r.get("metric_params"))
            for r in exp["results"]
        ]
        exp["dataset"] = exp["dataset"]["name"]

        exp_create = ExperimentCreateIgnoreExtra.parse_obj(exp)
        expset["experiments"].append(exp_create.model_dump(exclude_none=True))

    # Try to convert to GridCV format
    cv = experiments_to_gridcv(expset["experiments"])

    if cv:  # Only use CV if there are actually varying parameters
        expset.pop("experiments")
        expset["cv"] = cv.model_dump(exclude_defaults=True)

    return expset
