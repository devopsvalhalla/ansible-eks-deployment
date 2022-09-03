resource "aws_eks_cluster" "eks_cluster" {
  name     = var.eks_cluster_name
  role_arn = aws_iam_role.eks-role.arn
  version = var.k8s_version == "" ? var.k8s_version : null

  vpc_config {
    subnet_ids = [aws_subnet.example1.id, aws_subnet.example2.id]
    endpoint_private_access = var.private_cluster == "true" ? var.private_cluster : false
    endpoint_public_access = var.private_cluster == "false" ? var.private_cluster : true
  }

  kubernetes_network_config {
    ip_family = "ipv4"
    service_ipv4_cidr = var.eks_cluster_cidr
  }

  depends_on = [
    aws_iam_role.eks_role,
    aws_cloudwatch_log_group.eks_cw_group
  ]
}