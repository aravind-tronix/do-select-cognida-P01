# do-select-cognida-P01

This project is designed to provide a flexible and efficient solution for dynamically processing and evaluating complex datasets using mathematical expressions. Developed using FastAPI, this API is capable of interpreting formulas involving various data types, including numbers, strings, booleans, dates, and currencies, and supports formula chaining for more advanced computations.

## Features

Dynamic Formula Evaluation: Accepts JSON payloads with structured data and a series of mathematical expressions.
Formula Validation: Ensures all expressions are mathematically valid before execution.
Formula Chaining: Supports chained calculations where the output of one formula becomes the input for another.
Data Type Support: Handles multiple data types including numbers, booleans, dates, percentages, and currencies.
High Performance: Optimized for sub-second response times, even under high loads.

## API Overview

Endpoint: `/api/v1/execute-formula`
The API is designed with proper structuring of directories with versioning.
Maintaining a directory level versioning makes it easier for a developer to identify a particular version in the code base while upgrading/developing.

## Folder structure Overview

Organization: A well-organized folder structure makes it easier to locate and manage your application's files and modules. By grouping related files together in directories, you can quickly navigate through the codebase and understand its structure.

Scalability: As your application grows, having a clear folder structure helps maintain scalability. It allows you to add new features, endpoints, and modules without cluttering the main directory or getting lost in a tangled mess of files.

Modularity: A modular folder structure promotes code reusability and maintainability. By breaking down your application into smaller, self-contained modules or packages, you can easily update, replace, or extend specific components without affecting the entire application.

Separation of Concerns: A well-structured folder layout encourages the separation of concerns, where different parts of your application handle distinct responsibilities. For example, you might have separate directories for routes, models, controllers, middleware, static files, templates, etc., each focusing on a specific aspect of the application.

Collaboration: When working in a team environment, a standardized folder structure helps team members understand where to find specific files and how to contribute to the project consistently. It reduces confusion and minimizes the learning curve for new team members joining the project.

Testing and Debugging: A clear folder structure makes it easier to write tests for your application and debug issues. Test files can be organized alongside the corresponding modules they are testing, and debugging becomes more straightforward when code is logically grouped.

FastAPI itself doesn't enforce a specific folder structure, as it gives you the flexibility to organize your application in a way that best suits your needs. However, following best practices for folder structure, such as those outlined above, can greatly improve the maintainability, scalability, and collaboration aspects of your FastAPI project.

## Request model

In FastAPI, request models are used to define the structure and data types expected in the request body for API endpoints that accept POST, PUT, or PATCH requests. These request models are typically defined using Pydantic models, which allow you to specify the expected data shape, data types, validation rules, and more.

## Response model

In FastAPI, response models are used to define the structure and data types of the responses returned by API endpoints. By specifying response models, you can ensure that the data returned by your endpoints is well-structured, typed, and documented. FastAPI automatically serializes the response data to JSON based on the defined response models.

## Why FastAPI

The reason for slecting FastAPI is, it is

- modern python framework
- As the name implies, faster development time
- seamless data validating via pydantic

## Installation

- create a conda environment by
  `conda create -n env_name python=3.9`
  Note: python version > 3.9.xx is required
- clone the repo and install requirements by running the command from requirements folder
  `pip install -r requirements.txt`
- start the server by
  `fastapi run main.py`

## test coverage

- run the test coverage by
  `pytest --cov`

## API specs - AWS (manual hosting)

API specs can be found on
https://2lx003f6l5.execute-api.us-east-1.amazonaws.com/dev/api/v1/docs#/

- the app is hosted on AWS lambda
- the core_services are converted into lambda layers
- other services are uploaded to lambda functions
- the lambda is invoked by API gateway.
