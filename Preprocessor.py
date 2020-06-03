import json

from TweetParser import TweetParser
from dbModels.GraphDbModel import GraphDbModel
from dbModels.GraphDbService import GraphDbService
from dbModels.MongoDbModel import MongoDbModel
from dbModels.MongoDbService import MongoDbService


def main():
    # filename = "single_tweet.json"
    filename = "nys_tweets_filtered_2017_0.json"
    # filename = "test"
    filepath = "./data/"
    file = f"{filepath}{filename}"

    parser = TweetParser(file)
    parser.extract_large_tweets(1)

    graphDbService = GraphDbService("bolt://localhost:7687", "neo4j", "test", 1)
    graphModel = GraphDbModel(graphDbService.driver, 1)
    graphModel.insert(parser.tweets)
    graphDbService.close()

    mongoDbService = MongoDbService('mongodb://localhost:27017/')
    mongoDbModel = MongoDbModel(mongoDbService.client, 'Twitter', 1)
    mongo_data = parser.data_package
    for each_data in mongo_data:
        json_data = json.loads(each_data)
        for tableName in json_data.keys():
            value = json_data[tableName]
            if len(value) != 0:
                mongoDbModel.insert(value['id'], value['data'], tableName)
    mongoDbService.close()


if __name__ == '__main__':
    main()
