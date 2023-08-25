
import sys
#sys.path.append('/home/lurching/.local/lib/python3.10/site-packages/')


from flask import Flask, render_template, request

import pandas as pd
import matplotlib.pyplot as plt

import json

import numpy as np

from rdkit import Chem
from mordred import Calculator, descriptors

import mordred
import pubchempy as pcp

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

from datetime import datetime

now = datetime.now()

dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

plt.rcParams["figure.figsize"] = (12,12)

app = Flask(__name__)
app.config["DEBUG"] = True

df = pd.read_csv("/home/lurching/mysite/demo-odor_data.csv")

x = df.iloc[:, 6:53]
x=StandardScaler().fit_transform(x)

#Applying PCA
pca = PCA(n_components=2)
PC = pca.fit_transform(x)
scores_pca = pca.transform(x)


#Descriptor variance
PCloadings = pca.components_.T * np.sqrt(pca.explained_variance_)
components=df.columns.tolist()
components=components[6:53]
loadingdf=pd.DataFrame(PCloadings,columns=('PC1','PC2'))
loadingdf["variable"]=components


#cluster
kmeans_pca = KMeans(n_clusters=6, init='k-means++', random_state=42)
kmeans_pca.fit(scores_pca)

df_new = pd.concat([df.reset_index(drop= True), pd.DataFrame(scores_pca)], axis=1)
df_new.columns.values[-5:] = ['Component0','Component1','Component2','Component3','Component4']

df_new['Segment K-means PCA'] = kmeans_pca.labels_

df_new['Segment'] = df_new['Segment K-means PCA'].map({0:'first',
                                                      1:'second',
                                                      2:'third',
                                                      3:'fourth',
                                                      4:'fifth',
                                                      5:'sixth',
                                                      6:'seventh',
                                                      7:'eighth'})

colors = { 0:'lightgreen', 1:'red',  2:'cyan',3:'fuchsia', 4:'black', 5:'gold'}



@app.route("/")
def index():

    df_new = pd.concat([df.reset_index(drop= True), pd.DataFrame(scores_pca)], axis=1)
    df_new.columns.values[-5:] = ['Component0','Component1','Component2','Component3','Component4']

    df_new['Segment K-means PCA'] = kmeans_pca.labels_

    df_new['Segment'] = df_new['Segment K-means PCA'].map({0:'first',
                                                          1:'second',
                                                          2:'third',
                                                          3:'fourth',
                                                          4:'fifth',
                                                          5:'sixth',
                                                          6:'seventh',
                                                          7:'eighth'})

    return render_template("index.html")

@app.route('/pca-distribution')
def pca():


    odor_berry = []
    odor_alliaceaous = []
    odor_coffee = []
    odor_citrus = []
    odor_fishy = []
    odor_jasmine = []
    odor_minty = []
    odor_earthy = []
    odor_smoky = []

    for i in range(10):
        odor_berry.append({'x' : round(PC[:,0][i], 2), 'y' : round(PC[:,1][i],2), 'name' : df["Name"][i]})
    for i in range(10, 21):
        odor_alliaceaous.append({'x' : round(PC[:,0][i], 2), 'y' : round(PC[:,1][i],2), 'name' : df["Name"][i]})
    for i in range(21, 32):
        odor_coffee.append({'x' : round(PC[:,0][i], 2), 'y' : round(PC[:,1][i],2), 'name' : df["Name"][i]})
    for i in range(32, 43):
        odor_citrus.append({'x' : round(PC[:,0][i], 2), 'y' : round(PC[:,1][i],2), 'name' : df["Name"][i]})
    for i in range(43, 54):
        odor_fishy.append({'x' : round(PC[:,0][i], 2), 'y' : round(PC[:,1][i],2), 'name' : df["Name"][i]})
    for i in range(54, 64):
        odor_jasmine.append({'x' : round(PC[:,0][i], 2), 'y' : round(PC[:,1][i],2), 'name' : df["Name"][i]})
    for i in range(64, 74):
        odor_minty.append({'x' : round(PC[:,0][i], 2), 'y' : round(PC[:,1][i],2), 'name' : df["Name"][i]})
    for i in range(74, 85):
        odor_earthy.append({'x' : round(PC[:,0][i], 2), 'y' : round(PC[:,1][i],2), 'name' : df["Name"][i]})
    for i in range(85, 95):
        odor_smoky.append({'x' : round(PC[:,0][i], 2), 'y' : round(PC[:,1][i],2), 'name' : df["Name"][i]})



    return render_template("pca-distribution.html", odor_berry=json.dumps(odor_berry),
                                                    odor_alliaceaous = json.dumps(odor_alliaceaous),
                                                    odor_coffee = json.dumps(odor_coffee),
                                                    odor_citrus = json.dumps(odor_citrus),
                                                    odor_fishy = json.dumps(odor_fishy),
                                                    odor_jasmine = json.dumps(odor_jasmine),
                                                    odor_minty = json.dumps(odor_minty),
                                                    odor_earthy = json.dumps(odor_earthy),
                                                    odor_smoky = json.dumps(odor_smoky))


@app.route('/descriptor-variance')
def descriptor():

    descriptor_variance = []

    for i in range(47):
        descriptor_variance.append({'x' : round(loadingdf["PC1"][i], 2), 'y' : round(loadingdf['PC2'][i],2), 'name' : loadingdf["variable"][i]})


    return render_template("descriptor-variance.html", descriptor_variance=json.dumps(descriptor_variance))

@app.route('/cluster-by-pca')
def cluster():

    segment_1 = []
    segment_2 = []
    segment_3 = []
    segment_4 = []
    segment_5 = []
    segment_6 = []


    for i in range(95):

        if df_new["Segment K-means PCA"][i] == 0:

            segment_1.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : df_new["Odor Class"][i]})

        if df_new["Segment K-means PCA"][i] == 1:

            segment_2.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : df_new["Odor Class"][i]})

        if df_new["Segment K-means PCA"][i] == 2:

            segment_3.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : df_new["Odor Class"][i]})

        if df_new["Segment K-means PCA"][i] == 3:

            segment_4.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : df_new["Odor Class"][i]})

        if df_new["Segment K-means PCA"][i] == 4:

            segment_5.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : df_new["Odor Class"][i]})

        if df_new["Segment K-means PCA"][i] == 5:

            segment_6.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : df_new["Odor Class"][i]})




    return render_template("cluster-by-pca.html", segment_1=json.dumps(segment_1),
                                                    segment_2 = json.dumps(segment_2),
                                                    segment_3 = json.dumps(segment_3),
                                                    segment_4 = json.dumps(segment_4),
                                                    segment_5 = json.dumps(segment_5),
                                                    segment_6 = json.dumps(segment_6))


@app.route('/submit', methods=['POST'])
def submit():

    segment_1 = []
    segment_2 = []
    segment_3 = []
    segment_4 = []
    segment_5 = []
    segment_6 = []
    segment_7 = [] # for inputs


    for i in range(len(df_new)):

        if df_new["Segment K-means PCA"][i] == 0:

            segment_1.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : df_new["Odor Class"][i]})

        if df_new["Segment K-means PCA"][i] == 1:

            segment_2.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : df_new["Odor Class"][i]})

        if df_new["Segment K-means PCA"][i] == 2:

            segment_3.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : df_new["Odor Class"][i]})

        if df_new["Segment K-means PCA"][i] == 3:

            segment_4.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : df_new["Odor Class"][i]})

        if df_new["Segment K-means PCA"][i] == 4:

            segment_5.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : df_new["Odor Class"][i]})

        if df_new["Segment K-means PCA"][i] == 5:

            segment_6.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : df_new["Odor Class"][i]})

        else :
            segment_7.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : "Undefine"})


    def is_smiles(s):
        try:
            mol = Chem.MolFromSmiles(s)
            if mol is None:
                return False
            else:
                return True
        except:
            return False

    text = request.form['text']

    if not is_smiles(text):
        return render_template('cluster-by-pca.html', message='Please enter a valid value', segment_1 = json.dumps(segment_1),
                                                                                            segment_2 = json.dumps(segment_2),
                                                                                            segment_3 = json.dumps(segment_3),
                                                                                            segment_4 = json.dumps(segment_4),
                                                                                            segment_5 = json.dumps(segment_5),
                                                                                            segment_6 = json.dumps(segment_6))

    mol = Chem.MolFromSmiles(text)
    new = len(df_new)

    df_new.loc[new, ("Component0")] = mordred.Weight.Weight(True, False)(mol)
    df_new.loc[new, ("Component1")] = mordred.WienerIndex.WienerIndex(False)(mol)
    df_new.loc[new, ("Name")] = pcp.get_compounds(text, 'smiles')[0].iupac_name
    df_new.loc[new, ("Segment K-means PCA")] = 6

    df_new.drop_duplicates(inplace=True)

    segment_1 = []
    segment_2 = []
    segment_3 = []
    segment_4 = []
    segment_5 = []
    segment_6 = []
    segment_7 = [] # for inputs


    for i in range(len(df_new)):

        if df_new["Segment K-means PCA"][i] == 0:

            segment_1.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : df_new["Odor Class"][i]})

        if df_new["Segment K-means PCA"][i] == 1:

            segment_2.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : df_new["Odor Class"][i]})

        if df_new["Segment K-means PCA"][i] == 2:

            segment_3.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : df_new["Odor Class"][i]})

        if df_new["Segment K-means PCA"][i] == 3:

            segment_4.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : df_new["Odor Class"][i]})

        if df_new["Segment K-means PCA"][i] == 4:

            segment_5.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : df_new["Odor Class"][i]})

        if df_new["Segment K-means PCA"][i] == 5:

            segment_6.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : df_new["Odor Class"][i]})

        if df_new["Segment K-means PCA"][i] == 6:
            segment_7.append({'x' : int(df_new['Component0'][i]), 'y' : int(df_new['Component1'][i]), 'name' : df_new["Name"][i], 'odor' : "Undefine"})



    return render_template('cluster-by-pca-2.html', message='You can add an other SMILE', segment_1 = json.dumps(segment_1),
                                                                                        segment_2 = json.dumps(segment_2),
                                                                                        segment_3 = json.dumps(segment_3),
                                                                                        segment_4 = json.dumps(segment_4),
                                                                                        segment_5 = json.dumps(segment_5),
                                                                                        segment_6 = json.dumps(segment_6),
                                                                                        segment_7 = json.dumps(segment_7))


