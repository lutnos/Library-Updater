#!/usr/bin/env python3

import json
import os

from graphqlclient import GraphQLClient

client = GraphQLClient('https://api.github.com/graphql')
client.inject_token(os.environ.get('GITOAUTH'))  # OauthToken 'bearer {token}'


def graph_ql_search(lib_name):
    return client.execute('''
                query {
                  repository(owner:"hmrc", name:"''' + lib_name + '''") {
                    releases(first: 100, orderBy: {direction: DESC, field: CREATED_AT}) {
                            nodes {
                        name
                      }
                    }
                  }
                }
                ''')


def fetch_release(sbt_version, library_name, current_version, domain):
    if domain == "uk.gov.hmrc":
        version_number = current_version.replace("-play-25", "").replace("-play-26", "")

        for release in json.loads(graph_ql_search(library_name))["data"]["repository"]["releases"]["nodes"]:
            release_name = str(release["name"])
            test = version_number
            release_number = str(
                release_name.replace("-play-25", "").replace("-play-26", "").replace(",", "").split(" ")[0])
            if test.split(".")[0] == release_number.split(".")[0]:
                if "-play-25" in release_name:
                    if sbt_version == "2.5.19":
                        return str(release_number + "-play-25")
                    else:
                        return str(release_number + "-play-26")
                else:
                    return str(release_number)
