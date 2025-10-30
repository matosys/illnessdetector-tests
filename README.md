# BalderHub CRUD Example: Illness-Detector

It includes a sample web application that asks users a series of conditional questions to determine their possible 
illness. You can find the Flask app in the 
[``./docker/webdriver`` directory of this repository](https://github.com/matosys/illnessdetector-tests/tree/main/docker/webserver).

## Application Overview

The following screenshots show the flow of the app, when pressing "Yes" for every question:

The following screenshots illustrate the flow of the application when the user selects "Yes" for every question:

![Application: First Question](docs/static/question1.png)

![Application: Second Question](docs/static/question2.png)

![Application: Third Question](docs/static/question3.png)

![Application: Result](docs/static/result.png)

If you select "No" for a question, the app will display different follow-up questions.

When you provide answers, the Flask app stores your decisions in an SQLite database. It uses the session ID as a 
reference to keep track of each user's choices, allowing for easy retrieval and analysis of the session data later on.

## Testing

We will test the user's workflow through the illness-detector application. We also need to verify that the data is 
correctly stored in the database. This includes not only the questions asked and the user's answers but also the final 
result, such as the detected illness. Both the workflow and the database entries are checked to ensure everything works 
as expected.


### Using ``balderhub-crud``

We are using the ``balderhub-crud`` package. This package provides ready-made 
test scenarios for creating, updating, reading, and deleting data items. In our tests, we specifically use the 
``ScenarioSingleCreateTriangle`` scenario. We have imported it in the file 
[./src/scenario_balderhub.py](https://github.com/matosys/illnessdetector-tests/blob/main/src/scenario_balderhub.py).

According to the package documentation, we need to implement several features to make this work. These features are 
assigned to different "devices" in the Balder framework, which represent roles in the testing setup.

* **Creator device**: triggers and executes the creation of the data
  * **implementation of [``balderhub.data.lib.scenario_features.ExampleDataProviderFeature``](https://github.com/balder-dev/balderhub-data/blob/main/src/balderhub/data/lib/scenario_features/example_data_provider_feature.py)**: holds the example data to be entered into the app, along with the expected result.
  * **implementation of [``balderhub.crud.lib.scenario_features.SingleDataCreatorFeature``](https://github.com/balder-dev/balderhub-crud/blob/main/src/balderhub/crud/lib/scenario_features/single_data_creator_feature.py)**: provides bindings to the application for filling out the questions automatically during tests.
* **Reader device**: will read the database file and returns list of all existing entries
  * **implementation of [``balderhub.crud.lib.scenario_features.MultipleDataReaderFeature``](https://github.com/balder-dev/balderhub-crud/blob/main/src/balderhub/crud/lib/scenario_features/multiple_data_reader_feature.py)**: bindings to the SQLite database to check what data has been stored on the server.
* **PointOfTruth device**: represents our device-under-test, which is the web app itself. Since we do not have direct access to its internal code in this setup, we do not add any features here.

For the web app, we additionally , that is used within our implementation.

For interacting with the web app, we also 
[implemented an HtmlPage](https://github.com/matosys/illnessdetector-tests/blob/main/src/lib/pages.py), 
which is used in our feature implementations to simulate user interactions, such as navigating pages and submitting answers.

### Environment

The application and Selenium are provided through a Docker Compose file.

Once you start it up, you can access the Selenium Grid at http://localhost:4444 and the main application 
at http://localhost:5000.

### Running the tests

Start docker compose:

```shell
$ docker compose up -d
```

And run your test:

```shell
$ docker compose run test balder --working-dir src
```

```shell

+----------------------------------------------------------------------------------------------------------------------+
| BALDER Testsystem                                                                                                    |
|  python version 3.10.9 (main, Dec  8 2022, 02:19:14) [GCC 12.2.1 20220924] | balder version 0.1.0                    |
+----------------------------------------------------------------------------------------------------------------------+
Collect 1 Setups and 1 Scenarios
  resolve them to 1 valid variations

================================================== START TESTSESSION ===================================================
SETUP SetupApp
  SCENARIO ScenarioSingleCreateTriangle
    VARIATION ScenarioSingleCreateTriangle.Creator:SetupApp.ClientBrowser | ScenarioSingleCreateTriangle.PointOfTruth:SetupApp.InternDevice | ScenarioSingleCreateTriangle.Reader:SetupApp.DatabaseSpy
      TEST ScenarioSingleCreateTriangle.test_create_valid[Example<QuestionResultDataItem: Yes-Yes-Yes>] [.]
      TEST ScenarioSingleCreateTriangle.test_create_valid[Example<QuestionResultDataItem: No-No-No-No>] [.]
      TEST ScenarioSingleCreateTriangle.test_create_valid[Example<QuestionResultDataItem: No-Yes-Wet>] [.]
================================================== FINISH TESTSESSION ==================================================
TOTAL NOT_RUN: 0 | TOTAL FAILURE: 0 | TOTAL ERROR: 0 | TOTAL SUCCESS: 3 | TOTAL SKIP: 0 | TOTAL COVERED_BY: 0


```

### Adding REST tests

There is a branch `adding-validation-of-api` which adds webtest to the environment. You only need to provide a own implementation for
the [``balderhub.crud.lib.scenario_features.SingleDataCreatorFeature``](https://github.com/balder-dev/balderhub-crud/blob/main/src/balderhub/crud/lib/scenario_features/single_data_creator_feature.py) 
that executes the same commands to the REST and assign it to a new device in your setup:

There is a branch named ``adding-validation-of-api`` that integrates API test into the environment.  

[Have a look at the diff view](https://github.com/matosys/illnessdetector-tests/compare/main...adding-validation-of-api).
That's all needed to add the same tests for testing the api instead of the gui:

```shell
+----------------------------------------------------------------------------------------------------------------------+
| BALDER Testsystem                                                                                                    |
|  python version 3.10.9 (main, Dec  8 2022, 02:19:14) [GCC 12.2.1 20220924] | balder version 0.1.0                    |
+----------------------------------------------------------------------------------------------------------------------+
Collect 1 Setups and 1 Scenarios
  resolve them to 2 valid variations

================================================== START TESTSESSION ===================================================
SETUP SetupApp
  SCENARIO ScenarioSingleCreateTriangle
    VARIATION ScenarioSingleCreateTriangle.Creator:SetupApp.ClientBrowser | ScenarioSingleCreateTriangle.PointOfTruth:SetupApp.InternDevice | ScenarioSingleCreateTriangle.Reader:SetupApp.DatabaseSpy
      TEST ScenarioSingleCreateTriangle.test_create_valid[Example<QuestionResultDataItem: Yes-Yes-Yes>] [.]
      TEST ScenarioSingleCreateTriangle.test_create_valid[Example<QuestionResultDataItem: No-No-No-No>] [.]
      TEST ScenarioSingleCreateTriangle.test_create_valid[Example<QuestionResultDataItem: No-Yes-Wet>] [.]
    VARIATION ScenarioSingleCreateTriangle.Creator:SetupApp.ClientRest | ScenarioSingleCreateTriangle.PointOfTruth:SetupApp.InternDevice | ScenarioSingleCreateTriangle.Reader:SetupApp.DatabaseSpy
      TEST ScenarioSingleCreateTriangle.test_create_valid[Example<QuestionResultDataItem: Yes-Yes-Yes>] [.]
      TEST ScenarioSingleCreateTriangle.test_create_valid[Example<QuestionResultDataItem: No-No-No-No>] [.]
      TEST ScenarioSingleCreateTriangle.test_create_valid[Example<QuestionResultDataItem: No-Yes-Wet>] [.]
================================================== FINISH TESTSESSION ==================================================
TOTAL NOT_RUN: 0 | TOTAL FAILURE: 0 | TOTAL ERROR: 0 | TOTAL SUCCESS: 6 | TOTAL SKIP: 0 | TOTAL COVERED_BY: 0

```


# License

This software is free and Open-Source

Copyright (c)  2025  Max Stahlschmidt

Distributed under the terms of the MIT license