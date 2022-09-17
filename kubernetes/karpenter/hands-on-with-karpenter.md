# Getting hands on with Karpenter in your EKS cluster

The steps in this document will allow you to install, configure and test Karpenter with a sample deployment. We assume that you have an EKS cluster created already.

1. Set some environment variables:
```
export KARPENTER_VERSION=v0.16.1
export CLUSTER_NAME=<EKS cluster name>
export AWS_DEFAULT_REGION=<region>
export AWS_ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
export CLUSTER_ENDPOINT="$(aws eks describe-cluster --name ${CLUSTER_NAME} --query "cluster.endpoint" --output text)"
```

The instances launched by Karpenter must run with an InstanceProfile that grants permissions necessary to run containers and configure networking.
Karpenter discovers the InstanceProfile using the name KarpenterNodeRole-${ClusterName}.

2. Now, create the IAM resources using AWS CloudFormation.
```
TEMPOUT=$(mktemp)

curl -fsSL https://karpenter.sh/"${KARPENTER_VERSION}"/getting-started/getting-started-with-eksctl/cloudformation.yaml  > $TEMPOUT \
&& aws cloudformation deploy \
  --stack-name "Karpenter-${CLUSTER_NAME}" \
  --template-file "${TEMPOUT}" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides "ClusterName=${CLUSTER_NAME}"
```

3. Next, grant access to instances using the profile to connect to the cluster. This command adds the Karpenter node role to your aws-auth configmap, allowing nodes with this role to connect to the cluster.
```
eksctl create iamidentitymapping \
  --username system:node:{{EC2PrivateDNSName}} \
  --cluster "${CLUSTER_NAME}" \
  --arn "arn:aws:iam::${AWS_ACCOUNT_ID}:role/KarpenterNodeRole-${CLUSTER_NAME}" \
  --group system:bootstrappers \
  --group system:nodes
```
Now, Karpenter can launch new EC2 instances and those instances can connect to your cluster.

4. Create the KarpenterController IAM Role. Karpenter requires permissions like launching instances.
To see your existing service accounts and roles, you can run the following command:
```
eksctl get iamserviceaccount --cluster "${CLUSTER_NAME}"
```

To create an AWS IAM Role, Kubernetes service account, and associate them using IRSA, run the following command:
```
eksctl create iamserviceaccount \
  --cluster "${CLUSTER_NAME}" --name karpenter --namespace karpenter \
  --role-name "${CLUSTER_NAME}-karpenter" \
  --attach-policy-arn "arn:aws:iam::${AWS_ACCOUNT_ID}:policy/KarpenterControllerPolicy-${CLUSTER_NAME}" \
  --role-only \
  --approve


export KARPENTER_IAM_ROLE_ARN="arn:aws:iam::${AWS_ACCOUNT_ID}:role/${CLUSTER_NAME}-karpenter"
```

5. Create the EC2 Spot Service Linked Role. This step is only necessary if this is the first time you’re using EC2 Spot in this account. See here for more details: https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html
```
aws iam create-service-linked-role --aws-service-name spot.amazonaws.com || true
```

6. Install the Karpenter Helm Chart
```
helm repo add karpenter https://charts.karpenter.sh/

helm repo update

helm upgrade --install --namespace karpenter --create-namespace \
  karpenter karpenter/karpenter \
  --version ${KARPENTER_VERSION} \
  --set serviceAccount.annotations."eks\.amazonaws\.com/role-arn"=${KARPENTER_IAM_ROLE_ARN} \
  --set clusterName=${CLUSTER_NAME} \
  --set clusterEndpoint=${CLUSTER_ENDPOINT} \
  --set aws.defaultInstanceProfile=KarpenterNodeInstanceProfile-${CLUSTER_NAME} \
  --wait # for the defaulting webhook to install before creating a Provisioner
```

7. Create a default provisioner using the YAML file below. Remember to replace the <cluster name> with your cluster name.
```
apiVersion: karpenter.sh/v1alpha5
kind: Provisioner
metadata:
  name: default
spec:
  requirements:
    - key: karpenter.sh/capacity-type
      operator: In
      values: ["spot"]
  limits:
    resources:
      cpu: 1000
  providerRef:
    name: default
  ttlSecondsAfterEmpty: 30
---
apiVersion: karpenter.k8s.aws/v1alpha1
kind: AWSNodeTemplate
metadata:
  name: default
spec:
  subnetSelector:
    karpenter.sh/discovery: <cluster name>
  securityGroupSelector:
    karpenter.sh/discovery: <cluster name>
```

8. Add the following tag to the cluster, subnets and security groups associated with the cluster
```
  Key: karpenter.sh/discovery; Value: <cluster name>
```

Karpenter is now active and ready to begin provisioning nodes. Create some pods using a deployment, and watch Karpenter provision nodes in response.

9. Test Karpenter! This deployment uses the pause image and starts with zero replicas.
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: inflate
spec:
  replicas: 0
  selector:
    matchLabels:
      app: inflate
  template:
    metadata:
      labels:
        app: inflate
    spec:
      terminationGracePeriodSeconds: 0
      containers:
        - name: inflate
          image: public.ecr.aws/eks-distro/kubernetes/pause:3.2
          resources:
            requests:
              cpu: 1
```
Now scale the deployment and see Karpenter in action!
```
kubectl scale deployment inflate --replicas 5
kubectl logs -f -n karpenter -l app.kubernetes.io/name=karpenter -c controller
```

10. To delete the deployment, run the following command. After 30 seconds (ttlSecondsAfterEmpty), Karpenter should terminate the now empty nodes.
```
kubectl delete deployment inflate
kubectl logs -f -n karpenter -l app.kubernetes.io/name=karpenter -c controller
  ```
