#!/usr/bin/env python3
"""
Simple test script to verify the coin plugin structure and imports
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from endstone_coin_plugin.coin_plugin import CoinPlugin
    print("✓ Successfully imported CoinPlugin")

    # Test plugin initialization
    plugin = CoinPlugin()
    print("✓ Successfully created CoinPlugin instance")

    # Check if default coins are loaded
    print(f"✓ Default coins count: {len(plugin.DEFAULT_COINS)}")

    # Test data structure
    for i, coin in enumerate(plugin.DEFAULT_COINS[:3]):  # Show first 3 coins
        print(f"  Coin {i+1}: {coin['display_name']} - {coin['points']} pts")

    # Test API methods
    print("\n✓ Testing API methods:")
    print(f"  - list_coins(): Returns {type(plugin.list_coins()).__name__}")
    print(f"  - add_coin(): Method exists: {hasattr(plugin, 'add_coin')}")
    print(f"  - remove_coin(): Method exists: {hasattr(plugin, 'remove_coin')}")
    print(f"  - reload_coins_from_file(): Method exists: {hasattr(plugin, 'reload_coins_from_file')}")

    print("\n✓ Plugin structure looks good!")
    print("\nTo use the coin manager:")
    print("1. Install the plugin in your Endstone server")
    print("2. Edit coins.json file or use the programmatic API")
    print("3. See COIN_MANAGEMENT.md for detailed instructions")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Make sure Endstone is installed: pip install endstone>=0.11.8,<0.12")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
