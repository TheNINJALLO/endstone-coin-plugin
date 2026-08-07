from endstone.plugin import Plugin
from endstone.event import event_handler, PlayerInteractEvent
from endstone.scoreboard import Criteria
import json
import os
from typing import Dict, List, Optional, Any


class CoinPlugin(Plugin):
    api_version = "0.11"

    def __init__(self):
        super().__init__()
        self.coins_file = None
        self.coins_data = []

    # Default configuration for all coin types
    DEFAULT_COINS = [
        {
            'currency_obj': 'Money',
            'display_name': '§6Wooden TK Coin §f$1',
            'name': 'ninjos:coin_wood',
            'points': 1
        },
        {
            'currency_obj': 'Money',
            'display_name': '§7Glass TK Coin §f$5',
            'name': 'ninjos:coin_glass',
            'points': 5
        },
        {
            'currency_obj': 'Money',
            'display_name': '§8Iron TK Coin §f$25',
            'name': 'ninjos:coin_iron',
            'points': 25
        },
        {
            'currency_obj': 'Money',
            'display_name': '§2Emerald TK Coin §f$100',
            'name': 'ninjos:coin_emerald',
            'points': 100
        },
        {
            'currency_obj': 'Money',
            'display_name': '§cRuby TK Coin §f$500',
            'name': 'ninjos:coin_ruby',
            'points': 500
        },
        {
            'currency_obj': 'Money',
            'display_name': '§eGolden TK Coin §f$1,000',
            'name': 'ninjos:coin_gold',
            'points': 1000
        },
        {
            'currency_obj': 'Money',
            'display_name': '§bDiamond TK Coin §f$10,000',
            'name': 'ninjos:coin_diamond',
            'points': 10000
        },
        {
            'currency_obj': 'Money',
            'display_name': '§8Netherite TK Coin §f$1,000,000',
            'name': 'ninjos:coin_netherite',
            'points': 1000000
        }
    ]

    def on_load(self) -> None:
        """Called when plugin is loaded"""
        self.logger.info("Coin Plugin is loading...")

        # Set up data file path
        self.coins_file = os.path.join(self.data_folder, "coins.json")

        # Load coin data
        self._load_coins_data()

    def on_enable(self) -> None:
        """Called when plugin is enabled"""
        self.logger.info("Coin Plugin has been enabled!")

        # Register event listeners
        self.register_events(self)

        # Ensure scoreboard exists
        self._ensure_scoreboard_exists()

    def on_disable(self) -> None:
        """Called when plugin is disabled"""
        self.logger.info("Coin Plugin has been disabled!")

    def _load_coins_data(self) -> None:
        """Load coin data from file or create default"""
        try:
            # Create data folder if it doesn't exist
            os.makedirs(self.data_folder, exist_ok=True)

            if os.path.exists(self.coins_file):
                with open(self.coins_file, 'r', encoding='utf-8') as f:
                    self.coins_data = json.load(f)
                self.logger.info(f"Loaded {len(self.coins_data)} coins from file")
            else:
                # Use default coins and save them
                self.coins_data = self.DEFAULT_COINS.copy()
                self._save_coins_data()
                self.logger.info("Created default coin configuration")
        except Exception as e:
            self.logger.error(f"Error loading coin data: {e}")
            self.coins_data = self.DEFAULT_COINS.copy()

    def _save_coins_data(self) -> None:
        """Save coin data to file"""
        try:
            os.makedirs(self.data_folder, exist_ok=True)
            with open(self.coins_file, 'w', encoding='utf-8') as f:
                json.dump(self.coins_data, f, indent=2, ensure_ascii=False)
            self.logger.info("Coin data saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving coin data: {e}")

    def reload_coins_from_file(self) -> None:
        """Public method to reload coins from file - can be called by other plugins or console"""
        try:
            old_count = len(self.coins_data)
            self._load_coins_data()
            new_count = len(self.coins_data)
            self.logger.info(f"Reloaded coin data! ({old_count} → {new_count} coins)")
        except Exception as e:
            self.logger.error(f"Error reloading coins: {e}")

    def add_coin(self, currency_obj: str, display_name: str, item_name: str, points: int) -> bool:
        """Add a new coin configuration"""
        try:
            # Check if item ID already exists
            for coin in self.coins_data:
                if coin['name'] == item_name:
                    self.logger.warning(f"Coin with item name '{item_name}' already exists!")
                    return False

            # Add new coin
            new_coin = {
                'currency_obj': currency_obj,
                'display_name': display_name,
                'name': item_name,
                'points': points
            }

            self.coins_data.append(new_coin)
            self._save_coins_data()
            self.logger.info(f"Added new coin: {display_name} ({item_name}) - {points} points")
            return True

        except Exception as e:
            self.logger.error(f"Error adding coin: {e}")
            return False

    def remove_coin(self, item_name: str) -> bool:
        """Remove a coin configuration by item name"""
        try:
            for i, coin in enumerate(self.coins_data):
                if coin['name'] == item_name:
                    removed_coin = self.coins_data.pop(i)
                    self._save_coins_data()
                    self.logger.info(f"Removed coin: {removed_coin['display_name']} ({item_name})")
                    return True

            self.logger.warning(f"Coin with item name '{item_name}' not found!")
            return False

        except Exception as e:
            self.logger.error(f"Error removing coin: {e}")
            return False

    def list_coins(self) -> List[Dict[str, Any]]:
        """Get a list of all configured coins"""
        return self.coins_data.copy()

    def _ensure_scoreboard_exists(self) -> None:
        """Ensure the Money scoreboard objective exists"""
        try:
            scoreboard = self.server.scoreboard

            # Try to get existing objective
            money_obj = scoreboard.get_objective("Money")
            if money_obj:
                self.logger.info("Money scoreboard objective already exists")
                return
        except:
            pass

        # Create the objective if it doesn't exist
        try:
            scoreboard = self.server.scoreboard
            scoreboard.add_objective(
                name="Money",
                criteria=Criteria.Type.DUMMY,
                display_name="§6Money"
            )
            self.logger.info("Money scoreboard objective created successfully")
        except Exception as e:
            self.logger.error(f"Failed to create Money scoreboard: {e}")

    @event_handler
    def on_player_interact(self, event: PlayerInteractEvent) -> None:
        """Handle player interaction events"""
        # Only process right-click in air actions
        if event.action != PlayerInteractEvent.Action.RIGHT_CLICK_AIR:
            return

        player = event.player

        # Check if player has an item
        if not event.has_item:
            return

        item = event.item
        if not item:
            return

        # Get the item type identifier
        item_type_id = item.type.id

        # Find matching coin configuration
        coin_config = None
        for coin in self.coins_data:
            if coin['name'] == item_type_id:
                coin_config = coin
                break

        # If no matching coin found, ignore
        if not coin_config:
            return

        # Get the amount of coins in the stack
        num_coins = item.amount
        if num_coins <= 0:
            return

        # Calculate total points
        total_points = num_coins * coin_config['points']

        # Update the scoreboard using server command to bypass permission issues
        try:
            # Ensure the scoreboard objective exists
            scoreboard = self.server.scoreboard
            objective = scoreboard.get_objective(coin_config['currency_obj'])

            if not objective:
                self.logger.warning(f"Scoreboard objective '{coin_config['currency_obj']}' not found!")
                return

            # Use server command to add points - this bypasses player permission restrictions
            # Format player name properly for commands (handle spaces with quotes if needed)
            player_name = player.name
            if ' ' in player_name:
                player_name = f'"{player_name}"'

            command = f"scoreboard players add {player_name} {coin_config['currency_obj']} {total_points}"

            # Execute the command as the server console
            success = self.server.dispatch_command(self.server.command_sender, command)

            if not success:
                self.logger.error(f"Failed to execute scoreboard command: {command}")
                return

            # Remove the coins from inventory
            player.inventory.remove_item(item)

            # Play sound at player's location (correct argument order: location, sound, volume, pitch)
            player.play_sound(player.location, "note.bell", 1.0, 1.0)

            # Send popup message (action bar equivalent in Bedrock)
            player.send_popup(f"§2+ {total_points} {coin_config['display_name']}")

            # Get the updated score for logging
            try:
                score = objective.get_score(player.name)
                new_balance = score.value
            except:
                new_balance = "unknown"

            self.logger.info(
                f"{player.name} deposited {num_coins}x {coin_config['name']} "
                f"for {total_points} points (new balance: {new_balance})"
            )

        except Exception as e:
            self.logger.error(f"Error processing coin deposit: {e}")
            import traceback
            traceback.print_exc()