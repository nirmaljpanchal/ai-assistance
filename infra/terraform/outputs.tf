output "resource_group_id" {
  description = "Resource Group ID"
  value       = azurerm_resource_group.main.id
}

output "resource_group_name" {
  description = "Resource Group Name"
  value       = azurerm_resource_group.main.name
}

output "azure_location" {
  description = "Azure Location"
  value       = azurerm_resource_group.main.location
}
