#!/usr/bin/env python3
"""
POF Version Handler - Comprehensive version compatibility system.

Based on Rust reference implementation with version-specific parsing.
"""

import logging
from typing import Dict, List, Optional, Any

from .pof_types import POFVersion

logger = logging.getLogger(__name__)


class POFVersionHandler:
    """Handler for POF version compatibility and format-specific parsing."""
    
    def __init__(self):
        """Initialize version handler with version-specific configurations."""
        self._version_configs = self._initialize_version_configs()
    
    def _initialize_version_configs(self) -> Dict[POFVersion, Dict[str, Any]]:
        """Initialize configuration for each supported POF version."""
        return {
            POFVersion.VERSION_1800: {
                'name': 'FS1 Format',
                'compatible': True,
                'warnings': ['FS1 format may have limited feature support'],
                'chunk_requirements': ['OHDR', 'SOBJ', 'TXTR'],
                'optional_chunks': ['SPCL', 'PATH'],
                'bsp_format': 'legacy',
                'has_mass_properties': False,
                'has_cross_sections': False,
                'has_lights': False,
            },
            POFVersion.VERSION_2100: {
                'name': 'FS2 Base Format',
                'compatible': True,
                'warnings': [],
                'chunk_requirements': ['OHDR', 'SOBJ', 'TXTR'],
                'optional_chunks': ['SPCL', 'PATH', 'GPNT', 'MPNT', 'DOCK', 'FUEL'],
                'bsp_format': 'legacy',
                'has_mass_properties': True,
                'has_cross_sections': False,
                'has_lights': False,
            },
            POFVersion.VERSION_2112: {
                'name': 'FS2 Enhanced',
                'compatible': True,
                'warnings': [],
                'chunk_requirements': ['OHDR', 'SOBJ', 'TXTR'],
                'optional_chunks': ['SPCL', 'PATH', 'GPNT', 'MPNT', 'DOCK', 'FUEL', 'SHLD', 'EYE'],
                'bsp_format': 'enhanced',
                'has_mass_properties': True,
                'has_cross_sections': True,
                'has_lights': False,
            },
            POFVersion.VERSION_2117: {
                'name': 'WCS Current',
                'compatible': True,
                'warnings': [],
                'chunk_requirements': ['OHDR', 'SOBJ', 'TXTR'],
                'optional_chunks': ['SPCL', 'PATH', 'GPNT', 'MPNT', 'DOCK', 'FUEL', 'SHLD', 'EYE', 'INSG', 'ACEN', 'GLOW', 'SLDC'],
                'bsp_format': 'enhanced',
                'has_mass_properties': True,
                'has_cross_sections': True,
                'has_lights': True,
            },
        }
    
    def validate_version(self, version: int) -> Dict[str, Any]:
        """
        Validate POF version and return compatibility information.
        
        Args:
            version: POF version number
            
        Returns:
            Dictionary with validation results and compatibility info
        """
        try:
            pof_version = POFVersion(version)
            config = self._version_configs.get(pof_version, {})
            
            return {
                'valid': True,
                'version': pof_version,
                'compatible': config.get('compatible', False),
                'name': config.get('name', 'Unknown'),
                'warnings': config.get('warnings', []),
                'config': config
            }
            
        except ValueError:
            # Unknown version
            return {
                'valid': False,
                'version': version,
                'compatible': False,
                'name': 'Unknown',
                'warnings': [f'Unknown POF version {version}'],
                'config': {}
            }
    
    def check_chunk_compatibility(self, version: int, chunk_id: int) -> Dict[str, Any]:
        """
        Check if a chunk type is compatible with the given version.
        
        Args:
            version: POF version number
            chunk_id: Chunk ID to check
            
        Returns:
            Compatibility information for the chunk
        """
        validation = self.validate_version(version)
        if not validation['valid']:
            return {
                'compatible': False,
                'warning': f'Unknown version {version}',
                'recommendation': 'skip'
            }
        
        # Map chunk IDs to names (simplified)
        chunk_names = {
            0x4F484452: 'OHDR',  # 'OHDR'
            0x4F424A32: 'SOBJ',  # 'OBJ2'
            0x54585452: 'TXTR',  # 'TXTR'
            0x5350434C: 'SPCL',  # 'SPCL'
            0x50415448: 'PATH',  # 'PATH'
            0x47504E54: 'GPNT',  # 'GPNT'
            0x4D504E54: 'MPNT',  # 'MPNT'
            0x444F434B: 'DOCK',  # 'DOCK'
            0x4655454C: 'FUEL',  # 'FUEL'
            0x53484C44: 'SHLD',  # 'SHLD'
            0x45594550: 'EYEP',  # 'EYEP'
            0x494E5347: 'INSG',  # 'INSG'
            0x4143454E: 'ACEN',  # 'ACEN'
            0x474C4F57: 'GLOW',  # 'GLOW'
            0x534C4443: 'SLDC',  # 'SLDC'
        }
        
        chunk_name = chunk_names.get(chunk_id, f'UNKNOWN_{chunk_id:08X}')
        config = validation['config']
        
        # Check if chunk is required
        if chunk_name in config.get('chunk_requirements', []):
            return {
                'compatible': True,
                'required': True,
                'chunk_name': chunk_name,
                'recommendation': 'process'
            }
        
        # Check if chunk is optional
        if chunk_name in config.get('optional_chunks', []):
            return {
                'compatible': True,
                'required': False,
                'chunk_name': chunk_name,
                'recommendation': 'process'
            }
        
        # Unknown chunk for this version
        return {
            'compatible': False,
            'required': False,
            'chunk_name': chunk_name,
            'warning': f'Chunk {chunk_name} not supported in version {version}',
            'recommendation': 'skip'
        }
    
    def get_version_specific_parser(self, version: int, chunk_id: int):
        """
        Get version-specific parser function for a chunk.
        
        Args:
            version: POF version number
            chunk_id: Chunk ID
            
        Returns:
            Parser function or None if not available
        """
        # This would return different parser functions based on version
        # For now, return None to use default parsers
        return None
    
    def apply_version_specific_fixes(self, parsed_data: Dict[str, Any], version: int) -> Dict[str, Any]:
        """
        Apply version-specific fixes and transformations to parsed data.
        
        Args:
            parsed_data: Parsed POF data
            version: POF version number
            
        Returns:
            Fixed and normalized data
        """
        validation = self.validate_version(version)
        if not validation['valid']:
            return parsed_data
        
        config = validation['config']
        fixed_data = parsed_data.copy()
        
        # Apply version-specific fixes
        if not config.get('has_mass_properties', True):
            # Add default mass properties for older versions
            if 'header' in fixed_data and 'mass' not in fixed_data['header']:
                fixed_data['header']['mass'] = 0.0
                fixed_data['header']['mass_center'] = [0.0, 0.0, 0.0]
                fixed_data['header']['moment_inertia'] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        
        if not config.get('has_cross_sections', True):
            # Add empty cross sections
            if 'header' in fixed_data and 'cross_sections' not in fixed_data['header']:
                fixed_data['header']['cross_sections'] = []
        
        if not config.get('has_lights', True):
            # Add empty lights
            if 'header' in fixed_data and 'lights' not in fixed_data['header']:
                fixed_data['header']['lights'] = []
        
        # Normalize texture names
        if 'textures' in fixed_data:
            fixed_data['textures'] = [
                self._normalize_texture_name(tex, version)
                for tex in fixed_data['textures']
            ]
        
        return fixed_data
    
    def _normalize_texture_name(self, texture_name: str, version: int) -> str:
        """Normalize texture name based on version."""
        # Remove any path components for consistency
        if '/' in texture_name:
            texture_name = texture_name.split('/')[-1]
        if '\\' in texture_name:
            texture_name = texture_name.split('\\')[-1]
        
        # Ensure proper extension
        if not texture_name.lower().endswith(('.dds', '.png', '.tga', '.jpg')):
            # Older versions might not have extensions
            if version <= POFVersion.VERSION_2100:
                texture_name += '.dds'  # Assume DDS for older versions
            else:
                texture_name += '.dds'  # Default to DDS
        
        return texture_name
    
    def generate_compatibility_report(self, version: int, chunks_found: List[str]) -> Dict[str, Any]:
        """
        Generate comprehensive compatibility report.
        
        Args:
            version: POF version number
            chunks_found: List of chunk names found in the file
            
        Returns:
            Compatibility report with issues and recommendations
        """
        validation = self.validate_version(version)
        report = {
            'version_info': validation,
            'issues': [],
            'warnings': [],
            'recommendations': []
        }
        
        if not validation['valid']:
            report['issues'].append(f'Unknown POF version {version}')
            report['recommendations'].append('Use with caution - format may be incompatible')
            return report
        
        config = validation['config']
        
        # Check for missing required chunks
        required_chunks = config.get('chunk_requirements', [])
        missing_chunks = [chunk for chunk in required_chunks if chunk not in chunks_found]
        
        if missing_chunks:
            report['issues'].append(f'Missing required chunks: {missing_chunks}')
            report['recommendations'].append('File may be incomplete or corrupted')
        
        # Check for unsupported chunks
        all_supported_chunks = required_chunks + config.get('optional_chunks', [])
        unsupported_chunks = [chunk for chunk in chunks_found if chunk not in all_supported_chunks]
        
        if unsupported_chunks:
            report['warnings'].append(f'Unsupported chunks for this version: {unsupported_chunks}')
            report['recommendations'].append('These chunks will be ignored during processing')
        
        # Add version-specific warnings
        report['warnings'].extend(config.get('warnings', []))
        
        return report


# Global instance for convenience
_version_handler = POFVersionHandler()


def validate_pof_version(version: int) -> Dict[str, Any]:
    """Validate POF version (convenience function)."""
    return _version_handler.validate_version(version)


def check_chunk_compatibility(version: int, chunk_id: int) -> Dict[str, Any]:
    """Check chunk compatibility (convenience function)."""
    return _version_handler.check_chunk_compatibility(version, chunk_id)


def apply_version_fixes(parsed_data: Dict[str, Any], version: int) -> Dict[str, Any]:
    """Apply version-specific fixes (convenience function)."""
    return _version_handler.apply_version_specific_fixes(parsed_data, version)


def generate_compatibility_report(version: int, chunks_found: List[str]) -> Dict[str, Any]:
    """Generate compatibility report (convenience function)."""
    return _version_handler.generate_compatibility_report(version, chunks_found)