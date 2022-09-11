# How to setup Amazon Managed Prometheus to monitor your EKS cluster

1. Go to the Amazon Managed Prometheus (AMP) console and create a workspace

2. Create a helm values file with AMP parameters. You will use this in the next step when you install prometheus. See this doc for more details: https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-onboard-ingest-metrics-new-Prometheus.html
```
serviceAccounts:
  server:
    name: amp-iamproxy-ingest-service-account
    annotations: 
      eks.amazonaws.com/role-arn: ${IAM_PROXY_PROMETHEUS_ROLE_ARN}
server:
  remoteWrite:
    - url: https://aps-workspaces.${AWS_REGION}.amazonaws.com/workspaces/${WORKSPACE_ID}/api/v1/remote_write
      sigv4:
        region: ${AWS_REGION}
      queue_config:
        max_samples_per_send: 1000
        max_shards: 200
        capacity: 2500
```

3. Install Prometheus in your EKS cluster
```
helm version
kubectl create namespace prometheus
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm upgrade -i prometheus prometheus-community/prometheus --namespace prometheus --set alertmanager.persistentVolume.storageClass="gp2",server.persistentVolume.storageClass="gp2" -f <Path to the helm values file you created in step 2 above>
```

4. Create an Amazon Managed Grafana workspace. Under "Authentication", assign the user you created to access the workspace URL.
   If you do not see any dashboards in the AMG workspace console, go back to AMG in the AWS console. Then click on Data Sources, select AMP, and click on "Configure in Grafana".
   Go to Add "Data Source" in the AMG workspace console and select AMP. I was getting a permission denied error for about 10 minutes and it seemed to go away automatically. If you have problems selecting AMP as the data source, see this page: https://docs.aws.amazon.com/grafana/latest/userguide/AMP-adding-AWS-config.html

5. After you have added data sources in AMG, you can query metrics. Click on the "+" sign on the LHN. Select Import. In the Import screen, type 3119 in Import via grafana.com textbox and click Import.

