##########################################################
# Furniture carbon module.                        #
# Xinyuan Wei                                            #
# 2021/05/11                                             #
##########################################################
import scipy.integrate as integrate
import math

#%%
##########################################################
# Furniture carbon module.                        #
##########################################################

def Furniture_C (ty,fur_C,dp1,dp2,dp3):
    
    # ty:      total years
    # fur_C:   annual home application carbon
    # dp1:     furniture disposal rate parameter 1 
    # dp2:     furniture disposal rate parameter 2 
    # dp3:     furniture disposal rate parameter 3 (service life)

    fur_yrA=[] # Current year, the accumulated home application carbon.
    fur_yrD=[] # Annual home application carbon disposed.
    
    # Furniture disposal rate.
    # TSD: time since production
    def fur_dr(TSP):
        part1=dp1/math.sqrt(2*math.pi)
        part2=math.exp((-dp2*math.pow((TSP-dp3),2))/dp3)
        return(part1*part2)
             
    # Accumulated furniture carbon.
    for i in range (ty): 
        # Current year, the accumulated furniture carbon (Carbon Pool).
        acc_A=0
            
        if i<=dp3:
            for j in range (i+1):
                temp_A=0
                yr_C=fur_C.at[j]
                lfr=integrate.quad(fur_dr,0,i+1-j)[0]
                temp_A=temp_A+yr_C*(1-lfr)
                acc_A=acc_A+temp_A
                
        if i>dp3:
           for j in range (int(dp3)):
               temp_A=0
               yr_C=fur_C.at[int(i-dp3+j)]
               lfr=integrate.quad(fur_dr,0,dp3-j)[0]
               temp_A=temp_A+yr_C*(1-lfr)
               acc_A=acc_A+temp_A      
        
        fur_yrA.append(acc_A)       
    
    # Furniture carbon disposed.
    for i in range (ty):
        acc_D=0
    
        if i<=dp3:
            for j in range (i+1):
                temp_D=0
                yr_C=fur_C.at[j]
                dfr=fur_dr(i-j+1)
                temp_D=yr_C*dfr
                acc_D=acc_D+temp_D

        if i>dp3:
           for j in range (int(dp3)):
               temp_D=0
               yr_C=fur_C.at[int(i-dp3+j)]
               dfr=fur_dr(dp3-j+1)
               temp_D=yr_C*dfr
               acc_D=acc_D+temp_D

        fur_yrD.append(acc_D)
             
    # Return:
    # accumulated furniture carbon
    # disposed furniturecarbon
    return(fur_yrA,fur_yrD)