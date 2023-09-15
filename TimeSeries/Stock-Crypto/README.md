# Credits
Mostly developed by me, but LSTM backbone Keras framework adopted from here: https://www.altumintelligence.com/articles/a/Time-Series-Prediction-Using-LSTM-Deep-Neural-Networks 
Huge thanks also to this fantastic resources:
- https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/ 
- https://arxiv.org/abs/2104.09700 

# How does it work?
Program atempts to forecast if Bitcoin price (or any other asset price) will go up or down in next few days - see above article (arxiv).
It is using asset price and other signals (like feer and greed index).
Current version (v3) is using few (~5) different LSTM models in each run.

## Conclusion
Some models have certain predictive power (certainly above random guess).
LSTM models are not working that well. I suspect that they cant cope with high degree of randomness in the market.

## Future work
I would like to expand the solutioon to use Transformes and also XGBoost / CatBoost in next versions

# The program can run in following modes
1. on local PC (compute): `v3\main_daily.ipynb`
2. on Azure ML: `v3-aml\pipeline-singlestep-train-eval`

## 1. Running on local PC
- make sure to use the conda environment `..\environment.yaml`
- run notebook `v3\main_daily.ipynb`

## 2. Running on Azure ML
### preprequisites: 
- You need to have Azure ML (AML) and all prerequisites: https://learn.microsoft.com/en-us/azure/machine-learning/overview-what-is-azure-machine-learning?view=azureml-api-2 
- Have a storage account (can be the same AML is using to store data) - see config.yaml to setup the path to data
- create a data store in AML to mount data path. Make sure AML has access to the Storage account (in IAM settings)
- create compute instance and compute target (see naming conventions expected in `ccb_pipeline.ipynb`)
- upload code files to AML workspace
### To schedule to run it (one time)
- on AML compute instance run notebook `v3-aml\environment\environment.ipynb` to create AML environment
- on AML compute instance run notebook `v3-aml\pipeline-singlestep-train-eval\ccb_pipeline.ipynb` to create & schedule AML pipeline. Default timing is daily, but you can adjust in the notebook
### To evaluate results
- on AML compute instance run notebook `v3-aml\pipeline-singlestep-train-eval\v3-aml\model-eval.ipynb`
### Good to know
The run cost of v3 on AML is ~ $50 / month if you run jobs daily.