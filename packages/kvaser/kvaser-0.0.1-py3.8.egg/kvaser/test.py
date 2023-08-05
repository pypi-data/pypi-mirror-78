import kvaser
from io import BytesIO
import pandas as pd

df = kvaser.getdata()
a = kvaser.BlobStorage('test')
a.delete('a.pq')
a.write_pq(df, 'a.pq')
a.read_pq('a.pq')

for x in self.container.list_blobs():
    print(x.name + ()



blob_client = a.blobservice.get_blob_client(container=a.container_name, blob='a.pq')
buf = BytesIO()
df.to_parquet(buf, index=False)
val = blob_client.upload_blob(buf, blob_type='BlockBlob', overwrite=True)
buf.close()


blob_client = a.blobservice.get_blob_client(container=a.container_name, blob='a.pq')
dl = blob_client.download_blob()
df = pd.read_parquet(BytesIO(dl.content_as_bytes()))

a.read_pq('a.pq')



import kvaser

blob = kvaser.BlobStorage('my-kvaser-test')
df = kvaser.getdata() # A test pandas dataframe
blob.write_pq(df, 'a.pq')
blob.read_pq('a.pq')
blob.write_csv(df, 'a.csv')
blob.list()
blob.read_csv('a.csv')
blob.delete_container()
del(blob)
