Persona-Driven Document Intelligence
This project is a solution for the Adobe Hackathon 2025 (Problem 1b). It's an offline system that analyzes a collection of PDF documents and extracts the most relevant sections based on a given user persona and their job-to-be-done.

How to Build and Run
The entire solution is containerized using Docker for easy and consistent execution.

Prerequisites
Docker must be installed and running on your machine.

Instructions
Place Input Files: Add your test case folder (containing PDFs and an input.json file) into the input/ directory. For example: input/test_case_1/.

Build the Docker Image: Open a terminal in the project's root directory and run the build command.

docker build --platform linux/amd64 -t doc-intel-1b:1.0 .

Run the Container: Execute the following command to run the script. It will process the files from the input folder and save the result to output/challenge1b_output.json.

docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" --network none doc-intel-1b:1.0

(Note for Windows users: In Command Prompt, replace $(pwd) with %cd%. In PowerShell, use ${pwd}.)

NOTE: please run download_model.py first or either unarchieve the zip folder from unstop website to run this project properly
