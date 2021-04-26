from __future__ import print_function
import functools
from behave.model import ScenarioOutline


def scenario_repeat(scenario, max_attempts=3):
    """
    any scenario with tag @autorepeat will be repeated "max_attempts" times
    example:
                @autorepeat @12
                Scenario: check propreports_api_daily_import
                    Given get random ticker (review_date==2020-08-18)
    :param scenario: object of scenario
    :param max_attempts: number of repeats
    """
    def scenario_run_with_retries(scenario_run, scenario,  *args, **kwargs):
        for attempt in range(1, max_attempts+1):
            scenario_run(*args, **kwargs)
            if str(scenario.status) == "Status.failed":
                break
        return True

    if isinstance(scenario, ScenarioOutline):
        scenario_outline = scenario
        for scenario in scenario_outline.scenarios:
            scenario_run = scenario.run
            scenario.run = functools.partial(scenario_run_with_retries, scenario_run, scenario)
    else:
        scenario_run = scenario.run
        scenario.run = functools.partial(scenario_run_with_retries, scenario_run, scenario)
