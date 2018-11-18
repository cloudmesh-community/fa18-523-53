# Orchestarting Microservices for a Credit Scoring Application in Kafka :o: fa18-523-53

| Chaitanya Kakarala
| ckakara@iu.edu
| Indiana University, Example University
| hid: fa18-523-53
| github: [:cloud:](https://github.com/cloudmesh-community/fa18-523-53/project-report/report.md)
| code: [:cloud:](https://github.com/cloudmesh-community/fa18-523-53/project-code)


---

Keywords: Kafka, Zookeeper, Microservices, Python.

---

## Abstract

This Project deals with orchestration of micro services in a Credit Scoring application using a Kafka cluster. A user keys in his personal identification information in a user interface created in Python and upon submitting the same multiple micro services written in python will be executed. These light weighted and autonomous interact with one another using a Kafka broker Which works in a subscribe-publish model. The user will then see his credit report and the factors that impact his credit.

## Introduction

With the increase in the amount of data being processed there is a great need of developing the applications with better performance. One such technique to make the application perform better is breaking the application to smaller units. These units are light weighted and autonomous in nature. These small applications provides scalability and because of their autonomous nature they can be plugged into any system. These small applications are also known as Microservices. Since we are breaking the big or complex application to multiple small or light weighted microservices, a mechanism to efficiently communicate between these microservices is required. Apache Kafka is one such mechanism which provides a message streaming platform so that the microservices can either subscribe or publish the data. 

## Apache Kafka

Apache Kafka is an open source streaming platform that streams the data in the form of messages. The messages are nothing but a collection of bytes and kafka has nothing to do with the content of these messages. Each of these messages will be tagged with a topic name and these messages will be published into a partition (disk space) of the topic it is associated with. These partitions can be made available across different machines which makes kafka a horizontally scalable streaming platform.
Optionally each of these messages can be given with a key and whose hash values determines the partition it should be saved in. Hence the messages with the same key value will be stacked together in the same partition.

There are two users of the kafka system. They are producers and consumers. Producers sends the messages and they are also known as publishers. producers while sending the messages does not care about the partition the message is going to save. However, publishing the message with a key value ensures all the messages with same key stored in the same partition. On the other hand consumers consumes those messages by the producers.The consumers saves the offset of each message it reads and process the same. Saving the offset helps restarting from the point of failure in case of an issue rather starting all over again. These consumers can be grouped together called as consumer group and each consumer in the consumer group could be hosted in a different machine which makes the consumer aspect scale horizontally. Consumer groups also restricts the partition to be read by multiple consumers if required. The data retention in each partition can be controlled in different ways. For example the message in a partition can be removed after 1 month or the partition can always be maintained at the capacity threshold set to 1 GB. 

A single kafka server is called as kafka broker. Each broker receives messages from producers and save them into thier respective partitions. The broker also responds to the consumer requests and saves the offset of the consumed messages. Kafka is designed to have multiple brokers and collection of all such brokers is called as kafka cluster. A leader broker can be defined in each cluster and the data replicates from leader broker to the other brokers to provide high data availability and persistent data. Kafa also supports the communication between the clusters in different data centers.

## Requirements

All images must be referred to in the text. The words bellow and above
must not be used in your paper for images, tables, and code.

+@fig:fromonetotheorther shows a nice figure exported from Powerpoint
to png. If you like you can use this as a basis for your drawings.

![A simple flow chart](images/from-one-to-the-other.png){#fig:fromonetotheorther}

Figures must not be cited with an explicit number, but automated
numbering must be used. Here is how we did it for this paper:

```
+@fig:fromonetotheorther shows a nice
figure exported from Powerpoint to png.
If you like you can use this as a basis
for your drawings.

![A simple flow chart](images/from-one-to-the-other.png){#fig:fromonetotheorther}
```

## Design 

## Architecture

## Dataset

## Implementation

## Benchmark

## Conclusion

## Acknowledgement

## Workbreakdown

Only needed if you work in a group.
