from typing import Dict, List,Union
import numpy as np
# to scale the data using z-score
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import warnings

from DAO.stock_impl import db_dao


warnings.filterwarnings("ignore")

class clustering:

    def __init__(self):
       pass

    def fetch_data(self):
        fetch=db_dao()
        tab=fetch.execute_table_select()
        return tab

    def scaled_df(self,df_scaled):
        df_scaled=StandardScaler().fit_transform(df_scaled)
        return df_scaled

    def distortions(self,clusters,scaled_df):
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

    def silhouette_score(self,clusters,df_scaled):
        km_means=df_scaled.copy()
        sil_score = []
        cluster_list = range(2, clusters)
        for n_clusters in cluster_list:
            clusterer = KMeans(n_clusters=n_clusters, random_state=1)
            preds = clusterer.fit_predict((df_scaled))
            score = silhouette_score(km_means, preds)
            sil_score.append("For n_clusters = {}, the silhouette score is {})".format(n_clusters, score))
        return sil_score

    def km_means_fit(self,clusters,df_scaled,df):

        kmeans = KMeans(n_clusters=clusters, random_state=1)
        kmeans.fit(df_scaled)
        df["KM_segments"] = kmeans.labels_
        return df



