from pymongo import MongoClient
import pandas as pd
from IPython.display import display

import plotly.express as px
import matplotlib.pyplot as plt






class DatabaseController:
    def __init__(self):
        client = MongoClient('mongodb://localhost:27017/')
        self.db = client.MMM_Task
        self.meta_data = list(self.db['MMM_Task.meta'].find())[0]


    def get_name4id(self, id):
        # "5L06EAtZOEauIJhwGKVqyw", "AuP-SAqPu02Vrgu6df6Txg" , "BENamAV8rkibLIBc8asHhQ"
        world_object_ids = self.meta_data
        id_df = pd.DataFrame(world_object_ids["individuals"])
        id_df = id_df.set_index("id")
        return id_df.loc[id]

    def plot_object(self, id, plot=True):
        play_data = list(self.db.MMM_1_T.find())
        #filter the object of interest
        play_data = pd.DataFrame(play_data)
        object_data = []
        for index, frame in play_data.iterrows():
            for object in frame["individuals"]:
                if object["id"] == id:
                    object_data.append(object)
        object_data = ( pd.DataFrame(object_data))
        object_data["timestamp"] = play_data["timestamp"]
        del play_data["individuals"]
        del play_data["skel_individuals"]

        object_data[["x","y","z"]] = (pd.DataFrame(object_data["loc"].tolist()))
        name = self.get_name4id(id).values[0]
        object_data["label"] = [name for x in range(len(object_data))]
        if plot:
            fig = px.line_3d(object_data, x="x", y="y", z="z", color="label")
            fig.show()
        else :
            return object_data

    def plot_hands_side_by_side(self):
        right_hand = self.plot_object("BENamAV8rkibLIBc8asHhQ", plot=False)
        left_hand = self.plot_object("AuP-SAqPu02Vrgu6df6Txg", plot=False)
        hands = right_hand.append(left_hand)
        first_ =["left hand" for x in range(len(left_hand))]
        second_ =["right hand" for x in range(len(right_hand))]
        first_.extend(second_)
        hand_lables = first_
        hands["label"] = hand_lables
        fig = px.line_3d(hands, x="x", y="y", z="z", color="label")
        fig.show()

    def plot_bones(self, left_hand=True, right_hand= True):
        if(left_hand):
            self.plot_bones_of_hand("AuP-SAqPu02Vrgu6df6Txg")


        if (right_hand):
            self.plot_bones_of_hand("BENamAV8rkibLIBc8asHhQ")





    def plot_bones_of_hand(self, id):
        play_data = list(self.db.MMM_1_T.find())
        # filter the object of interest
        play_data = pd.DataFrame(play_data)
        object_data = []
        X = []
        Y = []
        Z = []
        colors = []
        for index, frame in play_data.iterrows():
            for object in frame["skel_individuals"]:
                if object["id"] == id:
                    for bone in object["bones"]:
                        loc = bone["loc"]
                        X.append(loc["x"])
                        Y.append(loc["y"])
                        Z.append(loc["z"])
                        colors.append(bone["idx"])

                    object_data.append(object)
        object_data = (pd.DataFrame(object_data))
        object_data["timestamp"] = play_data["timestamp"]
        del play_data["individuals"]
        del play_data["skel_individuals"]

        df = pd.DataFrame({
            "x":X,
            "y":Y,
            "z":Z
        })
        fig = px.line_3d(df, x="x", y="y", z="z", color=colors)
        fig.show()
