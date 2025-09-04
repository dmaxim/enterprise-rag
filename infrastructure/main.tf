

resource "azurerm_resource_group" "ent_rag" {
  name     = join("-", ["rg", var.namespace, var.environment, var.location_abbreviation])
  location = var.location

  tags = local.tags
}
