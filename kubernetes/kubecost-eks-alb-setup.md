##Kubecost ALB setup cheatsheet

##How to setup the AWS Load Balancer Controller to expose the Kubecost dashboard

ssh -i ec2-pem-files/ec2instance-august2022.pem ec2-user@44.194.235.109

The steps in this doc are from here and here.

1. Create an IAM policy. (This might already exist and you might be able to skip this step. Check if AWSLoadBalancerControllerIAMPolicy exists)
curl -o iam_policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.4.3/docs/install/iam_policy.json

2. Use the eksctl CLI to associate an IAM OIDC provider with the cluster:
eksctl utils associate-iam-oidc-provider --region=us-east-1 --cluster=eks-cluster-august2022

3. Create the IAM role and Kubernetes service account:

eksctl create iamserviceaccount \
  --cluster=eks-cluster-august2022 \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --role-name "AmazonEKSLoadBalancerControllerRole" \
  --attach-policy-arn=arn:aws:iam::119277115670:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve

4. Install the AWS Load Balancer Controller using Helm V3 or later 

helm repo add eks https://aws.github.io/eks-charts

helm repo update

Make sure that you set the correct image.repository for your region (see here: https://docs.aws.amazon.com/eks/latest/userguide/add-ons-images.html)
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=eks-cluster-august2022 \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --set image.repository=602401143452.dkr.ecr.us-east-1.amazonaws.com/amazon/aws-load-balancer-controller

kubectl apply -f ingress-alb.yaml -n kubecost



