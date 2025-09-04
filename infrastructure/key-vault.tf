data "azurerm_client_config" "current" {

}

data "azuread_client_config" "current" {}

resource "azurerm_key_vault" "ent_rag" {
  name                          = var.key_vault_name
  location                      = azurerm_resource_group.ent_rag.location
  resource_group_name           = azurerm_resource_group.ent_rag.name
  tenant_id                     = data.azuread_client_config.current.tenant_id
  sku_name                      = "standard"
  enabled_for_disk_encryption   = false
  soft_delete_retention_days    = 7
  enable_rbac_authorization     = true
  public_network_access_enabled = true

  tags = local.tags
}


resource "azurerm_role_assignment" "key_vault_role" {
  for_each           = local.key_vault_secret_managers
  scope              = azurerm_key_vault.ent_rag.id
  role_definition_id = "/subscriptions/${data.azurerm_client_config.current.subscription_id}/providers/Microsoft.Authorization/roleDefinitions/b86a8fe4-44ce-4948-aee5-eccb2c155cd7"
  principal_id       = each.value.object_id
}