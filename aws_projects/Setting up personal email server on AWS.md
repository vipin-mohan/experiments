## These are my  notes based on my experience setting up personal email server on AWS
1. Create an Alternate User Account: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/managing-users.html
	1. To prevent entering a passowrd, Add, this line to the sudoers file, in the user privileges section:
		Vipin ALL=(ALL) NOPASSWD:ALL
2. Associating an Elastic IP Address with a Running Instance: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html#using-instance-addressing-eips-associating
	1. When you associate an elastic IP address with an instance, the public IP address is released
3. Note that if you selected MariaDB, then you don’t need password to log into MariaDB shell. Instead of running the normal command mysql -u root -p, you can run the following command to login, with sudo and without providing MariaDB root password.
		sudo mysql -u root
4. Error when restarting firewall: Review this
	1. [ INFO ] Updating ClamAV database (freshclam), please wait...<br/>
	ERROR: /var/log/clamav/freshclam.log is locked by another process<br/>
	It's safe to ignore, at this stage ClamAV daemon is not running, so freshclam can not talk to its socket to notify ClamAV to reload the virus signature database<br/>
	https://forum.iredmail.org/topic15062-error-during-installation-while-updating-clamav-database.html
5. In /etc/hosts, add both domain.com and the mail.domain.com
6. Check setting in security group
