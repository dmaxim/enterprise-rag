

resource "azurerm_search_service" "ent_rag" {
  name                = join("-", [var.namespace, var.environment, var.location_abbreviation])
  resource_group_name = azurerm_resource_group.ent_rag.name
  location            = azurerm_resource_group.ent_rag.location
  sku                 = "standard"

  local_authentication_enabled = true
  authentication_failure_mode  = "http403"
}

# resource "azurerm_key_vault_secret" "search_endpoint" {
#   key_vault_id = azurerm_key_vault.ent_rag.id
#   name         = "AISearch--Endpoint"
#   value        = azurerm_search_service.ent_rag.
#   depends_on = [
#     azurerm_key_vault.ent_rag,
#     azurerm_search_service.ent_rag
#   ]
# }


resource "azurerm_key_vault_secret" "search_key" {
  key_vault_id = azurerm_key_vault.ent_rag.id
  name         = "AISearch--SearchKey"
  value        = azurerm_search_service.ent_rag.primary_key
  depends_on   = [azurerm_key_vault.ent_rag, azurerm_search_service.ent_rag]
}

resource "azurerm_key_vault_secret" "search_name" {
  key_vault_id = azurerm_key_vault.ent_rag.id
  name         = "AISearch--SearchName"
  value        = azurerm_search_service.ent_rag.name
  depends_on   = [azurerm_key_vault.ent_rag, azurerm_search_service.ent_rag]
}