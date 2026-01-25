# ci_blogpost

Here you can find the scripts referenced by the SAP Blogpost.

In case you want to give it a try to build / try out the demo on your own, please note that there are some adjustments you will need to do:

- In llm_model/download_model.py enter your huggingface token.
- In fastapi/app/mariadb_client.py enter your password.

In case you want to give it a go and use a different model, please pay attention to the following files as well:

- In fastapi/app/llm_client.py, please adjust the MODEL_PATH variable as it contains the specific model.
- In llm_model/download_model.py make sure to adjust the repo & filename.
    
