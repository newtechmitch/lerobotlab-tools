"""
LeRobotLab Tools - Convert Module

Handles conversion of robot datasets to different formats (HDF5, Zarr, Parquet).
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional, List

import click
from .droid_conversion import DROIDConverter
from .vjepa2_ac_conversion import VJEPA2ACConverter


def convert_datasets(
    selection_data: Dict[str, Any],
    output_path: str,
    input_path: Optional[str] = None,
    format: str = 'hdf5',
    verbose: bool = False
) -> None:
    try:
        # Create output directory if it doesn't exist
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if verbose:
            click.echo(f"Created output directory: {output_dir.absolute()}")
        
        # Handle input path
        if input_path is None:
            if verbose:
                click.echo("No input path provided - datasets will be downloaded first")
            # Here would trigger download process
            input_dir = output_dir / "temp_downloads"
            click.echo("Downloading datasets for conversion...")
            # Would call download function here
        else:
            input_dir = Path(input_path)
            if not input_dir.exists():
                raise click.ClickException(f"Input directory does not exist: {input_path}")
        
        # Get datasets from selection
        datasets = selection_data.get('datasets', [])
        
        if verbose:
            metadata = selection_data.get('metadata', {})
            click.echo(f"Converting {len(datasets)} datasets to {format.upper()} format...")
            if 'total_episodes' in metadata:
                click.echo(f"Total episodes to convert: {metadata['total_episodes']}")
        
        # Process each dataset
        for i, dataset in enumerate(datasets, 1):
            repo_id = dataset['repo_id']
            selected_videos = dataset['selected_videos']
            
            if verbose:
                click.echo(f"\n[{i}/{len(datasets)}] Converting dataset: {repo_id}")
                click.echo(f"Selected videos: {', '.join(selected_videos)}")
            
            converter = _get_converter(format, verbose)
            
            # Convert the dataset using the appropriate converter
            click.echo(f"Converting dataset: {repo_id}")
            click.echo(f"  Output file: {output_dir}")
            
            result = converter.convert_dataset(repo_id, selected_videos, input_dir, output_dir)
            
            if result['status'] == 'error':
                click.echo(f"  ✗ {result['message']}")
            elif verbose:
                click.echo(f"  ✓ {result['message']}")
                if 'episodes_converted' in result:
                    click.echo(f"    Episodes converted: {result['episodes_converted']}")
            
            if verbose:
                click.echo(f"  -> Dataset {repo_id} converted successfully")
        
        click.echo(f"\nAll {len(datasets)} datasets converted to {format.upper()} format")
        click.echo(f"Output directory: {output_dir.absolute()}")
        
        # Clean up temporary downloads if they were created
        if input_path is None and input_dir.name == "temp_downloads":
            if verbose:
                click.echo("Cleaning up temporary download files...")
        
    except Exception as e:
        raise click.ClickException(f"Conversion failed: {e}")


def validate_output_path(output_path: str) -> Path:
    try:
        path = Path(output_path)
        
        # Check if parent directory is writable
        parent = path.parent
        if not parent.exists():
            raise click.ClickException(f"Parent directory does not exist: {parent}")
        
        if not os.access(parent, os.W_OK):
            raise click.ClickException(f"No write permission for directory: {parent}")
        
        return path
        
    except Exception as e:
        if isinstance(e, click.ClickException):
            raise
        raise click.ClickException(f"Invalid output path: {e}")


def validate_input_path(input_path: str) -> Path:
    try:
        path = Path(input_path)
        
        if not path.exists():
            raise click.ClickException(f"Input directory does not exist: {input_path}")
        
        if not path.is_dir():
            raise click.ClickException(f"Input path is not a directory: {input_path}")
        
        if not os.access(path, os.R_OK):
            raise click.ClickException(f"No read permission for directory: {input_path}")
        
        return path
        
    except Exception as e:
        if isinstance(e, click.ClickException):
            raise
        raise click.ClickException(f"Invalid input path: {e}")


def get_supported_formats() -> List[str]:
    return ['droid', 'vjepa2-ac']


def validate_format(format: str) -> str:
    format_lower = format.lower()
    supported = get_supported_formats()
    
    if format_lower not in supported:
        raise click.ClickException(
            f"Unsupported format '{format}'. Supported formats: {', '.join(supported)}"
        )
    
    return format_lower


def estimate_conversion_time(selection_data: Dict[str, Any]) -> Optional[str]:
    metadata = selection_data.get('metadata', {})
    total_frames = metadata.get('total_frames')
    
    if total_frames:
        # Rough estimate: assume ~1000 frames per second processing
        estimated_seconds = total_frames / 1000
        
        if estimated_seconds < 60:
            return f"~{estimated_seconds:.0f} seconds"
        elif estimated_seconds < 3600:
            return f"~{estimated_seconds / 60:.1f} minutes"
        else:
            return f"~{estimated_seconds / 3600:.1f} hours"
    
    return None


def _get_converter(format: str, verbose: bool = False):
    """
    Factory function to get the appropriate converter based on format.
    
    Args:
        format: Target conversion format ('droid' or 'vjepa2-ac')
        verbose: Whether to enable verbose logging
        
    Returns:
        Converter instance for the specified format
        
    Raises:
        click.ClickException: If format is not supported
    """
    if format == 'droid':
        return DROIDConverter(verbose=verbose)
    elif format == 'vjepa2-ac':
        return VJEPA2ACConverter(verbose=verbose)
    else:
        raise click.ClickException(f"Unsupported format: {format}. Supported formats: {get_supported_formats()}") 