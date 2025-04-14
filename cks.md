# Falco
- config rule file at: `/etc/falco/falco_rules.yaml`
- apply changes: `service falco restart`
- check status : `service falco status`
- check log: tail -f /var/log/syslog | grep falco

# seccomp?

# AppArmor
- Check status:  `apparmor_status`
- Apply profile: `apparmor_parser /root/profile`
- Config deployment use apparmor profile:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - image: nginx
        imagePullPolicy: IfNotPresent
        name: nginx
      securityContext:
        appArmorProfile:
          localhostProfile: docker-default
          type: Localhost
      terminationGracePeriodSeconds: 30
```

# Verify platform binaries
```
# print hashcode of binary
sha512sum ./kubelet
eg: 66e1194d1ef2886bd30a0617a938732af1b5e9f70fcf5607e178c9b4431935bfada519f70cc17857ed93792dff479eac2574f0d950778f82f4443706234da235

# compare hashcode and installed kubelet
echo "66e1194d1ef2886bd30a0617a938732af1b5e9f70fcf5607e178c9b4431935bfada519f70cc17857ed93792dff479eac2574f0d950778f82f4443706234da235 /usr/bin/kubelet" | sha512sum --check
```

# CIS Benchmark
- print all benchmark: `kube-bench`
- only master node: `kube-bench run --targets master`
- view only one result: `kube-bench run --targets master --check 1.2.15`

# Audit Logging
- reference: https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/
- killercoda: https://killercoda.com/killer-shell-cks/scenario/auditing-enable-audit-logs
- youtube: https://www.youtube.com/watch?v=O80HmhOGBsY&list=PLpbwBK0ptssx38770vYNwZEuCeGNw54CH&index=9
- mount volumes for file, folder and add parameters
```
# sample policy.yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:

# log Secret resources audits, level Metadata
- level: Metadata
  resources:
  - group: ""
    resources: ["secrets"]

# log node related audits, level RequestResponse
- level: RequestResponse
  userGroups: ["system:nodes"]

# for everything else don't log anything
- level: None

---
# add new Volumes
volumes:
  - name: audit-policy
    hostPath:
      path: /etc/kubernetes/audit-policy/policy.yaml
      type: File
  - name: audit-logs
    hostPath:
      path: /etc/kubernetes/audit-logs
      type: DirectoryOrCreate

---
# add new VolumeMounts
volumeMounts:
  - mountPath: /etc/kubernetes/audit-policy/policy.yaml
    name: audit-policy
    readOnly: true
  - mountPath: /etc/kubernetes/audit-logs
    name: audit-logs
    readOnly: false

---
# enable Audit Logs
spec:
  containers:
  - command:
    - kube-apiserver
    - --audit-policy-file=/etc/kubernetes/audit-policy/policy.yaml
    - --audit-log-path=/etc/kubernetes/audit-logs/audit.log
    - --audit-log-maxsize=7
    - --audit-log-maxbackup=2
```


# CertificateSigningRequests sign manually: HARD to remember
- killercoda: https://killercoda.com/killer-shell-cks/scenario/certificate-signing-requests-sign-manually
- reference link to generate certificate manually: https://kubernetes.io/docs/tasks/administer-cluster/certificates/

# CertificateSigningRequests sign via API: HARD
- https://killercoda.com/killer-shell-cks/scenario/certificate-signing-requests-sign-k8s


# SecurityContext: HARD
https://killercoda.com/killer-shell-cks/scenario/static-manual-analysis-k8s
https://killercoda.com/killer-shell-cks/scenario/immutability-readonly-fs
What is different?
```
#1
securityContext:
    privileged: true

#2
securityContext:
    runAsNonRoot: true
    runAsUser: 10001

#3
securityContext:
    capabilities:
    drop: []
    allowPrivilegeEscalation: true

#4
securityContext:
    readOnlyRootFilesystem: true

-> If you want to write file, mount emptyDir
```

# Service Account Token
```
# sa
apiVersion: v1
kind: ServiceAccount
metadata:
  name: build-robot
automountServiceAccountToken: false

# po
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  serviceAccountName: build-robot
  automountServiceAccountToken: false
```

# Use Service Account in environment and configmap
- Notice indent

```
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: secret-manager
  name: secret-manager
  namespace: ns-secure
spec:
  volumes:
    - name: sec-a2
      secret:
        secretName: sec-a2
  serviceAccountName: secret-manager
  containers:
    - image: httpd:alpine
      name: secret-manager
      volumeMounts:
        - name: sec-a2
          mountPath: /etc/sec-a2
          readOnly: true
      env:
        - name: SEC_A1
          valueFrom:
            secretKeyRef:
              name: sec-a1
              key: user
  dnsPolicy: ClusterFirst
  restartPolicy: Always
```

# # RBAC, Role binding: HARD
- https://killercoda.com/killer-shell-cks/scenario/rbac-serviceaccount-permissions


# Enable ETCD Encryption
- reference: https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/#generate-key-no-kms
- killercoda: https://killercoda.com/killer-shell-cks/scenario/secret-etcd-encryption
```
Steps
# 1. Encode password
echo my-password | base64

# 2. create EncryptionConfiguration
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
    - secrets
    - ... <more resources if needed>
    providers:
    - aesgcm:
        keys:
        - name: key1
          secret: <base64>
    - identity: {}

# 3. mount EncryptionConfiguration file and configure params in `kube-apiserver` static pod
```

# Runtime Class
- reference: https://kubernetes.io/docs/concepts/containers/runtime-class/
- killercoda: https://killercoda.com/killer-shell-cks/scenario/sandbox-gvisor



# affinity, antiAffinity

# upgrade cluster
https://www.youtube.com/watch?v=e0eoEXSkpQY&list=PLpbwBK0ptssx38770vYNwZEuCeGNw54CH&index=13

# NetworkPolicy


# trivy 

# apiserver misconfigured

# noderestriction

# Cilium, Istio

# ImagePolicyWebhook

# Review
- Find out secret value in restricted context through service account token
https://www.youtube.com/watch?v=mul1YPi9iq0&list=PLpbwBK0ptssx38770vYNwZEuCeGNw54CH&index=17

# Syscall Activity Strace
- killercoda: https://killercoda.com/killer-shell-cks/scenario/syscall-activity-strace
- youtube task: https://www.youtube.com/watch?v=R31JFzuMVMw&list=PLpbwBK0ptssx38770vYNwZEuCeGNw54CH&index=11


```
# Use `strace` to see which syscalls
# strace will actually list various syscalls a process makes
# strace with command
strace kill -9 1234
strace kill -9 1234 2>&1 | grep 1234

# strace with PID
strace -p 19890 [-f] [-cw] # use your PID, we use -f for "follow forks", -cw for count and summarize

```
