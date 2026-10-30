resource "aws_security_group" "school_portal" {
  name        = "school-portal-sg"
  description = "Security group for the school portal"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "school_portal" {
  ami                         = "ami-06fb1802e2b757f09"
  instance_type               = "t3.micro"
  subnet_id                   = "subnet-0bf6dbce982c87a8a"
  associate_public_ip_address = true
  key_name                    = "dockerkey"

  vpc_security_group_ids = [aws_security_group.school_portal.id]
}
