# Takon
A chat application integrated with LLMs.

# Introduction
Takon is a chat application integrated with a Large Language Model (LLM). 
Currently, it provides features similar to Chat-GPT. The supported LLM 
models include:

- Google Gemini
  - gemini-pro
  - gemini-pro-vision (coming soon)
- GPT (coming soon)

The User Interface (UI) of this application is created using [Streamlit](https://streamlit.io/).

# Installation
## Python Environment
Takon uses `pipenv` to manage its Python environment and dependencies.
Follow these steps to set up the Python environment for this project:

1. **Install Pipenv**\
    If you haven't already installed `pipenv`, you can do with `pip`.
    ```bash
   pip install pipenv
    ```

2. **Create the Virtual Environment and Install Dependencies**\
   Run the following command in your project directory to create a 
virtual environment and install the project's dependencies from the `Pipfile.lock`:

   ```bash
   pipenv install --dev
   ```

3. **Activate the Virtual Environment**\
   To activate the virtual environment, use the following command:

   ```bash
   pipenv shell
   ```

4. **Running the Application**\
   You can now run the applications. Use the following command:

   ```bash
   streamlit run main.py
   ```

## Environment Variables
To use this application, setting environment variable is required. 
The required environment variable is `GOOGLE_API_KEY`, which contains 
the API key for the Google Gemini model. The API Key value is stored 
in a secret file that managed by Streamlit, where the global secret 
file is stored at `~/.streamlit/secrets.toml` for macOS/Linux or 
`%userprofile%/.streamlit/secrets.toml` for Windows.

Example of content of the file:
```toml
GOOGLE_API_KEY="SECRET KEY VALUE"
```

If you do not have a Google API Key, you can visit [Get an API Key](https://ai.google.dev/tutorials/setup)
to get the API Key.

# Contributing
We welcome contributions from the community to make this project even 
better! If you have ideas, bug fixes, or new features to propose, feel 
free to open an issue or submit a pull request.
