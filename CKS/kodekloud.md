# Cluster setup and hardening

### CIS Benchmark (CIS = Center for Internet Security)
1. Export CIS Benchmark report at `/var/www/html` named `index.html, interactive mode, no timestamp
```
sh ./Assessor-CLI.sh -i -rd /var/www/html/ -nts -rp index
```

2. Install kube-bench from source with config file in same dir

### Authentication
```
# authen by user
curl -v -k https://master-node-ip:6443/api/v1/pods -u "user1:password123"

# authen by token
curl -v -k https://master-node-ip:6443/api/v1/pods --header "Authorization: Bearer <token>"
```

### Service Account
1. create token for service account to access kubernetes dashboard
k create token <service_account>

2. create api token for service account
create sa
create secret point to sa
edit sa to use secret

access api pods through token
curl https://localhost:6443/api/v1/namespaces/<namespace>/pods --header "Authorization: Bearer <token>" --insecure

### Certificates API: khó quá bỏ qua

### RBAC
run as user: k get pods --as user-dev

### Network Policy
```yaml
# sample 1:  
# allow traffic from the Internal application only to the payroll-service and db-service
# allow egress traffic to DNS ports TCP and UDP (port 53) to enable DNS resolution from the internal pod.
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
        matchLabels:
          role: payroll
    ports:
    - protocol: TCP
      port: 8080
  - to:
    - podSelector:
        matchLabels:
          role: payroll
    ports:
    - protocol: TCP
      port: 3306
  - ports:
    - port: 53
      protocol: UDP
    - port: 53
      protocol: TCP


# sample 2
# allow all connection from (pod with label name=api-pod AND belong to namespace prod) OR (server ip: 102.168.5.10)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          name: api-pod         # match all pod label name=api-pod, in all namespace
      namespaceSelector:
        matchLabels:
          name: prod            # match all pod in namespace label prod
    - ipBlock:
        cidr: 192.168.5.10/32   # allow traffic from server ip
    ports:
    - protocol: TCP
      port: 3306


# compare to sample 2
# allow all connection from pod with label name=api-pod OR pod in namespace prod OR server ip: 102.168.5.10
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          name: api-pod 
    - namespaceSelector:    # different here, there is "-"
        matchLabels:
          name: prod    
    - ipBlock:
        cidr: 192.168.5.10/32
    ports:
    - protocol: TCP
      port: 3306

```

### Docker daemon
unix socket: /var/run/docker.sock


### Audit
4 audit levels:
- `None`: don't log events that match this rule.
- `Metadata`: log events with metadata (requesting user, timestamp, resource, verb, etc.) but not request or response body.
- `Request`: log events with request metadata and body but not response body. This does not apply for non-resource requests.
- `RequestResponse`: log events with request metadata, request body and response body. This does not apply for non-resource requests

### Limit Node Access
```yaml
# delele user
deluser USER

# delete group
delgroup GROUP

# delete user from group
deluser USER GROUP

# Suspend user so that this user cannot login to the system but make sure not to delete it
# Make user as system account
usermod -s /usr/sbin/nologin USER

# ssh config
vi /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no

# add existing user to group
usermod -aG GROUP USER

# copy ssh key to node01 user jim
ssh-copy-id -i ~/.ssh/id_rsa.pub jim@node01
ssh jim@node01 

# run user jim as sudo without password
vi /etc/sudoers
jim  ALL=(ALL) NOPASSWD:ALL
```

# https://learn.kodekloud.com/user/courses/certified-kubernetes-security-specialist-cks/module/d67be5ee-871d-4435-a187-382610cb6a1f/lesson/4be6aacf-94b3-44da-8b02-e57bbf1e7f41
### Remove unwanted packages, services
```yaml
# List installed packages
apt list --installed

# We want to blacklist the evbug kernel module on controlplane host
vim /etc/modprobe.d/blacklist.conf
```