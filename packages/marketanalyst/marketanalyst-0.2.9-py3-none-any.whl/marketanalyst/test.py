import client

client = client.client()

# df = client.getdata(exchange=1,security_type=4,indicator_category=1,date_start="2020-01-01,07:00:00",date_end="2020-01-05,12:00:00",master_id="45406,45549",indicator_id="377,379")
df = client.getOHLCVData(exchange=1,security_type=4,date_start="2020-01-01,07:00:00",date_end="2020-01-05,12:00:00")

print(df)