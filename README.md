
# CloudFront
- to improve performance for global audience -> use CloudFront instead of S3 Bucket
- `signed-URL`: give access to one file
- `signed cookies`: give access to multiple file
- Cloudfront `field level encryption`: to `encrypt sensitive data` in an HTTPS form
- content is cached at the edges (`216 edge locations` around the world)
- `DDos protection` -> use WAF or Shield
- to force update content in cache -> use `Cache Invalidation`
- to get logs -> use Kinesis Data Streams for real-time or Kinesis Data Firehose for near real-time


# API Gateway
- APIS -> resources (/, /home) -deploy to-> stages (dev, prod, ...) 
- ${stageVariables.lambdaAlias} 
- 3 ways to deploy:
  + `edge optimized`: for global clients, requests are routed through CloudFront Edge Locations
  + `regional`: clients in same region
  + `private`: accessed from your VPC
- if changes code -> need to deploy to take effect on stages
- `each stage has own configuration` (limit request, caching, ...),  possible override settings on method
- canary deployment
- Integration types:
  + `MOCK`: return response without sending request to backend
  + `HTTP/AWS (Lambda & AWS service)`: can use mapping template for request and response (muse config both integration request and response phase) 
  + `AWS_PROXY` (Lambda proxy): request from client is input for lambda
  + `HTTP_PROXY`: request are passed to backend
- `Caching: default is 300s` (0 -> 3600s), is expensive
- `Usage plan`: control who an access, how much and how fast they can access
- Cloudwatch logs and Cloud watch metric (by Stage): 
  + CacheHitCount, CacheMissCount
  + Count
  + Integration latency: time between -> backend + <- backend
  + Latency: time between from client + to client
