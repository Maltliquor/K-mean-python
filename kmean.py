#coding=utf-8
from __future__ import division
from numpy import *


dataLabel = []
def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split(',')
        label = curLine.pop()
        dataLabel.append(label)
        
        fltLine = map(float, curLine)
        dataMat.append(fltLine)
    # print(dataLabel)
    return dataMat
    
#计算两个向量的距离，用的是欧几里得距离
def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))

#随机生成初始的质心（ng的课说的初始方式是随机选K个点）    
def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))
    for j in range(n):
        minJ = min(dataSet[:,j])
        rangeJ = float(max(array(dataSet)[:,j]) - minJ)
        centroids[:,j] = minJ + rangeJ * random.rand(k,1)
    return centroids
    
def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))#create mat to assign data points 
                                      #to a centroid, also holds SE of each point
                                      #clusterAssment[0] represented the centroid
                                      #clusterAssment[0] represented the distance from center
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):#for each data point assign it to the closest centroid
            minDist = inf  #infinite
            minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j,:],dataSet[i,:])   # every sample's distance with every center
                if distJI < minDist:
                    minDist = distJI;   # update mindist
                    minIndex = j
            if clusterAssment[i,0] != minIndex:   #update center isn't equal to previous one
                clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        # print (centroids)
        for cent in range(k):# recalculate centroids
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]#get all the point in this cluster
            centroids[cent,:] = mean(ptsInClust, axis=0) #assign centroid to mean 
    return centroids, clusterAssment
    
def show(dataSet, k, centroids, clusterAssment):
    from matplotlib import pyplot as plt  
    numSamples, dim = dataSet.shape        # sample number
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']  
    for i in xrange(numSamples):          
        # show data points
        markIndex = int(clusterAssment[i, 0])  
        plt.plot( dataSet[i, 1], dataSet[i,2], mark[markIndex])  
    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']  
    for i in range(k):  
        # show centroids
        plt.plot(centroids[i, 1], centroids[i, 2], mark[i], markersize = 12)  
    plt.show()
    
def rank_index(clusterAssment,dataLabel):
    A = 0
    B = 0
    C = 0
    D = 0
    numSamples = len(dataLabel)
    for i in range(numSamples):
        for j in range(i+1,numSamples):
            if dataLabel[i] == dataLabel[j] :
                if clusterAssment[i, 0] == clusterAssment[j, 0] :
                    A = A + 1
                else: B = B + 1
            else: 
                if clusterAssment[i, 0] == clusterAssment[j, 0] :
                    C = C + 1
                else: D = D + 1
    print(A,B,C,D)
    accuracy = (A+D)/(A+B+C+D)*100
    return accuracy
            
      
def main():
    dataMat = mat(loadDataSet('pillmaData.txt'))
    myCentroids, clustAssing= kMeans(dataMat,2)
    print myCentroids
    accuracy = rank_index(clustAssing,dataLabel)
    print('%d%%' %accuracy)
    # show(dataMat, 2, myCentroids, clustAssing)  
    
    
if __name__ == '__main__':
    main()