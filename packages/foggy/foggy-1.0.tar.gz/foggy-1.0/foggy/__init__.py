"""  foggy is a python package for training and testing convolutional 
neural networks on atmospheric grib files to predict the occurence 
of fog at airports.  """

from .foggy import (ReDirecter, DataDealer, Normalizer, RandomSampler, DataframeCreator, DFtoCSVSaver, QuickPlotter, RightSideUpPlotter,
	 				Base5kBuilder, Base3kBuilder, CropBuilder, ModelSaver, ModelLoader, 
	 				ROCScorer)

from .mainloop import (CNNActivator)