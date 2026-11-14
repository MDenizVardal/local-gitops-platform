# Helm talks to the cluster created in cluster.tf, using the credentials kind returns.
provider "helm" {
  kubernetes = {
    host                   = kind_cluster.this.endpoint
    client_certificate     = kind_cluster.this.client_certificate
    client_key             = kind_cluster.this.client_key
    cluster_ca_certificate = kind_cluster.this.cluster_ca_certificate
  }
}

resource "helm_release" "argocd" {
  name             = "argocd"
  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  version          = "10.18.0"
  namespace        = "argocd"
  create_namespace = true
  values           = [file("${path.module}/values/argocd.yaml")]
}

# The root Application ("app of apps"). It is created through a Helm chart instead of
# kubernetes_manifest, because the Application CRD doesn't exist yet at plan time.
resource "helm_release" "root_app" {
  name       = "root-app"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argocd-apps"
  version    = "2.0.8"
  namespace  = "argocd"
  values     = [file("${path.module}/values/root-app.yaml")]

  depends_on = [helm_release.argocd]
}
