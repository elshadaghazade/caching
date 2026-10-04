# Python Backend: Caching Service

## FastAPI Microservice // Caching service

The goal of this coding task is to assess your problem-solving and coding skills as a developer. This task is based on a real feature in our software stack, and therefore the code should adhere to high coding standards, as expected from any code submitted by our developers. Keep in mind that your code will be reviewed and evaluated as if you are submitting code to our product.

**Description**: Create a simple caching microservice using FastAPI. The service should:

1. Provide endpoints to create and read generated payloads files. The _create_ endpoint returns an identifier of the generated payload, and the _read_ endpoint returns the actual payload.
2. Payloads are generated as follows:
    - The input is two lists of strings (of same length)
    - The strings are transformed by a "transformer function" (to simulate external service)
    - The output is the interleaving of the transformed strings from the two lists
3. The service should cache the outcome of the "transformer function" for use in future requests. (Note: minimize the calls number of calls to the "transformer function", i.e. service).
    - Reuse cached outcomes instead of calling the "transformer function" if possible
    - Reuse payload identifier for generated payloads already generated before
4. Store the cached outcome results in a SQLite or PostgreSQL database.
5. In addition to the service, write a simple CLI tool that can be used to test the service programattically.

**Requirements**:

- Use FastAPI to create the API endpoints.
- Use SQLModel or SQLAlchemy for database interactions.
- Dockerize the application for deployment.

**Sample Input**:

- POST /payload with JSON payload

    ```json
    {
      "list_1": ["first string", "second string", "third string"],
      "list_2": ["other string", "another string", "last string"]
    }
    ```

- GET /payload/{id}

**Sample Output**:

- Confirmation message for POST request, with the identifier of the newly created payload
- Response with generated payload for GET requests. For the example above

    ```json
    {
      "output": "FIRST STRING, OTHER STRING, SECOND STRING, ANOTHER STRING, THIRD STRING, LAST STRING"
    }
    ```

**CLI tool:**

- The tools should use Pydantc Settings to implement command line parsing and sanitizing of the input parameters.

- Command line arguments are as follows:

    ```bash
    cache-cli [-h|--host URL] [-r|--repeat N] [-i|--input FILE|-] [-j|--json JSON] [-o|--output FILE|-] [-h|--help]

    # Where:
    # "--host" points to the server
    # "--repeat" inidcates number of iterations
    # "--input" indicates the input file ("-" for stdin)
    # "--json" indicates an input argument in json from (properly escaped)
    # "--output" indicates the output file ("-" for stdout)
    ```

**Guidelines for coding assessment**

- Thoroughly review the task, make sure the goal and the requirements are clear. Communicate directly any questions and concerns.
- Follow the coding style and conventions when writing your code/scripts. Write clear and concise comments and documentation, focus on the "why" (not on the "how").
- Use _git_ for version control. Commit in small and manageable chunks with meaningful commit messages. Review and clean up the code before final submission. Refactor the code as needed.
- Test and debug your code. Add some tests to demonstrate knowledge of unit- and integration-testing. It's ok to make necessary shortcuts as long as they are clearly documented and justified.

## Submission

AI tools are allowed. You own every line you submit: at the interview you explain your decisions and change the solution live.

Reply to the email you got this task in with two links.

**1. Git repository.** A public repository on GitHub or GitLab, keep the commit history: we read how the solution grew, so do not squash it into one commit. Give the repository a neutral name, without our company name in it. 

**2. Video walkthrough.** Loom or an unlisted YouTube video, up to 10 minutes, in English, screen share with your camera on. One take is fine, we do not grade the editing. 

In the same reply, tell us how many hours the task really took. It does not affect the result, we use it to calibrate the task.