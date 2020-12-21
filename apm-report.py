import os
import csv
from python_graphql_client import GraphqlClient

FORMATTED_CSV_ORDER = [
    'Tribe',
    'Squad',
    'squad',
    'name',
    'reporting',
    'language',
    'Environment',
    'Application',
    'Cost-Center',
    'feature',
    'Location',
    'accountid',
    'Service',
    'trustedAccountId',
    'feature',
    'account',
    'squad',
    'Alerting',
    'Contact',
    'guid',
    'accountId',
    'permalink',
    'apmSummary_apdexScore',
    'apmSummary_errorRate',
    'apmSummary_hostCount',
    'apmSummary_instanceCount',
    'apmSummary_nonWebThroughput',
    'apmSummary_Throughput',
    'apmSummary_webThroughput',
]

def get_apm_metadata():
    headers = {}
    headers['Api-Key'] = os.getenv('USER_API_KEY')
    headers['Content-Type'] = 'application/json'
    client = GraphqlClient(endpoint="https://api.newrelic.com/graphql")
    client.headers=headers
    query = """
 {
  actor {
    entitySearch(queryBuilder: {domain: APM, type: APPLICATION, name: ""}) {
      results {
        entities {
          tags {
            key
            values
          }
          guid
          name
          reporting
          permalink
          accountId
          account {
            id
            name
          }
          ... on ApmApplicationEntityOutline {
            guid
            name
            apmSummary {
              apdexScore
              errorRate
              hostCount
              instanceCount
              nonWebResponseTimeAverage
              nonWebThroughput
              responseTimeAverage
              throughput
              webResponseTimeAverage
              webThroughput
            }
          }
        }
      }
    }
  }
}

        """
    _result = client.execute(query=query)
    return [data for data in _result['data']['actor']['entitySearch']['results']['entities']]

data = get_apm_metadata()


key_set = set()
apm_objects = []
for item in data:
    scrubbed = {}
    scrubbed['Tribe'] = 'UNKNOWN'
    scrubbed['reporting'] = False
    scrubbed['accountid'] = item['account']['id']
    scrubbed['account'] = item['account']['name']
    scrubbed['name'] = item['name']
    if (item['apmSummary']):
        scrubbed['apmSummary_apdexScore'] = item['apmSummary']['apdexScore']
        scrubbed['apmSummary_errorRate'] = item['apmSummary']['errorRate']
        scrubbed['apmSummary_hostCount'] = item['apmSummary']['hostCount']
        scrubbed['apmSummary_instanceCount'] = item['apmSummary']['instanceCount']
        scrubbed['apmSummary_nonWebThroughput'] = item['apmSummary']['nonWebThroughput']
        scrubbed['apmSummary_Throughput'] = item['apmSummary']['throughput']
        scrubbed['apmSummary_webThroughput'] = item['apmSummary']['webThroughput']
    scrubbed['reporting'] = item['reporting']
    scrubbed['permalink'] = item['permalink']

    for tag in item['tags']:
        scrubbed[tag['key']] = tag['values'][0]
    for k in scrubbed.keys():
        key_set.add(k)
    apm_objects.append(scrubbed)
    apm_objects.sort(key = lambda i: (i['Tribe'], i['reporting']))   

with open('apm-report.csv', 'w') as f:
    w = csv.DictWriter(f, FORMATTED_CSV_ORDER, extrasaction='ignore')
    w.writeheader()
    w.writerows(apm_objects)