"""
Plugin loader for domain discovery and registration.

Automatically discovers and loads domain plugins from graphmodels/domains/.
"""

import importlib.util
import sys
from pathlib import Path
from typing import List, Dict, Any

from graphmodels.core.registries import register_domain


def discover_domains(domains_path: Path) -> List[str]:
    """
    Discover available domain plugins.

    Args:
        domains_path: Path to graphmodels/domains/ directory

    Returns:
        List of discovered domain names

    Example:
        >>> domains_path = Path('graphmodels/domains')
        >>> domains = discover_domains(domains_path)
        >>> print(domains)
        ['business', 'aaoifi']
    """
    if not domains_path.exists():
        return []

    domains = []
    for item in domains_path.iterdir():
        if item.is_dir() and not item.name.startswith('_'):
            # Check if has __init__.py
            if (item / '__init__.py').exists():
                domains.append(item.name)

    return domains


def load_domain(domain_name: str, domains_path: Path) -> Dict[str, Any]:
    """
    Load a domain plugin and return its registries.

    Args:
        domain_name: Name of the domain to load
        domains_path: Path to graphmodels/domains/ directory

    Returns:
        Dict with 'entities' and 'edges' registries

    Raises:
        ImportError: If domain cannot be loaded
        AttributeError: If domain doesn't have required registries

    Example:
        >>> domains_path = Path('graphmodels/domains')
        >>> domain_data = load_domain('business', domains_path)
        >>> entities = domain_data['entities']
        >>> edges = domain_data['edges']
    """
    domain_path = domains_path / domain_name
    if not domain_path.exists():
        raise ImportError(f"Domain not found: {domain_name}")

    # Import domain module
    module_path = domain_path / '__init__.py'
    spec = importlib.util.spec_from_file_location(
        f"graphmodels.domains.{domain_name}",
        module_path
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load domain: {domain_name}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    # Extract registries
    if not hasattr(module, 'ENTITIES'):
        raise AttributeError(f"Domain '{domain_name}' missing ENTITIES registry")
    if not hasattr(module, 'EDGES'):
        raise AttributeError(f"Domain '{domain_name}' missing EDGES registry")

    return {
        'entities': module.ENTITIES,
        'edges': module.EDGES,
    }


def load_all_domains(domains_path: Path) -> List[str]:
    """
    Discover and load all available domain plugins.

    Args:
        domains_path: Path to graphmodels/domains/ directory

    Returns:
        List of successfully loaded domain names

    Example:
        >>> domains_path = Path('graphmodels/domains')
        >>> loaded = load_all_domains(domains_path)
        >>> print(f"Loaded {len(loaded)} domains: {', '.join(loaded)}")
    """
    discovered = discover_domains(domains_path)
    loaded = []

    for domain_name in discovered:
        try:
            domain_data = load_domain(domain_name, domains_path)
            register_domain(
                domain_name,
                domain_data['entities'],
                domain_data['edges']
            )
            loaded.append(domain_name)
        except (ImportError, AttributeError) as e:
            print(f"Warning: Failed to load domain '{domain_name}': {e}", file=sys.stderr)
            continue

    return loaded


__all__ = [
    "discover_domains",
    "load_domain",
    "load_all_domains",
]
