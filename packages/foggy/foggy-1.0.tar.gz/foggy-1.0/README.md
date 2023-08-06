# foggy

foggy package for Pypi

foggy is a python package for training and testing convolutional 
	 neural networks on atmospheric grib files to predict the occurrence 
	 of fog at airports. 

## How to install foggy

"""
pip install foggy
"""

## How to run foggy
"""

Can be run individually or use CNNActivator() which does the following:

1. Create dataframe (using DataframeCreator) of all of the dates in column 1 and whether 	it was a fog event or not in column 2.

2. ReDirecter: takes balanced subset of data files (all fog and some no fog) moves to new 	 folder
   DataDealer: Extracts data (eg. mslp and rh) into X and uses fog or nofog column from the dataframe as Y
   Normalizer: Normalizes X

3. Build CNN model with Base5kBuilder

4. Split data into test and train 

5. Then use RandomSampler to randomly oversample data to obtain more data 

6. Test model: prints a confusion matrix 

7. Save the model! Inbuilt try and if statements to help save computing time if dataframe, 	  model, etc. are already saved

7. ROC metric and the AUC to evaluate how good the model was


"""
