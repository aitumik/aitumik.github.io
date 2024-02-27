---
title: "Elastic Search Basics"
date: 2023-03-10T17:00:22+03:00
draft: true
---

# ES from first principles
Elasticsearch is a search engine based on Lucene that provides distributed full text search over http and provides a schemaless JSON documents
ES is used by github to search for code in repositories,used by Wikipedia on search as you type for full text search,used by data dog to enable their 
huge logs searching and queries

## ES concepts - logical layout

* **index** this is the equivalent of the table in SQL
* **document** this is the equivalent of row in elastic 
* **shard** you must answer the question what is a shard and why is it used
* **field** something with fields on the document

## ES basics(CRUD)

### Indexing new data 
You can index data to ES by sending an http request with JSON format to an URI. This can be done by using curl
#### body.json
```bash
{
	"price": 1000,
	"color": "red",
	"make": "honda",
	"sold": "2023-01-12"
}
```

```bash
curl PUT http://localhost:9200/<index-name>/_doc/<id> -d 
	@body.json -H 'Content-type:application/json'
```

Understand how to create,read,updated and delete documents here, it should be a quick review

## Search

* structure of search request and response
* filters and how they differ from queries


Search finds documents with a 'needle' in their haystack

## Aggregations

Aggregation summarizes data as metrics,statistics or other analytics this means in other words aggregation 
helps you answer questions about the needles such as what is the average length of the needles

### High Level concpets

* The DSL query for aggregations has composable syntax: independent units of functionality
* You can combine these units to form any aggregation you might need so you just need to master the basics here

To master aggregation you only need to understand these two concepts

* **Buckets** - a collection of documents based on certain criterion e.g fielvalue,range or any other criterion
* **Metrics** - statistics run on documents in a bucket for example average,sum e.t.c

In simple terms an aggregation is a combination of one or more bucket together with zero or more metrics 

Let translate a simple SQL query to a structure of an aggregation

```sql
SELECT count(colors)
FROM table
GROUP BY color
```

In the above query `count(colors)` is the metric while `GROUP BY color` is the bucket


#### Buckets

A bucket is simply a collection of documents that meet a certain criterion so for example :

* An employee would land in either `male` or `female` category
* An organization like jumia would land in the `africa` region bucket 

As an aggregation is run the documents are searched and checked if they would fall under a bucket, if they 
do then they are added to the bucket. Buckets can also be nested for example :

* A town Eldoret would fall under the `uasin-gishu` county bucket and then `uasin-gishu` county  will fall under `kenya` country bucket

#### Metrics

Metrics are just simple mathematical operations performed on the buckets that have already been partitioned for example
sum,avewrage,min,max and percentiles

#### Combining the Two 

Like we mentioned aggregation is a combination metrics and buckets and the buckets can be nested which is a powerful thing as you can see from example below

* Partition documents by country(bucket)
* Partition each country bucket by gender(bucket)
* Partition each gender bucket by age ranges(bucket)
* Run a metric to calculate the average salary for each range(metric)

This will give you the average salary by age,country,gender in one request

## Aggregation Test Drive

