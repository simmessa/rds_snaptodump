provider "aws" {
  region = "eu-west-1" # put your AWS region here!
}

# Get latest snapshot from production DB
data "aws_db_snapshot" "latest_prod_snapshot" {
    most_recent = true
    db_instance_identifier = "mydbname" # put the name of your db here!
}
# Create new staging DB
resource "aws_db_instance" "db_snapshot_dumper" {
  instance_class       = "db.t2.micro"
  identifier           = "db-snapshot-dumper"
  username             = "user" # necessary, but won't be used since a snapshot identifier is provided...
  password             = "password" # necessary, but won't be used since a snapshot identifier is provided...
  snapshot_identifier  = "${data.aws_db_snapshot.latest_prod_snapshot.id}"
  #vpc_security_group_ids = ["sg-12345678"] # if you are running inside a VPC uncomment and put yours here
  skip_final_snapshot = true # Won't produce a final snapshot when disposing of db
}

output "address" {
  value = "${aws_db_instance.db_snapshot_dumper.address}"
}

output "snapshot" {
  value = "${aws_db_instance.db_snapshot_dumper.snapshot_identifier}"
}