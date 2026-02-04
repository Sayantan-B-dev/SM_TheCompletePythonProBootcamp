import pandas as pd

data = pd.read_csv("2018_Squirrel_Data.csv")



gray_squirrels = data[data["Primary Fur Color"] == "Gray"]
black_squirrels = data[data["Primary Fur Color"] == "Black"]
red_squirrels = data[data["Primary Fur Color"] == "Cinnamon"]

data_dictionary={
    "Fur color":["Gray","Black","Cinnamon"],
    "Count":[len(gray_squirrels),len(black_squirrels),len(red_squirrels)]
}

data_df = pd.DataFrame(data_dictionary)
data_df.to_csv("squirrel_count.csv", index=False)
