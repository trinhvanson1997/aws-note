
# CloudFront
- to improve performance for global audience -> use CloudFront instead of S3 Bucket
- **signed-URL**: give access to one file
- **signed cookies**: give access to multiple file
- Cloudfront **field level encryption**: to **encrypt sensitive data** in an HTTPS form
- content is cached at the edges (**216 edge locations** around the world)
- **DDos protection** -> use WAF or Shield
- to force update content in cache -> use **Cache Invalidation**
- to get logs -> use Kinesis Data Streams for real-time or Kinesis Data Firehose for near real-time


# API Gateway
- **max API gateway concurrency: 10.000**
- APIS -> resources (/, /home) -deploy to-> stages (dev, prod, ...) 
- ${stageVariables.lambdaAlias} 
- 3 ways to deploy:
  + **edge optimized**: for global clients, requests are routed through CloudFront Edge Locations
  + **regional**: clients in same region
  + **private**: accessed from your VPC
- if changes code -> need to deploy to take effect on stages
- **each stage has own configuration** (limit request, caching, ...),  possible override settings on method
- canary deployment
- Integration types:
  + **MOCK**: return response without sending request to backend
  + **HTTP/AWS (Lambda & AWS service)**: can use mapping template for request and response (muse config both integration request and response phase) 
  + **AWS_PROXY** (Lambda proxy): request from client is input for lambda
  + **HTTP_PROXY**: request are passed to backend
- **Caching: default is 300s** (0 -> 3600s), is expensive
- **Usage plan**: control who an access, how much and how fast they can access
- Cloudwatch logs and Cloud watch metric (by Stage): 
  + CacheHitCount, CacheMissCount
  + Count
  + Integration latency: time between -> backend + <- backend
  + Latency: time between from client + to client


# Kinesis vs SQS
- AWS recommends using Amazon SQS for cases where individual message fail/success are important, message delays are needed and there is only one consumer for the messages received (if more than one consumers need to consume the message, then AWS suggests configuring more queues)

# SQS
- size message: **minimum 1KB, maximum 256KB**
- message can contain text data
- **unlimited throughput, unlimited number of message** in queue
- default retention: 4 days, max 14 days
- use param **DelaySeconds** to wait for processing data after being push
- **MessageVisibilityTimeout**: after message is polled by consumer, it is invisible to other consumer
- if consumer process too long, it can call **ChangeMessageVisibilityTimout** to get more time
- **Dead Letter Queue (DLQ)**:
  + use for **DEBUG**
  + after **MaximumReceives** threshold, message goes to DLQ
  + DLQ of **FIFO     queue** must be a **FIFO     queue**
  + DLQ of **standard queue** must be a **standard queue**
- to **send file with large size** -> use **SQS extended client** (Java library)


# SNS
- up to **100.000 topics**
- event producer only send message to one topic
- Fan-out pattern
- **Mesage Filtering**: use Filter Policy to send specific message to consumer


# CDK
- **define clound infra using programming languagues**: JavaScript, Python, Java, .NET
- code is **compiled to CloudFormation template**
- great for Lambda functions
- great for docker containers in ECS/EKS
- Flow: 
Create the app from a template provided by AWS CDK -> Add code to the app to create resources within stacks -> Build the app (optional) -> Synthesize one or more stacks in the app -> Deploy stack(s) to your AWS account
- commands to remember:  
  + **cdk synth**: print out CloudFormation template
  + **cdk bootstrap**: deploy CDKToolkit (create stack on CloudFormation named CDKToolkit, provision resources before you can deploy include S3 Bucket to store files and IAM Role grant permission to deploy)
  + **cdk deploy**:

- **to test cdk -> use CDK Assertions Module**
- to import a template:
  + **Template.fromStack(myStack)**: stack built in CDK
  + **Template.fromString(mystring)**: stack built outside CDK


# CloudFormation
- Infrastructure as Code (IaC)
- **written in JSON or YAML**
- **Template have to be uploaded to S3** before CloudFormation create Stack
- Can't update old template, must upload new version of template
- Building blocks:
  + **Resources (mandatory)**: AWS resources declared
  + Parameters: dynamic input
  + Mappings: static variables
  + Outputs: reference to what has been created
  + Conditional: 
  + Metadata:
- Pseudo parameters:
  + AWS::AccountID
  + AWS::NotificationARNs
  + AWS::NoValue
  + AWS::Region
  + AWS::StackId
  + AWS::StackName

- Example Mappings
```
Mappings:
  EnvironmentToInstanceType:
    development:
      instanceType: t2.micro
    production:
      instanceType: m4.large

Resources:
  EC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !FindInMap [AWSRegionArch2AMI, !Ref 'AWS::Region', HVM64]
```

- **Outputs**:
  + must be unique within region
  + output value can be imported into other stack
  + can't delete CloudFormation if it's outputs are being used by another CloudFormation

- **Intrisic Functions**:
  + Ref
  + Fn::GetAtt
  + Fn::FindInMap
  + Fn::ImportValue
  + Fn::Join
  + Fn::Sub
  + Condition Functions: Fn::If, Fn::Not, Fn::Equals, ...

- If CF update fails, auto **rollback to previous known working state**
- **ChangeSet**: used to know what changed before apply
- **StackSets**: 
  + create, update or delete stacks **across multiple accounts and regions** with single operations
  + **need administrator account** to create StackSet
  + can use trusted accounts to create, update, delete stack instances from StackSet
- **CloudFormation Drift**: detect changes (drifted) from expected template configuration




ECS?