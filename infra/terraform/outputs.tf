output "kubeconfig_path" {
  value = abspath(kind_cluster.this.kubeconfig_path)
}

output "shortener_url" {
  value = "http://localhost:8080"
}

output "grafana_url" {
  value = "http://localhost:3000"
}

output "argocd_url" {
  value = "https://localhost:8443"
}

output "argocd_password_command" {
  description = "The Argo CD username is admin."
  value       = "make argocd-password"
}
