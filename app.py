from flask import Flask
from MLProcess.clustering import clustering

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/clustering')
def get_table_data():
   clstr=clustering()
   tab=clstr.fetch_data()
   tab_scaled=clstr.scaled_df(tab.iloc[:,5:14])
   distortions=clstr.distortions(15,tab_scaled)
   silScores=clstr.silhouette_score(15,tab_scaled)
   kmeans=clstr.km_means_fit(8,tab_scaled,tab)
   return kmeans.to_json()



if __name__ == '__main__':
    app.run()
