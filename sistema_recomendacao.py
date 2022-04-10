import pandas as pd 
def rank (df,mi,mg):
    v = df['target_counts']
    R = df['target']
    return(v/(v+mi) * R) +(mi/(mi+v) *mg)
def Recomendar(arquivo='https://github.com/danielicapui/machine_learning/blob/main/winemag-data-130k-v2.csv.zip?raw=true',compression='zip',feature='title',target='points',target_count=4):
    target_count=int(target_count)
    df=pd.read_csv(arquivo,compression=compression,header=0,sep=',',quotechar='"')
    df.dropna()
    df['feature']=df[feature]
    df['target']=df[target]
    novo_df=df.groupby('feature'). filter(lambda x: x['target'].count()>= target_count)
    target_df = pd.DataFrame(novo_df.groupby(by='feature')['target'].mean())
    target_df['target_counts'] =novo_df.groupby(by='feature')['target'].count()
    target_df.sort_values(by = 'target_counts', ascending = False)
    mg=target_df['target'].mean()
    mi=target_df['target_counts'].min()
    target_df['ranking']=target_df.apply(rank,args=(mi,mg),axis=1)
    target_df.sort_values(by='ranking',ascending=False)
    tam=target_df.ranking.shape[0]
    return target_df.ranking.head(tam)
