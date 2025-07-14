output "app_server_public_ip" {
  description = "Public IP of the app server"
  value       = aws_instance.app_server.public_ip
}

output "app_server_public_dns" {
  description = "Public DNS of the app server"
  value       = aws_instance.app_server.public_dns
}
