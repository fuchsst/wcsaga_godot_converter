"""
Enhanced Asset Catalog Package

This module provides extended functionality for the AssetCatalog class,
including advanced search, dependency tracking, and asset grouping capabilities.

Author: Qwen Code Assistant
"""

# The EnhancedAssetCatalog functionality has been consolidated into the main AssetCatalog class
# This file is kept for backward compatibility

from .asset_catalog import AssetCatalog

# For backward compatibility, we can alias the enhanced functionality
EnhancedAssetCatalog = AssetCatalog

__all__ = ["AssetCatalog", "EnhancedAssetCatalog"]