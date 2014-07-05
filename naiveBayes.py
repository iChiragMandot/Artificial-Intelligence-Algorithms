# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
import classificationMethod
import math
import dataClassifier

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method *
    self.pfeaturegivenlabel = []
    self.plabels = []
    self.k_ = 0.0
    
  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

 # def oddsratio(self, trainingData, trainingLabels ):


  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    # might be useful in your code later...
    # this is a list of all features in the training set.
    self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));
    
    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]

    evalk = []


    for i in kgrid:
        self.k_ = i
        self.trainAndTune(trainingData, trainingLabels, [], [],  [])
        guesses = self.classify(validationData)

        zipped= zip(guesses,validationLabels)

        c1=0.0
        n1=0.0
        for i,j in zipped:
            if i == j:
                c1+=1
            n1+=1

        evalk.append(c1/n1)

  #  print evalk

    i=evalk.index(max(evalk))
    self.k_ = kgrid[i]
    self.trainAndTune(trainingData, trainingLabels, [], [], [])

  def flatindex(self,i,j,k,l):
      """
      there are 28 values of i, 28 values of j, 2 values of k , and 10 values of label all 0 based
      """
      return 28*3*10*i + 3*10*j + 10*k + l



  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter 
    that gives the best accuracy on the held-out validationData.
    
    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """

    countlabels = []
    n = len(trainingData)

    for i in range(10):
        countlabels.append(0.0)
        self.plabels.append(0.0)

    countfeaturegivenlabel = [ ]

    for i in range(100000):
        countfeaturegivenlabel.append(0.0)
        self.pfeaturegivenlabel.append(0.0)


    for i in trainingLabels:

        countlabels[i] = countlabels[i] + 1


    #self.plabels = { }

    for i in range(0,10):
        self.plabels[i]=countlabels[i]/n


    fulltraining = zip(trainingData, trainingLabels)


    for i,j in fulltraining:
            for k in i.keys():
                l = i[k]
                countfeaturegivenlabel[ self.flatindex(k[0],k[1],l,j) ] +=  1



    for ij in self.features:
            for k in range(len(self.legalLabels)):
                for l in range(0,10):
                    self.pfeaturegivenlabel[self.flatindex(ij[0],ij[1],k,l)] = (countfeaturegivenlabel[self.flatindex(ij[0],ij[1],k,l)] + self.k_) / (countlabels[l] + 2*self.k_)


  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.
    
    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses
      
  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.    
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """
    logJoint = util.Counter()
    for l in range(0,10):
      #  print l
        lg = math.log(self.plabels[l],2)
        for i in datum.keys():
   #         print self.pfeaturegivenlabel[self.flatindex(i[0],i[1],datum[i],l)]
            lg+=  math.log(self.pfeaturegivenlabel[self.flatindex(i[0],i[1],datum[i],l)],2)
        logJoint[l]=lg

    return logJoint
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
    

  
  def findHighOddsFeatures(self, label1, label2,trainingData, trainingLabels):
    """
    Returns the 100 best features for the odds ratio:
            P(feature=1 | label1)/P(feature=1 | label2) 
    
    Note: you may find 'self.features' a useful way to loop through all possible features
    """
    featuresOdds = []

    countfeaturegivenlabel = [ ]
    pfeaturegivenlabel = [ ]

    for i in range(100000):
        countfeaturegivenlabel.append(0.0)
        pfeaturegivenlabel.append(0.0)

    fulltraining = zip(trainingData, trainingLabels)

    countlabels = []
    for z in range(len(self.legalLabels)):
            countlabels.append(0.0)

    for i in trainingLabels:
        countlabels[i] = countlabels[i] + 1

    for i,j in fulltraining:
            for k in i.keys():
                l = i[k]
                countfeaturegivenlabel[ self.flatindex(k[0],k[1],l,j) ] +=  1


    for ij in self.features:
            for k in range(0,2):
                for l in range(0,10):
                    pfeaturegivenlabel[self.flatindex(ij[0],ij[1],k,l)] = (countfeaturegivenlabel[self.flatindex(ij[0],ij[1],k,l)] + self.k) / (countlabels[l] + 2*self.k)

    featureslist = []

    for f in self.features:
        featureslist.append( ( pfeaturegivenlabel[self.flatindex(f[0],f[1],1,label1)]/ pfeaturegivenlabel[self.flatindex(f[0],f[1],1,label2)] , f) )

    featureslist.sort()
    featureslist.reverse()

    cnt = 0
    for f in featureslist:
      if cnt < 100:
        featuresOdds.append(f[0])

    cnt+=1

    return featuresOdds[:100]
    

    
      
