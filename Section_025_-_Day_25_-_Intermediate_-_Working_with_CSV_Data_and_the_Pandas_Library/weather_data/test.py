import csv
import pandas as pd

def printline():
    print("-"*50)

def printline2():
    print("="*50)

data =pd.read_csv("weather_data.csv")
data_dict = data.to_dict()
printline2()

#entire data frame as dictionary
print("data_dict : \n",data_dict)
printline2()


# series methods
temp_average = data["temp"].mean()
temp_max = data["temp"].max()
print(f"temp_average : \n {temp_average:.2f}")
print("temp_max : \n",temp_max)
printline2()

# series
print("data[\"condition\"] : \n",data["condition"]) # treating like an dictionary
printline()
print("data.condition : \n",data.condition) # treating like an object
printline2()

# Get data in row
print("getting monday row : \n",data[data.day=="Monday"])
printline2()

# getting mainimum temparature row
print("minimum temparature row : \n",data[data.temp==data.temp.min()])
printline2()


# getting one single info from row
monday=data[data.day=="Monday"]
print("monday condition is : \n",monday.condition.item())
print("monday temprature is : \n",monday.temp.item())
print("monday temprature in fahrenheit is : \n",(monday.temp.item()*9/5)+32)
printline2()


# creating a dataframe from scratch
dummy_data={
    "students":["John","Mark","Pam"],
    "scores":[76,56,65]
}
dummy_df=pd.DataFrame(dummy_data)
dummy_df.to_csv("dummy_data.csv",index=False)
print(dummy_df)
print("dummy_data.csv created")
printline2()