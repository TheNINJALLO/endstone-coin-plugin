# Coin Management Guide

## Overview

The Endstone Coin Plugin now supports dynamic coin configuration through JSON files and programmatic methods. While the GUI forms are not available in this version due to import limitations, you can still manage coins through file editing and programmatic access.

## Configuration File

Coins are stored in `plugins/endstone-coin-plugin/coins.json`. The plugin will automatically create this file with default coins on first run.

### JSON Structure

```json
[
  {
    "currency_obj": "Money",
    "display_name": "§6Wooden TK Coin §f$1",
    "name": "ninjos:coin_wood",
    "points": 1
  },
  {
    "currency_obj": "Money",
    "display_name": "§7Glass TK Coin §f$5",
    "name": "ninjos:coin_glass",
    "points": 5
  }
]
```

### Field Descriptions

- **currency_obj**: The scoreboard objective name (usually "Money")
- **display_name**: The formatted name shown to players (supports Minecraft color codes)
- **name**: The unique item identifier (e.g., "ninjos:coin_gold")
- **points**: The point value of the coin (must be a positive integer)

## Managing Coins

### Method 1: Direct File Editing

1. Stop your server
2. Edit `plugins/endstone-coin-plugin/coins.json`
3. Add, modify, or remove coin entries
4. Start your server

### Method 2: Programmatic Access

The plugin provides several public methods for other plugins to use:

```python
# Get the coin plugin instance
coin_plugin = server.plugin_manager.get_plugin("coin-plugin")

# Add a new coin
success = coin_plugin.add_coin(
    currency_obj="Money",
    display_name="§5Purple Coin §f$250",
    item_name="ninjos:coin_purple",
    points=250
)

# Remove a coin
success = coin_plugin.remove_coin("ninjos:coin_purple")

# List all coins
coins = coin_plugin.list_coins()

# Reload coins from file
coin_plugin.reload_coins_from_file()
```

### Method 3: Runtime File Editing

1. Edit the `coins.json` file while the server is running
2. Use the reload method to apply changes without restart:
   ```python
   coin_plugin.reload_coins_from_file()
   ```

## Color Codes

You can use Minecraft color codes in display names:

- `§0` - Black
- `§1` - Dark Blue
- `§2` - Dark Green
- `§3` - Dark Aqua
- `§4` - Dark Red
- `§5` - Dark Purple
- `§6` - Gold
- `§7` - Gray
- `§8` - Dark Gray
- `§9` - Blue
- `§a` - Green
- `§b` - Aqua
- `§c` - Red
- `§d` - Light Purple
- `§e` - Yellow
- `§f` - White
- `§l` - Bold
- `§o` - Italic
- `§n` - Underline
- `§m` - Strikethrough
- `§k` - Obfuscated
- `§r` - Reset

## Example Configurations

### Basic Coin Set
```json
[
  {
    "currency_obj": "Money",
    "display_name": "§6Copper Coin §f$1",
    "name": "mypack:copper_coin",
    "points": 1
  },
  {
    "currency_obj": "Money",
    "display_name": "§7Silver Coin §f$10",
    "name": "mypack:silver_coin",
    "points": 10
  },
  {
    "currency_obj": "Money",
    "display_name": "§eGold Coin §f$100",
    "name": "mypack:gold_coin",
    "points": 100
  }
]
```

### Multi-Currency Setup
```json
[
  {
    "currency_obj": "Money",
    "display_name": "§6Dollar Coin §f$1",
    "name": "currency:dollar",
    "points": 1
  },
  {
    "currency_obj": "Gems",
    "display_name": "§bDiamond Gem §f1 Gem",
    "name": "currency:diamond_gem",
    "points": 1
  },
  {
    "currency_obj": "XP",
    "display_name": "§aXP Bottle §f10 XP",
    "name": "currency:xp_bottle",
    "points": 10
  }
]
```

## Troubleshooting

### Common Issues

1. **Coin not working**: Check that the item identifier matches exactly
2. **Points not adding**: Verify the scoreboard objective exists
3. **Changes not applied**: Make sure to reload the plugin or restart the server
4. **JSON errors**: Validate your JSON syntax using an online validator

### Validation Rules

- Item names must be unique
- Points must be positive integers
- Display names should include color codes for better appearance
- Currency objectives should exist in the scoreboard system

## Future Updates

GUI forms may be added in future versions when the required Endstone modules become available. The current file-based and programmatic approaches will continue to be supported.
