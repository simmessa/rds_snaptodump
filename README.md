# RDS snaptodump

A set of tools for dumping Amazon RDS databases (MySQL only, right now) with Python and Terraform. Find out more about how this was created and why [here](https://medium.com/@simmessa/fare-un-dump-da-uno-snapshot-rds-con-python-e-terraform-7cbd0fa026fc).

*Warning: linked page is in italian language*

## Prerequisites

Before using these tools you should install the following prerequisites:

- mysqldump (any reasonably recent version should work)
- Python 2 (tested on 2.7.12)
- Terraform (tested on 0.11.10 x64)

## Security credentials

The Python script requires you to set up your AWS credentials as environment variables. You might already have these if you use the AWS cli, but here's what you need to have:

```
export AWS_ACCESS_KEY_ID="xxx"
export AWS_SECRET_ACCESS_KEY="yyy"
```

Also, make sure the AWS IAM account linked to these credentials has the RDS permissions set to create, modify and destroy RDS instances plus seeing the various data snapshots.

## Usage

First of all install all the prerequisites.

### Terraform

```
wget https://releases.hashicorp.com/terraform/0.11.10/terraform_0.11.10_linux_amd64.zip; unzip terraform_0.11.10_linux_amd64.zip
```

**Please note this Terraform version might not be current in the future, so feel free to put the latest one in the previous command**

mysqldump and python 2 should be trivial to install according to your Linux distro of choice.

### Modify scripts

After this you can modify the *main.tf* script inserting your own environment details, such as AWS regions:

```
provider "aws" {
  region = "eu-west-1" # put your AWS region here!
}
[...]
```

db_instance_identifier:

```
[...]
# Get latest snapshot from production DB
data "aws_db_snapshot" "latest_prod_snapshot" {
    most_recent = true
    db_instance_identifier = "mydbname" # put the name of your db here!
}
[...]
```

And if you use VPCs and security groups:

```
[...]
  #vpc_security_group_ids = ["sg-12345678"] # if you are running inside a VPC uncomment and put yours here
[...]
```

Next you should edit the *snaptodump.py* script, putting your MySQL credentials:

```
[...]
dbusr = "your_mysql_username" 
dbname = "your_mysql_database_name"
[...]
```

After all this, you should be ready to launch:

```
python snaptodump.py
```

Feel free to post issues if you encounter any.

### Notes

- At the moment, we're using a db.t2.micro instance to restore and dump our snapshot, if that's unsuitable for you please modify this behaviour in *main.tf*

- Currently this tool will look for the LATEST snapshot of the specified db_instance_identifier. That's the way it was meant to work, of course you can ovverride this behaviour in *main.tf* (have a look [here](https://www.terraform.io/docs/providers/aws/d/db_snapshot.html) to find out how)