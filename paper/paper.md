# Microservices and Kafka :hand: fa18-523-53

| Chaitanya Kakarala
| ckakara@iu.edu
| Indiana University
| hid: fa18-523-53
| github: [:cloud:](https://github.com/cloudmesh-community/fa18-523-53/tree/master/paper)

---

Keywords: fa18-523-53, Microservices, Kafka, Python

---

## Introduction

With the increase in demand for Agile methodology (Citation Needed) in software development where the user stories should be completed in a given sprint (Citation Needed - Sprint Definition), there is great need of shrinking down the applications to smaller units. These smaller units are otherwise known as Microservices. These Microservices are loosely coupled and the instructions inside them are light weight. Microservices are autonomous by nature and they can be plugged in any host and bring them up provided the software and hardware requirements are met. As a result, small independent teams can work on these Microservices in parallel and deploy them independently. Depending on the complexity of an application there could be  hundreds of Microservices defined and each of them might interact with each other. In other words, an event occured on one  Microservice could start another Microservice. With the interactions between these Microservices increasing, it's hard trace the connection between them and hence creating a technical debt to mitigate the issue.
Apche Kafka is designed to solve the above stated problem. It is also known as "Distrubuted Streaming Platform" which works on a subscribe-publish model. Microservices communicate with each other through a Kafka cluster by either subscribing or publishing the topics rather than communicating directly. Kafka was originally designed in LinkedIn (Citation Needed) to address issue with one of thier internal system. The Primary objectives of Kafka were to persist the message data so multiple consumers can access the same and provide horizontal scaling. 


## Architecture

The metric for data in Kafka is message. These messages are nothing but an array of bytes and Kafka is least worried about the content of these messages. Optionally a message can have a key which is again an array of text whose hash value determines the partition the message will be written to. Doing so will guarantee that the messages with same hash value will be stored into the same partition.  Messages can also be sent in batches which in other words, a bunch of messages sent all at once. That leaves us with questions like, what are these messages? Where are they stored? who uses these messages? 
Messages in Kafka are classified into Topics. Topics are nothing but a group of partitions (Can also be described as disk space) where a collection of similar messages are stored. Messages will be appended to these partitions and will be read from beginning to end fashion. The Partitions can be hosted by different servers which makes the topic scale horizontally.
Below figure describes 4 partitions of a single topic (Citation Needed)

![](/images/kafkaPartitions.png)

## Use Cases

TBD

## Conclusion

TBD

## Acknowledgements

The author would like to thank Professor Gregor Von Laszewski for providing this opportunity to work on this paper summary.
The author would also like to thank the Associate Instructors of the class for their continuos help in resolving issues.
