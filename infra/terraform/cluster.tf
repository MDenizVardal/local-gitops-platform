# A local Kubernetes cluster running in Docker: one control-plane node and one worker.
resource "kind_cluster" "this" {
  name            = "gitops"
  node_image      = "kindest/node:v1.37.0@sha256:a1ed56cfb0e7b93589bdf97c8cd566405a265939e3620fc4f5de89adff580ae5"
  kubeconfig_path = "${path.module}/kubeconfig"
  wait_for_ready  = true

  kind_config {
    kind        = "Cluster"
    api_version = "kind.x-k8s.io/v1alpha4"

    node {
      role = "control-plane"

      # Publish three NodePorts on localhost. A NodePort is open on every node, so mapping
      # one node is enough. These can't change without recreating the cluster.
      extra_port_mappings { # shortener
        container_port = 30080
        host_port      = 8080
      }
      extra_port_mappings { # Grafana
        container_port = 30300
        host_port      = 3000
      }
      extra_port_mappings { # Argo CD UI
        container_port = 30443
        host_port      = 8443
      }
    }

    node {
      role = "worker"
    }
  }
}
