az version
az extension list
az extension remove -n azure-cli-ml
az extension remove -n ml
az extension add -n ml -y

az configure --defaults group="<your id>" workspace="<your id>"
az account set --subscription <your id>

az login

# <hello_mlflow> - works ok
az ml environment create --file env-sample.yml
az ml job create -f aml_train.yml
# </hello_mlflow>

# <fbprophet_sample>
az ml environment create --file env-fbp-sample.yml
az ml job create --file job_fbp_sample_train.yml
# </fbprophet_sample>

# <fbprophet_BTC>
az ml environment create --file env-fbp-sweep.yml
az ml job create --file job_fbp_sweep.yml
# </fbprophet_BTC>