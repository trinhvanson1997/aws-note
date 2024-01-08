
# S3 Security
4 methods to encrypt objects in s3 bucket
- **SSE-S3**:
  + use **keys handled, owned by AWS**
  + encryption type: **AES-256**
  + **x-amx-server-side-encryption: "AES-256"** header
  + **enabled by default** for new buckets and objects
- **SSE-KMS**:
  + **keys handled, managed by KMS**
  + **x-amz-server-side-encryption: "aws:kms"** header
  + **limitation**: can be impacted by **KMS Limit** -> can request quota increase
- **SSE-C**:
  + **keys managed by customer** outside of AWS
  + **ONLY HTTPS**
  + keys **must provided in header for every request**

- **Client-side encryption**

# CloudFront
- to improve performance for global audience -> use CloudFront instead of S3 Bucket
- **signed-URL**: give access to one file
- **signed cookies**: give access to multiple file
- Cloudfront **field level encryption**: to **encrypt sensitive data** in an HTTPS form
- content is cached at the edges (**216 edge locations** around the world)
- **DDos protection** -> use WAF or Shield
- to force update content in cache -> use **Cache Invalidation**
- to get logs -> use Kinesis Data Streams for real-time or Kinesis Data Firehose for near real-time
- AWS Lambda@Edge is a general-purpose serverless compute feature that supports a wide range of computing needs and customizations. Lambda@Edge is best suited for computationally intensive operations


# API Gateway
- **max API gateway concurrency: 10.000 rps** > **Account level throttling: 5000 rps**
- When your API's resources receive requests from a domain other than the API's own domain and you want to restrict servicing these requests, you must disable cross-origin resource sharing (CORS) for selected methods on the resource
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

# Beanstalk
- Many web apps have the same architecture (3-tier) ALB+ASG+RDS
- components:
  + **Application**: collection of components (environments, versions,...)
  + **Application version**: an iteration of application code, **up to 1000 versions**
  + **Environment**: collection of resources running an application version (only one application version at a time)
- deployment modes:
  + **All at one**
  + **Rolling**
  + **Rolling with additional batch**
  + **Immutable**: deploy in new temp ASG, merge temp ASG to current ASG
  + **Traffic splitting (canary test)**
  + **Blue/green**
- Beanstalk extensions:
  + add **.ebextensions/ directory** in root of source code
  + YAML/JSON format
  + .config extension (eg. logging.config)
  + able to modify some default settings or add resources (RDS, ElastiCache,...)
- **Beanstalk migration**:
  + After create environment, you cannot change ELB type
  + **to migrate**: create new env with same config except LB
  + **to decouple RDS**: create snapshot for RDS DB -> turn on protect RDS from deletion, 

# Kinesis vs SQS
- AWS recommends using Amazon SQS for cases where individual message fail/success are important, message delays are needed and there is only one consumer for the messages received (if more than one consumers need to consume the message, then AWS suggests configuring more queues)

# SQS
- size message: **minimum 1KB, maximum 256KB**
- message can contain text data
- **unlimited throughput, unlimited number of message** in queue
- default retention: 4 days, max 14 days
- use param **DelaySeconds** to wait for processing data after being push
- **MessageVisibilityTimeout**: **default: 30 seconds** after message is polled by consumer, it is invisible to other consumer, range from 0 -> 12h
- if consumer process too long, it can call **ChangeMessageVisibilityTimout** to get more time
- **Dead Letter Queue (DLQ)**:
  + use for **DEBUG**
  + after **MaximumReceives** threshold, message goes to DLQ
  + DLQ of **FIFO     queue** must be a **FIFO     queue**
  + DLQ of **standard queue** must be a **standard queue**
- to **send file with large size** -> use **SQS extended client** (Java library)
- **DeleteQueue**: delete queue and all messages
- **PurgeQueue**: just remove all messages

# SNS
- up to **100.000 topics**
- up to **12.500.000 subscriptions per topic**
- event producer only send message to one topic
- subscriber can be: **SQS, Lambda, Kinesis Data Firehose**
- Fan-out pattern
- **Mesage Filtering**: use Filter Policy to send specific message to consumer
- Encryption:
  + in-flight encryption with HTTPS API
  + At-rest encryption with KMS keys
  + client-side encryption
- Access Controls: IAM policy to regulate access to SNS API
- SNS Access Policies: similar to s3 bucket policy
  + useful for cross-account access to SNS topic
  + allow other services (s3, ...) write to topic


# CDK
- define cloud infra **using programming languagues**: JavaScript, Python, Java, .NET
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

# SAM (Serverless Application Model)
- framework for deploying serverless service
- **written in YAML**
- support anything from CloudFormation
- header indicate SAM: **Transform: 'AWS::Serverless-2016-10-31'**
- Write code:
  + AWS::Serverless:Function
  + AWS::Serverless:Api
  + AWS::Serverless:SimpleTable
- Package & Deploy:
  + **aws cloudformation package / sam package**
  + **aws cloudformation deploy  / sam deploy**
- sam build (convert to cloud) -> sam package or aws cloudformation package (package and upload to s3) -> sam deploy or aws cloudformation deploy (create ChangeSet)


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

# ELB
- **Cross-Zone Load Balancing**: ALB (enabled by default), NLB, GWLB, CLB (disabled by default)


# Step Function
- **model your workflows** as state machine (one per workflow)
- written in **JSON**
- **Resource field is a required parameter for Task state**
- 
```
{
  "Comment": "A Hello World example of the Amazon States Language using Pass states",
  "StartAt": "Lambda Invoke",
  "States": {
    "Lambda Invoke": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "OutputPath": "$.Payload",
      "Parameters": {
        "Payload.$": "$",
        "FunctionName": "<ENTER FUNCTION NAME HERE>"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2
        }
      ],
      "Next": "Choice State"
    },
    "Choice State": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$",
          "StringMatches": "*Stephane*",
          "Next": "Is Teacher"
        }
      ],
      "Default": "Not Teacher"
    },
    "Is Teacher": {
      "Type": "Pass",
      "Result": "Woohoo!",
      "End": true
    },
    "Not Teacher": {
      "Type": "Fail",
      "Error": "ErrorCode",
      "Cause": "Stephane the teacher wasn't found in the output of the Lambda Function"
    }
  }
}
```
**PRACTICE WITH STEP FUNCTION**
**PRACTICE WITH ECS**
**PRACTICE WITH BEANSTALK**
**REVIEW SECTION 10**
**REVIEW SECTION 14**
**EFS**
**S3 UPLOAD**
**Amazon ElasticCache**

**1. How lambda connect to aws service?**
```
You can configure a Lambda function to connect to private subnets in a virtual private cloud (VPC) in your account. Use Amazon Virtual Private Cloud (Amazon VPC) to create a private network for resources such as databases, cache instances, or internal services. Connect your lambda function to the VPC to access private resources during execution. When you connect a function to a VPC, Lambda creates an elastic network interface for each combination of the security group and subnet in your function's VPC configuration. This is the right way of giving RDS access to Lambda.
```

**2. Migrate code from Github to CodeCommit**
```
The simplest way to set up connections to AWS CodeCommit repositories is to configure Git credentials for CodeCommit in the IAM console, and then use those credentials for HTTPS connections.
```

**3. Drift Detection feature in Cloudformation**
```

```

**4. Query the metadata at http://169.254.169.254/latest/meta-data**

**5. RDS Auto Scaling storage**
```
ASG storage is enabled by default in Aurora
For other RDS, must enabled by hand
```
