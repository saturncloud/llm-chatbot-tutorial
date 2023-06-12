# llm-chatbot-tutorial

## Download model weights

The first step is to download Vicuna model weights. If you are running in Saturn Cloud Hosted, we have stored Vicuna weights conveniently in SaturnFS. You can download the model weights with the following command:

`$ saturnfs cp --recursive sfs://community/saturncloud/shared/llm-weights/vicuna-7b/ /tmp/vicuna-7b/`

This command takes approximately 10 minutes to run. We recommend downloading to `/tmp` since Saturn Cloud free tier users may not have enough disk space to store all model weights. If you do, feel free to change the download location. If you download them to your home directory, you will not have to re-download the weights when restart your workspace.

set the `MODEL_PATH` environment variable to point to the directory where you've downloaded the weights. For example:

`export MODEL_PATH=/tmp/vicuna-7b`

## Start the streamlit application

`$ streamlit run streamlit/chat.py`


## To run this in Saturn Cloud in a Jupyter notebook:

[![Run in Saturn Cloud](https://saturncloud.io/images/embed/run-in-saturn-cloud.svg)](https://app.community.saturnenterprise.io/dash/o/community/resources?templateId=9926e5ceb5ea44248babd3217f95e45b)

Or to deploy the streamlit application:

[![Run in Saturn Cloud](https://saturncloud.io/images/embed/run-in-saturn-cloud.svg)](https://app.community.saturnenterprise.io/dash/o/community/resources?templateId=b66bf80f75154deea4800febdafbdbb3)
