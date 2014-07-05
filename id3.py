__author__ = 'chirag'

# id3.py


import util
import classificationMethod
import math
import dataClassifier

class Node(object):
    def __init__(self, f, isleaf, label, zerochild, onechild):
        self.feature = f
        self.isleaf = isleaf
        self.label = label
        self.zerochild = zerochild
        self.onechild = onechild


class id3(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.

  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **

    self.labelCount = None
    self.priorProb = None
    self.condProb = []
    self.dectree = None
    self.k_ = 0.0


  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """

    # might be useful in your code later...
    # this is a list of all features in the training set.
    self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));


    if (self.automaticTuning):
        kgrid = [0.005, 0.01, 0.15, 0.2, 0.25, 0.3, 0.35, 0.40, 0.45, 0.50, 0.55, 0.6, 0.7, 0.8, 0.9 ]
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
    print kgrid
    print evalk
    i=evalk.index(max(evalk))
    self.k_ = kgrid[i]
    #print self.k_
    self.trainAndTune(trainingData, trainingLabels, [], [], [])



  def CalculateEntropy(self,trainingData, trainingLabels):
      a=[]
      for i in range(10):
          a.append(0.0000000001)

      entropy=0
      for i in trainingLabels:
          a[i]=a[i]+1

      for i in range(0, 10):
          entropy+=(-(a[i]/len(trainingLabels))* self.log2(a[i]/len(trainingLabels)))
      return entropy


  def log2(self, x ):
      return math.log( x,2 )


  def InformationGain(self,trainingData,trainingLabels):
       countzero=0.0
       countone=0.0
       zerotrainingdata=[]
       onetrainingdata=[]
       zerotraininglabels=[]
       onetraininglabels=[]
       gain={}
       entropy=self.CalculateEntropy(trainingData,trainingLabels)
      #for l in range(0,dataClassifier.DIGIT_DATUM_WIDTH):
       #   for m in range(0,dataClassifier.DIGIT_DATUM_HEIGHT):
       for l in (trainingData[0]).keys():
             countzero=0.0
             countone=0.0
             zerotrainingdata=[]
             onetrainingdata=[]
             zerotraininglabels=[]
             onetraininglabels=[]


             for i in range(len(trainingLabels)):
                 if (trainingData[i][l]==0):
                      zerotrainingdata.append(trainingData[i])
                      zerotraininglabels.append(trainingLabels[i])
                      #print zerotrainingdata
                      #print zerotraininglabels
                      countzero+=1
                 else:
                      onetrainingdata.append(trainingData[i])
                      onetraininglabels.append(trainingLabels[i])
                      countone+=1
                      #print onetrainingdata
                      #print onetraininglabels
             zeroentropy = 0.0
             oneentropy = 0.0
             if countzero != 0.0:
                zeroentropy=self.CalculateEntropy(zerotrainingdata,zerotraininglabels)
             if countone != 0.0:
                oneentropy=self.CalculateEntropy(onetrainingdata,onetraininglabels)
           #  print (l,m)
          #   print "zero"+str(zeroentropy)
          #   print "one"+str(oneentropy)
             gain[l]=entropy-(countzero/len(trainingLabels))*(zeroentropy)-(countone/len(trainingLabels))*(oneentropy)
         #    print gain[l,m]
             #print "gain"+str(gain)

       maxval = -1.0
       for i in gain.keys():
          if gain[i] >= maxval:
              maxval = gain[i]

       for i in gain.keys():
          if gain[i] == maxval:
              return (i,gain[i])


  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
      count=0
      one=0
 #     print "ID3 Called"

      self.dectree = self.decisiontree(trainingData,trainingLabels)

  def decisiontree(self,trainingData,trainingLabels):

  #    print trainingData
  #    print trainingLabels

      t = trainingLabels[0]
      alleqflag = True
      for i in trainingLabels:
          if i != t:
              alleqflag = False

      if alleqflag:
         return Node(None,True, trainingLabels[0], None, None)

      if len(trainingData[0].keys()) == 0:
          a1 = []
          for z in range(10):
            a1.append(0)

          for z in trainingLabels:
            a1[z]+=1

          l1 = a1.index(max(a1))

          return Node(None,True,l1,None,None)

 #
 # print "before info gain call"
      (f,v)=self.InformationGain(trainingData,trainingLabels)
#      print "gain"
#      print f

      if v <= self.k_:
          a1 = []
          for z in range(10):
            a1.append(0)

          for z in trainingLabels:
            a1[z]+=1

          l1 = a1.index(max(a1))

          return Node(None,True,l1,None,None)

      zerotrain=[]
      onetrain=[]
      zerotrainlabels=[]
      onetrainlabels=[]
      
      for i in range(len(trainingLabels)):
          if trainingData[i][f]==0:
              copyzerotrainingData=trainingData[i].copy()
              del copyzerotrainingData[f]
              zerotrain.append(copyzerotrainingData)
              zerotrainlabels.append(trainingLabels[i])
          else:
              copyonetrainingData=trainingData[i].copy()
              del copyonetrainingData[f]
              onetrain.append(copyonetrainingData)
              onetrainlabels.append(trainingLabels[i])



      return Node(f,False,None,self.decisiontree(zerotrain,zerotrainlabels),self.decisiontree(onetrain,onetrainlabels))

  def classify(self,testdata):
        guesses = []

        for datum in testdata:
            r=self.dectree

            while r.isleaf == False:
                if datum[r.feature] == 0:
                    r=r.zerochild
                if datum[r.feature] == 1:
                    r=r.onechild

            guesses.append(r.label)

        return guesses

