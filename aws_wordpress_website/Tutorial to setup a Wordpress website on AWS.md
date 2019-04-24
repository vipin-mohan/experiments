## How to Launch a WordPress Website on AWS
#Step 1: Launch an Amazon EC2 Instance. Now you are in the EC2 dashboard, click Launch Instance from the dashboard to create and configure your virtual machine.
#Step 2: Configure your Instance. Now you're in the Amazon EC2 configuration wizard, we will be using an existing Amazon Machine Image (AMI) from the AWS Marketplace that has WordPress already installed. The AWS Marketplace provides access to thousands of pre-configured images for common pieces of software.
1. Click on AWS Marketplace on the left-hand side, search for WordPress, look for WordPress powered by BitNami, then click Select.
1. You will be presented a detailed pricing page. In this case, the price will be $0.00 for the software regardless of the size of the instance that you use. Scroll to the bottom and click Continue.
1. Click on t2.micro in the Type column (it should be the first one), then click Next: Configure Instance Details. It may take a few seconds to load. On the following screens, click Next: Add Storage and then Next: Tag Instance.
1. We will set a name for your instance in this step. Enter Name in the Key box and WordPress in the Value box. Click Review and Launch to continue.
1. You can review your instance configurations, then click Launch when you’re ready to start your Amazon EC2 instance running WordPress.
1. The next screen deals with key-pairs. Key-pairs are how you can connect to your EC2 instances via a terminal program using Secure Shell (SSH). To connect to your instance directly, you will need to create a new key pair. Click Launch Instances to launch your instance. Be aware that starting the instance up may take a few minutes.
1. Click View Instances on the bottom right of the page (you may need to scroll down to see it). Then select the WordPress instance, make sure the Instance State says running. If Instance State says launching then AWS is still preparing your WordPress instance.
1. Once your instance is running, you can now test your WordPress website. Find the Public IP for your instance at the bottom of this page.
1. Copy the Public IP into a new tab in your web browser, and you should see a Hello World blog page appear.
#Step 3: Make Changes to Your Website
Now that you have your WordPress site up and running, it’s time to log into its administration page so you can customize your site. To find your password, please follow the steps below:
1. Switch back to your EC2 management console in your web browser. Select WordPress instance, and click the Actions button. In the drop down menu, select Instance Setting, and choose Get System Log.
1. In the system log window, scroll through to the bottom to find the password that's surrounded by hash marks.
1. Now that you have your password, switch back to the tab that you used to access the WordPress Hello World page. Add /admin to the end of the URL so it looks something like 54.192.32.144/admin. Hit enter. Enter the Username user and the Password that you read from the log file.
Congratulations! You now have your WordPress site up and running. You can now manage, customize, and configure it as you like.