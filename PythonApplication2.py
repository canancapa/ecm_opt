from __future__ import print_function
from ortools.linear_solver import pywraplp
from random import randrange

def create_data_model():
    data = {}
    data['times']={1:{'day':'T1', 'threshold':0,'budget':2},
                   2:{'day':'T2', 'threshold':0,'budget':2},
                   3:{'day':'T3', 'threshold':0,'budget':2},
                   4:{'day':'T4', 'threshold':0,'budget':2},
                   5:{'day':'T5', 'threshold':0,'budget':2},
                   6:{'day':'T6', 'threshold':0,'budget':2}}
    data['times'].update({7:{'day':'T7', 'threshold':0}})
    data['channels']={1:{'name':'EM','cost':0.10,'capacity':5},2:{'name':'SMS','cost':2.50,'capacity':4}}
    #data['channels'].update({3:{'name':'DM','cost':1.0}})
    data['categories']={1:'PUC01',2:'PUC02'}
    data['campaigns'] = {1:{'id':1,'dType':'OFFER','category':'PUC01','priority':5,'threshold':0,'budget':2},
                         2:{'id':2,'dType':'OFFER','category':'PUC01','priority':10,'threshold':0,'budget':2},
                         3:{'id':3,'dType':'OFFER','category':'PUC02','priority':15,'threshold':0,'budget':2}}
    data['customers'] = {  1:{'id':1, 'churn':0.90},
                           2:{'id':2,'churn':0.50}};  
    data['probability'] = [	[1.0, 1.0, 1.0],
				            [1.00, 1, 1]]; 
    data['offers'] = {    1: {'id':1,'revenue': 100,'capacity':2},
                          2: {'id':2,'revenue':  100,'capacity':2},
                          3: {'id':3,'revenue':  100,'capacity':2} };
    data['Ici'] = [     [1,1],
                        [1,1],
                        [1,1]];    
    data['Oco'] = [     [1,1,1],
                        [1,1,1],
                        [1,1,1]];
    data['active'] = [ 	[1, 1, 1, 1, 1, 1, 1],
			            [1, 1, 1, 1, 1, 1, 1],
			            [1, 1, 1, 1, 1, 1, 1]];
    data['E'] =[[1, 1, 1],
	            [1, 1, 1]];
    data['PRESENT'] =[	[0, 0, 0],
			            [0, 0, 0]];
    data['PRESENT_io'] =[	[0, 0, 0],
			                [0, 0, 0]];
    data['DSLC'] =[	[[5, 4],[5,9]],
		            [[3, 5],[4,5]]];
    data['CONTACT']=[	[2, 3],
			            [2, 3]];
    data['CONSENT']=[	[[1,1],[1,1],[1,1]],
			            [[1,1],[1,1],[1,1]]];
    data['ChannelAv']=[	[1,1],
			            [1,1]];
    data['dTypes'] =  {    1:{'name':'INFO'},
                           2:{'name':'OFFER'}};
    data['threshold'] =  6;
    data['capacity']= [	    [1,1,1,1,1,1,1],
				            [1,1,1,1,1,1,1]];
    data['budget']=7;
    data['constConfig']={   1:{'name': 'OVERLAP','status': 1},
                            2:{'name': 'PRESENT_CAMPAIGN','status': 1},
                            3:{'name': 'PRESENT_OFFER','status': 1},
                            4:{'name': 'ELIGIBILITY_CONTACT','status': 1},
                            5:{'name': 'ELIGIBILITY_CONSENT','status': 1},
                            6:{'name': 'CAPACITY_CHANNEL','status': 0},
                            7:{'name': 'CAPACITY_OFFER','status': 1},
                            8:{'name': 'BUDGET','status': 0},
                            9:{'name': 'ELIGIBILITY_CHANNEL','status': 0},
                            10:{'name': 'ELIGIBILITY_OFFER','status': 0}
                            };
    return data
def printSolution2(solver, data, X, Y):
    print('Solution:')
    print('Objective value =', solver.Objective().Value()+0)
    print('X=')
    for i in range(len(data['customers'])):
        for c in range(len(data['campaigns'])):
           for v in range(len(data['channels'])):
             for t in range(len(data['times'])):
                print('X{}{}{}{}'.format(i,c,v,t),':',X[i,c,v,t].solution_value(), end=" ")
             print()
           print()
        print()

    print('Y=')
    for i in range(len(data['customers'])):
        for c in range(len(data['campaigns'])):
           for o in range(len(data['offers'])):
             for t in range(len(data['times'])):
                   print('Y{}{}{}{}'.format(i,c,o,t),':',Y[i,c,o,t].solution_value(), end=" ")
             print()
           print()
        print()  
def printSolution(solver, data, X, Y):
    print('Solution:')
    print('Objective value =', solver.Objective().Value()+0)
    campaignResult={}
    for c in range(len(data['campaigns'])):
        offersC={}
        channelsC={}
        campaignCost=0
        campaignTargetCount=0
        campaignRevenue=0                                                          
        iter1=0   
        iter=0
        print('C:',c+1)
        for i in range(len(data['customers'])):
            for t in range(len(data['times'])):
               for v in range(len(data['channels'])):
                        if(X[i,c,v,t].solution_value()>0):
                            iter1+=1
                            print('iter1:',iter1)
                            if(iter1==1):
                                channelsC.update({iter1:{'key':data['channels'][v+1]['name']}})
                            else:
                                for w in range(len(channelsC)):
                                    if(channelsC[w+1]['key']!=data['channels'][v+1]['name']):
                                        channelsC.update({iter1:{'key':data['channels'][v+1]['name']}})
                            print(channelsC)
                            campaignTargetCount+=1
                            if('cost' in data['channels'][v+1]):
                                campaignCost+=data['channels'][v+1]['cost']

        print('C',c+1,':',channelsC)
        for i in range(len(data['customers'])):
                 for t in range(len(data['times'])):
                    iter=0
                    for o in range(len(data['offers'])):
                        if(Y[i,c,o,t].solution_value()>0):
                            iter+=1
                            offersC.update({iter:{'key':data['offers'][o+1]['id']}})
                            campaignRevenue+=data['offers'][o+1]['revenue']*data['probability'][i][o]
        #print(offersC)
        campaignResult.update({data['campaigns'][c+1]['id']: {'campaignID':data['campaigns'][c+1]['id'], 
                                                                        'campaignCost':campaignCost,
                                                                        'targetCount':campaignTargetCount,
                                                                        'expected revenue':campaignRevenue,
                                                                        'expected profit':campaignRevenue-campaignCost,
                                                                        'ofrList':offersC,
                                                                        'channelList':channelsC
                                                                        }})       
    print(campaignResult)
    targetCount=0
    totalScore=0
    totalCost=0
    for i in range(len(data['customers'])):
        for c in range(len(data['campaigns'])):
           for v in range(len(data['channels'])):
             for t in range(len(data['times'])):
                targetCount+=X[i,c,v,t].solution_value()
                totalScore+=X[i,c,v,t].solution_value()*data['campaigns'][c+1]['priority']
                if('cost' in data['channels'][v+1]):
                    totalCost+=X[i,c,v,t].solution_value()*data['channels'][v+1]['cost']

    totalRevenue=0
    totalConversion=0
    totalChurn=0
    for i in range(len(data['customers'])):
        for c in range(len(data['campaigns'])):
           for o in range(len(data['offers'])):
             for t in range(len(data['times'])):
                    if('revenue' in data['offers'][o+1] and 'probability' in data):
                        totalRevenue+=Y[i,c,o,t].solution_value()*data['offers'][o+1]['revenue']*data['probability'][i][o]
                    if('probability' in data):
                        totalConversion+=Y[i,c,o,t].solution_value()*data['probability'][i][o]
                    if('churn'in data['customers'][i+1] and 'probability' in data):
                        totalChurn+=Y[i,c,o,t].solution_value()*data['customers'][i+1]['churn']*data['probability'][i][o]
                   
    print('target count:',targetCount)
    print('total score:',totalScore)
    print('total cost:',totalCost)
    print('total revenue', totalRevenue)
    print('total profit', totalRevenue-totalCost)
    print('total conversion', totalConversion)
    print('total churn', totalChurn)
def writePromotion(solver, data, X, Y):
    promotion={}
    iter=0
    for i in range(len(data['customers'])):
        for c in range(len(data['campaigns'])):
           for v in range(len(data['channels'])):
             for t in range(len(data['times'])):
                for o in range(len(data['offers'])):
                    if(X[i,c,v,t].solution_value()>0 and Y[i,c,o,t].solution_value()>0):
                        iter+=1
                        promotion.update({iter:{'customerID': data['customers'][i+1]['id'], 
                                                'campaignID':data['campaigns'][c+1]['id'], 
                                                'offerID':data['offers'][o+1]['id'],
                                                'channelName':data['channels'][v+1]['name'],
                                                'date':data['times'][t+1]['day']
                                                }})
    print(promotion)
def printModel(solver):
    print(solver.ExportModelAsLpFormat(False).replace('\\', '').replace(',_', ','), sep='\n')
def buildModel(data,selection):
  # Instantiate the solver
  solver = pywraplp.Solver('OptSolver',pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
  # Declare decision variables
  infinity=solver.infinity()
  # X[(i, c, v, t)]: 
  X={}
  for i in range(len(data['customers'])):
    for c in range(len(data['campaigns'])):
       for v in range(len(data['channels'])):
         for t in range(len(data['times'])):
             X[(i,c,v,t)] = solver.IntVar(0,infinity,"x({},{},{},{})".format(i, c, v, t) )
  # Y[(i, c, o, t)]: 
  Y={}
  for i in range(len(data['customers'])):
    for c in range(len(data['campaigns'])):
       for o in range(len(data['offers'])):
         for t in range(len(data['times'])):
             Y[(i,c,o,t)] = solver.IntVar(0,infinity,"y({},{},{},{})".format(i, c, o, t) )

  # Objectives:
  if(selection['objective']=='Max TargetCount'):
      print('Solving to Maximize Target Count')
      targetCount=solver.IntVar(0,infinity,'TargetCount')
      solver.Add(solver.Sum(X[i,c,v,t] for i in range(len(data['customers']))
                                            for c in range(len(data['campaigns']))
                                            for v in range(len(data['channels']))
                                            for t in range(len(data['times'])))==targetCount,'OBJECTIVE:MAX TARGET COUNT')
      solver.Maximize(targetCount)
  if(selection['objective']=='Max TotalScore'):
      print('Solving to Maximize Total Score')
      totalScore=solver.IntVar(0,infinity,'TotalScore')
      solver.Add(solver.Sum(X[i,c,v,t]*data['campaigns'][i+1]['priority'] for i in range(len(data['customers']))
                                            for c in range(len(data['campaigns']))
                                            for v in range(len(data['channels']))
                                            for t in range(len(data['times'])))==totalScore,'OBJECTIVE:MAX TOTAL SCORE') 
      solver.Maximize(totalScore)
  if(selection['objective']=='Max TotalRevenue'):
      print('Solving to Maximize Total Revenue')
      totalRevenue=solver.IntVar(0,infinity,'TotalRevenue')
      solver.Add(solver.Sum(Y[i,c,o,t]*data['offers'][o+1]['revenue']*data['probability'][i][o] 
                                            for o in range(len(data['offers']))
                                            for c in range(len(data['campaigns']))
                                            for i in range(len(data['customers']))
                                            for t in range(len(data['times'])))==totalRevenue,'OBJECTIVE:MAX TOTAL REVENUE')
      solver.Maximize(totalRevenue)
  if(selection['objective']=='Max TotalConversion'):
      print('Solving to Maximize Total Conversion')
      totalConversion=solver.IntVar(0,infinity,'TotalConversion')
      solver.Add(solver.Sum(Y[i,c,o,t]*data['probability'][i][o] 
                                            for o in range(len(data['offers']))
                                            for c in range(len(data['campaigns']))
                                            for i in range(len(data['customers']))
                                            for t in range(len(data['times'])))==totalConversion,'OBJECTIVE:MAX TOTAL CONVERSION')
      solver.Maximize(totalConversion)
  if(selection['objective']=='Min TotalChurn'):
      print('Solving to Minimize Total Churm')
      totalChurn=solver.NumVar(0,infinity,'TotalChurn')
      solver.Add(solver.Sum(Y[i,c,o,t]*data['customers'][i+1]['churn']*data['probability'][i][o] 
                                            for o in range(len(data['offers']))
                                            for c in range(len(data['campaigns']))
                                            for i in range(len(data['customers']))
                                            for t in range(len(data['times'])))==totalChurn,'TOTAL CHURN')
      totalChurnRev=solver.IntVar(0,infinity,'TotalChurnRev')
      solver.Add(solver.Sum(Y[i,c,o,t]*data['customers'][i+1]['churn']*data['probability'][i][o]*data['offers'][o+1]['revenue'] 
                                            for o in range(len(data['offers']))
                                            for c in range(len(data['campaigns']))
                                            for i in range(len(data['customers']))
                                            for t in range(len(data['times'])))==totalChurnRev,'OBJECTIVE: MAX TOTAL CHURN REV')     

      solver.Maximize(totalChurn)
  if(selection['objective']=='Min TotalCost'):
      print('Solving to Minimize Total Cost')
      totalCost=solver.NumVar(0,infinity,'TotalCost')
      solver.Add(solver.Sum(X[i,c,v,t]*data['channels'][v+1]['cost'] 
                                            for v in range(len(data['channels']))
                                            for c in range(len(data['campaigns']))
                                            for i in range(len(data['customers']))
                                            for t in range(len(data['times'])))==totalCost,'OBJECTIVE:MAX TOTAL COST')
      if('threshold' in data):
          solver.Add(solver.Sum(X[i,c,v,t]  for v in range(len(data['channels']))
                                            for c in range(len(data['campaigns']))
                                            for i in range(len(data['customers']))
                                            for t in range(len(data['times'])))>=data['threshold'],'THRESHOLD')
      for c in range(len(data['campaigns'])):
          if('threshold' in data['campaigns'][c+1]):
              solver.Add(solver.Sum(X[i,c,v,t]  for v in range(len(data['channels']))
                                                for i in range(len(data['customers']))
                                                for t in range(len(data['times'])))>=data['campaigns'][c+1]['threshold'],'THRESHOLDc{}'.format(c))
      for t in range(len(data['times'])):
          if('threshold' in data['times'][t+1]):
              solver.Add(solver.Sum(X[i,c,v,t]  for v in range(len(data['channels']))
                                                for i in range(len(data['customers']))
                                                for c in range(len(data['campaigns'])))>=data['times'][t+1]['threshold'],'THRESHOLDt{}'.format(t))     
      solver.Minimize(totalCost)
  if(selection['objective']=='Max TotalProfit'):
      print('Solving to Maximize Total Profit')
      totalProfit=solver.IntVar(0,infinity,'TotalProfit')
      solver.Add((solver.Sum(Y[i,c,o,t]*data['offers'][o+1]['revenue']*data['probability'][i][o] 
                                            for o in range(len(data['offers']))
                                            for c in range(len(data['campaigns']))
                                            for i in range(len(data['customers']))
                                            for t in range(len(data['times']))) - 
                  solver.Sum(X[i,c,v,t]*data['channels'][v+1]['cost']
                                            for v in range(len(data['channels']))
                                            for c in range(len(data['campaigns']))
                                            for i in range(len(data['customers']))
                                            for t in range(len(data['times'])))) ==totalProfit,'OBJECTIVE:MAX TOTAL PROFIT')
      solver.Maximize(totalProfit)
  if(selection['offerTreatment']=='single'):
      for i in range(len(data['customers'])):
        for c in range(len(data['campaigns'])):
             for t in range(len(data['times'])):
                 solver.Add(solver.Sum(Y[i,c,o,t] for o in range(len(data['offers']))
                                                 if (data['Oco'][c][o]==1))<=1,'SingleOffer {}{}{}'.format(i, c, t))
  
  #Add Constraints
  #Channel Capacity
  if(data['constConfig'][6]['status']==1):
      for v in range(len(data['channels'])):
          if('capacity' in data['channels'][v+1]):
              solver.Add(solver.Sum(X[i,c,v,t]      for i in range(len(data['customers']))
                                                    for c in range(len(data['campaigns']))
                                                    for t in range(len(data['times']))
                                                    )<=data['channels'][v+1]['capacity'],'ChannelCap {}'.format(v))
      if('capacity' in data):
            for v in range(len(data['channels'])):
                  for t in range(len(data['times'])):
                        solver.Add(solver.Sum(X[i,c,v,t]      for i in range(len(data['customers']))
                                                              for c in range(len(data['campaigns']))
                                                              )<=data['capacity'][v][t],'ChannelCapT {}{}'.format(v,t))
  #Offer Capacity
  if(data['constConfig'][7]['status']==1):
      for o in range(len(data['offers'])):
          if('capacity' in data['offers'][o+1]):
              solver.Add(solver.Sum(Y[i,c,o,t]      for i in range(len(data['customers']))
                                                    for c in range(len(data['campaigns']))
                                                    for t in range(len(data['times']))
                                                    )<=data['offers'][o+1]['capacity'],'OfferCap {}'.format(o))
  #Budget Constaints
  if(data['constConfig'][8]['status']==1):
      for c in range(len(data['campaigns'])):
          if('budget' in data['campaigns'][c+1]):
              solver.Add(solver.Sum(X[i,c,v,t]      for i in range(len(data['customers']))
                                                    for v in range(len(data['channels']))
                                                    for t in range(len(data['times']))
                                                    )<=data['campaigns'][c+1]['budget'],'BudgetC {}'.format(c))
      if('budget' in data):
          solver.Add(solver.Sum(X[i,c,v,t]      for i in range(len(data['customers']))
                                                for c in range(len(data['campaigns']))
                                                for v in range(len(data['channels']))
                                                for t in range(len(data['times']))
                                                              )<=data['budget'],'Budget')
  #Channel Eligibility Constraints
  if(data['constConfig'][9]['status']==1):
      if('ChannelAv' in data):
          for i in range(len(data['customers'])):
            for c in range(len(data['campaigns'])):
               for v in range(len(data['channels'])):
                 for t in range(len(data['times'])):
                     solver.Add(X[i,c,v,t]<=data['ChannelAv'][v][i],'Channel Eligibility {}{}{}{}'.format(i, c, v, t))
  #Overlap Constraints
  if(data['constConfig'][1]['status']==1):
      for i in range(len(data['customers'])):
        for kk in range(len(data['dTypes'])):
             for t in range(len(data['times'])):
                solver.Add(solver.Sum(X[i,c,v,t] for c in range(len(data['campaigns']))
                                                     for v in range(len(data['channels']))
                                                     if (data['campaigns'][c+1]['dType']==data['dTypes'][kk+1]['name']))<=1,'Overlap {}{}{}'.format(i, kk, t))
  #PRESENT Constraints
  if(data['constConfig'][2]['status']==1):
      for i in range(len(data['customers'])):
        for c in range(len(data['campaigns'])):
                solver.Add(solver.Sum(X[i,c,v,t] for v in range(len(data['channels']))
                                                     for t in range(len(data['times'])))+ data['PRESENT'][i][c]<=1,'PRESENT {}{}'.format(i,c))
  #Contact Eligibility
  if(data['constConfig'][4]['status']==1):
      for i in range(len(data['customers'])):
        for kk in range(len(data['dTypes'])):
             for v in range(len(data['channels'])):
                solver.Add(solver.Sum(X[i,c,v,0] for c in range(len(data['campaigns']))
                                                if (data['campaigns'][c+1]['dType']==data['dTypes'][kk+1]['name']))+data['CONTACT'][kk][v]-data['DSLC'][i][v][kk]<=1,'CONTACT1 {}{}{}'.format(i,kk,v))
      #Contact Eligibility for t>0   
      for i in range(len(data['customers'])):
        for kk in range(len(data['dTypes'])):
             for v in range(len(data['channels'])):
                 for t in range(len(data['times'])):
                    if(t>0):
                        solver.Add(solver.Sum(X[i,c,v,t2] for c in range(len(data['campaigns']))
                                                          for t2 in range(len(data['times']))
                                                          if (data['campaigns'][c+1]['dType']==data['dTypes'][kk+1]['name']) and t2>=t and t2<t+data['CONTACT'][kk][v])<=1,'CONTACTt {}{}{}{}'.format(i,kk,v,t))
  #Consent Eligibility 
  if(data['constConfig'][5]['status']==1):
      for i in range(len(data['customers'])):
        for c in range(len(data['campaigns'])):
           for v in range(len(data['channels'])):
             for t in range(len(data['times'])):
                 solver.Add(X[i,c,v,t]<=data['CONSENT'][i][c][v],'Consent Eligibility {}{}{}{}'.format(i, c, v, t))          
  #Offer Eligibility
  if(data['constConfig'][10]['status']==1): 
      for i in range(len(data['customers'])):
        for c in range(len(data['campaigns'])):
           for o in range(len(data['offers'])):
             for t in range(len(data['times'])):
                 if(data['campaigns'][c+1]['dType']=='OFFER' and data['Oco'][c][o]==1):
                    solver.Add(Y[i,c,o,t]<=data['E'][i][o],'Offer Eligibility {}{}{}{}'.format(i, c, o, t))    
  #Connectivity 
  for i in range(len(data['customers'])):
    for c in range(len(data['campaigns'])):
         for t in range(len(data['times'])):
             if(data['campaigns'][c+1]['dType']=='OFFER'):
                 solver.Add(solver.Sum(Y[i,c,o,t] for o in range(len(data['offers']))
                                                  if (data['Oco'][c][o]==1))
                            -solver.Sum(X[i,c,v,t] for v in range(len(data['channels'])))
                            >=0,'Connectivity1 {}{}{}'.format(i,c,t))
  for i in range(len(data['customers'])):
    for c in range(len(data['campaigns'])):
         for t in range(len(data['times'])):
             for o in range(len(data['offers'])):
                 if(data['Oco'][c][o]==1):
                     solver.Add((Y[i,c,o,t]-solver.Sum(X[i,c,v,t] for v in range(len(data['channels']))))<=0,'Connectivity2 {}{}{}{}'.format(i,c,t,o))
  #Offer Sent 
  if(data['constConfig'][3]['status']==1):
      for i in range(len(data['customers'])):
        for o in range(len(data['offers'])):
            solver.Add(solver.Sum(Y[i,c,o,t] for c in range(len(data['campaigns']))
                                                for t in range(len(data['times'])))+data['PRESENT_io'][i][o]<=1,'Offer Sent {}{}'.format(i, o))
  #Campaign Status
  for i in range(len(data['customers'])):
    for c in range(len(data['campaigns'])):
       for v in range(len(data['channels'])):
         for t in range(len(data['times'])):
             solver.Add(X[i,c,v,t]<=data['active'][c][v],'Campaign Status {}{}{}{}'.format(i, c, v, t))  

  printModel(solver)
  status = solver.Solve()
  if status == solver.OPTIMAL:
      print(selection)
      printSolution2(solver,data,X,Y)
      writePromotion(solver,data,X,Y)
  else:  # No optimal solution was found.
      if status == solver.FEASIBLE:
          print('A potentially suboptimal solution was found.')
      else:
          if status==solver.UNBOUNDED:
                print('UNBOUNDED')
          else:
                print('The solver could not solve the problem.')
  return solver

def initializeSettings(data):
    optimizationMode=checkData(data)
    return optimizationMode

def checkData(data):
    optimizationMode={'objectives':{1:'Max TargetCount'},
                      'offerTreatment':{1:'single',2:'multi'}}

    optimizationMode['objectives'].update({2:'Max TotalScore'})
    if('revenue' in data['offers'][1] and 'probability' in data):
            print('probability and offer revenue exist')
            optimizationMode['objectives'].update({3: 'Max TotalRevenue'})
    if('probability' in data):
        optimizationMode['objectives'].update({4:'Max TotalConversion'})
        if('churn' in data['customers'][1]):
            print('churn scores and probabilities exist')
            optimizationMode['objectives'].update({5:'Min TotalChurn'})
    if(('threshold' in data or 'threshold' in data['campaigns'][1]) and 'cost'  in  data['channels'][1] ):
            print('thresholds exist')
            optimizationMode['objectives'].update({6:'Min TotalCost'})
    if('revenue' in data['offers'][1] and 'probability' in data and 'cost'  in  data['channels'][1] ):
            optimizationMode['objectives'].update({7:'Max TotalProfit'})
    print(optimizationMode['objectives'])


    return optimizationMode

def makeSelection(optimizationMode):
    rnd= randrange(1,len(optimizationMode['objectives'])+1)
    print(rnd)
    rnd2= randrange(1,len(optimizationMode['offerTreatment'])+1)
    #to be deleted later
    rnd=7
    rnd2=1
    selection={"objective":optimizationMode['objectives'][rnd],
               "offerTreatment":optimizationMode['offerTreatment'][rnd2]}
    print(selection)
    return selection

def main():
  data=create_data_model()
  optimizationMode=initializeSettings(data)
  selection=makeSelection(optimizationMode)
  solver=buildModel(data,selection)
  

if __name__ == '__main__':
    main()