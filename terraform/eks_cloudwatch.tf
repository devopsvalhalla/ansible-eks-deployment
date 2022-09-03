resource "aws_cloudwatch_log_group" "eks_cw_group" {
  name              = "/aws/eks/${var.cluster_name}/cluster"
  retention_in_days = 7
}