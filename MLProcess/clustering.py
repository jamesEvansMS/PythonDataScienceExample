from typing import Dict, List,Union
import numpy as np
import pandas as pd

# to scale the data using z-score
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from sklearn.preprocessing import StandardScaler

# to compute distances
#from scipy.spatial.distance import cdist, pdist

# to perform k-means clustering and compute silhouette scores
# from sklearn.cluster import KMeans
# from sklearn.metrics import silhouette_score


# to perform hierarchical clustering, compute cophenetic correlation, and create dendrograms
# from sklearn.cluster import AgglomerativeClustering
# from scipy.cluster.hierarchy import dendrogram, linkage, cophenet

# to suppress warnings
import warnings

from DAO.stock_impl import execute_table_select
from config.postgresConfig import connect

warnings.filterwarnings("ignore")

class clustering:

    def __init__(self):
        pass


    def fetch_data():
        conn = connect()
        tab=execute_table_select(conn)
        return tab  #pd.DataFrame(execute_table_select(conn))

    def scaled_df(df_scaled):
        df_scaled=StandardScaler().fit_transform(df_scaled)
        return df_scaled

    def distortions(clusters,scaled_df):
        km_df = scaled_df.copy()
        meanDistortions = []

        for k in range(1,clusters):
            km_model = KMeans(n_clusters=k, random_state=1)
            km_model.fit(scaled_df)
            prediction = km_model.predict(km_df)
            distortion = (
                    sum(np.min(cdist(km_df, km_model.cluster_centers_, "euclidean"), axis=1))
                    / km_df.shape[0]
            )

            meanDistortions.append(distortion)
        return meanDistortions

    def silhouette_score(clusters,df_scaled):
        km_means=df_scaled.copy()
        sil_score = []
        cluster_list = range(2, clusters)
        for n_clusters in cluster_list:
            clusterer = KMeans(n_clusters=n_clusters, random_state=1)
            preds = clusterer.fit_predict((df_scaled))
            score = silhouette_score(km_means, preds)
            sil_score.append("For n_clusters = {}, the silhouette score is {})".format(n_clusters, score))
        return sil_score

    def km_means_fit(clusters,df_scaled):
        df=df_scaled.copy()
        kmeans = KMeans(n_clusters=clusters, random_state=1)
        kmeans.fit(df_scaled)
        df["KM_segments"] = kmeans.labels_
        return df

        return kmeans


#I'll probably make these a series of API calls

df=clustering.fetch_data()
subset = df.iloc[:,5:14].copy()
df_scaled=pd.DataFrame(clustering.scaled_df(subset),columns=subset.columns)
mean_d=clustering.distortions(15,df_scaled)
sil_score=clustering.silhouette_score(15,df_scaled)
fullDF=df.iloc[:,5:14].copy()
fullDFscaled=pd.DataFrame(clustering.scaled_df(fullDF),columns=fullDF.columns)
df=clustering.km_means_fit(8,fullDFscaled)
print(df)
